import pandas as pd
import requests
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_municipalities_of_Sweden"

headers = {
    "User-Agent": "RuthDataLearningProject/1.0"
}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

tables = pd.read_html(StringIO(response.text))

print("Number of tables found:", len(tables))
for index, table in enumerate(tables):
    print(f"\nTABLE {index}")
    print(table.head())
    df = tables[1]

print("\nSelected municipality table:")
print(df.head())

print("\nRows and columns:", df.shape)

print("\nData information:")
df.info()

print("\nMissing values:")
print(df.isnull().sum())
duplicate_rows = df.duplicated().sum()

print("\nDuplicate rows:", duplicate_rows)

df.columns = [
    "code",
    "municipality",
    "seat",
    "county",
    "population",
    "land_area_km2",
    "density"
]

df["code"] = df["code"].astype(str).str.zfill(4)

print(df.head())
print(df.dtypes)
df.to_csv("swedish_municipalities.csv", index=False)
