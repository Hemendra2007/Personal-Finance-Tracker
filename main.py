import pandas as pd
from datetime import datetime
from collections import defaultdict
import csv
import matplotlib.pyplot as plt

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

    def show_transactions(self, filtered_transactions=None):
        transactions_to_show = filtered_transactions if filtered_transactions else self.transactions
        for transaction in transactions_to_show:
            print(transaction)

    def total_balance(self, filtered_transactions=None):
        transactions_to_sum = filtered_transactions if filtered_transactions else self.transactions
        return sum(t.amount for t in transactions_to_sum)

    def category_summary(self, filtered_transactions=None):
        summary = defaultdict(float)
        transactions_to_summarize = filtered_transactions if filtered_transactions else self.transactions
        for t in transactions_to_summarize:
            summary[t.category] += t.amount
        return summary

    def summary_by_category(self, filtered_transactions=None):
        summary = self.category_summary(filtered_transactions)
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

    def filter_by_date_range(self, start_date, end_date):
        return [t for t in self.transactions if start_date <= t.date <= end_date]

    def filter_by_category(self, category):
        return [t for t in self.transactions if t.category == category]

    def plot_category_summary(self):
        summary = self.category_summary()
        categories = list(summary.keys())
        amounts = list(summary.values())

        plt.figure(figsize=(10, 7))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Spending by Category")
        plt.show()

    def plot_monthly_trends(self):
        monthly_summary = defaultdict(float)
        for t in self.transactions:
            month = t.date.strftime('%Y-%m')
            monthly_summary[month] += t.amount
        
        months = sorted(monthly_summary.keys())
        amounts = [monthly_summary[m] for m in months]

        plt.figure(figsize=(12, 6))
        plt.bar(months, amounts, color='skyblue')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Monthly Spending Trends')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def get_valid_date(prompt):
    while True:
        try:
            return datetime.fromisoformat(input(prompt))
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def main_menu():
    tracker = FinanceTracker()
    tracker.load_from_csv()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. Show Transactions")
        print("3. Show Category Summary")
        print("4. Show Total Balance")
        print("5. Filter Transactions by Date")
        print("6. Filter Transactions by Category")
        print("7. Plot Spending by Category")
        print("8. Plot Monthly Spending Trends")
        print("9. Save Transactions")
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            date = get_valid_date("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description (optional): ")
            tracker.add_transaction(Transaction(date, amount, category, description))

        elif choice == '2':
            tracker.show_transactions()

        elif choice == '3':
            tracker.summary_by_category()

        elif choice == '4':
            print("Total Balance:", tracker.total_balance())

        elif choice == '5':
            start_date = get_valid_date("Enter start date (YYYY-MM-DD): ")
            end_date = get_valid_date("Enter end date (YYYY-MM-DD): ")
            filtered_transactions = tracker.filter_by_date_range(start_date, end_date)
            tracker.show_transactions(filtered_transactions)
            print("Filtered Total Balance:", tracker.total_balance(filtered_transactions))

        elif choice == '6':
            category = input("Enter category to filter: ")
            filtered_transactions = tracker.filter_by_category(category)
            tracker.show_transactions(filtered_transactions)
            print("Filtered Total Balance:", tracker.total_balance(filtered_transactions))

        elif choice == '7':
            tracker.plot_category_summary()

        elif choice == '8':
            tracker.plot_monthly_trends()

        elif choice == '9':
            tracker.save_to_csv()
            print("Transactions saved.")

        elif choice == '10':
            tracker.save_to_csv()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
