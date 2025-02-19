To get stock data using the Yahoo Finance API (via the `yfinance` Python package), you need to use stock ticker symbols. Here are some common stock tickers you can use:

### U.S. Stock Market:
- **Technology:**
  - Apple Inc. – `AAPL`
  - Microsoft Corp. – `MSFT`
  - Alphabet Inc. (Google) – `GOOGL` (Class A), `GOOG` (Class C)
  - Amazon.com Inc. – `AMZN`
  - Meta Platforms Inc. (Facebook) – `META`
  - NVIDIA Corp. – `NVDA`
  - Tesla Inc. – `TSLA`

- **Financials:**
  - JPMorgan Chase & Co. – `JPM`
  - Bank of America – `BAC`
  - Wells Fargo & Co. – `WFC`

- **Consumer Goods:**
  - Procter & Gamble – `PG`
  - Coca-Cola – `KO`
  - PepsiCo – `PEP`

- **Healthcare:**
  - Johnson & Johnson – `JNJ`
  - Pfizer Inc. – `PFE`
  - Moderna Inc. – `MRNA`

- **Energy:**
  - Exxon Mobil – `XOM`
  - Chevron Corp. – `CVX`

- **Retail:**
  - Walmart Inc. – `WMT`
  - Home Depot – `HD`

- **Entertainment:**
  - Netflix Inc. – `NFLX`
  - Walt Disney Co. – `DIS`

### Indices:
- S&P 500 – `^GSPC`
- Dow Jones Industrial Average – `^DJI`
- Nasdaq Composite – `^IXIC`

### Cryptocurrencies:
- Bitcoin – `BTC-USD`
- Ethereum – `ETH-USD`

### International Stocks:
- Alibaba Group (China) – `BABA`
- Tencent Holdings (China) – `TCEHY`
- Toyota Motor Corp. (Japan) – `TM`
- Samsung Electronics (South Korea) – `005930.KS`

### Example Usage with `yfinance`:
```python
import yfinance as yf

# Download historical data for Apple Inc.
apple_data = yf.download('AAPL', start='2022-01-01', end='2023-01-01')
print(apple_data.head())
```

### How to Find More Tickers:
You can find more ticker symbols on [Yahoo Finance](https://finance.yahoo.com) by searching for company names or browsing market sectors.