from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import jobs

app = FastAPI(title="VC Multi-Agent API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
