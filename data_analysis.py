import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from data_collection import FinancialDataCollector
import pandas_ta as ta

class FinancialAnalyzer:
    def __init__(self):
        self.collector = FinancialDataCollector()

    def calculate_technical_indicators(
        self, 
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate technical indicators for the given financial data
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with additional technical indicators
        """
        try:
            # RSI
            df['RSI'] = ta.rsi(df['Close'], length=14)
            
            # MACD
            macd = ta.macd(df['Close'])
            df = pd.concat([df, macd], axis=1)
            
            # Bollinger Bands
            bb = ta.bbands(df['Close'])
            df = pd.concat([df, bb], axis=1)
            
            # Average True Range (ATR)
            df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'])
            
            # Volume Moving Average
            df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
            
            return df
            
        except Exception as e:
            print(f"Error calculating technical indicators: {str(e)}")
            return df

    def generate_statistics(
        self, 
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Generate statistical analysis of the financial data
        
        Args:
            df: DataFrame with financial data
            
        Returns:
            Dictionary containing statistical metrics
        """
        try:
            return {
                'daily_returns': {
                    'mean': df['Close'].pct_change().mean(),
                    'std': df['Close'].pct_change().std(),
                    'skew': df['Close'].pct_change().skew()
                },
                'volatility': df['Close'].pct_change().std() * np.sqrt(252),  # Annualized volatility
                'current_price': df['Close'].iloc[-1],
                'price_change': {
                    '1d': self._calculate_change(df['Close'], 1),
                    '1w': self._calculate_change(df['Close'], 5),
                    '1m': self._calculate_change(df['Close'], 20)
                },
                'volume_analysis': {
                    'avg_volume': df['Volume'].mean(),
                    'volume_trend': self._calculate_change(df['Volume'], 5)
                }
            }
            
        except Exception as e:
            print(f"Error generating statistics: {str(e)}")
            return {}

    def generate_insights(
        self, 
        symbol: str, 
        period: str = "6mo"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive insights for a financial instrument
        
        Args:
            symbol: Trading symbol
            period: Time period for analysis
            
        Returns:
            Dictionary containing analysis insights
        """
        try:
            # Fetch data
            df = self.collector.get_stock_data(symbol, period)
            if df is None:
                return {}
            
            # Calculate indicators
            df = self.calculate_technical_indicators(df)
            print("Fetching data...cripto")
            
            # Generate statistics
            stats = self.generate_statistics(df)
            
            # Generate trading signals
            signals = self._generate_trading_signals(df)
            
            print(df, "\nstats\n",stats, "signals\n",signals)
            # Identify key levels
            support, resistance = self._identify_key_levels(df)
            
            return {
                'statistics': stats,
                'signals': signals,
                'key_levels': {
                    'support': support,
                    'resistance': resistance
                },
                'trend_analysis': self._analyze_trend(df),
                'risk_metrics': self._calculate_risk_metrics(df)
            }
            
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return {}

    def _calculate_change(
        self, 
        series: pd.Series, 
        periods: int
    ) -> float:
        """Calculate percentage change over specified periods"""
        if len(series) < periods:
            return 0.0
        return ((series.iloc[-1] / series.iloc[-periods-1]) - 1) * 100

    def _generate_trading_signals(
        self, 
        df: pd.DataFrame
    ) -> List[str]:
        """Generate trading signals based on technical indicators"""
        signals = []
        
        # RSI signals
        if df['RSI'].iloc[-1] < 30:
            signals.append("RSI indicates oversold conditions")
        elif df['RSI'].iloc[-1] > 70:
            signals.append("RSI indicates overbought conditions")
            
        # MACD signals
        if df['MACD_12_26_9'].iloc[-1] > df['MACDs_12_26_9'].iloc[-1] and \
           df['MACD_12_26_9'].iloc[-2] <= df['MACDs_12_26_9'].iloc[-2]:
            signals.append("MACD bullish crossover")
        elif df['MACD_12_26_9'].iloc[-1] < df['MACDs_12_26_9'].iloc[-1] and \
             df['MACD_12_26_9'].iloc[-2] >= df['MACDs_12_26_9'].iloc[-2]:
            signals.append("MACD bearish crossover")
            
        return signals

    def _identify_key_levels(
        self, 
        df: pd.DataFrame
    ) -> Tuple[List[float], List[float]]:
        """Identify support and resistance levels"""
        try:
            # Simple method using recent highs and lows
            window = 20
            support = df['Low'].rolling(window=window).min().iloc[-1]
            resistance = df['High'].rolling(window=window).max().iloc[-1]
            
            return [support], [resistance]
            
        except Exception as e:
            print(f"Error identifying key levels: {str(e)}")
            return [], []

    def _analyze_trend(
        self, 
        df: pd.DataFrame
    ) -> Dict[str, str]:
        """Analyze current market trend"""
        try:
            # Simple trend analysis using moving averages
            current_price = df['Close'].iloc[-1]
            sma_20 = df['SMA_20'].iloc[-1]
            sma_50 = df['SMA_50'].iloc[-1]
            
            trend = {
                'short_term': 'bullish' if current_price > sma_20 else 'bearish',
                'medium_term': 'bullish' if current_price > sma_50 else 'bearish',
                'strength': 'strong' if abs(current_price - sma_20) / sma_20 > 0.02 else 'weak'
            }
            
            return trend
            
        except Exception as e:
            print(f"Error analyzing trend: {str(e)}")
            return {}

    def _calculate_risk_metrics(
        self, 
        df: pd.DataFrame
    ) -> Dict[str, float]:
        """Calculate risk-related metrics"""
        try:
            returns = df['Close'].pct_change().dropna()
            
            return {
                'volatility': returns.std() * np.sqrt(252),
                'var_95': returns.quantile(0.05),
                'max_drawdown': (df['Close'] / df['Close'].cummax() - 1).min(),
                'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(252)
            }
            
        except Exception as e:
            print(f"Error calculating risk metrics: {str(e)}")
            return {}

# Example usage
if __name__ == "__main__":
    analyzer = FinancialAnalyzer()
    
    # Test analysis for Tesla stock
    insights = analyzer.generate_insights('TSLA')
    
    if insights:
        print("\nTesla Analysis Insights:")
        for category, data in insights.items():
            print(f"\n{category.upper()}:")
            print(data) 