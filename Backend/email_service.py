from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from typing import Dict, Any, List, Optional
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from jinja2 import Template
import os
from dotenv import load_dotenv
import pdfkit
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np


class EmailReportService:
    def __init__(self):
        load_dotenv()
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")

        # Ensure reports directory exists
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)

        # Initialize scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self._setup_templates()
        self._setup_alert_conditions()

    def _setup_templates(self):
        """Setup email templates using Jinja2"""
        self.summary_template = Template(
            """
            <html>
            <head>
                <style>
                    body { 
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .header {
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }
                    .metric {
                        margin: 15px 0;
                        padding: 15px;
                        background: #fff;
                        border: 1px solid #dee2e6;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    }
                    .alert {
                        color: #721c24;
                        background: #f8d7da;
                        border: 1px solid #f5c6cb;
                        font-weight: bold;
                    }
                    .chart {
                        margin: 20px 0;
                        padding: 10px;
                        border: 1px solid #dee2e6;
                        border-radius: 5px;
                    }
                    .positive { color: #28a745; }
                    .negative { color: #dc3545; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>Market Analysis Report - {{ symbol }}</h2>
                    <p>Generated on {{ date }}</p>
                </div>

                <div class="metric">
                    <h4>Current Statistics</h4>
                    <p>Current Price: ${{ stats.current_price | round(2) }}</p>
                    <p>Daily Change: 
                        <span class="{{ 'positive' if stats.price_change['1d'] > 0 else 'negative' }}">
                            {{ (stats.price_change['1d'] * 100) | round(2) }}%
                        </span>
                    </p>
                    <p>Volatility: {{ (stats.volatility * 100) | round(2) }}%</p>
                </div>

                {% if price_chart %}
                <div class="chart">
                    <h4>Price Chart</h4>
                    {{ price_chart | safe }}
                </div>
                {% endif %}

                {% if rsi_chart %}
                <div class="chart">
                    <h4>RSI Chart</h4>
                    {{ rsi_chart | safe }}
                </div>
                {% endif %}

                {% if macd_chart %}
                <div class="chart">
                    <h4>MACD Chart</h4>
                    {{ macd_chart | safe }}
                </div>
                {% endif %}

                {% if bb_chart %}
                <div class="chart">
                    <h4>Bollinger Bands</h4>
                    {{ bb_chart | safe }}
                </div>
                {% endif %}

                <div class="metric">
                    <h4>Technical Signals</h4>
                    <ul>
                    {% for signal in signals %}
                        <li>{{ signal }}</li>
                    {% endfor %}
                    </ul>
                </div>

                <div class="metric">
                    <h4>Risk Metrics</h4>
                    <p>Value at Risk (95%): {{ (risk.var_95 * 100) | round(2) }}%</p>
                    <p>Maximum Drawdown: {{ (risk.max_drawdown * 100) | round(2) }}%</p>
                    <p>Sharpe Ratio: {{ risk.sharpe_ratio | round(2) }}</p>
                </div>

                {% if alerts %}
                <div class="metric alert">
                    <h4>⚠️ Important Alerts</h4>
                    <ul>
                    {% for alert in alerts %}
                        <li>{{ alert }}</li>
                    {% endfor %}
                    </ul>
                </div>
                {% endif %}
            </body>
            </html>
        """
        )

    def _setup_alert_conditions(self):
        """Setup alert conditions with more sophisticated triggers"""
        self.alert_conditions = {
            "price_change": {
                "check": lambda x: abs(x) > 0.05,
                "message": lambda x: f"Significant price movement: {x:.2%}",
            },
            "volume_spike": {
                "check": lambda x: x > 2,
                "message": lambda x: f"Unusual volume: {x:.1f}x above average",
            },
            "volatility": {
                "check": lambda x: x > 0.02,
                "message": lambda x: f"High volatility: {(x * 100):.1f}% daily range",
            },
            "rsi_overbought": {
                "check": lambda x: x > 70,
                "message": lambda x: f"Overbought conditions (RSI: {x:.1f})",
            },
            "rsi_oversold": {
                "check": lambda x: x < 30,
                "message": lambda x: f"Oversold conditions (RSI: {x:.1f})",
            },
            "ma_crossover": {
                "check": lambda x: abs(x["SMA_20"] - x["SMA_50"]) < 0.01,
                "message": lambda x: "Moving average crossover detected",
            },
        }

    def create_market_summary(
        self, data: Dict[str, Any], insights: Dict[str, Any]
    ) -> str:
        """Create HTML market summary with enhanced charts"""
        try:
            df = pd.DataFrame(data.get("data", []))

            # Generate price chart
            fig_price = go.Figure()

            # Add candlestick chart
            fig_price.add_trace(
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
            for ma in ["SMA_20", "SMA_50"]:
                if ma in df.columns:
                    fig_price.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df[ma],
                            name=ma,
                            line=dict(
                                color="orange" if ma == "SMA_20" else "blue", width=1
                            ),
                        )
                    )

            # Update layout
            fig_price.update_layout(
                title=f"{data['symbol']} Price Chart",
                yaxis_title="Price",
                template="plotly_white",
                height=500,
                xaxis_rangeslider_visible=False,
                showlegend=True,
            )

            # Convert price chart to HTML
            price_chart_html = pio.to_html(fig_price, full_html=False)

            # Generate RSI chart
            fig_rsi = go.Figure()
            if "RSI" in df.columns:
                fig_rsi.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df["RSI"],
                        name="RSI",
                        line=dict(color="purple", width=1),
                    )
                )
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
                fig_rsi.update_layout(
                    title="Relative Strength Index (RSI)",
                    yaxis_title="RSI",
                    template="plotly_white",
                    height=400,
                )

            # Convert RSI chart to HTML
            rsi_chart_html = pio.to_html(fig_rsi, full_html=False)

            # Generate MACD chart
            fig_macd = make_subplots(rows=2, cols=1, shared_xaxes=True)
            if all(col in df.columns for col in ["MACD_12_26_9", "MACDs_12_26_9", "MACDh_12_26_9"]):
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
                        line=dict(color="red", width=1),
                    ),
                    row=1,
                    col=1,
                )
                fig_macd.add_trace(
                    go.Bar(
                        x=df.index,
                        y=df["MACDh_12_26_9"],
                        name="MACD Histogram",
                        marker_color="green",
                    ),
                    row=2,
                    col=1,
                )
                fig_macd.update_layout(
                    title="Moving Average Convergence Divergence (MACD)",
                    template="plotly_white",
                    height=600,
                )

            # Convert MACD chart to HTML
            macd_chart_html = pio.to_html(fig_macd, full_html=False)

            # Generate Bollinger Bands chart
            fig_bb = go.Figure()
            if all(col in df.columns for col in ["BBU_20_2.0", "BBM_20_2.0", "BBL_20_2.0"]):
                fig_bb.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df["BBU_20_2.0"],
                        name="Upper Band",
                        line=dict(color="gray"),
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
                        line=dict(color="gray"),
                    )
                )
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
                    template="plotly_white",
                    height=400,
                )

            # Convert Bollinger Bands chart to HTML
            bb_chart_html = pio.to_html(fig_bb, full_html=False)

            # Check for alerts
            alerts = self._check_alerts(df, insights)

            # Render template
            html_content = self.summary_template.render(
                symbol=data["symbol"],
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                stats=insights["statistics"],
                signals=insights["signals"],
                risk=insights["risk_metrics"],
                alerts=alerts,
                price_chart=price_chart_html,
                rsi_chart=rsi_chart_html,
                macd_chart=macd_chart_html,
                bb_chart=bb_chart_html,
            )

            return html_content

        except Exception as e:
            print(f"Error creating market summary: {str(e)}")
            return self._create_error_template(str(e))

    def _create_error_template(self, error_message: str) -> str:
        """Create an error report template"""
        return f"""
            <html>
            <body>
                <h2 style="color: red;">Error Generating Report</h2>
                <p>An error occurred while generating the report:</p>
                <pre>{error_message}</pre>
            </body>
            </html>
        """

    def _check_alerts(self, df: pd.DataFrame, insights: Dict[str, Any]) -> List[str]:
        """Check for alert conditions"""
        alerts = []

        # Price change alert
        daily_return = df["Close"].pct_change().iloc[-1]
        if self.alert_conditions["price_change"]["check"](daily_return):
            alerts.append(
                self.alert_conditions["price_change"]["message"](daily_return)
            )

        # Volume alert
        volume_ratio = df["Volume"].iloc[-1] / df["Volume"].mean()
        if self.alert_conditions["volume_spike"]["check"](volume_ratio):
            alerts.append(
                self.alert_conditions["volume_spike"]["message"](volume_ratio)
            )

        # RSI alerts
        if "RSI" in df.columns:
            rsi = df["RSI"].iloc[-1]
            if self.alert_conditions["rsi_overbought"]["check"](rsi):
                alerts.append(self.alert_conditions["rsi_overbought"]["message"](rsi))
            elif self.alert_conditions["rsi_oversold"]["check"](rsi):
                alerts.append(self.alert_conditions["rsi_oversold"]["message"](rsi))

        return alerts

    def generate_pdf_report(self, html_content: str, output_path: str) -> str:
        """Generate PDF report from HTML content"""
        try:
            pdfkit.from_string(html_content, output_path)
            return output_path
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None

    def schedule_report(
        self, email: str, symbol: str, frequency: str = "daily", time: str = "16:30"
    ):
        """Schedule periodic reports"""
        if frequency == "daily":
            self.scheduler.add_job(
                self.send_scheduled_report,
                "cron",
                hour=time.split(":")[0],
                minute=time.split(":")[1],
                args=[email, symbol],
            )
        elif frequency == "weekly":
            self.scheduler.add_job(
                self.send_scheduled_report,
                "cron",
                day_of_week="mon-fri",
                hour=time.split(":")[0],
                minute=time.split(":")[1],
                args=[email, symbol],
            )

    async def send_scheduled_report(self, email: str, symbol: str):
        """Send scheduled report"""
        from main import collector, analyzer  # Import here to avoid circular import

        try:
            data = collector.get_stock_data(symbol, period="1d")
            insights = analyzer.generate_insights(symbol, period="1d")

            html_content = self.create_market_summary(
                {"symbol": symbol, "data": data}, insights
            )

            # Generate PDF
            pdf_path = f"reports/{symbol}_{datetime.now().strftime('%Y%m%d')}.pdf"
            self.generate_pdf_report(html_content, pdf_path)

            # Send email with PDF attachment
            self.send_report(
                recipient_email=email,
                subject=f"Scheduled Report - {symbol}",
                html_content=html_content,
                attachments=[pdf_path],
            )

        except Exception as e:
            print(f"Error sending scheduled report: {str(e)}")

    def send_report(
        self,
        recipient_email: str,
        subject: str,
        html_content: str,
        attachments: List[str] = None,
    ) -> bool:
        """Send email report with optional attachments"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email

            # Attach HTML content
            msg.attach(MIMEText(html_content, "html"))

            # Attach files
            if attachments:
                for file_path in attachments:
                    with open(file_path, "rb") as f:
                        part = MIMEApplication(
                            f.read(), Name=os.path.basename(file_path)
                        )
                        part["Content-Disposition"] = (
                            f'attachment; filename="{os.path.basename(file_path)}"'
                        )
                        msg.attach(part)
            # Connect to SMTP server
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False


if __name__ == "__main__":
    email_service = EmailReportService()
    email_service.send_report(
        recipient_email="adman19940805@gmail.com",
        subject="Test Email last",
        html_content="<h3>This is a test email</h3>",
    )
