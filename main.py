import pandas as pd
from datetime import datetime

class Transaction:
    def __init__(self, date, amount, category, description=""):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def __repr__(self):
        return f"{self.date} - {self.amount} - {self.category} ({self.description})"

class FinanceTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def show_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def total_balance(self):
        return sum(t.amount for t in self.transactions)

if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.add_transaction(Transaction(datetime.now(), 50, "Food", "Grocery shopping"))
    tracker.add_transaction(Transaction(datetime.now(), -20, "Transport", "Taxi fare"))
    tracker.add_transaction(Transaction(datetime.now(), 100, "Income", "Freelance work"))

    tracker.show_transactions()
    print("Total Balance:", tracker.total_balance())
