from fastapi import FastAPI
from datetime import date, timedelta
import os
from dotenv import load_dotenv
import requests

load_dotenv()
key = os.getenv("CRYPTONEWS_API_KEY")
app = FastAPI()

@app.get("/")
def getRecentNews(ticker : str):
    url = "https://cryptonews-api.com/api/v1"

    start_date = date.today() - timedelta(days=7)
    end_date = date.today()

    params = {
        "tickers" : ticker,
        "items" : 10,
        "token" : key,
        "date" : format_date_range(start_date, end_date)
    }

    response = requests.get(url, params=params)

    data = response.json()

    if "data" not in data:
        print("'data' key not found. API response : ", data)
        return []
    
    news_list = [
        {
            "url" : item["news_url"],
            "image_url" : item.get("image_url"),
            "source_name" : item.get("source_name")
        }
        for item in data["data"]
    ]
    
    return news_list

def format_date_range(start :date, end : date):
    return f"{start.strftime('%m%d%Y')}-{end.strftime('%m%d%Y')}"