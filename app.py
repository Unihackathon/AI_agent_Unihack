import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from typing import Dict, Any
from plotly.subplots import make_subplots

# Configure page settings
st.set_page_config(page_title="Financial Data Analyzer", page_icon="📈", layout="wide")

# Constants
API_BASE_URL = "http://localhost:8000"


class FinancialDashboardApp:
    def __init__(self):
        self.setup_session_state()

    def setup_session_state(self):
        """Initialize session state variables"""
        if "current_symbol" not in st.session_state:
            st.session_state.current_symbol = "TSLA"
        if "current_period" not in st.session_state:
            st.session_state.current_period = "6mo"

    def fetch_stock_data(self, symbol: str, period: str) -> Dict[str, Any]:
        """Fetch stock data from API"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/stock/data",
                json={"symbol": symbol, "period": period},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching stock data: {str(e)}")
            return None

    def fetch_analysis(self, symbol: str, period: str) -> Dict[str, Any]:
        """Fetch stock analysis from API"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/stock/analysis",
                json={"symbol": symbol, "period": period},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching analysis: {str(e)}")
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

    def render_main_content(self):
        """Render main dashboard content"""
        st.title(f"Financial Analysis Dashboard - {st.session_state.current_symbol}")

        # Fetch data and analysis
        with st.spinner("Fetching data..."):
            data = self.fetch_stock_data(
                st.session_state.current_symbol, st.session_state.current_period
            )
            analysis = self.fetch_analysis(
                st.session_state.current_symbol, st.session_state.current_period
            )

        if data and analysis:
            # Convert data to DataFrame
            df = pd.DataFrame(data["data"])
            df.index = pd.to_datetime(df.index)

            # Create tabs for different views
            tabs = st.tabs(["Overview", "Technical Analysis", "Statistics", "Insights"])

            # Overview Tab
            with tabs[0]:
                self.render_overview_tab(df, analysis)

            # Technical Analysis Tab
            with tabs[1]:
                self.render_technical_tab(df)

            # Statistics Tab
            with tabs[2]:
                self.render_statistics_tab(analysis)

            # Insights Tab
            with tabs[3]:
                self.render_insights_tab(analysis)

    def render_overview_tab(self, df: pd.DataFrame, analysis: Dict[str, Any]):
        """Render overview tab content"""
        col1, col2 = st.columns([2, 1])

        with col1:
            # Price chart with moving averages
            fig = go.Figure()

            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="OHLC",
                )
            )

            # Add moving averages
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SMA_20"],
                    name="SMA 20",
                    line=dict(color="orange", width=1),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SMA_50"],
                    name="SMA 50",
                    line=dict(color="blue", width=1),
                )
            )

            fig.update_layout(
                title=f"{st.session_state.current_symbol} Price Chart",
                yaxis_title="Price",
                xaxis_title="Date",
                height=500,
                template="plotly_white",
                xaxis_rangeslider_visible=False,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Add volume chart below price chart
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"))
            fig_volume.update_layout(
                title="Volume",
                height=200,
                template="plotly_white",
                showlegend=False,
                margin=dict(t=30, b=30),
            )
            st.plotly_chart(fig_volume, use_container_width=True)

        with col2:
            # Key metrics
            st.subheader("Key Metrics")
            stats = analysis["insights"]["statistics"]

            st.metric(
                "Current Price",
                f"${stats['current_price']:.2f}",
                f"{stats['price_change']['1d']:.2f}%",
            )

            st.metric(
                "Volume",
                f"{stats['volume_analysis']['avg_volume']:,.0f}",
                f"{stats['volume_analysis']['volume_trend']:.2f}%",
            )

            st.metric("Volatility", f"{stats['volatility']*100:.2f}%")

    def render_technical_tab(self, df: pd.DataFrame):
        """Render technical analysis tab content"""
        st.subheader("Technical Indicators")

        # Check for required columns
        required_columns = {
            "RSI": "RSI indicator",
            "MACD_12_26_9": "MACD line",
            "MACDs_12_26_9": "MACD signal",
            "MACDh_12_26_9": "MACD histogram",
            "BBU_20_2.0": "Bollinger Bands",
        }

        missing_indicators = [
            name for col, name in required_columns.items() if col not in df.columns
        ]

        if missing_indicators:
            st.warning(f"Missing indicators: {', '.join(missing_indicators)}")
            return

        # RSI Chart
        if "RSI" in df.columns:
            fig_rsi = go.Figure()
            fig_rsi.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["RSI"],
                    name="RSI",
                    line=dict(color="purple", width=1),
                )
            )
            fig_rsi.add_hline(
                y=70, line_dash="dash", line_color="red", annotation_text="Overbought"
            )
            fig_rsi.add_hline(
                y=30, line_dash="dash", line_color="green", annotation_text="Oversold"
            )
            fig_rsi.update_layout(
                title="Relative Strength Index (RSI)",
                height=300,
                template="plotly_white",
                yaxis=dict(range=[0, 100]),
                showlegend=False,
            )
            st.plotly_chart(fig_rsi, use_container_width=True)

        # MACD Chart
        if all(
            col in df.columns
            for col in ["MACD_12_26_9", "MACDs_12_26_9", "MACDh_12_26_9"]
        ):
            fig_macd = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                subplot_titles=("MACD Line & Signal", "MACD Histogram"),
                row_heights=[0.7, 0.3],
            )

            # MACD and Signal lines
            fig_macd.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["MACD_12_26_9"],
                    name="MACD",
                    line=dict(color="blue", width=1),
                ),
                row=1,
                col=1,
            )

            fig_macd.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["MACDs_12_26_9"],
                    name="Signal",
                    line=dict(color="orange", width=1),
                ),
                row=1,
                col=1,
            )

            # MACD Histogram
            colors = ["red" if x < 0 else "green" for x in df["MACDh_12_26_9"]]
            fig_macd.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["MACDh_12_26_9"],
                    name="Histogram",
                    marker_color=colors,
                ),
                row=2,
                col=1,
            )

            fig_macd.update_layout(
                title="Moving Average Convergence Divergence (MACD)",
                height=500,
                template="plotly_white",
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )
            st.plotly_chart(fig_macd, use_container_width=True)

        # Bollinger Bands
        if all(col in df.columns for col in ["BBU_20_2.0", "BBM_20_2.0", "BBL_20_2.0"]):
            fig_bb = go.Figure()

            # Add Bollinger Bands
            fig_bb.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BBU_20_2.0"],
                    name="Upper Band",
                    line=dict(color="gray", dash="dash"),
                )
            )

            fig_bb.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BBM_20_2.0"],
                    name="Middle Band",
                    line=dict(color="blue"),
                )
            )

            fig_bb.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BBL_20_2.0"],
                    name="Lower Band",
                    line=dict(color="gray", dash="dash"),
                )
            )

            # Add price
            fig_bb.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["Close"],
                    name="Close Price",
                    line=dict(color="black"),
                )
            )

            fig_bb.update_layout(
                title="Bollinger Bands",
                height=400,
                template="plotly_white",
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )
            st.plotly_chart(fig_bb, use_container_width=True)

    def render_statistics_tab(self, analysis: Dict[str, Any]):
        """Render statistics tab content"""
        st.subheader("Statistical Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Daily Returns")
            stats = analysis["insights"]["statistics"]["daily_returns"]
            st.write(f"Mean: {stats['mean']:.4f}")
            st.write(f"Std Dev: {stats['std']:.4f}")
            st.write(f"Skewness: {stats['skew']:.4f}")

        with col2:
            st.write("Risk Metrics")
            risk = analysis["insights"]["risk_metrics"]
            st.write(f"Value at Risk (95%): {risk['var_95']:.4f}")
            st.write(f"Max Drawdown: {risk['max_drawdown']:.4f}")
            st.write(f"Sharpe Ratio: {risk['sharpe_ratio']:.4f}")

    def render_insights_tab(self, analysis: Dict[str, Any]):
        """Render insights tab content"""
        st.subheader("Trading Insights")

        # Trading signals
        st.write("Trading Signals")
        for signal in analysis["insights"]["signals"]:
            st.info(signal)

        # Trend analysis
        st.write("Trend Analysis")
        trend = analysis["insights"]["trend_analysis"]
        cols = st.columns(3)
        cols[0].metric("Short-term Trend", trend["short_term"])
        cols[1].metric("Medium-term Trend", trend["medium_term"])
        cols[2].metric("Trend Strength", trend["strength"])

        # Support/Resistance levels
        st.write("Key Price Levels")
        levels = analysis["insights"]["key_levels"]
        st.write(f"Support: ${levels['support'][0]:.2f}")
        st.write(f"Resistance: ${levels['resistance'][0]:.2f}")

    def run(self):
        """Run the Streamlit application"""
        self.render_sidebar()
        self.render_main_content()


# Run the application
if __name__ == "__main__":
    app = FinancialDashboardApp()
    app.run()
    