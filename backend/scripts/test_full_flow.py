from pprint import pprint

from app.agent.answer_generator import generate_answer
from app.agent.executor import execute_query_plan
from app.agent.query_generator import generate_query


question = "What are the top 5 departments by total spending?"


state = {
    "question": question
}


print("\n--- USER QUESTION ---")
print(question)


print("\n--- GENERATING QUERY PLAN ---")

state = generate_query(state)

plan = state["query_plan"]

print("\nQuery plan:")
print("Group by:", plan.group_by)
print("Metric:", plan.metric)
print("Metric field:", plan.metric_field)
print("Sort:", plan.sort_direction)
print("Limit:", plan.limit)


print("\n--- EXECUTING DATABASE QUERY ---")

results = execute_query_plan(plan)

state["query_result"] = results


print("\nDatabase results:")
pprint(results)


print("\n--- GENERATING FINAL ANSWER ---")

state = generate_answer(state)


print("\n--- FINAL ANSWER ---")

print(state["final_answer"])