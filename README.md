# AI Summarizer API

A FastAPI service that summarizes text using a real AI model (HuggingFace's facebook/bart-large-cnn), built as a hands-on learning project covering containerization, caching, CI/CD, and cloud deployment fundamentals.

## What It Does

Send any block of text to the /summarize endpoint, and it returns a genuinely AI-generated summary, not a basic word-count truncation. The model reads the input, identifies the most important sentences, and returns a condensed version that preserves meaning.

## Tech Stack

- FastAPI - Python web framework for the API
- HuggingFace Inference Providers - real AI model for summarization (facebook/bart-large-cnn)
- Pydantic - request validation
- python-dotenv - environment variable management
- Coming next: Docker, Redis caching, GitHub Actions CI/CD, cloud deployment

## Running Locally

1. Clone the repo:
git clone https://github.com/Qayyum404/ai-summarizer-api.git
cd ai-summarizer-api

2. Set up a virtual environment:
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn redis pydantic python-dotenv requests

3. Create a .env file with your own HuggingFace token:
HF_TOKEN=your_huggingface_token_here

Get a free token at https://huggingface.co/settings/tokens

4. Run the server:
uvicorn main:app --reload

5. Open http://localhost:8000/docs and test the /summarize endpoint interactively.

## Roadmap

- [x] Core FastAPI summarization endpoint
- [x] Real AI integration via HuggingFace Inference Providers
- [ ] Dockerize the app
- [ ] Add Redis caching to avoid redundant AI calls on repeated text
- [ ] Add a self-healing demo (deliberate crash + automatic Docker restart)
- [ ] Optimize Docker image size (multi-stage build comparison)
- [ ] CI/CD pipeline via GitHub Actions
- [ ] Live cloud deployment (Render/Railway)

## Why This Project

Built to get hands-on with the practical side of DevOps, containerization, and AI integration, going beyond tutorials by actually deploying something real.


<!-- testing credential storage -->
