import httpx
import logging
from typing import Dict, Any, List
import re

logger = logging.getLogger(__name__)

class GoogleSheetsParser:
    """
    Parse Google Sheets without API - uses CSV export
    NO MOCK DATA - Real parsing only!
    """

    @staticmethod
    def extract_sheet_id(sheet_url: str) -> str:
        """Extract Google Sheet ID from URL"""
        # https://docs.google.com/spreadsheets/d/SHEET_ID/edit
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheet_url)
        if match:
            return match.group(1)
        return None

    @staticmethod
    async def parse_sheet(sheet_url: str) -> Dict[str, Any]:
        """
        Parse Google Sheet by converting to CSV
        Expected columns: name, sector, stage, geography, ticket_size, summary, website, pdf_link

        Returns:
            Dict with success status and parsed rows
        """
        try:
            sheet_id = GoogleSheetsParser.extract_sheet_id(sheet_url)

            if not sheet_id:
                return {
                    "success": False,
                    "error": "Invalid Google Sheets URL"
                }

            # Convert to CSV export URL
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

            # Fetch CSV
            async with httpx.AsyncClient() as client:
                response = await client.get(csv_url, timeout=30.0)

                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"Failed to fetch sheet: {response.status_code}"
                    }

                csv_content = response.text

            # Parse CSV
            rows = csv_content.strip().split('\n')

            if len(rows) < 2:
                return {
                    "success": False,
                    "error": "Sheet is empty or has no data rows"
                }

            # Get headers (first row)
            headers = [h.strip().lower() for h in rows[0].split(',')]

            # Parse data rows
            startups = []
            for i, row in enumerate(rows[1:], start=2):
                try:
                    # Simple CSV parsing (handles quoted fields)
                    values = []
                    current_value = ""
                    in_quotes = False

                    for char in row:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:
                            values.append(current_value.strip())
                            current_value = ""
                        else:
                            current_value += char

                    values.append(current_value.strip())

                    # Map values to headers
                    row_data = {}
                    for j, header in enumerate(headers):
                        if j < len(values):
                            row_data[header] = values[j]

                    # Extract startup data
                    startup = {
                        "name": row_data.get("name", ""),
                        "sector": row_data.get("sector", ""),
                        "stage": row_data.get("stage", ""),
                        "geography": row_data.get("geography", ""),
                        "ticket_size": row_data.get("ticket_size", ""),
                        "summary": row_data.get("summary", ""),
                        "website": row_data.get("website", ""),
                        "pdf_link": row_data.get("pdf_link", ""),
                        "team": row_data.get("team", ""),
                        "traction": row_data.get("traction", ""),
                        "product": row_data.get("product", "")
                    }

                    # Parse ticket size if present
                    if startup["ticket_size"]:
                        startup["parsed_ticket_size"] = GoogleSheetsParser.parse_ticket_size(
                            startup["ticket_size"]
                        )

                    startups.append(startup)

                except Exception as e:
                    logger.warning(f"Failed to parse row {i}: {str(e)}")
                    continue

            return {
                "success": True,
                "startups": startups,
                "total_rows": len(startups)
            }

        except Exception as e:
            logger.error(f"Google Sheets parsing error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def parse_ticket_size(ticket_str: str) -> Dict[str, Any]:
        """
        Parse ticket size string like "$500k-$1M" or "$2M+"
        Returns min and max values in dollars
        """
        try:
            # Remove spaces and make lowercase
            ticket_str = ticket_str.replace(" ", "").lower()

            # Extract numbers
            numbers = re.findall(r'[\d.]+', ticket_str)

            if not numbers:
                return {"min": None, "max": None}

            # Check for 'k' (thousands) or 'm' (millions)
            multiplier = 1
            if 'k' in ticket_str:
                multiplier = 1000
            elif 'm' in ticket_str:
                multiplier = 1000000

            # Check if range
            if '-' in ticket_str or 'to' in ticket_str:
                if len(numbers) >= 2:
                    min_val = float(numbers[0]) * multiplier
                    max_val = float(numbers[1]) * multiplier
                    return {"min": min_val, "max": max_val}

            # Single value or "X+"
            if len(numbers) >= 1:
                value = float(numbers[0]) * multiplier
                if '+' in ticket_str:
                    return {"min": value, "max": None}
                else:
                    return {"min": value, "max": value}

            return {"min": None, "max": None}

        except Exception as e:
            logger.warning(f"Failed to parse ticket size '{ticket_str}': {str(e)}")
            return {"min": None, "max": None}

    @staticmethod
    async def download_pdf_from_url(pdf_url: str) -> bytes:
        """
        Download PDF from URL
        Returns PDF bytes or None if failed
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(pdf_url, timeout=60.0)

                if response.status_code == 200:
                    return response.content
                else:
                    logger.error(f"Failed to download PDF: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"PDF download error: {str(e)}")
            return None
