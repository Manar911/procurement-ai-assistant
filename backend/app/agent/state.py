from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    question: str

    query_type: str

    filter_query: dict[str, Any]

    aggregation_pipeline: list[dict[str, Any]]

    query_result: Any

    final_answer: str

    error: str