# Stock Portfolio Tracker

A simple console program that calculates the total value of a stock portfolio from manually defined prices,
and can save the result to a `.txt` or `.csv` file.

## Run
```bash
python portfolio_tracker.py        # Python 3.8+, no extra packages
python test_portfolio_tracker.py   # 13 automated tests
```

## How to use
1. The program lists the available stocks and prices.
2. Enter a stock symbol (any case), then the number of shares. Repeat for each stock you own.
3. Type `done` to finish. The program prints each holding's value and the **total investment**.
4. Choose `txt`, `csv` or `no` to save the report (`portfolio.txt` / `portfolio.csv` in the current folder).

Example:
```
Stock     Shares       Price         Value
------------------------------------------
AAPL          12     $180.00     $2,160.00
TSLA           5     $250.00     $1,250.00
------------------------------------------
TOTAL INVESTMENT                 $3,410.00
```
Unknown symbols, non-numeric or zero quantities are rejected and you are asked again. Entering the same stock
twice adds the shares together.

## Changing the prices
Edit the `STOCK_PRICES` dictionary at the top of `portfolio_tracker.py`:
```python
STOCK_PRICES = {"AAPL": 180, "TSLA": 250, "GOOGL": 140, "MSFT": 330, "AMZN": 135}
```
These are fixed example prices, not live market data.

## Project structure
```
stock_portfolio_tracker/
├── portfolio_tracker.py        # the program
├── test_portfolio_tracker.py   # unittest tests (scripted input, temporary folders for files)
└── README.md
```

## Concepts demonstrated
| Concept | Where |
|---|---|
| Dictionary | `STOCK_PRICES` (symbol -> price) and the portfolio (symbol -> quantity) |
| Input / output | `ask_symbol`, `ask_quantity`, `format_report` |
| Basic arithmetic | `calculate`: value = quantity x price, total = sum of values |
| File handling | `save_txt` (text file) and `save_csv` (csv module) |

## Ideas to extend
Remove or edit holdings, show each stock's percentage of the portfolio, load prices from a file, fetch live prices from an API,
or track purchase price to show profit and loss.
