import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
import numpy as np
import math

from fastapi.responses import HTMLResponse
from data_collection import FinancialDataCollector
from data_analysis import FinancialAnalyzer
from conversation import FinancialChatbot
from email_service import EmailReportService

# Initialize FastAPI app
app = FastAPI(
    title="Financial Data Analysis API",
    description="API for analyzing financial data and providing insights",
    version="1.0.0",
)

# Initialize components
collector = FinancialDataCollector()
analyzer = FinancialAnalyzer()
chatbot = FinancialChatbot()

# Initialize email service
email_service = EmailReportService()


# Pydantic models for request/response
class StockRequest(BaseModel):
    symbol: str
    period: str = "6mo"
    interval: str = "1d"


class QueryRequest(BaseModel):
    query: str
    symbol: str
    period: str = "6mo"


class AnalysisResponse(BaseModel):
    timestamp: datetime
    symbol: str
    data: Dict[str, Any]
    insights: Dict[str, Any]


class EmailReportRequest(BaseModel):
    email: str
    symbol: str
    period: str = "1d"
    report_type: str = "summary"  # summary, detailed, custom


class ScheduleReportRequest(BaseModel):
    email: str
    symbol: str
    frequency: str = "daily"  # daily, weekly
    time: str = "16:30"  # HH:MM format


app = FastAPI()


def sanitize_data(data):
    """Recursively replaces NaN, inf, -inf with valid values."""
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(v) for v in data]
    elif isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
        return None  # or use 0, "Infinity", etc.
    return data


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve a well-styled API documentation landing page"""

    with open("index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)


@app.post(
    "/api/stock/data",
    response_model=Dict[str, Any],
    summary="Get stock data",
    description="Retrieves historical stock data for a given symbol.",
)
async def get_stock_data(request: StockRequest):
    """Get stock data for a given symbol"""
    try:
        data = collector.get_stock_data(
            symbol=request.symbol, period=request.period, interval=request.interval
        )

        if data is None:
            raise HTTPException(
                status_code=404, detail=f"No data found for symbol {request.symbol}"
            )

        # Convert DataFrame to dict and handle NaN values
        data_dict = data.copy()
        data_dict.index = data_dict.index.strftime("%Y-%m-%d %H:%M:%S")
        # Replace NaN with None for JSON serialization
        data_dict = data_dict.where(data_dict.notna(), None)
        data_dict = data_dict.reset_index().to_dict(orient="records")

        return {
            "symbol": request.symbol,
            "timestamp": datetime.now().isoformat(),
            "data": data_dict,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching stock data: {str(e)}"
        )


@app.post(
    "/api/stock/analysis",
    summary="Get stock analysis",
    description="Provides comprehensive analysis for a given stock.",
)
async def get_stock_analysis(request: StockRequest):
    """Get comprehensive analysis for a stock"""
    try:
        # Get data and generate insights
        data = collector.get_stock_data(symbol=request.symbol, period=request.period)

        if data is None:
            raise HTTPException(
                status_code=404, detail=f"No data found for symbol {request.symbol}"
            )

        insights = analyzer.generate_insights(request.symbol, request.period)

        # Convert DataFrame to dict and handle NaN values
        data_dict = data.copy()
        data_dict.index = data_dict.index.strftime("%Y-%m-%d %H:%M:%S")
        # Replace NaN with None for JSON serialization
        data_dict = data_dict.where(data_dict.notna(), None)
        data_dict = data_dict.reset_index().to_dict(orient="records")

        # Convert numpy types to Python native types and handle NaN values
        def convert_to_native_types(obj):
            if isinstance(obj, dict):
                return {k: convert_to_native_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native_types(item) for item in obj]
            elif isinstance(obj, (np.floating, float)) and (
                np.isnan(obj) or np.isinf(obj)
            ):
                return None
            elif isinstance(obj, (np.floating, float)):
                return float(obj)
            elif isinstance(obj, (np.integer, int)):
                return int(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            return obj

        # Convert numpy types and handle NaN values in both data and insights
        data_dict = [convert_to_native_types(record) for record in data_dict]
        insights = convert_to_native_types(insights)
        data_dict = sanitize_data(data_dict)
        insights = sanitize_data(insights)
        response_data = {
            "timestamp": datetime.now().isoformat(),
            "symbol": request.symbol,
            "data": data_dict,
            "insights": insights,
        }

        return response_data

    except Exception as e:
        import traceback

        print(f"Error in get_stock_analysis: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Error generating analysis: {str(e)}"
        )


@app.post(
    "/api/crypto/data",
    response_model=Dict[str, Any],
    summary="Get cryptocurrency data",
    description="Retrieves cryptocurrency data for a given symbol.",
)
async def get_crypto_data(symbol: str = "btcusd"):
    """Get cryptocurrency data"""
    try:
        data = collector.get_crypto_data(symbol)

        if data is None:
            raise HTTPException(
                status_code=404, detail=f"No data found for crypto symbol {symbol}"
            )

        return {"symbol": symbol, "timestamp": datetime.now(), "data": data}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching crypto data: {str(e)}"
        )


@app.post(
    "/api/query",
    response_model=Dict[str, Any],
    summary="Process natural language query",
    description="Processes a natural language query about financial data.",
)
async def process_query(request: QueryRequest):
    """Process a natural language query about financial data"""
    try:
        print(
            f"Received query: {request.query}, symbol: {request.symbol}, period: {request.period}"
        )

        response = chatbot.process_query(
            query=request.query, symbol=request.symbol, period=request.period
        )
        return {
            "timestamp": datetime.now(),
            "query": request.query,
            "response": response,
            "symbol": request.symbol,
        }

    except Exception as e:
        import traceback

        error_message = f"Error processing query: {str(e)}"
        print(error_message)
        traceback.print_exc()  # Print the full traceback
        raise HTTPException(status_code=500, detail=error_message)


@app.get(
    "/api/conversation/history",
    response_model=Dict[str, Any],
    summary="Get conversation history",
    description="Retrieves the history of the conversation with the chatbot.",
)
async def get_conversation_history():
    """Get conversation history"""
    try:
        history = chatbot.get_conversation_history()
        return {"timestamp": datetime.now(), "history": [str(msg) for msg in history]}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching conversation history: {str(e)}"
        )


@app.post(
    "/api/reports/email",
    summary="Send email report",
    description="Sends an email report for a given stock.",
)
async def send_email_report(request: EmailReportRequest):
    """Send email report for a stock"""
    try:
        # Get stock data and analysis
        data = collector.get_stock_data(request.symbol, request.period)
        insights = analyzer.generate_insights(request.symbol, request.period)

        # Create report content
        html_content = email_service.create_market_summary(
            dict(data), insights
        )

        # Send email
        success = email_service.send_report(
            recipient_email=request.email,
            subject=f"Market Analysis Report - {request.symbol}",
            html_content=html_content,
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email report")

        return {"status": "success", "message": f"Report sent to {request.email}"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating report: {str(e)}"
        )


@app.post(
    "/api/reports/schedule",
    summary="Schedule email report",
    description="Schedules periodic email reports.",
)
async def schedule_email_report(request: ScheduleReportRequest):
    """Schedule periodic email reports"""
    try:
        email_service.schedule_report(
            email=request.email,
            symbol=request.symbol,
            frequency=request.frequency,
            time=request.time,
        )

        return {
            "status": "success",
            "message": f"Scheduled {request.frequency} report for {request.symbol} at {request.time}",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error scheduling report: {str(e)}"
        )


# Run the application
if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
