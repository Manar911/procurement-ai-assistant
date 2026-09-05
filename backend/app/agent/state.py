from typing import Any, TypedDict

from app.agent.query_models import MongoQueryPlan


class AgentState(TypedDict, total=False):
    question: str

    query_plan: MongoQueryPlan

    filter_query: dict[str, Any]

    aggregation_pipeline: list[dict[str, Any]]

    query_result: Any

    final_answer: str

    error: str