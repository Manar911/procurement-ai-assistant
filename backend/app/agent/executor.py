from datetime import datetime
from typing import Any

from app.agent.compiler import compile_query_plan
from app.database import purchase_orders_collection


def _convert_dates(value: Any):
    """
    Recursively convert ISO date strings into Python datetime objects
    so MongoDB can compare them with BSON Date fields.
    """

    if isinstance(value, dict):
        return {
            key: _convert_dates(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _convert_dates(item)
            for item in value
        ]

    if isinstance(value, str):
        try:
            if "T" in value:
                return datetime.fromisoformat(
                    value.replace("Z", "+00:00")
                )
        except ValueError:
            pass

    return value


def execute_query_plan(plan, result_limit: int = 100):
    """
    Compile the AI-generated analytical plan and execute it
    against the MongoDB purchase_orders collection.
    """

    filter_query, pipeline = compile_query_plan(plan)

    filter_query = _convert_dates(filter_query)
    pipeline = _convert_dates(pipeline)

    if plan.query_type == "find":

        cursor = purchase_orders_collection.find(
            filter_query,
            {"_id": 0}
        ).limit(result_limit)

        results = list(cursor)

    elif plan.query_type == "aggregate":

        results = list(
            purchase_orders_collection.aggregate(pipeline)
        )

        results = results[:result_limit]

    else:
        raise ValueError(
            f"Unsupported query type: {plan.query_type}"
        )

    return results