# indicators.py
import pandas as pd
import pandas_ta as ta
from .config import BOLLINGER_PERIOD, BOLLINGER_STD_DEV

def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate RSI using pandas_ta for accurate overbought/oversold signals.
    """
    if "close" not in data.columns:
        raise ValueError("Close column missing for RSI calculation.")
    return ta.rsi(data["close"], length=period)

def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """
    Calculate MACD for trend crossover confirmation.
    """
    if "close" not in data.columns:
        raise ValueError("Close column missing for MACD calculation.")
    return ta.macd(data["close"], fast=fast, slow=slow, signal=signal)

def calculate_bollinger_bands(data: pd.DataFrame, period: int = BOLLINGER_PERIOD, std_dev: float = BOLLINGER_STD_DEV) -> pd.DataFrame:
    """
    Calculate Bollinger Bands to detect price volatility and reversals.
    """
    if "close" not in data.columns:
        raise ValueError("Close column missing for Bollinger Bands calculation.")
    return ta.bbands(data["close"], length=period, std=std_dev)
