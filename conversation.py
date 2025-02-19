import os
from typing import Dict, Any, List
from datetime import datetime

# from langchain.llms import GoogleGenerativeAI
# from langchain_community.llms import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
# from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

from data_collection import FinancialDataCollector
from data_analysis import FinancialAnalyzer

load_dotenv()


class FinancialChatbot:
    def __init__(self):
        self.collector = FinancialDataCollector()
        self.analyzer = FinancialAnalyzer()
        self.llm = GoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7,
        )
        self.chat_history = ChatMessageHistory()
        self._setup_chains()

    def _setup_chains(self):
        """Setup LangChain prompts and chains"""
        # Template for analyzing financial data
        self.analysis_prompt = PromptTemplate.from_template(
            """
        You are a financial analyst assistant. Based on the following financial data and analysis:
        
        Data: {financial_data}
        Analysis: {analysis_results}
        
        Please provide a clear and concise response to the user's question: {user_question}
        
        Previous conversation context:
        {chat_history}
        
        Response:
        """
        )

        # Create the chain using the new syntax
        self.analysis_chain = (
            {
                "financial_data": lambda x: x["financial_data"],
                "analysis_results": lambda x: x["analysis_results"],
                "user_question": lambda x: x["user_question"],
                "chat_history": lambda x: "\n".join(
                    [f"{m.type}: {m.content}" for m in self.chat_history.messages]
                ),
            }
            | self.analysis_prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_data(self, data: Dict[str, Any]) -> str:
        """Format financial data for the prompt"""
        if not data:
            return "No data available"

        formatted = []
        if "statistics" in data:
            stats = data["statistics"]
            formatted.append("Statistics:")
            formatted.append(f"- Current Price: ${stats.get('current_price', 'N/A')}")
            formatted.append(
                f"- Daily Returns: Mean={stats.get('daily_returns', {}).get('mean', 'N/A'):.4f}"
            )
            formatted.append(f"- Volatility: {stats.get('volatility', 'N/A'):.4f}")

        if "signals" in data:
            formatted.append("\nTrading Signals:")
            for signal in data["signals"]:
                formatted.append(f"- {signal}")

        if "trend_analysis" in data:
            trend = data["trend_analysis"]
            formatted.append("\nTrend Analysis:")
            formatted.append(f"- Short-term: {trend.get('short_term', 'N/A')}")
            formatted.append(f"- Medium-term: {trend.get('medium_term', 'N/A')}")
            formatted.append(f"- Strength: {trend.get('strength', 'N/A')}")

        return "\n".join(formatted)

    def _format_analysis(self, insights: Dict[str, Any]) -> str:
        """Format analysis results for the prompt"""
        if not insights:
            return "No analysis available"

        formatted = []

        if "risk_metrics" in insights:
            risk = insights["risk_metrics"]
            formatted.append("Risk Analysis:")
            formatted.append(f"- Value at Risk (95%): {risk.get('var_95', 'N/A'):.4f}")
            formatted.append(
                f"- Maximum Drawdown: {risk.get('max_drawdown', 'N/A'):.4f}"
            )
            formatted.append(f"- Sharpe Ratio: {risk.get('sharpe_ratio', 'N/A'):.4f}")

        if "key_levels" in insights:
            levels = insights["key_levels"]
            formatted.append("\nKey Price Levels:")
            formatted.append(f"- Support: ${levels['support'][0]:.2f}")
            formatted.append(f"- Resistance: ${levels['resistance'][0]:.2f}")

        return "\n".join(formatted)

    def process_query(
        self, query: str, symbol: str = "TSLA", period: str = "6mo"
    ) -> str:
        """
        Process a natural language query about financial data

        Args:
            query: User's question
            symbol: Stock symbol to analyze
            period: Time period for analysis

        Returns:
            Response to the user's question
        """
        try:
            insights = self.analyzer.generate_insights(symbol, period)
            financial_data = self._format_data(insights)
            analysis_results = self._format_analysis(insights)

            # Add user message to history
            self.chat_history.add_user_message(query)

            response = self.analysis_chain.invoke(
                {
                    "financial_data": financial_data,
                    "analysis_results": analysis_results,
                    "user_question": query,
                }
            )

            # Add AI response to history
            self.chat_history.add_ai_message(response)

            return response

        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return "I apologize, but I encountered an error processing your query. Please try again."

    def get_conversation_history(self) -> List[str]:
        """Get the conversation history"""
        return self.chat_history.messages


# Example usage
if __name__ == "__main__":
    chatbot = FinancialChatbot()

    # Test some example queries
    test_queries = [
        "What is the current trend for Tesla stock?",
        "which stock has the highest volatility?",
        "what is the average daily return for Tesla stock?",
        "what is the maximum drawdown for Tesla stock?",
        "what is the value at risk for Tesla stock?",
        "what is the sharpe ratio for Tesla stock?",
        "what is the beta for Tesla stock?",
        "what is the correlation between Tesla and Apple stock?",
        "what is the correlation between Tesla and Amazon stock?",
    ]

    for query in test_queries:
        print(f"\nQ: {query}")
        response = chatbot.process_query(query)
        print(f"A: {response}")
