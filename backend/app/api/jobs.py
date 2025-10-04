from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
import json

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/")
async def create_job(
    files: Optional[List[UploadFile]] = File(None),
    google_sheet_link: Optional[str] = Form(None),
    filters: str = Form(...),
    context_text: Optional[str] = Form(None)
):
    """Create a new job for startup analysis"""
    filters_data = json.loads(filters)

    # TODO: Implement job creation logic
    return {
        "job_id": "placeholder",
        "user_token": "placeholder",
        "status": "pending",
        "message": "Job created successfully"
    }

@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get job status and results"""
    # TODO: Implement job retrieval logic
    return {
        "job_id": job_id,
        "status": "pending",
        "progress": {"step": "parsing", "percent": 0}
    }

@router.get("/{job_id}/results")
async def get_results(job_id: str):
    """Get job results"""
    # TODO: Implement results retrieval logic
    return {
        "job_id": job_id,
        "top_startups": []
    }

@router.post("/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a running job"""
    # TODO: Implement job cancellation logic
    return {"job_id": job_id, "status": "cancelled"}
