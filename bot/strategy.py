# strategy.py

import pandas as pd
from .config import RSI_UPPER, RSI_LOWER
from .indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands

class TradingStrategy:
    def __init__(self):
        """
        Advanced confluence strategy matching user requirements.
        Uses RSI, MACD, and Bollinger Bands to secure accurate signals.
        """
        self.rsi_buy = RSI_LOWER   # Set to 30 from config
        self.rsi_sell = RSI_UPPER  # Set to 70 from config

    def generate_signal(self, market_data: pd.DataFrame) -> str:
        """
        Analyzes candlestick data to return 'BUY', 'SELL', or 'HOLD'.
        Confluence Rules:
        - BUY: RSI < 30 AND MACD Bullish Cross AND Price <= Lower Bollinger Band
        - SELL: RSI > 70 AND MACD Bearish Cross AND Price >= Upper Bollinger Band
        """
        # Ensure enough data bars are available for accurate calculation
        if len(market_data) < 26:
            return "HOLD"

        # 1) Calculate RSI
        rsi_series = calculate_rsi(market_data, period=14)
        current_rsi = rsi_series.iloc[-1]

        # 2) Calculate MACD
        macd_df = calculate_macd(market_data)
        macd_col = [c for c in macd_df.columns if c.startswith("MACD_") and not c.startswith("MACDh_")][0]
        signal_col = [c for c in macd_df.columns if c.startswith("MACDs_")][0]

        macd_line_current = macd_df[macd_col].iloc[-1]
        macd_line_previous = macd_df[macd_col].iloc[-2]
        macd_signal_current = macd_df[signal_col].iloc[-1]
        macd_signal_previous = macd_df[signal_col].iloc[-2]

        # 3) Calculate Bollinger Bands
        bb_df = calculate_bollinger_bands(market_data)
        bbl_col = [c for c in bb_df.columns if c.startswith("BBL")][0]  # Lower band
        bbu_col = [c for c in bb_df.columns if c.startswith("BBU")][0]  # Upper band

        price_current = market_data["close"].iloc[-1]
        lower_band = bb_df[bbl_col].iloc[-1]
        upper_band = bb_df[bbu_col].iloc[-1]

        # Confluence Signals Verification
        touching_lower_band = (price_current <= lower_band)
        touching_upper_band = (price_current >= upper_band)

        rsi_buy_signal = (current_rsi < self.rsi_buy)
        rsi_sell_signal = (current_rsi > self.rsi_sell)

        macd_bullish_cross = (
            macd_line_current > macd_signal_current and
            macd_line_previous <= macd_signal_previous
        )
        macd_bearish_cross = (
            macd_line_current < macd_signal_current and
            macd_line_previous >= macd_signal_previous
        )

        # Execute absolute safe entries
        if rsi_buy_signal and macd_bullish_cross and touching_lower_band:
            return "BUY"
        elif rsi_sell_signal and macd_bearish_cross and touching_upper_band:
            return "SELL"
        else:
            return "HOLD"
