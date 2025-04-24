import json
import os
import pandas as pd


def save_to_json(data, path, filename):
    """
    Salva dados brutos em formato JSON.
    """
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON salvo em: {full_path}")


def save_to_parquet(df, path, filename):
    """
    Salva um DataFrame pandas em formato Parquet.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O objeto fornecido para save_to_parquet não é um DataFrame.")

    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, filename)

    df.to_parquet(full_path, index=False)
    print(f"✅ Parquet salvo em: {full_path}")
