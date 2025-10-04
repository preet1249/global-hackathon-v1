# Backend - VC Multi-Agent Platform

FastAPI backend with multi-agent AI system for startup due diligence.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

### With Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

## 📦 Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database**: Supabase (PostgreSQL)
- **Queue**: Redis + RQ
- **PDF Processing**: PyMuPDF, pdfplumber
- **Web Scraping**: Playwright, BeautifulSoup
- **LLMs**: OpenAI, Anthropic, Google, DeepSeek, xAI
- **Container**: Docker

## 🌐 Deploy to Render

### Step 1: Create Web Service
1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect your GitHub repository
4. Select `backend` folder as root directory

### Step 2: Configure Service
- **Name**: vc-multi-agent-api
- **Environment**: Docker
- **Dockerfile Path**: `./Dockerfile`
- **Instance Type**: Standard (or higher for production)

### Step 3: Add Environment Variables
Go to Environment tab and add (from `.env.example`):

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
REDIS_URL=your_redis_url
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
XAI_API_KEY=your_key
```

### Step 4: Add Redis
1. Create Redis instance on Render
2. Copy Internal Redis URL
3. Add to `REDIS_URL` environment variable

### Step 5: Deploy
Click "Create Web Service"

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in all API keys.

## 📁 Project Structure

```
backend/
├── app/
│   ├── agents/       # AI agent modules
│   ├── api/          # API endpoints
│   ├── models/       # Data models
│   ├── services/     # External services
│   ├── utils/        # Utility functions
│   ├── workers/      # Background workers
│   └── main.py       # FastAPI app
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🔄 API Endpoints

- `POST /api/jobs` - Create new analysis job
- `GET /api/jobs/{job_id}` - Get job status
- `GET /api/jobs/{job_id}/results` - Get results
- `POST /api/jobs/{job_id}/cancel` - Cancel job

## 🤖 AI Agents

1. **Parser Agent** (Qwen3-VL) - Parse PDFs/Sheets
2. **Filter Agent** (GPT-5 mini) - Relevance filtering
3. **Tech Validator** (DeepSeek) - Technical validation
4. **Market Analyst** (Gemini) - Market analysis
5. **Risk Agent** (Grok) - Risk assessment & predictions

## 📊 Database Schema

See `prompt.md` for complete Supabase schema.
