import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, SMAIndicator, MACD
from ta.volatility import BollingerBands

def enrich_with_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona indicadores técnicos ao DataFrame ajustados para candles de 30 minutos:
    - SMA(50), SMA(200)
    - EMA(9), EMA(21), EMA(50), EMA(111), EMA(350)
    - RSI(14)
    - MACD (12,26,9)
    - Bandas de Bollinger (20)
    - Pi Cycle Top Cross
    """
    df = df.copy()

    if df.empty:
        raise ValueError("❌ DataFrame está vazio.")
    if "close" not in df.columns:
        raise KeyError("❌ Coluna 'close' não encontrada.")

    # Candles por dia
    candles_per_day = 48  # 48 candles de 30min = 1 dia

    # ✅ SMA
    df["sma_50"] = SMAIndicator(close=df["close"], window=50 * candles_per_day).sma_indicator()
    df["sma_200"] = SMAIndicator(close=df["close"], window=200 * candles_per_day).sma_indicator()

    # ✅ EMA
    df["ema_9"] = EMAIndicator(close=df["close"], window=9 * candles_per_day).ema_indicator()
    df["ema_21"] = EMAIndicator(close=df["close"], window=21 * candles_per_day).ema_indicator()
    df["ema_50"] = EMAIndicator(close=df["close"], window=50 * candles_per_day).ema_indicator()
    df["ema_111"] = EMAIndicator(close=df["close"], window=111 * candles_per_day).ema_indicator()
    df["ema_350"] = EMAIndicator(close=df["close"], window=350 * candles_per_day).ema_indicator()
    df["ema_350_2x"] = df["ema_350"] * 2

    # ✅ RSI
    df["rsi_14"] = RSIIndicator(close=df["close"], window=14 * candles_per_day).rsi()

    # ✅ MACD
    macd = MACD(close=df["close"], window_slow=26 * candles_per_day, window_fast=12 * candles_per_day, window_sign=9 * candles_per_day)
    df["macd_line"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()

    # ✅ Bollinger Bands
    bb = BollingerBands(close=df["close"], window=20 * candles_per_day, window_dev=2)
    df["bb_mavg"] = bb.bollinger_mavg()
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]

    # ✅ Pi Cycle Top Cross (convertido para int: 1 se cruzou, 0 caso contrário)
    df["pi_cycle_cross"] = (
            (df["ema_111"] > df["ema_350_2x"]) &
            (df["ema_111"].shift(1) <= df["ema_350_2x"].shift(1))
    ).astype(int)

    return df
