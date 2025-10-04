import asyncio
import logging
import tempfile
import os
from typing import Dict, Any, List
from app.services.supabase_client import get_supabase_client
from app.services.pdf_parser import PDFParser
from app.services.sheets_parser import GoogleSheetsParser
from app.agents.agent_parser import ParserAgent
from app.agents.agent_filter import FilterAgent
from app.agents.agent_tech import TechAgent
from app.agents.agent_market import MarketAgent
from app.agents.agent_risk import RiskAgent

logger = logging.getLogger(__name__)

class JobProcessor:
    """
    Main job processor - orchestrates the entire pipeline
    NO MOCK DATA - Real processing only!
    """

    def __init__(self, job_id: str):
        self.job_id = job_id
        self.supabase = get_supabase_client()

    async def update_progress(self, step: str, percent: int, message: str):
        """Update job progress in Supabase"""
        try:
            self.supabase.table("jobs").update({
                "progress": {
                    "step": step,
                    "percent": percent,
                    "status_message": message
                }
            }).eq("id", self.job_id).execute()
            logger.info(f"Job {self.job_id}: {step} - {percent}% - {message}")
        except Exception as e:
            logger.error(f"Failed to update progress: {str(e)}")

    async def log_error(self, error_message: str):
        """Log error to job"""
        try:
            self.supabase.table("jobs").update({
                "error_log": error_message,
                "status": "failed"
            }).eq("id", self.job_id).execute()
            logger.error(f"Job {self.job_id} failed: {error_message}")
        except Exception as e:
            logger.error(f"Failed to log error: {str(e)}")

    async def process_job(self):
        """
        Main processing pipeline - follows prompt.md exactly
        """
        try:
            # Get job details
            job_response = self.supabase.table("jobs").select("*").eq("id", self.job_id).execute()

            if not job_response.data:
                await self.log_error("Job not found")
                return

            job = job_response.data[0]
            filters = job.get("filters", {})

            # Update status
            self.supabase.table("jobs").update({"status": "parsing"}).eq("id", self.job_id).execute()

            # STEP 1: PARSE FILES
            await self.update_progress("parsing", 10, "Starting file parsing...")
            startup_candidates = await self.parse_files()

            if not startup_candidates:
                await self.log_error("No startups extracted from files")
                return

            await self.update_progress("parsing", 30, f"Parsed {len(startup_candidates)} startups")

            # STEP 2: FILTER & RANK
            await self.update_progress("filtering", 40, "Filtering startups against thesis...")
            self.supabase.table("jobs").update({"status": "filtering"}).eq("id", self.job_id).execute()

            shortlisted = await self.filter_startups(startup_candidates, filters)

            if not shortlisted:
                await self.log_error("No startups matched the investment criteria")
                return

            await self.update_progress("filtering", 50, f"Shortlisted {len(shortlisted)} startups")

            # STEP 3: DUE DILIGENCE
            await self.update_progress("dd_running", 60, "Running due diligence on top startups...")
            self.supabase.table("jobs").update({"status": "dd_running"}).eq("id", self.job_id).execute()

            dd_results = await self.run_due_diligence(shortlisted)

            await self.update_progress("aggregating", 90, "Aggregating final results...")

            # STEP 4: FINALIZE
            await self.finalize_results(dd_results)

            # Mark complete
            self.supabase.table("jobs").update({
                "status": "completed",
                "progress": {
                    "step": "completed",
                    "percent": 100,
                    "status_message": "Analysis complete!"
                }
            }).eq("id", self.job_id).execute()

            logger.info(f"Job {self.job_id} completed successfully")

        except Exception as e:
            logger.exception(f"Job {self.job_id} failed with exception")
            await self.log_error(f"Critical error: {str(e)}")

    async def parse_files(self) -> List[Dict[str, Any]]:
        """Parse all uploaded files (PDFs and Google Sheets)"""
        try:
            # Get all files for this job
            files_response = self.supabase.table("files").select("*").eq("job_id", self.job_id).execute()

            if not files_response.data:
                logger.warning(f"No files found for job {self.job_id}")
                return []

            startups = []

            for file_record in files_response.data:
                file_type = file_record.get("file_type")

                if file_type == "pdf":
                    startup_data = await self.parse_pdf_file(file_record)
                    if startup_data:
                        startups.append(startup_data)

                elif file_type == "sheet":
                    sheet_startups = await self.parse_google_sheet(file_record)
                    startups.extend(sheet_startups)

            return startups

        except Exception as e:
            logger.error(f"File parsing error: {str(e)}")
            return []

    async def parse_pdf_file(self, file_record: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a single PDF file - NO MOCKS!"""
        try:
            storage_path = file_record.get("storage_path")

            # Download PDF from Supabase Storage
            file_data = self.supabase.storage.from_("pitch-decks").download(storage_path)

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file_data)
                tmp_path = tmp_file.name

            try:
                # Parse PDF with PyMuPDF
                pdf_data = PDFParser.parse_pdf(tmp_path)

                if not pdf_data.get("success"):
                    logger.error(f"PDF parsing failed: {pdf_data.get('error')}")
                    return None

                # Use AI to extract structured data
                parser_result = await ParserAgent.parse_pdf_content(
                    pdf_text=pdf_data.get("full_text", ""),
                    pdf_data=pdf_data
                )

                if not parser_result.get("success"):
                    logger.error(f"Parser agent failed: {parser_result.get('error')}")
                    return None

                extracted_data = parser_result.get("data", {})

                # Save parsed data to files table
                self.supabase.table("files").update({
                    "parsed": pdf_data
                }).eq("id", file_record.get("id")).execute()

                # Create startup entry
                startup_entry = {
                    "job_id": self.job_id,
                    "source_file_id": file_record.get("id"),
                    "name": extracted_data.get("name"),
                    "sector": extracted_data.get("sector"),
                    "stage": extracted_data.get("stage"),
                    "geography": extracted_data.get("geography"),
                    "ticket_size_min": extracted_data.get("ticket_size_min"),
                    "ticket_size_max": extracted_data.get("ticket_size_max"),
                    "summary": extracted_data.get("summary"),
                    "metadata": {
                        "team": extracted_data.get("team", []),
                        "traction": extracted_data.get("traction"),
                        "product": extracted_data.get("product"),
                        "claims": extracted_data.get("claims", [])
                    }
                }

                startup_response = self.supabase.table("startups").insert(startup_entry).execute()

                if startup_response.data:
                    return startup_response.data[0]

                return None

            finally:
                # Clean up temp file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"PDF file processing error: {str(e)}")
            return None

    async def parse_google_sheet(self, file_record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Google Sheet and extract startups - NO MOCKS!"""
        try:
            sheet_url = file_record.get("original_name")  # We store the URL in original_name for sheets

            # Parse the Google Sheet
            sheet_result = await GoogleSheetsParser.parse_sheet(sheet_url)

            if not sheet_result.get("success"):
                logger.error(f"Sheet parsing failed: {sheet_result.get('error')}")
                return []

            # Save parsed data to files table
            self.supabase.table("files").update({
                "parsed": sheet_result
            }).eq("id", file_record.get("id")).execute()

            startups = []
            sheet_startups = sheet_result.get("startups", [])

            for row_data in sheet_startups:
                # Handle PDF link if present
                pdf_link = row_data.get("pdf_link", "").strip()

                if pdf_link:
                    # Download and parse PDF from URL
                    pdf_bytes = await GoogleSheetsParser.download_pdf_from_url(pdf_link)

                    if pdf_bytes:
                        # Save to temp file and parse
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(pdf_bytes)
                            tmp_path = tmp_file.name

                        try:
                            pdf_data = PDFParser.parse_pdf(tmp_path)

                            if pdf_data.get("success"):
                                # Use AI to extract structured data
                                parser_result = await ParserAgent.parse_pdf_content(
                                    pdf_text=pdf_data.get("full_text", ""),
                                    pdf_data=pdf_data
                                )

                                if parser_result.get("success"):
                                    extracted_data = parser_result.get("data", {})
                                    # Merge sheet data with PDF extracted data
                                    row_data.update(extracted_data)

                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)

                # Create startup entry from sheet row
                parsed_ticket = row_data.get("parsed_ticket_size", {})

                startup_entry = {
                    "job_id": self.job_id,
                    "source_file_id": file_record.get("id"),
                    "name": row_data.get("name", ""),
                    "sector": row_data.get("sector", ""),
                    "stage": row_data.get("stage", ""),
                    "geography": row_data.get("geography", ""),
                    "ticket_size_min": parsed_ticket.get("min"),
                    "ticket_size_max": parsed_ticket.get("max"),
                    "summary": row_data.get("summary", ""),
                    "metadata": {
                        "team": row_data.get("team", ""),
                        "traction": row_data.get("traction", ""),
                        "product": row_data.get("product", ""),
                        "website": row_data.get("website", ""),
                        "pdf_link": row_data.get("pdf_link", "")
                    }
                }

                startup_response = self.supabase.table("startups").insert(startup_entry).execute()

                if startup_response.data:
                    startups.append(startup_response.data[0])

            logger.info(f"Parsed {len(startups)} startups from Google Sheet")
            return startups

        except Exception as e:
            logger.error(f"Google Sheet processing error: {str(e)}")
            return []

    async def filter_startups(self, startups: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter startups using AI - OPTIMIZED with parallel batches!"""
        try:
            filtered = []

            # Process in batches of 10 for speed (reduces 110 startups from 14min to 2-3min)
            batch_size = 10

            for i in range(0, len(startups), batch_size):
                batch = startups[i:i + batch_size]

                # Run batch in parallel
                tasks = [
                    FilterAgent.calculate_relevance(startup, filters)
                    for startup in batch
                ]

                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                # Process results
                for startup, filter_result in zip(batch, batch_results):
                    if isinstance(filter_result, Exception):
                        logger.error(f"Filter failed for {startup.get('name')}: {str(filter_result)}")
                        continue

                    if not filter_result.get("success"):
                        logger.error(f"Filter failed for {startup.get('name')}: {filter_result.get('error')}")
                        continue

                    relevance_score = filter_result.get("relevance_score", 0.0)

                    # Update startup with relevance score
                    self.supabase.table("startups").update({
                        "relevance_score": relevance_score
                    }).eq("id", startup.get("id")).execute()

                    if relevance_score >= 0.5:  # Threshold
                        startup["relevance_score"] = relevance_score
                        startup["filter_reasoning"] = filter_result.get("reasoning", "")
                        filtered.append(startup)

                # Progress update after each batch
                progress_pct = 40 + int((i + batch_size) / len(startups) * 10)
                await self.update_progress("filtering", progress_pct, f"Filtered {min(i + batch_size, len(startups))}/{len(startups)} startups...")

            # Sort by relevance score
            filtered.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

            # Take top 5
            return filtered[:5]

        except Exception as e:
            logger.error(f"Filtering error: {str(e)}")
            return []

    async def run_due_diligence(self, startups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run due diligence on shortlisted startups - NO MOCKS!"""
        results = []

        for i, startup in enumerate(startups):
            try:
                await self.update_progress("dd_running", 60 + (i * 5), f"Analyzing {startup.get('name')}...")

                # Run tech validation
                tech_result = await TechAgent.validate_tech(startup)

                # Run market analysis
                market_result = await MarketAgent.analyze_market(startup)

                if not tech_result.get("success") or not market_result.get("success"):
                    logger.error(f"DD failed for {startup.get('name')}")
                    continue

                # Run risk assessment
                risk_result = await RiskAgent.assess_risk_and_predict(
                    startup_data=startup,
                    tech_validation=tech_result.get("tech_validation", {}),
                    market_analysis=market_result,
                    relevance_data={"relevance_score": startup.get("relevance_score"), "reasoning": startup.get("filter_reasoning")}
                )

                if not risk_result.get("success"):
                    logger.error(f"Risk assessment failed for {startup.get('name')}")
                    continue

                # Save to due_diligence table
                dd_entry = {
                    "startup_id": startup.get("id"),
                    "tech_validation": tech_result.get("tech_validation"),
                    "market_analysis": market_result.get("market_analysis"),
                    "competitor_map": market_result.get("competitor_map"),
                    "financial_check": market_result.get("financial_check"),
                    "risk_heatmap": risk_result.get("risk_heatmap"),
                    "success_rate": risk_result.get("success_rate"),
                    "competition_difficulty": risk_result.get("competition_difficulty"),
                    "revenue_projection": risk_result.get("revenue_projection"),
                    "profit_margin": risk_result.get("profit_margin"),
                    "key_points": risk_result.get("key_points"),
                    "overall_summary": risk_result.get("overall_summary"),
                    "detailed_analysis": risk_result.get("detailed_analysis", "")
                }

                dd_response = self.supabase.table("due_diligence").insert(dd_entry).execute()

                if dd_response.data:
                    results.append({
                        "startup": startup,
                        "dd": dd_response.data[0]
                    })

            except Exception as e:
                logger.error(f"DD processing error for {startup.get('name')}: {str(e)}")
                continue

        return results

    async def finalize_results(self, dd_results: List[Dict[str, Any]]):
        """Create final results entry"""
        try:
            top_startups = []

            for i, result in enumerate(dd_results):
                top_startups.append({
                    "rank": i + 1,
                    "startup_id": result["startup"].get("id"),
                    "name": result["startup"].get("name"),
                    "success_rate": result["dd"].get("success_rate"),
                    "fit_reason": result["startup"].get("filter_reasoning")
                })

            result_entry = {
                "job_id": self.job_id,
                "top_startups": top_startups
            }

            self.supabase.table("results").insert(result_entry).execute()

        except Exception as e:
            logger.error(f"Finalize error: {str(e)}")
