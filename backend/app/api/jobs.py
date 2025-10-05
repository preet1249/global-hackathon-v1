from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import Response
from typing import List, Optional
import json
import uuid
import asyncio
from app.services.supabase_client import get_supabase_client
from app.workers.job_processor import JobProcessor
from app.services.pdf_generator import PDFGenerator

router = APIRouter(prefix="/jobs", tags=["jobs"])

supabase = get_supabase_client()

async def process_job_background(job_id: str):
    """Background task to process job"""
    processor = JobProcessor(job_id)
    await processor.process_job()

@router.post("/")
async def create_job(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(default=[]),
    google_sheet_link: Optional[str] = Form(None),
    filters: str = Form(...),
    context_text: Optional[str] = Form(None)
):
    """Create a new job for startup analysis - NO MOCK DATA!"""
    try:
        import logging
        logger = logging.getLogger(__name__)

        logger.info(f"Received job request - files: {len(files) if files else 0}, sheet: {bool(google_sheet_link)}")
        logger.info(f"Filters: {filters}")

        # Validate inputs
        if not files and not google_sheet_link:
            raise HTTPException(
                status_code=422,
                detail="Must provide either files or google_sheet_link"
            )

        filters_data = json.loads(filters)

        # Create job in database
        job_data = {
            "status": "pending",
            "filters": filters_data,
            "user_token": str(uuid.uuid4()),
            "progress": {
                "step": "pending",
                "percent": 0,
                "status_message": "Job created, waiting to start..."
            }
        }

        job_response = supabase.table("jobs").insert(job_data).execute()

        if not job_response.data:
            raise HTTPException(status_code=500, detail="Failed to create job")

        job = job_response.data[0]
        job_id = job.get("id")

        # Upload files to Supabase Storage
        if files:
            for file in files:
                file_content = await file.read()
                file_path = f"{job_id}/{file.filename}"

                # Upload to Supabase Storage
                supabase.storage.from_("pitch-decks").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": file.content_type}
                )

                # Create file record
                file_data = {
                    "job_id": job_id,
                    "file_type": "pdf",
                    "original_name": file.filename,
                    "storage_path": file_path
                }

                supabase.table("files").insert(file_data).execute()

        # Handle Google Sheet link if provided
        if google_sheet_link:
            sheet_data = {
                "job_id": job_id,
                "file_type": "sheet",
                "original_name": google_sheet_link,  # Store URL as original_name
                "storage_path": None  # No storage path for sheets
            }

            supabase.table("files").insert(sheet_data).execute()

        # Start processing in background
        background_tasks.add_task(process_job_background, job_id)

        return {
            "job_id": job_id,
            "user_token": job.get("user_token"),
            "status": "pending",
            "message": "Job created successfully and processing started"
        }

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid filters JSON: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job creation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get job status and progress - REAL DATA ONLY!"""
    try:
        job_response = supabase.table("jobs").select("*").eq("id", job_id).execute()

        if not job_response.data:
            raise HTTPException(status_code=404, detail="Job not found")

        job = job_response.data[0]

        # If completed, get results
        if job.get("status") == "completed":
            results_response = supabase.table("results").select("*").eq("job_id", job_id).execute()

            if results_response.data:
                job["results"] = results_response.data[0]

        return job

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}/results")
async def get_results(job_id: str):
    """Get detailed job results - REAL DATA ONLY!"""
    try:
        # Get job
        job_response = supabase.table("jobs").select("*").eq("id", job_id).execute()

        if not job_response.data:
            raise HTTPException(status_code=404, detail="Job not found")

        job = job_response.data[0]

        if job.get("status") != "completed":
            return {
                "job_id": job_id,
                "status": job.get("status"),
                "message": "Job not completed yet",
                "progress": job.get("progress")
            }

        # Get results
        results_response = supabase.table("results").select("*").eq("job_id", job_id).execute()

        if not results_response.data:
            raise HTTPException(status_code=404, detail="Results not found")

        results = results_response.data[0]
        top_startups = results.get("top_startups", [])

        # Get full details for each startup
        detailed_startups = []

        for startup_info in top_startups:
            startup_id = startup_info.get("startup_id")

            # Get startup
            startup_response = supabase.table("startups").select("*").eq("id", startup_id).execute()

            # Get due diligence
            dd_response = supabase.table("due_diligence").select("*").eq("startup_id", startup_id).execute()

            if startup_response.data and dd_response.data:
                detailed_startups.append({
                    "rank": startup_info.get("rank"),
                    "startup": startup_response.data[0],
                    "due_diligence": dd_response.data[0],
                    "fit_reason": startup_info.get("fit_reason")
                })

        return {
            "job_id": job_id,
            "status": "completed",
            "startups": detailed_startups
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a running job"""
    try:
        job_response = supabase.table("jobs").select("*").eq("id", job_id).execute()

        if not job_response.data:
            raise HTTPException(status_code=404, detail="Job not found")

        supabase.table("jobs").update({"status": "cancelled"}).eq("id", job_id).execute()

        return {"job_id": job_id, "status": "cancelled"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}/download/{startup_id}")
async def download_startup_pdf(job_id: str, startup_id: str):
    """Download PDF report for a single startup - REAL PDF with graphs!"""
    try:
        # Get startup
        startup_response = supabase.table("startups").select("*").eq("id", startup_id).eq("job_id", job_id).execute()

        if not startup_response.data:
            raise HTTPException(status_code=404, detail="Startup not found")

        startup = startup_response.data[0]

        # Get due diligence
        dd_response = supabase.table("due_diligence").select("*").eq("startup_id", startup_id).execute()

        if not dd_response.data:
            raise HTTPException(status_code=404, detail="Due diligence not found")

        dd = dd_response.data[0]

        # Generate PDF with graphs
        pdf_bytes = PDFGenerator.generate_startup_report(startup, dd)

        # Return as downloadable file
        filename = f"{startup.get('name', 'startup').replace(' ', '_')}_Report.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}/download-all")
async def download_portfolio_pdf(job_id: str):
    """Download complete portfolio report - REAL PDF with all startups!"""
    try:
        # Get results
        results_response = supabase.table("results").select("*").eq("job_id", job_id).execute()

        if not results_response.data:
            raise HTTPException(status_code=404, detail="Results not found")

        results = results_response.data[0]
        top_startups = results.get("top_startups", [])

        # Get full details for each startup
        detailed_startups = []

        for startup_info in top_startups:
            startup_id = startup_info.get("startup_id")

            # Get startup
            startup_response = supabase.table("startups").select("*").eq("id", startup_id).execute()

            # Get due diligence
            dd_response = supabase.table("due_diligence").select("*").eq("startup_id", startup_id).execute()

            if startup_response.data and dd_response.data:
                detailed_startups.append({
                    "rank": startup_info.get("rank"),
                    "startup": startup_response.data[0],
                    "due_diligence": dd_response.data[0]
                })

        # Generate portfolio PDF
        pdf_bytes = PDFGenerator.generate_portfolio_report(detailed_startups)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=Portfolio_Report.pdf"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
