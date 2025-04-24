import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, SMAIndicator, MACD
from ta.volatility import BollingerBands


def enrich_with_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona indicadores técnicos ao DataFrame:
    - SMA(10)
    - EMA(10)
    - RSI(14)
    - MACD (12, 26, 9)
    - Bollinger Bands (20, 2)
    """
    df = df.copy()

    if df.empty:
        raise ValueError("❌ DataFrame está vazio.")
    if "close" not in df.columns:
        raise KeyError("❌ Coluna 'close' não encontrada.")

    # ✅ SMA & EMA
    df["sma_10"] = SMAIndicator(close=df["close"], window=10).sma_indicator()
    df["ema_10"] = EMAIndicator(close=df["close"], window=10).ema_indicator()

    # ✅ RSI
    df["rsi_14"] = RSIIndicator(close=df["close"], window=14).rsi()

    # ✅ MACD
    macd = MACD(close=df["close"], window_slow=26, window_fast=12, window_sign=9)
    df["macd_line"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()

    # ✅ Bollinger Bands
    bb = BollingerBands(close=df["close"], window=20, window_dev=2)
    df["bb_mavg"] = bb.bollinger_mavg()
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]

    # ✅ Pi Cycle Indicator
    df["ema_111"] = EMAIndicator(close=df["close"], window=111).ema_indicator()
    df["ema_350_2x"] = EMAIndicator(close=df["close"], window=350).ema_indicator() * 2

    # Sinal de cruzamento (topo de mercado potencial)
    df["pi_cycle_cross"] = (
        (df["ema_111"] > df["ema_350_2x"]) &
        (df["ema_111"].shift(1) <= df["ema_350_2x"].shift(1))
    )

    return df
