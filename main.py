import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

class TextRequest(BaseModel):
    text: str

def ai_summarize(text: str) -> str:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error from HuggingFace API: {response.status_code} - {response.text}"

    result = response.json()
    return result[0]["summary_text"]

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/summarize")
def summarize(req: TextRequest):
    summary = ai_summarize(req.text)
    return {"summary": summary}
