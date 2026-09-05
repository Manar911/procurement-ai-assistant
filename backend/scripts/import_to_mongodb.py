import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
    raise ValueError("MONGODB_URI was not found in the .env file.")


client = MongoClient(mongodb_uri)

database = client["procurement_assistant"]
collection = database["purchase_orders"]

print("Connected to MongoDB Atlas.")


df = pd.read_csv("data/purchase_orders.csv")

print("Loaded rows:", len(df))


for column in ["Unit Price", "Total Price"]:
    df[column] = (
        df[column]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


for column in ["Creation Date", "Purchase Date"]:
    df[column] = pd.to_datetime(
        df[column],
        format="%m/%d/%Y",
        errors="coerce"
    )


df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("/", "_", regex=False)
)


df = df.astype(object).where(
    pd.notnull(df),
    None
)


records = df.to_dict("records")

print("Prepared documents:", len(records))


collection.delete_many({})


batch_size = 5000

for start in range(0, len(records), batch_size):
    end = start + batch_size

    batch = records[start:end]

    collection.insert_many(batch)

    print(
        f"Inserted {min(end, len(records))} "
        f"of {len(records)} documents"
    )


print("\nImport completed successfully.")
print(
    "MongoDB document count:",
    collection.count_documents({})
)