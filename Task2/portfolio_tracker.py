"""
Stock Portfolio Tracker - a simple console program.

You enter stock symbols and how many shares you own. The program looks up each price in a hardcoded
dictionary, calculates the value of every holding and the total investment, and can save the result
to a .txt or .csv file.

Concepts used: dictionary, input/output, basic arithmetic, file handling.
Run it with:  python portfolio_tracker.py
"""
import csv
from datetime import datetime

# ----------------------------------------------------------------------------- price list
# Prices are defined manually (US dollars per share) - no internet or API needed.
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 330,
    "AMZN": 135,
}


# ----------------------------------------------------------------------------- input
def ask_symbol(prices=STOCK_PRICES):
    """Ask for a stock symbol until it is valid. Returns the symbol, or None if the user types 'done'."""
    while True:
        text = input("\nStock symbol (or 'done' to finish): ").strip().upper()
        if text == "DONE":
            return None
        if text in prices:
            return text
        print(f"'{text}' is not in the price list. Choose from: {', '.join(prices)}")


def ask_quantity(symbol):
    """Ask for a whole number of shares greater than zero."""
    while True:
        text = input(f"How many shares of {symbol}? ").strip()
        if not text.isdigit():
            print("Please enter a whole number, e.g. 10.")
        elif int(text) == 0:
            print("Quantity must be at least 1.")
        else:
            return int(text)


def collect_portfolio(prices=STOCK_PRICES):
    """Let the user build a portfolio: a dictionary {symbol: quantity}."""
    portfolio = {}
    while True:
        symbol = ask_symbol(prices)
        if symbol is None:
            break
        quantity = ask_quantity(symbol)
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity    # adding the same stock twice combines it
        print(f"Added {quantity} x {symbol}.")
    return portfolio


# ----------------------------------------------------------------------------- calculation
def calculate(portfolio, prices=STOCK_PRICES):
    """Return (rows, total). Each row is (symbol, quantity, price, value)."""
    rows = []
    total = 0
    for symbol, quantity in portfolio.items():
        price = prices[symbol]
        value = quantity * price
        rows.append((symbol, quantity, price, value))
        total += value
    return rows, total


def money(amount):
    return f"${amount:,.2f}"


def format_report(rows, total):
    """Build the table that is printed on screen and saved to the .txt file."""
    lines = [f"{'Stock':<8}{'Shares':>8}{'Price':>12}{'Value':>14}", "-" * 42]
    for symbol, quantity, price, value in rows:
        lines.append(f"{symbol:<8}{quantity:>8}{money(price):>12}{money(value):>14}")
    lines.append("-" * 42)
    lines.append(f"{'TOTAL INVESTMENT':<28}{money(total):>14}")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- file handling
def save_txt(rows, total, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Stock Portfolio Report\n")
        f.write(f"Date: {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write(format_report(rows, total) + "\n")


def save_csv(rows, total, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock", "Shares", "Price", "Value"])
        writer.writerows(rows)
        writer.writerow(["TOTAL", "", "", total])


def offer_to_save(rows, total):
    choice = input("\nSave this report? (txt / csv / no): ").strip().lower()
    if choice == "txt":
        save_txt(rows, total, "portfolio.txt")
        print("Saved to portfolio.txt")
    elif choice == "csv":
        save_csv(rows, total, "portfolio.csv")
        print("Saved to portfolio.csv")
    else:
        print("Not saved.")


# ----------------------------------------------------------------------------- main
def main():
    print("=== STOCK PORTFOLIO TRACKER ===")
    print("Available stocks and prices:")
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol:<6} {money(price)}")

    portfolio = collect_portfolio()
    if not portfolio:
        print("\nNo stocks entered. Goodbye!")
        return

    rows, total = calculate(portfolio)
    print("\n" + format_report(rows, total))
    offer_to_save(rows, total)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram ended. Goodbye!")
