import os
import time
import hashlib
import requests
from dotenv import load_dotenv
import redis
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

class TextRequest(BaseModel):
    text: str

def call_huggingface(text: str):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}

    for attempt in range(2):
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result[0]["summary_text"], True
            elif response.status_code in (503, 504):
                time.sleep(5)
                continue
            else:
                return f"Error from HuggingFace API: {response.status_code}", False
        except requests.exceptions.Timeout:
            time.sleep(5)
            continue

    return "Error: HuggingFace API did not respond after multiple attempts.", False

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/summarize")
def summarize(req: TextRequest):
    key = hashlib.sha256(req.text.encode()).hexdigest()
    cached = cache.get(key)
    if cached:
        return {"summary": cached, "cached": True}

    summary, success = call_huggingface(req.text)

    if success:
        cache.set(key, summary, ex=3600)

    return {"summary": summary, "cached": False}

@app.get("/crash")
def crash():
    os._exit(1)
