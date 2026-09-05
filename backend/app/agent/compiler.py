from datetime import datetime
from typing import Any

from app.agent.query_models import MongoQueryPlan


OPERATOR_MAP = {
    "eq": "$eq",
    "ne": "$ne",
    "gt": "$gt",
    "gte": "$gte",
    "lt": "$lt",
    "lte": "$lte",
    "in": "$in"
}


DATE_FIELDS = {
    "creation_date",
    "purchase_date"
}


METRIC_OPERATORS = {
    "sum": "$sum",
    "average": "$avg",
    "minimum": "$min",
    "maximum": "$max"
}


def convert_value(
    field: str,
    value: Any
) -> Any:

    if (
        field in DATE_FIELDS
        and isinstance(value, str)
    ):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return value

    return value


def build_match_stage(
    plan: MongoQueryPlan
) -> dict[str, Any]:

    match_query = {}

    for condition in plan.filters:

        field = condition.field
        operator = condition.operator

        value = convert_value(
            field,
            condition.value
        )

        if operator == "eq":
            match_query[field] = value

        else:
            mongo_operator = OPERATOR_MAP[operator]

            if field not in match_query:
                match_query[field] = {}

            match_query[field][mongo_operator] = value

    return match_query


def build_group_id(
    fields: list[str]
) -> Any:

    if not fields:
        return None

    if len(fields) == 1:
        return f"${fields[0]}"

    return {
        field: f"${field}"
        for field in fields
    }


def compile_query_plan(
    plan: MongoQueryPlan
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]]
]:

    filter_query = build_match_stage(plan)

    if plan.query_type == "find":
        return filter_query, []

    pipeline = []

    if filter_query:
        pipeline.append({
            "$match": filter_query
        })

    # -----------------------------------------
    # Unique purchase-order count
    # -----------------------------------------

    if plan.metric == "count_unique_orders":

        pipeline.append({
            "$group": {
                "_id": {
                    "department_name": "$department_name",
                    "purchase_order_number":
                        "$purchase_order_number"
                }
            }
        })

        pipeline.append({
            "$count": "value"
        })

        return filter_query, pipeline

    # -----------------------------------------
    # Other aggregations
    # -----------------------------------------

    group_id = build_group_id(
        plan.group_by
    )

    if plan.metric == "count":

        pipeline.append({
            "$group": {
                "_id": group_id,
                "value": {
                    "$sum": 1
                }
            }
        })

    elif plan.metric in METRIC_OPERATORS:

        if not plan.metric_field:
            raise ValueError(
                f"metric_field is required for "
                f"metric '{plan.metric}'."
            )

        mongo_operator = (
            METRIC_OPERATORS[plan.metric]
        )

        pipeline.append({
            "$group": {
                "_id": group_id,
                "value": {
                    mongo_operator:
                        f"${plan.metric_field}"
                }
            }
        })

    # -----------------------------------------
    # Sorting
    # -----------------------------------------

    if plan.sort_direction != "none":

        direction = (
            -1
            if plan.sort_direction == "descending"
            else 1
        )

        pipeline.append({
            "$sort": {
                "value": direction
            }
        })

    # -----------------------------------------
    # Limit
    # -----------------------------------------

    if plan.limit is not None:

        pipeline.append({
            "$limit": plan.limit
        })

    return filter_query, pipeline