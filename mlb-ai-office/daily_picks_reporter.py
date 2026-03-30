class BankrollManager:
    def __init__(self, initial_bankroll, unit_size_pct, kelly_fraction):
        self.initial_bankroll = initial_bankroll
        self.unit_size_pct = unit_size_pct
        self.kelly_fraction = kelly_fraction
        self.current_bankroll = initial_bankroll
        self.history = []

    def get_flat_bet(self):
        return self.current_bankroll * self.unit_size_pct / 100

    def calculate_kelly_bet(self, odds: float, probability: float) -> float:
        fraction = probability - (1 - probability) / odds
        return self.current_bankroll * self.kelly_fraction * fraction

    def place_bet(self, amount: float):
        if amount <= self.current_bankroll:
            self.current_bankroll -= amount
            self.history.append(amount)
            return True
        return False

    def show_summary(self):
        return {
            'initial_bankroll': self.initial_bankroll,
            'current_bankroll': self.current_bankroll,
            'total_bets': len(self.history),
            'bet_history': self.history
        }

    def _save_history(self):
        # Implement saving history to a file or database
        pass

    def _load_history(self):
        # Implement loading history from a file or database
        pass


class DailyMLBPicksReporter:
    def __init__(self):
        self.picks = []

    def generate_report(self):
        # Generate picks for the day
        pass

    def save_report_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self.picks))
