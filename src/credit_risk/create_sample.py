
from pathlib import Path
import pandas as pd

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame({
    "SK_ID_CURR": [100001, 100002, 100003, 100004],
    "AMT_INCOME_TOTAL": [150000, 220000, 90000, 180000],
    "AMT_CREDIT": [500000, 750000, 250000, 600000],
    "DAYS_BIRTH": [-12000, -15000, -11000, -13500],
    "TARGET": [0, 0, 1, 0]
})

path = output_dir / "sample_credit_applications.csv"
df.to_csv(path, index=False)

print("Created:", path)
print(df)