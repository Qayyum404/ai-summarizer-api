from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

def fake_ai_summarize(text: str) -> str:
    words = text.split()
    return " ".join(words[:15]) + "..." if len(words) > 15 else text

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/summarize")
def summarize(req: TextRequest):
    summary = fake_ai_summarize(req.text)
    return {"summary": summary}
