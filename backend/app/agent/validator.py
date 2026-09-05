from typing import Any

from app.agent.query_models import MongoQueryPlan


ALLOWED_PIPELINE_STAGES = {
    "$match",
    "$group",
    "$sort",
    "$limit",
    "$project",
    "$count",
    "$unwind"
}


ALLOWED_ACCUMULATORS = {
    "$sum",
    "$avg",
    "$min",
    "$max",
    "$first",
    "$last",
    "$push",
    "$addToSet"
}


FORBIDDEN_OPERATORS = {
    "$out",
    "$merge"
}


def validate_query_plan(
    query_plan: MongoQueryPlan
) -> list[str]:

    errors = []

    if query_plan.query_type == "aggregate":

        if not query_plan.aggregation_pipeline:
            errors.append(
                "Aggregate query has no aggregation pipeline."
            )

        for stage in query_plan.aggregation_pipeline:

            if len(stage) != 1:
                errors.append(
                    f"Each aggregation stage must contain "
                    f"exactly one operator: {stage}"
                )
                continue

            stage_name = next(iter(stage))

            if stage_name in FORBIDDEN_OPERATORS:
                errors.append(
                    f"Forbidden aggregation stage: {stage_name}"
                )

            if stage_name not in ALLOWED_PIPELINE_STAGES:
                errors.append(
                    f"Unsupported aggregation stage: {stage_name}"
                )

            if stage_name == "$group":
                errors.extend(
                    validate_group_stage(stage["$group"])
                )

            if stage_name == "$sort":
                errors.extend(
                    validate_sort_stage(stage["$sort"])
                )

            if stage_name == "$limit":
                errors.extend(
                    validate_limit_stage(stage["$limit"])
                )

    elif query_plan.query_type == "find":

        if query_plan.aggregation_pipeline:
            errors.append(
                "Find query should not contain "
                "an aggregation pipeline."
            )

    else:
        errors.append(
            f"Unsupported query type: {query_plan.query_type}"
        )

    return errors


def validate_group_stage(
    group_stage: dict[str, Any]
) -> list[str]:

    errors = []

    for field_name, expression in group_stage.items():

        if field_name == "_id":
            continue

        if not isinstance(expression, dict):
            errors.append(
                f"$group field '{field_name}' must use "
                f"an accumulator such as $sum."
            )
            continue

        if len(expression) != 1:
            errors.append(
                f"$group field '{field_name}' must contain "
                f"exactly one accumulator."
            )
            continue

        accumulator = next(iter(expression))

        if accumulator not in ALLOWED_ACCUMULATORS:
            errors.append(
                f"Unsupported $group accumulator: "
                f"{accumulator}"
            )

    return errors


def validate_sort_stage(
    sort_stage: dict[str, Any]
) -> list[str]:

    errors = []

    for field_name, direction in sort_stage.items():

        if direction not in (1, -1):
            errors.append(
                f"Sort direction for '{field_name}' "
                f"must be 1 or -1."
            )

    return errors


def validate_limit_stage(
    limit_value: Any
) -> list[str]:

    errors = []

    if not isinstance(limit_value, int):
        errors.append(
            "$limit must be an integer."
        )

    elif limit_value <= 0:
        errors.append(
            "$limit must be greater than zero."
        )

    elif limit_value > 100:
        errors.append(
            "$limit cannot exceed 100."
        )

    return errors