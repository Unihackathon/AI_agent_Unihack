import yfinance as yf
import pandas as pd
from datetime import datetime
from email_service import EmailReportService
import streamlit as st

def get_demo_data(symbol: str = "AAPL", period: str = "1mo"):
    """Get sample stock data for demo"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return {
            "symbol": symbol,
            "data": data
        }
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def get_demo_insights(symbol: str):
    """Generate sample insights for demo"""
    return {
        "statistics": {
            "current_price": 175.50,
            "price_change": {"1d": 0.025},
            "volatility": 0.15
        },
        "signals": [
            "Strong buy signal based on RSI",
            "Price above 50-day moving average",
            "Volume showing bullish trend"
        ],
        "risk_metrics": {
            "var_95": 0.02,
            "max_drawdown": 0.05,
            "sharpe_ratio": 1.8
        }
    }

def run_demo():
    st.title("Email Report Service Demo")
    
    # Initialize email service
    email_service = EmailReportService()
    
    # User inputs
    recipient_email = st.text_input("Add your email")
    symbol = st.text_input("Enter stock symbol", value="AAPL")
    
    if st.button("Send Test Report"):
        if recipient_email:
            try:
                # Get demo data
                data = get_demo_data(symbol)
                if data:
                    # Get demo insights
                    insights = get_demo_insights(symbol)
                    
                    # Create HTML content
                    html_content = email_service.create_market_summary(data, insights)
                    
                    # Generate PDF
                    pdf_path = f"reports/{symbol}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    email_service.generate_pdf_report(html_content, pdf_path)
                    
                    # Send email
                    subject = f"Stock Analysis Report - {symbol}"
                    success = email_service.send_report(
                        recipient_email=recipient_email,
                        subject=subject,
                        html_content=html_content,
                        attachments=[pdf_path]
                    )
                    
                    if success:
                        st.success("Test report sent successfully! Check your email.")
                    else:
                        st.error("Failed to send test report.")
                else:
                    st.error("Failed to fetch stock data.")
            except Exception as e:
                st.error(f"Error running demo: {str(e)}")
        else:
            st.warning("Please enter an email address.")
    
    # Schedule report section
    st.subheader("Schedule Regular Reports")
    schedule_email = st.text_input("Enter email for scheduled reports")
    schedule_symbol = st.text_input("Enter symbol for scheduled reports", value="AAPL")
    frequency = st.selectbox("Select frequency", ["daily", "weekly"])
    time = st.time_input("Select time for report", value=datetime.strptime("16:30", "%H:%M"))
    
    if st.button("Schedule Report"):
        if schedule_email:
            try:
                email_service.schedule_report(
                    email=schedule_email,
                    symbol=schedule_symbol,
                    frequency=frequency,
                    time=time.strftime("%H:%M")
                )
                st.success(f"Successfully scheduled {frequency} report for {schedule_symbol}")
            except Exception as e:
                st.error(f"Error scheduling report: {str(e)}")
        else:
            st.warning("Please enter an email address for scheduled reports.")

if __name__ == "__main__":
    run_demo() 