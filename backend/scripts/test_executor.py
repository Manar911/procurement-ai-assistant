from pprint import pprint

from app.agent.query_generator import generate_query
from app.agent.compiler import compile_query_plan
from app.agent.executor import execute_query_plan


question = "What are the top 5 departments by total spending?"

print("\n--- USER QUESTION ---")
print(question)

state = {
    "question": question
}

print("\n--- GENERATING AI QUERY PLAN ---")

result = generate_query(state)
plan = result["query_plan"]

print("\n--- AI QUERY PLAN ---")
print("Query type:", plan.query_type)
print("Group by:", plan.group_by)
print("Metric:", plan.metric)
print("Metric field:", plan.metric_field)
print("Sort:", plan.sort_direction)
print("Limit:", plan.limit)

print("\n--- COMPILED QUERY ---")

filter_query, pipeline = compile_query_plan(plan)

print("Filter:")
pprint(filter_query)

print("\nPipeline:")
pprint(pipeline)

print("\n--- EXECUTING AGAINST MONGODB ---")

results = execute_query_plan(plan)

print("\n--- DATABASE RESULTS ---")

pprint(results)