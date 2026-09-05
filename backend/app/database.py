import os

from dotenv import load_dotenv
from pymongo import MongoClient


# Load variables from the .env file
load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
    raise ValueError("MONGODB_URI was not found in the .env file.")


# Create MongoDB connection
client = MongoClient(mongodb_uri)

# Select our database
database = client["procurement_assistant"]

# Select our collection
purchase_orders_collection = database["purchase_orders"]