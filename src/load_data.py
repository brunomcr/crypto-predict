import os
import json
import pandas as pd

BRONZE_DIR = "data/bronze"
SILVER_PATH = "data/silver/bitcoin_ohlc_silver.parquet"


def load_json_from_bronze():
    """
    Lê todos os arquivos .json da camada bronze e retorna uma lista de listas.
    """
    all_records = []

    for filename in os.listdir(BRONZE_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(BRONZE_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    all_records.extend(data)
                    print(f"📥 Carregado: {filename} ({len(data)} registros)")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar {filename}: {e}")

    return all_records


def load_silver_data():
    """
    Lê os dados da camada silver, garante ordenação e tipo de timestamp.
    """
    df = pd.read_parquet(SILVER_PATH)
    df = df.sort_values("timestamp").reset_index(drop=True)

    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"]), "❌ 'timestamp' não está em formato datetime!"
    return df
