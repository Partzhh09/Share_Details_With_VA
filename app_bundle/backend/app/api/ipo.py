from fastapi import APIRouter
import requests
import yfinance as yf
from datetime import datetime
import json
import os

router = APIRouter()

@router.get("/chart/{symbol}")
def one_day_chart(symbol: str):
    """
    Returns last 1-day price data (5 min interval)
    """
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d", interval="5m")

        if data.empty:
            return {"error": "No data available"}

        chart_data = []
        for index, row in data.iterrows():
            chart_data.append({
                "time": index.strftime("%H:%M"),
                "price": round(row["Close"], 2)
            })

        # Persist chart data to a local JSON file
        symbol_safe = symbol.replace("/", "_").replace("\\", "_").upper()
        charts_dir = os.path.join("data", "charts")
        os.makedirs(charts_dir, exist_ok=True)
        file_path = os.path.join(charts_dir, f"{symbol_safe}_1day.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                {"symbol": symbol.upper(), "data": chart_data},
                f,
                indent=4,
            )

        return {
            "symbol": symbol.upper(),
            "data": chart_data,
            "saved_to": file_path,
        }

    except Exception as e:
        return {"error": str(e)}

@router.get("/price/{symbol}")
def live_share_price(symbol: str):
    """
    Example symbols:
    TCS.NS
    RELIANCE.NS
    INFY.NS
    """

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return {"error": "Invalid symbol or no data"}

        last_price = round(data["Close"].iloc[-1], 2)

        return {
            "symbol": symbol.upper(),
            "price": last_price,
            "currency": "INR",
            "time": datetime.now().strftime("%H:%M:%S"),
            "exchange": "NSE"
        }

    except Exception as e:
        return {"error": str(e)}

@router.get("/predict/{ipo_name}")
def predict_ipo(ipo_name: str):
    return {
        "ipo": ipo_name.title(),
        "company": f"{ipo_name.title()} Limited",
        "issue_price": "₹250",
        "listing_price_expected": "₹295",
        "prediction": "Profit",
        "expected_gain": "18%",
        "risk_level": "Medium",
        "recommendation": "Apply"
    }

@router.get("/live")
def live_ipos():
    """
    Fetch live / open IPOs (India-focused example)
    NOTE: Replace URL with real API when you get a key
    """
    try:
        url = "https://api.ipoalerts.in/ipos?status=open"
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}