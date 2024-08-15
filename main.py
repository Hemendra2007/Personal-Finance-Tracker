import pandas as pd
from datetime import datetime
from collections import defaultdict
import csv

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

    def category_summary(self):
        summary = defaultdict(float)
        for t in self.transactions:
            summary[t.category] += t.amount
        return summary

    def summary_by_category(self):
        summary = self.category_summary()
        for category, total in summary.items():
            print(f"{category}: {total}")

    def save_to_csv(self, file_path='transactions.csv'):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Amount', 'Category', 'Description'])
            for t in self.transactions:
                writer.writerow([t.date, t.amount, t.category, t.description])

    def load_from_csv(self, file_path='transactions.csv'):
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.transactions.append(Transaction(
                        datetime.fromisoformat(row['Date']),
                        float(row['Amount']),
                        row['Category'],
                        row['Description']
                    ))
        except FileNotFoundError:
            print("No transactions found.")

if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.load_from_csv()

    tracker.add_transaction(Transaction(datetime.now(), 50, "Food", "Grocery shopping"))
    tracker.add_transaction(Transaction(datetime.now(), -20, "Transport", "Taxi fare"))
    tracker.add_transaction(Transaction(datetime.now(), 100, "Income", "Freelance work"))
    tracker.add_transaction(Transaction(datetime.now(), -30, "Entertainment", "Movie tickets"))

    tracker.show_transactions()
    print("Total Balance:", tracker.total_balance())

    print("\nCategory Summary:")
    tracker.summary_by_category()

    tracker.save_to_csv()
