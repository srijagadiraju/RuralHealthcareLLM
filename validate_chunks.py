import pandas as pd

# load preprocessed CSV
df = pd.read_csv("preprocessed_chunks.csv")

# check structure
print("Data Info:")
print(df.info())

# check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# review rows
print("\nSample rows:")
print(df.head())
