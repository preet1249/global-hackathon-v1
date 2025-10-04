import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import jobs

app = FastAPI(title="VC Multi-Agent API", version="1.0.0")

# CORS - Allow frontend and localhost
allowed_origins = [
    "https://global-hackathon-v1-olive.vercel.app",
    "http://localhost:3000",
    "http://localhost:3001",
]

# Add any additional origins from environment variable
if os.getenv("ALLOWED_ORIGINS"):
    allowed_origins.extend(os.getenv("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(jobs.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "VC Multi-Agent API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
