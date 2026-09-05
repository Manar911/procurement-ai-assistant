from fastapi import FastAPI

from app.database import client, purchase_orders_collection


app = FastAPI(
    title="Procurement AI Assistant",
    description="AI-powered assistant for querying procurement data.",
    version="1.0.0"
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
        purchase_orders_collection.distinct("department_name")
    )

    suppliers = (
        purchase_orders_collection.distinct("supplier_name")
    )

    return {
        "total_records": total_records,
        "total_departments": len(departments),
        "total_suppliers": len(suppliers)
    }    