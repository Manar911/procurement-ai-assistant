from typing import Any

from app.agent.compiler import compile_query_plan
from app.agent.query_models import MongoQueryPlan


# Fields the AI is allowed to reference.
# These must correspond to fields that actually exist
# in our procurement MongoDB collection.
ALLOWED_FIELDS = {
    "creation_date",
    "purchase_date",
    "fiscal_year",
    "lpa_number",
    "purchase_order_number",
    "requisition_number",
    "acquisition_type",
    "sub-acquisition_type",
    "acquisition_method",
    "sub-acquisition_method",
    "department_name",
    "supplier_code",
    "supplier_name",
    "supplier_qualifications",
    "supplier_zip_code",
    "calcard",
    "item_name",
    "item_description",
    "quantity",
    "unit_price",
    "total_price",
    "classification_codes",
    "normalized_unspsc",
    "commodity_title",
    "class",
    "class_title",
    "family",
    "family_title",
    "segment",
    "segment_title",
    "location"
}


ALLOWED_PIPELINE_STAGES = {
    "$match",
    "$group",
    "$sort",
    "$limit",
    "$project",
    "$count",
    "$unwind"
}


FORBIDDEN_PIPELINE_STAGES = {
    "$out",
    "$merge"
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


def validate_query_plan(
    plan: MongoQueryPlan
) -> list[str]:
    """
    Validate the AI-generated analytical plan before
    converting or executing it against MongoDB.
    """

    errors = []

    # -----------------------------------------
    # 1. Validate filters
    # -----------------------------------------

    for condition in plan.filters:

        if condition.field not in ALLOWED_FIELDS:
            errors.append(
                f"Unknown filter field: "
                f"{condition.field}"
            )

    # -----------------------------------------
    # 2. Validate group-by fields
    # -----------------------------------------

    for field in plan.group_by:

        if field not in ALLOWED_FIELDS:
            errors.append(
                f"Unknown group-by field: {field}"
            )

    # -----------------------------------------
    # 3. Validate metric field
    # -----------------------------------------

    metrics_requiring_field = {
        "sum",
        "average",
        "minimum",
        "maximum"
    }

    if plan.metric in metrics_requiring_field:

        if not plan.metric_field:
            errors.append(
                f"Metric '{plan.metric}' requires "
                f"a metric_field."
            )

        elif plan.metric_field not in ALLOWED_FIELDS:
            errors.append(
                f"Unknown metric field: "
                f"{plan.metric_field}"
            )

    # -----------------------------------------
    # 4. Validate find queries
    # -----------------------------------------

    if plan.query_type == "find":

        if plan.metric != "none":
            errors.append(
                "Find queries cannot contain "
                "an analytical metric."
            )

        if plan.group_by:
            errors.append(
                "Find queries cannot contain "
                "group-by fields."
            )

    # -----------------------------------------
    # 5. Validate aggregate queries
    # -----------------------------------------

    elif plan.query_type == "aggregate":

        if plan.metric == "none":
            errors.append(
                "Aggregate queries must specify "
                "an analytical metric."
            )

    else:
        errors.append(
            f"Unsupported query type: "
            f"{plan.query_type}"
        )

    # -----------------------------------------
    # 6. Validate limit
    # -----------------------------------------

    if plan.limit is not None:

        if plan.limit <= 0:
            errors.append(
                "Limit must be greater than zero."
            )

        elif plan.limit > 100:
            errors.append(
                "Limit cannot exceed 100."
            )

    return errors


def validate_compiled_query(
    plan: MongoQueryPlan
) -> list[str]:
    """
    Compile the analytical plan into MongoDB syntax
    and validate the resulting pipeline before execution.
    """

    errors = []

    try:
        filter_query, pipeline = compile_query_plan(plan)

    except Exception as error:
        return [
            f"Query compilation failed: {error}"
        ]

    # -----------------------------------------
    # Validate find query
    # -----------------------------------------

    if plan.query_type == "find":

        if pipeline:
            errors.append(
                "Find query unexpectedly produced "
                "an aggregation pipeline."
            )

        return errors

    # -----------------------------------------
    # Validate aggregation pipeline
    # -----------------------------------------

    for stage in pipeline:

        if not isinstance(stage, dict):
            errors.append(
                "Every aggregation stage must "
                "be a dictionary."
            )
            continue

        if len(stage) != 1:
            errors.append(
                f"Aggregation stage must contain "
                f"exactly one operator: {stage}"
            )
            continue

        stage_name = next(iter(stage))

        if stage_name in FORBIDDEN_PIPELINE_STAGES:
            errors.append(
                f"Forbidden MongoDB stage: "
                f"{stage_name}"
            )

        elif stage_name not in ALLOWED_PIPELINE_STAGES:
            errors.append(
                f"Unsupported MongoDB stage: "
                f"{stage_name}"
            )

        if stage_name == "$group":
            errors.extend(
                validate_group_stage(
                    stage["$group"]
                )
            )

        elif stage_name == "$sort":
            errors.extend(
                validate_sort_stage(
                    stage["$sort"]
                )
            )

        elif stage_name == "$limit":
            errors.extend(
                validate_limit_stage(
                    stage["$limit"]
                )
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
                f"$group field '{field_name}' "
                f"must use an accumulator."
            )
            continue

        if len(expression) != 1:
            errors.append(
                f"$group field '{field_name}' "
                f"must contain exactly one accumulator."
            )
            continue

        accumulator = next(iter(expression))

        if accumulator not in ALLOWED_ACCUMULATORS:
            errors.append(
                f"Unsupported accumulator: "
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