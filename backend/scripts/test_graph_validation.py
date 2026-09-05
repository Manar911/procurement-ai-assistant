from app.agent.query_models import MongoQueryPlan
from app.agent.validator import (
    validate_compiled_query,
    validate_query_plan
)


invalid_plan = MongoQueryPlan(
    query_type="aggregate",
    filters=[],
    group_by=["fake_field"],
    metric="sum",
    metric_field="total_price",
    sort_direction="descending",
    limit=5,
    explanation="Deliberately invalid test plan."
)


print("\n--- INVALID VALIDATION TEST ---")


plan_errors = validate_query_plan(
    invalid_plan
)

compiled_errors = []

if not plan_errors:
    compiled_errors = validate_compiled_query(
        invalid_plan
    )


all_errors = (
    plan_errors
    + compiled_errors
)


print("\nValidation errors:")

for error in all_errors:
    print("-", error)


if all_errors:
    print(
        "\nPASS: Invalid plan was blocked "
        "before database execution."
    )
else:
    print(
        "\nFAIL: Invalid plan was not detected."
    )