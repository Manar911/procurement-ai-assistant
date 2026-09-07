from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 

from app.agent.graph import procurement_agent
from app.database import client, purchase_orders_collection
from app.models.chat import ChatRequest, ChatResponse


app = FastAPI(
    title="Procurement AI Assistant",
    description="AI-powered assistant for querying procurement data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Procurement AI Assistant API"
    }


@app.get("/health")
def health_check():

    try:
        # Check whether MongoDB responds
        client.admin.command("ping")

        document_count = (
            purchase_orders_collection.count_documents({})
        )

        return {
            "status": "healthy",
            "database": "connected",
            "documents": document_count
        }

    except Exception as error:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }


@app.get("/stats")
def get_stats():

    total_records = (
        purchase_orders_collection.count_documents({})
    )

    departments = (
        purchase_orders_collection.distinct(
            "department_name"
        )
    )

    suppliers = (
        purchase_orders_collection.distinct(
            "supplier_name"
        )
    )

    return {
        "total_records": total_records,
        "total_departments": len(departments),
        "total_suppliers": len(suppliers)
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:
        # Initial state given to the LangGraph agent
        initial_state = {
            "question": request.question
        }

        # Run the complete AI workflow
        result = procurement_agent.invoke(
            initial_state
        )

        final_answer = result.get(
            "final_answer"
        )

        if not final_answer:
            raise HTTPException(
                status_code=500,
                detail=(
                    "The assistant did not produce "
                    "a final answer."
                )
            )

        return ChatResponse(
            answer=final_answer
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Assistant error: {str(error)}"
        )