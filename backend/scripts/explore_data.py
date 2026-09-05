import pandas as pd

df = pd.read_csv("data/purchase_orders.csv")

print(df.shape)

print("\n--- COLUMN NAMES ---")
for column in df.columns:
    print(column)

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- MISSING VALUE PERCENTAGES ---")
missing_percentage = (df.isnull().sum() / len(df)) * 100
print(missing_percentage.sort_values(ascending=False))

print("\n--- PURCHASE ORDER ANALYSIS ---")

print("Total rows:", len(df))

print(
    "Unique Purchase Order Numbers:",
    df["Purchase Order Number"].nunique()
)

print(
    "Unique Department + Purchase Order combinations:",
    df[["Department Name", "Purchase Order Number"]]
    .drop_duplicates()
    .shape[0]
)

print("\n--- IMPORTANT FIELD VALUES ---")

for column in [
    "Acquisition Type",
    "Acquisition Method",
    "CalCard"
]:
    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False).head(20))

    print("\n--- PRICE SAMPLES ---")
print(df[["Unit Price", "Total Price"]].head(10))

print("\n--- DATE SAMPLES ---")
print(df[["Creation Date", "Purchase Date", "Fiscal Year"]].head(10))

print("\n--- QUANTITY SUMMARY ---")
print(df["Quantity"].describe())