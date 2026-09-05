from typing import Any, Literal

from pydantic import BaseModel, Field


class FilterCondition(BaseModel):
    field: str = Field(
        description="Database field to filter."
    )

    operator: Literal[
        "eq",
        "ne",
        "gt",
        "gte",
        "lt",
        "lte",
        "in"
    ] = Field(
        description="Comparison operator for the filter."
    )

    value: Any = Field(
        description="Value used by the filter."
    )


class MongoQueryPlan(BaseModel):
    query_type: Literal["find", "aggregate"] = Field(
        description=(
            "Use find for simple record retrieval. "
            "Use aggregate for calculations, grouping, "
            "ranking, counting, or comparisons."
        )
    )

    filters: list[FilterCondition] = Field(
        default_factory=list,
        description="Filters that must be applied to the dataset."
    )

    group_by: list[str] = Field(
        default_factory=list,
        description=(
            "Database fields used to group results. "
            "Example: ['department_name']."
        )
    )

    metric: Literal[
        "none",
        "count",
        "count_unique_orders",
        "sum",
        "average",
        "minimum",
        "maximum"
    ] = Field(
        default="none",
        description="Calculation required to answer the question."
    )

    metric_field: str | None = Field(
        default=None,
        description=(
            "Database field used by sum, average, minimum, "
            "or maximum. Example: total_price."
        )
    )

    sort_direction: Literal[
        "none",
        "ascending",
        "descending"
    ] = Field(
        default="none",
        description="How calculated results should be sorted."
    )

    limit: int | None = Field(
        default=None,
        description=(
            "Maximum number of results requested by the user."
        )
    )

    explanation: str = Field(
        description=(
            "Brief explanation of the analytical plan."
        )
    )