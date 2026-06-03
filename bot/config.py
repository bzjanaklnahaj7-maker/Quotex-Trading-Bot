# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- ACCOUNT CONFIGURATION ---
QUOTEX_USERNAME = os.environ.get('QUOTEX_EMAIL', 'demo@example.com')
QUOTEX_PASSWORD = os.environ.get('QUOTEX_PASSWORD', 'mypassword123')
ACCOUNT_MODE = os.environ.get("ACCOUNT_MODE", "PRACTICE").upper()
USE_DEMO = True if ACCOUNT_MODE == "PRACTICE" else False

# --- SECURITY ACCESS ---
# Secret code to access the Alking app
APP_LOCK_CODE = os.environ.get('APP_LOCK_CODE', '1234')

# --- TECHNICAL INDICATORS SETTINGS ---
RSI_PERIOD = 14
RSI_UPPER = 70
RSI_LOWER = 30
BOLLINGER_PERIOD = 20
BOLLINGER_STD_DEV = 2.0

# --- RISK & SESSION MANAGEMENT ---
TRADE_AMOUNT = float(os.environ.get('TRADE_AMOUNT', 1.0))
MAX_WINS = int(os.environ.get('MAX_WINS_PER_SESSION', 8))
MAX_LOSSES = int(os.environ.get('MAX_LOSS_PER_SESSION', 2))

# --- HUMAN STEALTH DELAY ---
MIN_DELAY = int(os.environ.get('MIN_DELAY', 180))
MAX_DELAY = int(os.environ.get('MAX_DELAY', 300))

# --- BROWSER IDENTITY (Anti-Detection) ---
USER_AGENT = "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
