from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI(title="PHISHORA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "PHISHORA Backend is Running"}


@app.post("/scan")
def scan(data: dict):

    text = data.get("text", "")

    prompt = f"""
You are PHISHORA AI, a cybersecurity assistant.

Analyze the following website information.

Check for:

- Phishing
- Fake login pages
- Credential harvesting
- Suspicious forms
- Suspicious links
- Social engineering
- URL tricks
- Fake domains
- Hidden login forms
- Overall website safety

Website Information:

{text}

Return ONLY valid JSON in this format:

{{
"type":"",
"risk_score":0,
"confidence":0,
"summary":""
}}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    ai = response.json()

    content = ai["choices"][0]["message"]["content"]

    return {"result": content}