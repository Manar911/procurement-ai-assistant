from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.prompts import QUERY_GENERATION_PROMPT
from app.agent.query_models import MongoQueryPlan
from app.agent.state import AgentState


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


structured_model = model.with_structured_output(
    MongoQueryPlan
)


def generate_query(state: AgentState) -> AgentState:

    question = state["question"]

    messages = [
        (
            "system",
            QUERY_GENERATION_PROMPT
        ),
        (
            "human",
            question
        )
    ]

    query_plan = structured_model.invoke(messages)

    return {
        **state,
        "query_plan": query_plan
    }