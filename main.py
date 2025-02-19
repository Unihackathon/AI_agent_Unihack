import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
import numpy as np

from data_collection import FinancialDataCollector
from data_analysis import FinancialAnalyzer
from conversation import FinancialChatbot

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


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Financial Data Analysis API",
        "version": "1.0.0",
        "status": "active",
    }


@app.post("/api/stock/data", response_model=Dict[str, Any])
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


@app.post("/api/stock/analysis")
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


@app.post("/api/crypto/data", response_model=Dict[str, Any])
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


@app.post("/api/query", response_model=Dict[str, Any])
async def process_query(request: QueryRequest):
    """Process a natural language query about financial data"""
    try:
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
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/api/conversation/history", response_model=Dict[str, Any])
async def get_conversation_history():
    """Get conversation history"""
    try:
        history = chatbot.get_conversation_history()
        return {"timestamp": datetime.now(), "history": [str(msg) for msg in history]}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching conversation history: {str(e)}"
        )


# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
