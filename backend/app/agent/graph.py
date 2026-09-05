from langgraph.graph import END, StateGraph

from app.agent.answer_generator import generate_answer
from app.agent.compiler import compile_query_plan
from app.agent.executor import execute_query_plan
from app.agent.query_generator import generate_query
from app.agent.state import AgentState
from app.agent.validator import (
    validate_compiled_query,
    validate_query_plan
)


def validate_query(
    state: AgentState
) -> AgentState:
    """
    Validate both the AI-generated analytical plan
    and the MongoDB query produced by our compiler.
    """

    plan = state["query_plan"]

    errors = []

    # Validate AI analytical plan
    errors.extend(
        validate_query_plan(plan)
    )

    # Only compile and validate MongoDB syntax
    # if the analytical plan itself is valid.
    if not errors:

        errors.extend(
            validate_compiled_query(plan)
        )

    return {
        **state,
        "validation_errors": errors
    }


def route_after_validation(
    state: AgentState
) -> str:
    """
    Tell LangGraph where to go after validation.
    """

    if state.get("validation_errors"):
        return "validation_error"

    return "execute_query"


def handle_validation_error(
    state: AgentState
) -> AgentState:
    """
    Return a safe response when the generated query
    fails validation.
    """

    errors = state.get(
        "validation_errors",
        []
    )

    error_message = (
        "I couldn't safely generate a valid "
        "database query for that request."
    )

    if errors:
        error_message += (
            " Please try rephrasing the question."
        )

    return {
        **state,
        "error": "; ".join(errors),
        "final_answer": error_message
    }


def execute_query(
    state: AgentState
) -> AgentState:
    """
    Execute the validated query plan against MongoDB.
    """

    plan = state["query_plan"]

    filter_query, pipeline = (
        compile_query_plan(plan)
    )

    results = execute_query_plan(plan)

    return {
        **state,
        "filter_query": filter_query,
        "aggregation_pipeline": pipeline,
        "query_result": results
    }


def build_graph():

    graph = StateGraph(AgentState)

    # -----------------------------------------
    # Nodes
    # -----------------------------------------

    graph.add_node(
        "generate_query",
        generate_query
    )

    graph.add_node(
        "validate_query",
        validate_query
    )

    graph.add_node(
        "execute_query",
        execute_query
    )

    graph.add_node(
        "generate_answer",
        generate_answer
    )

    graph.add_node(
        "validation_error",
        handle_validation_error
    )

    # -----------------------------------------
    # Entry point
    # -----------------------------------------

    graph.set_entry_point(
        "generate_query"
    )

    # -----------------------------------------
    # Workflow
    # -----------------------------------------

    graph.add_edge(
        "generate_query",
        "validate_query"
    )

    graph.add_conditional_edges(
        "validate_query",
        route_after_validation,
        {
            "execute_query": "execute_query",
            "validation_error": "validation_error"
        }
    )

    graph.add_edge(
        "execute_query",
        "generate_answer"
    )

    graph.add_edge(
        "generate_answer",
        END
    )

    graph.add_edge(
        "validation_error",
        END
    )

    return graph.compile()


procurement_agent = build_graph()