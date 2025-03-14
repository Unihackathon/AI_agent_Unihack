# AI Financial Analyst

## Overview
The AI Financial Analyst project is designed to assist financial analysts by leveraging artificial intelligence to analyze financial data. This application gathers, processes, and analyzes financial information to provide insights and predictions that can aid in decision-making. The project uses `yfinance` for data collection, `Streamlit` for the frontend, and `FastAPI` for the backend.

## API Documentation
The backend exposes multiple endpoints for financial data analysis. You can access the API documentation here:  

- **Swagger UI:** [/docs](/docs)  
- **ReDoc:** [/redoc](/redoc)  

Replace `localhost:8000` with your deployment URL if running on a server.

## Project Structure
```
ai-financial-analyst
├── reports/
├── app.py               # Streamlit application for the frontend
├── conversation.py      # Handles natural language queries and conversation history
├── data_analysis.py     # Analyzes financial data and generates insights
├── data_collection.py   # Collects financial data from various sources
├── email_demo.py        # Demonstration script for sending email reports
├── email_service.py     # Service for generating and sending email reports
├── main.py              # FastAPI application for the backend
├── readme.md            # Project documentation
├── requirements.txt     # Project dependencies
├── visualization.py     # Visualization functions for financial data
├── .env                 # Environment variables
└── .gitignore           # Files and directories to ignore in Git
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd ai-financial-analyst
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv myvenv
   source myvenv/bin/activate  # On Windows use `myvenv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a .env file in the root directory and add the following variables:
   ```
   EMAIL_SENDER=<your-email>
   EMAIL_PASSWORD=<your-email-password>
   GEMINI_API_KEY=<your-gemini-api-key>
   BASE_URL=<your-api-base-url>
   ```

## Usage
### Running the FastAPI Application 
To run the FastAPI application, execute the following command:
```sh
uvicorn main:app --reload
```
This will start the backend API server for handling data analysis and queries.
### Running the Streamlit Application
To run the Streamlit application, execute the following command:
```sh
streamlit run app.py
```
This will start the frontend application where you can interact with the financial data analysis dashboard.

#### U.S. Stock Market:
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

### Sending Email Reports
To send an email report, use the following command:
```sh
python email_demo.py
```

## Features
- **Data Collection**: Collects financial data from `yfinance` and other sources.
- **Data Analysis**: Analyzes financial data to generate insights, including technical indicators and risk metrics.
- **Visualization**: Visualizes financial data using `Plotly` and `Streamlit`.
- **Email Reports**: Generates and sends email reports with financial analysis.
- **Natural Language Queries**: Processes natural language queries to provide financial insights.

## Example
The application will load financial data, process it, and provide insights based on the AI model. You can modify the data sources and configurations in main.py to suit your needs.

## Testing
To run the unit tests, use the following command:
```sh
python -m unittest discover
```

## Contribution
Contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [Adane Moges](adanemoges6@gmail.com)- for the development and maintenance of this project.
- Any libraries or resources used in the project.
