import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
    raise ValueError("MONGODB_URI was not found in the .env file.")

client = MongoClient(mongodb_uri)

client.admin.command("ping")

print("MongoDB connection successful!")