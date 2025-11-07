from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)

extract_system_prompt = """
You are an information extraction model.

You will be given:
1) A user question
2) Today's date (reference_date) in YYYY-MM-DD format

Your task:
Extract from the user's question:
1) The stock ticker(s) or company name(s).
    - if multiple exist, return comma-seperated with NO spaces. e.g. "BTC,ETH"
2) The explicit date range mentioned in the question.
3) If the question includes a relative date (e.g. "last week", "this month"):
    -> Convert it into explicit start and end dates based on reference_date.
4) If NO date is mentioned, set:
    start = reference_date - 14days
    end = reference_date

Return ONLY JSON in this exact form:
{
    "ticker" : "string or null",
    "start" : "YYYY-MM-DD",
    "end" : "YYYY-MM-DD"
}

Rules:
- If no ticker is found, return ticker = null.
- If no date or timeframe is mentioned, start = null and end = null.
- Whhen converting dates, always use reference_date as the "today" baseline.
- Do not include additional text, comments, or explanations.
- NEVER return null for start or end.
"""

# 뉴스 분석을 위해 사용자 질문에서 ticker와 기간 추출
def extract_ticker_and_period(question : str):
    today = datetime.utcnow().strftime("%Y-%m-%d")

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        temperature=0,
        messages = [
            {
                "role" : "system",
                "content" : extract_system_prompt
            },
            {
                "role" : "user",
                "content" : f"reference_date: {today}\nquestion: {question}"
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    return json.loads(result)