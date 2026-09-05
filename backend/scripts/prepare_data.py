import pandas as pd

# Load the original dataset
df = pd.read_csv("data/purchase_orders.csv")

print("Original shape:", df.shape)


# --------------------------------------------------
# 1. Convert price columns to numeric values
# --------------------------------------------------

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

print("\nPrice data types after conversion:")
print(df[["Unit Price", "Total Price"]].dtypes)

print("\nPrice samples after conversion:")
print(df[["Unit Price", "Total Price"]].head(10))


# --------------------------------------------------
# 2. Convert date columns to real datetime values
# --------------------------------------------------

for column in ["Creation Date", "Purchase Date"]:
    df[column] = pd.to_datetime(
        df[column],
        format="%m/%d/%Y",
        errors="coerce"
    )

print("\nDate data types after conversion:")
print(df[["Creation Date", "Purchase Date"]].dtypes)

print("\nDate samples after conversion:")
print(
    df[
        ["Creation Date", "Purchase Date", "Fiscal Year"]
    ].head(10)
)


# --------------------------------------------------
# 3. Rename columns using snake_case
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("/", "_", regex=False)
)

print("\nColumn names after renaming:")
print(df.columns.tolist())


# --------------------------------------------------
# 4. Convert missing pandas values to None
# --------------------------------------------------

df = df.astype(object).where(
    pd.notnull(df),
    None
)


# --------------------------------------------------
# 5. Save the cleaned dataset
# --------------------------------------------------

output_path = "data/purchase_orders_cleaned.csv"

df.to_csv(
    output_path,
    index=False
)

print("\nCleaned dataset saved successfully.")
print("Output:", output_path)
print("Final shape:", df.shape)