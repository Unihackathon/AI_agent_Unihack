import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from data_collection import FinancialDataCollector
from data_analysis import FinancialAnalyzer

class FinancialDashboard:
    def __init__(self):
        self.collector = FinancialDataCollector()
        self.analyzer = FinancialAnalyzer()
        
    def run_dashboard(self):
        """Main dashboard function"""
        st.title("Financial Data Analysis Dashboard")
        
        # Sidebar for user inputs
        st.sidebar.header("Settings")
        symbol = st.sidebar.text_input("Enter Stock Symbol", value="TSLA")
        period = st.sidebar.selectbox(
            "Select Time Period",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=2
        )
        
        # Fetch and analyze data
        data = self.collector.get_stock_data(symbol, period)
        if data is not None:
            data = self.analyzer.calculate_technical_indicators(data)
            insights = self.analyzer.generate_insights(symbol, period)
            
            # Display main price chart
            self._plot_price_chart(data, symbol)
            
            # Display technical indicators
            self._plot_technical_indicators(data)
            
            # Display statistics and insights
            self._display_insights(insights)
            
            # Display crypto comparison if requested
            if st.sidebar.checkbox("Compare with Cryptocurrency"):
                crypto_symbol = st.sidebar.selectbox(
                    "Select Crypto",
                    options=["btcusd", "ethusd"],
                    index=0
                )
                self._plot_crypto_comparison(symbol, crypto_symbol)
        else:
            st.error(f"No data found for symbol {symbol}")

    def _plot_price_chart(self, data: pd.DataFrame, symbol: str):
        """Create main price and volume chart"""
        st.subheader(f"{symbol} Price Chart")
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'{symbol} Price', 'Volume'),
            row_width=[0.7, 0.3]
        )

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC'
            ),
            row=1, col=1
        )

        # Add moving averages
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['SMA_20'],
                name='SMA 20',
                line=dict(color='orange')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['SMA_50'],
                name='SMA 50',
                line=dict(color='blue')
            ),
            row=1, col=1
        )

        # Volume bar chart
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume'
            ),
            row=2, col=1
        )

        fig.update_layout(
            height=800,
            xaxis_rangeslider_visible=False,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    def _plot_technical_indicators(self, data: pd.DataFrame):
        """Plot technical indicators"""
        st.subheader("Technical Indicators")
        
        # Create tabs for different indicators
        tabs = st.tabs(["RSI", "MACD", "Bollinger Bands"])
        
        with tabs[0]:
            self._plot_rsi(data)
            
        with tabs[1]:
            self._plot_macd(data)
            
        with tabs[2]:
            self._plot_bollinger_bands(data)

    def _plot_rsi(self, data: pd.DataFrame):
        """Plot RSI indicator"""
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['RSI'],
                name='RSI'
            )
        )
        
        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red")
        fig.add_hline(y=30, line_dash="dash", line_color="green")
        
        fig.update_layout(
            title="Relative Strength Index (RSI)",
            yaxis_title="RSI",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _plot_macd(self, data: pd.DataFrame):
        """Plot MACD indicator"""
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['MACD_12_26_9'],
                name='MACD'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['MACDs_12_26_9'],
                name='Signal'
            ),
            row=1, col=1
        )
        
        # MACD Histogram
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['MACDh_12_26_9'],
                name='MACD Histogram'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Moving Average Convergence Divergence (MACD)",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _plot_bollinger_bands(self, data: pd.DataFrame):
        """Plot Bollinger Bands"""
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['BBU_20_2.0'],
                name='Upper Band',
                line=dict(color='gray')
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['BBM_20_2.0'],
                name='Middle Band',
                line=dict(color='blue')
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['BBL_20_2.0'],
                name='Lower Band',
                line=dict(color='gray')
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Close Price',
                line=dict(color='black')
            )
        )
        
        fig.update_layout(
            title="Bollinger Bands",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _display_insights(self, insights: Dict[str, Any]):
        """Display analysis insights"""
        st.subheader("Analysis Insights")
        
        # Create columns for different metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Price Statistics")
            stats = insights.get('statistics', {})
            if stats:
                st.metric(
                    "Current Price",
                    f"${stats['current_price']:.2f}",
                    f"{stats['price_change']['1d']:.2f}%"
                )
                st.metric(
                    "Volatility (Annualized)",
                    f"{stats['volatility']*100:.2f}%"
                )

        with col2:
            st.write("Trading Signals")
            signals = insights.get('signals', [])
            for signal in signals:
                st.info(signal)

        # Display trend analysis
        trend = insights.get('trend_analysis', {})
        if trend:
            st.write("Trend Analysis")
            cols = st.columns(3)
            cols[0].metric("Short-term Trend", trend['short_term'])
            cols[1].metric("Medium-term Trend", trend['medium_term'])
            cols[2].metric("Trend Strength", trend['strength'])

    def _plot_crypto_comparison(self, stock_symbol: str, crypto_symbol: str):
        """Plot comparison between stock and cryptocurrency"""
        st.subheader(f"Comparison: {stock_symbol} vs {crypto_symbol}")
        
        # Get crypto data
        crypto_data = self.collector.get_crypto_data(crypto_symbol)
        if crypto_data:
            st.metric(
                f"{crypto_symbol.upper()} Price",
                f"${crypto_data['last_price']:.2f}",
                f"Volume: ${crypto_data['volume']:,.0f}"
            )

# Run the dashboard
if __name__ == "__main__":
    dashboard = FinancialDashboard()
    dashboard.run_dashboard() 