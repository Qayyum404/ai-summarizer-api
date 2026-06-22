# AI Summarizer API

A FastAPI service that summarizes text using a real AI model (HuggingFace's facebook/bart-large-cnn), containerized with Docker and backed by Redis caching. Built as a hands-on learning project covering containerization, caching, CI/CD, and cloud deployment fundamentals.

## What It Does

Send any block of text to the /summarize endpoint, and it returns a genuinely AI-generated summary, not a basic word-count truncation. The model reads the input, identifies the most important sentences, and returns a condensed version that preserves meaning. Repeated requests for the same text are served instantly from a Redis cache instead of re-calling the AI model.

## Tech Stack

- FastAPI - Python web framework for the API
- HuggingFace Inference Providers - real AI model for summarization (facebook/bart-large-cnn)
- Redis - caching layer for repeated requests
- Docker and Docker Compose - containerization and multi-service orchestration
- Pydantic - request validation
- python-dotenv - environment variable management
- Coming next: GitHub Actions CI/CD, cloud deployment, self-healing demo, image size optimization

## How Caching Works

1. Incoming text is hashed with SHA-256 to create a unique cache key
2. Redis is checked first for that key
3. On a cache miss: the real HuggingFace API is called (1-3+ seconds), the result is stored in Redis with a 1-hour expiration, and returned with cached: false
4. On a cache hit: the stored result is returned instantly from memory (under 15ms), with cached: true

## Running Locally with Docker

1. Clone the repo:
git clone https://github.com/Qayyum404/ai-summarizer-api.git
cd ai-summarizer-api

2. Create a .env file with your own HuggingFace token:
HF_TOKEN=your_huggingface_token_here

Get a free token at https://huggingface.co/settings/tokens

3. Build and run both containers (API + Redis):
docker compose up --build

4. Open http://localhost:8000/docs and test the /summarize endpoint interactively.

## Running Locally without Docker

1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. uvicorn main:app --reload

Note: without Docker, you'll need Redis running separately and may need to adjust REDIS_HOST in your environment.

## A Bug I Found and Fixed

During testing, I discovered that error responses from the HuggingFace API (such as a 504 Gateway Timeout during a model cold start) were being cached and returned for repeated requests, since the original caching logic stored whatever the AI function returned, including errors. I fixed this by having the summarization function return a success flag alongside the result, so only genuinely successful AI responses get cached, never errors. I also added a request timeout and a basic retry for cold-start scenarios.

## Roadmap

- [x] Core FastAPI summarization endpoint
- [x] Real AI integration via HuggingFace Inference Providers
- [x] Dockerize the app
- [x] Add Redis caching to avoid redundant AI calls on repeated text
- [ ] Add a self-healing demo (deliberate crash + automatic Docker restart)
- [ ] Optimize Docker image size (multi-stage build comparison)
- [ ] CI/CD pipeline via GitHub Actions
- [ ] Live cloud deployment (Render/Railway)

## Why This Project

Built to get hands-on with the practical side of DevOps, containerization, and AI integration, going beyond tutorials by actually deploying something real and debugging real issues along the way, including a deprecated API endpoint migration and a caching logic bug.
