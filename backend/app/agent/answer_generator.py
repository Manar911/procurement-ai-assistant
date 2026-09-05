from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.state import AgentState


# Load environment variables from .env
load_dotenv()


# Gemini model used to turn database results into
# a natural-language answer for the user.
model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


ANSWER_GENERATION_PROMPT = """
You are a procurement analytics assistant.

Answer the user's question using ONLY the database results provided.

Rules:

1. Do not invent facts or values.

2. Do not use outside knowledge to answer the procurement question.

3. If the database result is empty, clearly say that no matching
   records were found.

4. Present monetary values clearly and naturally.

5. When ranking results, preserve the ranking returned by the database.

6. Keep the answer concise but informative.

7. If useful, explain what metric was used.

8. Do not mention MongoDB implementation details unless the user asks.

9. Do not claim that a result represents a full purchase order when
   the result actually refers to procurement line records.

10. Base every factual claim on the supplied database result.
"""


def generate_answer(state: AgentState) -> AgentState:
    """
    Generate a natural-language answer using the user's question
    and the results returned from MongoDB.
    """

    question = state["question"]
    query_result = state["query_result"]

    messages = [
        (
            "system",
            ANSWER_GENERATION_PROMPT
        ),
        (
            "human",
            f"""
User question:

{question}


Database result:

{query_result}


Formulate the final answer for the user.
"""
        )
    ]

    # Ask Gemini to formulate the final response.
    response = model.invoke(messages)

    # Gemini may return its content either as a normal string
    # or as a list containing text blocks and metadata.
    content = response.content

    if isinstance(content, list):
        text_parts = []

        for part in content:
            if (
                isinstance(part, dict)
                and part.get("type") == "text"
            ):
                text_parts.append(
                    part.get("text", "")
                )

        final_answer = "\n".join(text_parts)

    else:
        final_answer = str(content)

    # Return the existing agent state together with
    # the generated final answer.
    return {
        **state,
        "final_answer": final_answer
    }