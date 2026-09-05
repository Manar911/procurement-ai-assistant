from app.agent.graph import procurement_agent


question = "What are the top 5 departments by total spending?"

initial_state = {
    "question": question
}


print("\n--- USER QUESTION ---")
print(question)


print("\n--- RUNNING LANGGRAPH AGENT ---")

result = procurement_agent.invoke(
    initial_state
)


print("\n--- FINAL ANSWER ---")

print(
    result["final_answer"]
)