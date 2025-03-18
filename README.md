# AI Financial Analyst Agent 🤖📈

An intelligent AI agent for stock market analysis and insights, powered by machine learning and natural language processing.

## 🌟 Features

- **Real-time Stock Analysis**: Get instant analysis of stock performance using advanced technical indicators
- **AI-Powered Insights**: Natural language processing for answering questions about stocks
- **Interactive Dashboard**: Visual representation of stock data and analysis
- **Automated Reports**: Scheduled email reports with detailed market analysis
- **Technical Indicators**: 
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Moving Averages (20-day and 50-day)
  - Volume Analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- pip package manager
- Virtual environment (recommended)

### Installation

#### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-financial-analyst
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
cd Backend
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the Backend directory with:
```bash
EMAIL_SENDER=<your-email>
EMAIL_PASSWORD=<your-email-password>
GEMINI_API_KEY=<your-gemini-api-key>
GROK_API_KEY=<your-grok-api-key>
BASE_URL=<your-api-base-url>
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd Frontend
```

2. Install frontend dependencies:
```bash
npm install
# or
yarn install
```

3. Create `.env` file in the Frontend directory:
```bash
REACT_APP_API_URL=http://localhost:8000
```

## 🏗️ Project Structure

```
ai-financial-analyst/
├── Backend/
│   ├── app.py               # Streamlit dashboard application
│   ├── conversation.py      # AI chatbot for natural language queries
│   ├── data_analysis.py     # Financial analysis and indicators
│   ├── data_collection.py   # Stock data collection using yfinance
│   ├── email_service.py     # Automated email reporting
│   ├── main.py             # FastAPI backend server
│   └── visualization.py     # Data visualization components
├── Frontend/
│   ├── public/             # Static files
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── styles/        # CSS/SCSS files
│   │   └── utils/         # Utility functions
│   ├── package.json
│   └── README.md
├── reports/                # Generated analysis reports
├── requirements.txt        # Backend dependencies
└── README.md              # Project documentation
```

## 🎯 Usage

### Starting the Backend Server

```bash
cd Backend
uvicorn main:app --reload
```

### Starting the Frontend Development Server

```bash
cd Frontend
npm start
# or
yarn start
```

### Running the Streamlit Dashboard

```bash
cd Backend
streamlit run app.py
```

## 💻 Frontend Features

### Dashboard
- Real-time stock price charts
- Technical analysis indicators
- Market sentiment analysis
- Portfolio tracking
- Watchlist management

### Interactive Components
- Stock search with autocomplete
- Date range selectors
- Custom indicator settings
- Report generation interface
- AI chat interface

### Visualization Tools
- Candlestick charts
- Line charts
- Volume analysis
- Technical indicators
- Comparison charts

## 📊 Available Analysis

### Technical Analysis
- Price trends and patterns
- Volume analysis
- Moving averages
- RSI indicators
- MACD signals
- Bollinger Bands

### Risk Metrics
- Volatility analysis
- Value at Risk (VaR)
- Maximum drawdown
- Sharpe ratio

### AI-Powered Features
- Natural language queries about stocks
- Automated market insights
- Trend predictions
- Risk assessment

## 📧 Email Reports

The system can send automated reports containing:
- Market summaries
- Technical analysis
- Risk metrics
- Custom alerts
- Price charts and indicators

### Scheduling Reports

```python
# Example: Schedule daily report
email_service.schedule_report(
    email="user@example.com",
    symbol="AAPL",
    frequency="daily",
    time="16:30"
)
```

## 🔍 Supported Markets

### U.S. Stocks
- Technology (AAPL, MSFT, GOOGL, etc.)
- Finance (JPM, BAC, WFC)
- Healthcare (JNJ, PFE, MRNA)
- And more...

### Indices
- S&P 500 (^GSPC)
- Dow Jones (^DJI)
- Nasdaq (^IXIC)

### Cryptocurrencies
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)

## 🛠️ API Documentation

Access the API documentation at:
- Swagger UI: [`/docs`](https://data-analist-agent.onrender.com/docs)
- ReDoc: [`/redoc`](https://data-analist-agent.onrender.com/redoc)

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [Streamlit](https://streamlit.io/) for the dashboard interface
- [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- [React](https://reactjs.org/) for the frontend interface
- [Plotly](https://plotly.com/) for interactive charts
- [pandas-ta](https://github.com/twopirllc/pandas-ta) for technical analysis
- [n8n](https://n8n.io/) for workflow automation

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Always conduct your own research and consult with financial advisors before making investment decisions.
