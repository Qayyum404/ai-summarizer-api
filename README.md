# AI Summarizer API

A FastAPI service that summarizes text using a real AI model (HuggingFace's facebook/bart-large-cnn), containerized with Docker, backed by Redis caching, and configured for self-healing recovery. Built as a hands-on learning project covering containerization, caching, resilience, CI/CD, and cloud deployment fundamentals.

## What It Does

Send any block of text to the /summarize endpoint, and it returns a genuinely AI-generated summary, not a basic word-count truncation. Repeated requests for the same text are served instantly from a Redis cache instead of re-calling the AI model. The service is also configured to automatically recover if the application process crashes.

## Tech Stack

- FastAPI - Python web framework for the API
- HuggingFace Inference Providers - real AI model for summarization (facebook/bart-large-cnn)
- Redis - caching layer for repeated requests
- Docker and Docker Compose - containerization, multi-service orchestration, restart policies, health checks
- Pydantic - request validation
- python-dotenv - environment variable management
- Coming next: GitHub Actions CI/CD, cloud deployment

## How Caching Works

1. Incoming text is hashed with SHA-256 to create a unique cache key
2. Redis is checked first for that key
3. On a cache miss: the real HuggingFace API is called (1-3+ seconds), the result is stored in Redis with a 1-hour expiration, and returned with cached: false
4. On a cache hit: the stored result is returned instantly from memory (under 15ms), with cached: true

## How Self-Healing Works

The app includes a /crash endpoint that deliberately kills the running process to simulate a real crash. Docker Compose is configured with restart: on-failure, so when the process dies, Docker automatically starts a fresh container without any manual intervention. A health check also runs every 10 seconds against the root endpoint, so Docker can detect if the app becomes unresponsive even without a full crash.

Demo:
docker ps                          # container shows healthy, running for some time
curl http://localhost:8000/crash   # deliberately kill the process
sleep 3
docker ps                          # same container, uptime reset to a few seconds - it restarted automatically

## Image Size Optimization

Compared three approaches to measure actual impact on image size:

| Image | Disk usage | Content size |
|---|---|---|
| Full python:3.11 base image | 1.64GB | 421MB |
| python:3.11-slim base image | 260MB | 62.6MB |
| python:3.11-slim with multi-stage build | 243MB | 58.6MB |

Switching from the full Python base image to the slim variant gave a roughly 6x reduction in image size. A multi-stage build was also tested, giving a further modest improvement (about 6.5% smaller), but the gain was limited because this project's dependencies (FastAPI, Redis client, Pydantic, requests) are lightweight pure-Python packages without heavy build-time tooling to strip out. Given the small additional gain, the project sticks with the simpler single-stage slim build for maintainability.

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

## Bugs Found and Fixed Along the Way

- Error responses from the HuggingFace API (such as a 504 during a model cold start) were initially being cached and returned for repeated requests. Fixed by having the summarization function return a success flag alongside the result, so only genuine successes get cached.
- The original HuggingFace Inference API endpoint (api-inference.huggingface.co) was deprecated mid-project and replaced with their new router-based endpoint, requiring a URL update and a debugging session to trace the actual cause via DNS resolution checks.

## Roadmap

- [x] Core FastAPI summarization endpoint
- [x] Real AI integration via HuggingFace Inference Providers
- [x] Dockerize the app
- [x] Add Redis caching to avoid redundant AI calls on repeated text
- [x] Add a self-healing demo (deliberate crash + automatic Docker restart)
- [x] Optimize Docker image size (multi-stage build comparison)
- [ ] CI/CD pipeline via GitHub Actions
- [ ] Live cloud deployment (Render/Railway)

## Why This Project

Built to get hands-on with the practical side of DevOps, containerization, and AI integration, going beyond tutorials by actually deploying something real and debugging real issues along the way, including a deprecated API endpoint migration, a caching logic bug, and verifying container self-healing and image size tradeoffs firsthand.
