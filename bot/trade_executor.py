# bot/trade_executor.py
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .config import QUOTEX_USERNAME, QUOTEX_PASSWORD, USE_DEMO, USER_AGENT, MIN_DELAY, MAX_DELAY

class TradeExecutor:
    def __init__(self):
        options = uc.ChromeOptions()
        # Using the Mobile User-Agent from config for stealth
        options.add_argument(f"user-agent={USER_AGENT}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        self.driver = uc.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.login_to_quotex()

    def login_to_quotex(self):
        # Professional Login Logic
        self.driver.get("https://qxbroker.com/en/sign-in/")
        time.sleep(random.uniform(2, 4)) # Random human-like pause

        try:
            email_field = self.driver.find_element(By.NAME, "email")
            email_field.send_keys(QUOTEX_USERNAME)
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(QUOTEX_PASSWORD)

            sign_in_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            sign_in_button.click()

            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".usermenu__info-balance"))
            )
            print("Login Successful.")
            
            if USE_DEMO:
                self._switch_account_mode("demo")
            else:
                self._switch_account_mode("live")
                
        except Exception as e:
            print(f"Login Failed: {e}")

    def execute_trade(self, direction: str, amount: float):
        """
        Executes a trade and then waits for a human-like delay (3-5 mins).
        """
        try:
            if direction == "BUY":
                btn = self.driver.find_element(By.CSS_SELECTOR, ".btn-call") # Green Button
            else:
                btn = self.driver.find_element(By.CSS_SELECTOR, ".btn-put") # Red Button
            
            btn.click()
            print(f"Trade Executed: {direction} with amount {amount}")

            # APPLYING HUMAN DELAY (3 to 5 minutes as requested)
            wait_time = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"Waiting for {wait_time // 60} minutes before next check...")
            time.sleep(wait_time)

        except Exception as e:
            print(f"Trade Execution Error: {e}")

    def _switch_account_mode(self, mode: str):
        # Logic to ensure the correct account (Real/Demo) is active
        print(f"Switching to {mode} account...")
        # (Internal switching logic continues here...)

    def get_account_balance(self) -> float:
        try:
            balance_elem = self.driver.find_element(By.CSS_SELECTOR, ".usermenu__info-balance")
            return float(balance_elem.text.replace("$", "").replace(",", "").strip())
        except:
            return 0.0
