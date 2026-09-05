from pprint import pprint

from app.agent.compiler import compile_query_plan
from app.agent.query_generator import generate_query


test_questions = [
    "What are the top 5 departments by total spending?",

    "Show purchases for IT Goods.",

    "What is the total spending by acquisition type?",

    "Which 10 suppliers received the most spending?",

    "How many purchase orders were created in January 2014?"
]


for question in test_questions:

    print("\n" + "=" * 70)
    print("USER QUESTION")
    print("=" * 70)

    print(question)

    state = {
        "question": question
    }

    print("\n--- AI QUERY PLAN ---")

    result = generate_query(state)

    plan = result["query_plan"]

    print("\nQuery type:")
    print(plan.query_type)

    print("\nFilters:")
    pprint(plan.filters)

    print("\nGroup by:")
    pprint(plan.group_by)

    print("\nMetric:")
    print(plan.metric)

    print("\nMetric field:")
    print(plan.metric_field)

    print("\nSort:")
    print(plan.sort_direction)

    print("\nLimit:")
    print(plan.limit)

    print("\nExplanation:")
    print(plan.explanation)


    print("\n--- COMPILED MONGODB QUERY ---")

    filter_query, pipeline = compile_query_plan(plan)

    print("\nFilter:")
    pprint(filter_query)

    print("\nAggregation pipeline:")
    pprint(pipeline)