import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class FinancialDataCollector:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_base_url = "https://api.gemini.com/v1"

    def get_stock_data(
        self, symbol: str, period: str = "6mo", interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data using yfinance

        Args:
            symbol: Stock ticker symbol
            period: Time period to fetch (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

        Returns:
            DataFrame with historical stock data
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                print(f"No data found for symbol {symbol}")
                return None

            # Add basic technical indicators
            df["SMA_20"] = df["Close"].rolling(window=20).mean()
            df["SMA_50"] = df["Close"].rolling(window=50).mean()

            # Add Bollinger Bands
            std_dev = df["Close"].rolling(window=20).std()
            df["BBU_20_2.0"] = df["SMA_20"] + (std_dev * 2)
            df["BBM_20_2.0"] = df["SMA_20"]
            df["BBL_20_2.0"] = df["SMA_20"] - (std_dev * 2)

            return df

        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {str(e)}")
            return None

    def get_crypto_data(self, symbol: str = "btcusd") -> Optional[Dict[str, Any]]:
        """
        Fetch cryptocurrency data from Gemini API

        Args:
            symbol: Cryptocurrency symbol (e.g., 'btcusd', 'ethusd')

        Returns:
            Dictionary containing current crypto data
        """
        try:
            # Get ticker information
            ticker_url = f"{self.gemini_base_url}/pubticker/{symbol}"
            response = requests.get(ticker_url)
            response.raise_for_status()

            # Get recent trades
            trades_url = f"{self.gemini_base_url}/trades/{symbol}"
            trades_response = requests.get(trades_url)
            trades_response.raise_for_status()

            ticker_data = response.json()
            trades_data = trades_response.json()

            # Calculate additional metrics
            recent_prices = [float(trade["price"]) for trade in trades_data[:100]]
            avg_price = sum(recent_prices) / len(recent_prices)

            return {
                "symbol": symbol,
                "last_price": float(ticker_data["last"]),
                "bid": float(ticker_data["bid"]),
                "ask": float(ticker_data["ask"]),
                "volume": float(ticker_data["volume"]["USD"]),
                "avg_price": avg_price,
                "timestamp": datetime.fromtimestamp(
                    float(ticker_data["volume"]["timestamp"]) / 1000
                ),
                "recent_trades": trades_data[:10],
            }

        except Exception as e:
            print(f"Error fetching crypto data for {symbol}: {str(e)}")
            return None

    def get_combined_data(
        self, stock_symbol: str, crypto_symbol: str
    ) -> Dict[str, Any]:
        """
        Fetch both stock and crypto data for comparison

        Args:
            stock_symbol: Stock ticker symbol
            crypto_symbol: Cryptocurrency symbol

        Returns:
            Dictionary containing both stock and crypto data
        """
        stock_data = self.get_stock_data(stock_symbol)
        crypto_data = self.get_crypto_data(crypto_symbol)

        return {"stock_data": stock_data, "crypto_data": crypto_data}


# Example usage
if __name__ == "__main__":
    collector = FinancialDataCollector()

    # Test stock data collection
    tesla_data = collector.get_stock_data("TSLA")
    if tesla_data is not None:
        print("\nTesla Stock Data:")
        print(tesla_data.tail())

    # Test crypto data collection
    btc_data = collector.get_crypto_data("btcusd")
    if btc_data is not None:
        print("\nBitcoin Data:")
        print(btc_data)

    # Test combined data
    combined = collector.get_combined_data("TSLA", "btcusd")
    if combined["stock_data"] is not None and combined["crypto_data"] is not None:
        print("\nCombined Data Retrieved Successfully")
