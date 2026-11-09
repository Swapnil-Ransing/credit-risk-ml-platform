from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/application_train.csv")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH.resolve()}"
    )

df = pd.read_csv(DATA_PATH)

print("Shape:", df.shape)
print("\nFirst five rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes.value_counts())

print("\nTarget distribution:")
print(df["TARGET"].value_counts(dropna=False))

print("\nTarget proportions:")
print(df["TARGET"].value_counts(normalize=True, dropna=False))

print("\nMemory usage:")
print(f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")