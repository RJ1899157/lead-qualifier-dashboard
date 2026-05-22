# data_loader.py

import pandas as pd


REQUIRED_COLUMNS = [
    "name",
    "role",
    "company",
    "industry",
    "country",
    "company_size",
    "engagement"
]


def load_csv(file_path):
    df = pd.read_csv(file_path)

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    records = df.to_dict(orient="records")

    for r in records:
        r["knowledge_base"] = []
        r["interaction_count"] = 0

    return records