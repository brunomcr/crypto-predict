import pandas as pd

SILVER_DIR = "data/silver"
SILVER_FILENAME = "bitcoin_ohlc_silver.parquet"

def transform_to_dataframe(data):
    """
    Transforma dados brutos em um DataFrame estruturado e remove duplicações por timestamp.
    """
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    # Remove duplicações por timestamp mantendo o último valor coletado
    df = df.sort_values("timestamp").drop_duplicates(subset="timestamp", keep="last")

    df = df.reset_index(drop=True)

    return df

