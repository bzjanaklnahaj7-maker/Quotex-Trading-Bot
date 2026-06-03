# main.py
import time
import random
import logging
from .strategy import TradingStrategy
from .risk_management import RiskManager
from .trade_executor import TradeExecutor
from .config import TRADE_AMOUNT, MIN_DELAY, MAX_DELAY, APP_LOCK_CODE

# Configure Professional Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def main():
    # --- SECURITY CHECK ---
    # Access control for Alking App
    secret = input("Enter Activation Code to start Alking: ")
    if secret != APP_LOCK_CODE:
        logging.error("Unauthorized Access! Closing app.")
        return

    logging.info("Initializing Alking Intelligent Terminal...")
    executor = TradeExecutor()
    strategy = TradingStrategy()
    risk_manager = RiskManager()

    try:
        while True:
            # Check Session Limits (8 Wins or 2 Losses)
            if risk_manager.should_stop():
                logging.info("Session Target Met. Shutting down for safety.")
                break

            logging.info("===== Scanning Market for Opportunities =====")

            # 1) Sync Account Balance
            current_balance = executor.get_account_balance()
            logging.info(f"Current Balance: ${current_balance}")

            # 2) Fetch Live Market Data (Online Sync)
            market_data = executor.fetch_market_data()
            
            # 3) Generate Analysis Signal (RSI + Bollinger)
            signal = strategy.generate_signal(market_data)
            logging.info(f"Signal Result: {signal}")

            # 4) Execute Logic with Session Tracking
            if signal in ["BUY", "SELL"]:
                # Execute Trade
                executor.execute_trade(direction=signal, amount=TRADE_AMOUNT)
                
                # Update Risk Manager (This part will be synced with win/loss detection)
                # For now, it logs the attempt and prepares for next cycle
                logging.info(f"Trade {signal} executed. Initiating Human-Like Delay...")
                
                # 5) Human-Like Delay (3 to 5 minutes randomized)
                wait_time = random.randint(MIN_DELAY, MAX_DELAY)
                logging.info(f"Stealth Mode: Waiting {wait_time // 60} minutes before next scan.")
                time.sleep(wait_time)
            else:
                logging.info("No strong confluence found. Waiting 60 seconds for next candle...")
                time.sleep(60)

    except Exception as e:
        logging.error(f"System Error: {e}")

    finally:
        logging.info("Alking Terminal Closing. Protecting your data...")
        executor.driver.quit()

if __name__ == "__main__":
    main()
