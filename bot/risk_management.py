# risk_management.py
from .config import MAX_WINS, MAX_LOSSES

class RiskManager:
    """
    Manages risk based on specific win/loss session targets:
    - Stop after 8 wins
    - Stop after 2 losses
    """

    def __init__(self):
        self.max_wins = MAX_WINS
        self.max_losses = MAX_LOSSES
        self.current_wins = 0
        self.current_losses = 0

    def update_session(self, is_win: bool):
        """
        Updates the session counter after each trade.
        """
        if is_win:
            self.current_wins += 1
        else:
            self.current_losses += 1

    def should_stop(self) -> bool:
        """
        Checks if the session targets have been met to stop the bot.
        """
        if self.current_wins >= self.max_wins:
            print(f"Target Reached: {self.current_wins} Wins. Stopping session.")
            return True
        
        if self.current_losses >= self.max_losses:
            print(f"Stop Loss Reached: {self.current_losses} Losses. Stopping session.")
            return True
            
        return False

    def reset_session(self):
        """
        Resets the counters for a new trading session.
        """
        self.current_wins = 0
        self.current_losses = 0

    def get_trade_amount(self, base_amount: float) -> float:
        """
        Returns the fixed trade amount as specified in config.
        """
        return base_amount
