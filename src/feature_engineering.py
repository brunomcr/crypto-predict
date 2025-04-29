# src/feature_engineering.py

import pandas as pd
import numpy as np

# Constante para candles de 30 minutos
CANDLES_PER_DAY = 48

def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona features derivadas básicas e avançadas ao DataFrame de OHLC.

    Features adicionadas:
    - close_diff: diferença entre fechamento e abertura
    - volatility: amplitude do candle
    - log_return: retorno logarítmico entre candles consecutivos (30min)
    - candle_body_size: tamanho do corpo do candle
    - candle_wick_size: tamanho dos pavios
    - candle_direction: direção do candle (1 = alta, 0 = baixa ou neutro)
    - momentum_3d: diferença do close atual com close de 3 dias atrás (3 × 48 = 144 candles)
    - high_low_ratio: amplitude intradiária normalizada pelo fechamento
    - rsi_over_50: flag (1 ou 0) se RSI está acima de 50
    - log_return_3d: retorno logarítmico de 3 dias

    :param df: DataFrame contendo colunas ['open', 'high', 'low', 'close', 'rsi_14']
    :return: DataFrame com novas features adicionadas
    """
    df = df.copy()

    # 1. Diferença entre fechamento e abertura
    df["close_diff"] = df["close"] - df["open"]

    # 2. Volatilidade (amplitude do candle)
    df["volatility"] = df["high"] - df["low"]

    # 3. Retorno logarítmico (1 candle = 30min)
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))

    # 4. Tamanho do corpo do candle
    df["candle_body_size"] = (df["close"] - df["open"]).abs()

    # 5. Tamanho dos pavios (wick)
    df["candle_wick_size"] = df["volatility"] - df["candle_body_size"]

    # 6. Direção do candle (1 = alta, 0 = baixa ou neutro)
    df["candle_direction"] = np.where(df["close"] > df["open"], 1, 0)

    # ====== Novas Features Avançadas Correção para 3 dias ======

    # 7. Momentum de 3 dias (144 candles de 30min)
    df["momentum_3d"] = df["close"] - df["close"].shift(3 * CANDLES_PER_DAY)

    # 8. Amplitude intradiária normalizada
    df["high_low_ratio"] = (df["high"] - df["low"]) / df["close"]

    # 9. Flag RSI acima de 50
    if "rsi_14" in df.columns:
        df["rsi_over_50"] = (df["rsi_14"] > 50).astype(int)
    else:
        raise KeyError("❌ A coluna 'rsi_14' é necessária para calcular 'rsi_over_50'. Verifique se aplicou enrich_with_indicators primeiro.")

    # 10. Retorno logarítmico de 3 dias
    df["log_return_3d"] = np.log(df["close"] / df["close"].shift(3 * CANDLES_PER_DAY))

    # ============================================================

    return df
