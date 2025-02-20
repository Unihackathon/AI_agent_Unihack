import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from typing import Dict, Any
from plotly.subplots import make_subplots
import os
from data_collection import FinancialDataCollector
from data_analysis import FinancialAnalyzer  # Import FinancialAnalyzer
from email_service import EmailReportService  # Correct import

# Configure page settings
st.set_page_config(page_title="Financial Data Analyzer", page_icon="📈", layout="wide")

# Constants
API_BASE_URL = os.getenv("BASE_URL")


class FinancialDashboardApp:
    def __init__(self):
        self.setup_session_state()
        self.collector = FinancialDataCollector()
        self.analyzer = FinancialAnalyzer()  # Initialize FinancialAnalyzer
        self.email_service = EmailReportService()  # Correct initialization

    def setup_session_state(self):
        """Initialize session state variables"""
        if "current_symbol" not in st.session_state:
            st.session_state.current_symbol = "TSLA"
        if "current_period" not in st.session_state:
            st.session_state.current_period = "6mo"

    def fetch_stock_data(self, symbol: str, period: str) -> pd.DataFrame:
        """Fetch stock data using FinancialDataCollector"""
        data = self.collector.get_stock_data(symbol, period)
        return data

    def fetch_analysis(self, symbol: str, period: str) -> Dict[str, Any]:
        """Fetch stock analysis from FinancialAnalyzer"""
        data = self.collector.get_stock_data(symbol, period)
        if data is not None:
            data = self.analyzer.calculate_technical_indicators(data)
            insights = self.analyzer.generate_insights(symbol, period)
            return insights
        else:
            st.error(f"No data found for symbol {symbol}")
            return None

    def process_query(self, query: str, symbol: str, period: str) -> str:
        """Process natural language query"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/query",
                json={"query": query, "symbol": symbol, "period": period},
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            return None

    def render_sidebar(self):
        """Render sidebar controls"""
        with st.sidebar:
            st.title("Settings")

            # Stock symbol input
            symbol = st.text_input(
                "Stock Symbol", value=st.session_state.current_symbol
            ).upper()

            # Time period selection
            period = st.selectbox(
                "Time Period", options=["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2
            )

            # Update button
            if st.button("Update Analysis"):
                st.session_state.current_symbol = symbol
                st.session_state.current_period = period

            st.divider()

            # Query section
            st.subheader("Ask Questions")
            query = st.text_area("Enter your question:")
            if st.button("Ask"):
                if query:
                    with st.spinner("Processing query..."):
                        response = self.process_query(query, symbol, period)
                        if response:
                            st.info(response)
                else:
                    st.warning("Please enter a question")

            st.divider()

            # Email report section
            st.subheader("Email Report")
            email = st.text_input("Enter your email address")
            if st.button("Send Report"):
                if email:
                    with st.spinner("Sending report..."):
                        success = self.send_email_report(email, symbol, period)
                        if success:
                            st.success("Report sent successfully!")
                        else:
                            st.error("Failed to send report")
                else:
                    st.warning("Please enter a valid email address")

    def render_main_content(self):
        """Render main dashboard content"""
        st.title(f"Financial Analysis Dashboard - {st.session_state.current_symbol}")

        # Fetch data and analysis
        with st.spinner("Fetching data..."):
            data = self.fetch_stock_data(
                st.session_state.current_symbol, st.session_state.current_period
            )
            insights = self.fetch_analysis(
                st.session_state.current_symbol, st.session_state.current_period
            )

        if data is not None and insights is not None:
            # Calculate technical indicators
            data = self.analyzer.calculate_technical_indicators(data)

            # Display main price chart
            self._plot_price_chart(data, st.session_state.current_symbol)

            # Display technical indicators
            self._plot_technical_indicators(data)

            # Display statistics and insights
            self._display_insights(insights)

    def _plot_price_chart(self, data: pd.DataFrame, symbol: str):
        """Create main price and volume chart"""
        st.subheader(f"{symbol} Price Chart")

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f"{symbol} Price", "Volume"),
            row_width=[0.7, 0.3],
        )

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="OHLC",
            ),
            row=1,
            col=1,
        )

        # Add moving averages
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["SMA_20"],
                name="SMA 20",
                line=dict(color="orange"),
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["SMA_50"],
                name="SMA 50",
                line=dict(color="blue"),
            ),
            row=1,
            col=1,
        )

        # Volume bar chart
        fig.add_trace(
            go.Bar(x=data.index, y=data["Volume"], name="Volume"), row=2, col=1
        )

        fig.update_layout(height=800, xaxis_rangeslider_visible=False, showlegend=True)

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

        fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], name="RSI"))

        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red")
        fig.add_hline(y=30, line_dash="dash", line_color="green")

        fig.update_layout(
            title="Relative Strength Index (RSI)", yaxis_title="RSI", height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    def _plot_macd(self, data: pd.DataFrame):
        """Plot MACD indicator"""
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

        fig.add_trace(
            go.Scatter(x=data.index, y=data["MACD_12_26_9"], name="MACD"),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(x=data.index, y=data["MACDs_12_26_9"], name="Signal"),
            row=1,
            col=1,
        )

        # MACD Histogram
        fig.add_trace(
            go.Bar(x=data.index, y=data["MACDh_12_26_9"], name="MACD Histogram"),
            row=2,
            col=1,
        )

        fig.update_layout(
            title="Moving Average Convergence Divergence (MACD)", height=600
        )

        st.plotly_chart(fig, use_container_width=True)

    def _plot_bollinger_bands(self, data: pd.DataFrame):
        """Plot Bollinger Bands"""
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["BBU_20_2.0"],
                name="Upper Band",
                line=dict(color="gray"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["BBM_20_2.0"],
                name="Middle Band",
                line=dict(color="blue"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["BBL_20_2.0"],
                name="Lower Band",
                line=dict(color="gray"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                name="Close Price",
                line=dict(color="black"),
            )
        )

        fig.update_layout(title="Bollinger Bands", height=400)

        st.plotly_chart(fig, use_container_width=True)

    def _display_insights(self, insights: Dict[str, Any]):
        """Display analysis insights"""
        st.subheader("Analysis Insights")

        # Create columns for different metrics
        col1, col2 = st.columns(2)

        with col1:
            st.write("Price Statistics")
            stats = insights.get("statistics", {})
            if stats:
                st.metric(
                    "Current Price",
                    f"${stats['current_price']:.2f}",
                    f"{stats['price_change']['1d']:.2f}%",
                )

    def send_email_report(self, email: str, symbol: str, period: str) -> bool:
        """Send email report with PDF attachment"""
        try:
            data = self.fetch_stock_data(symbol, period)
            insights = self.fetch_analysis(symbol, period)
            if data is not None and insights is not None:
                html_content = self.email_service.create_market_summary(
                    {"symbol": symbol, "data": data}, insights
                )
                pdf_path = f"reports/{symbol}_{datetime.now().strftime('%Y%m%d')}.pdf"
                self.email_service.generate_pdf_report(html_content, pdf_path)
                success = self.email_service.send_report(
                    recipient_email=email,
                    subject=f"Market Analysis Report - {symbol}",
                    html_content=html_content,
                    attachments=[pdf_path],
                )
                return success
            else:
                return False
        except Exception as e:
            st.error(f"Error sending email report: {str(e)}")
            return False


# Run the dashboard
if __name__ == "__main__":
    app = FinancialDashboardApp()
    app.render_sidebar()
    app.render_main_content()
