import pandas as pd
import os


def prepare_target(df):
    """
    Adiciona a coluna "target" ao DataFrame:
    1 = fechamento do próximo candle > fechamento atual
    0 = fechamento do próximo candle <= fechamento atual
    """
    df = df.copy()
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)

    return df