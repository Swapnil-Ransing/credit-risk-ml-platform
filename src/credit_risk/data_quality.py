
from pathlib import Path
import json

import pandas as pd

DATA_PATH = Path("data/raw/application_train.csv")
REPORT_DIR = Path("reports")


def run_data_quality_checks(path: Path) -> dict:
    """Inspect a credit application dataset without modifying it."""
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset contains no rows.")

    required_columns = {"SK_ID_CURR", "TARGET"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    target = df["TARGET"]

    report = {
        "dataset": path.name,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_application_ids": int(
            df["SK_ID_CURR"].duplicated().sum()
        ),
        "missing_target": int(target.isna().sum()),
        "target_values": {
            str(k): int(v)
            for k, v in target.value_counts(dropna=False).items()
        },
        "target_proportions": {
            str(k): float(v)
            for k, v in target.value_counts(
                normalize=True, dropna=False
            ).items()
        },
        "invalid_target_values": int(
            (~target.isin([0, 1]) & target.notna()).sum()
        ),
        "columns_with_missing_values": int(
            df.isna().any().sum()
        ),
        "total_missing_cells": int(df.isna().sum().sum()),
        "top_missing_columns": {
            str(k): float(v)
            for k, v in (
                df.isna().mean()
                .sort_values(ascending=False)
                .head(15)
                .items()
            )
        },
        "column_dtypes": {
            str(k): str(v) for k, v in df.dtypes.items()
        },
    }

    return report


if __name__ == "__main__":
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report = run_data_quality_checks(DATA_PATH)

    output_path = REPORT_DIR / "day01_data_quality.json"
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nReport saved to: {output_path}")