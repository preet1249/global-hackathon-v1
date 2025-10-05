import pandas as pd
import logging
from typing import Dict, Any, List
import io

logger = logging.getLogger(__name__)

class ExcelParser:
    """
    Parse Excel files (.xlsx, .xls) and CSV files
    Flexible column mapping - handles various naming conventions
    """

    # Column name variations (lowercase for matching)
    COLUMN_MAPPINGS = {
        "name": ["name", "company", "startup", "company name", "startup name", "business name"],
        "sector": ["sector", "industry", "vertical", "category", "domain", "market"],
        "stage": ["stage", "funding stage", "round", "series", "investment stage"],
        "geography": ["geography", "location", "region", "country", "city", "market", "geo"],
        "ticket_size": ["ticket_size", "ticket size", "funding", "investment", "amount", "raise", "capital"],
        "summary": ["summary", "description", "about", "overview", "pitch", "brief"],
        "website": ["website", "url", "link", "web", "site"],
        "pdf_link": ["pdf_link", "pdf link", "deck", "pitch deck", "pdf", "document"],
        "team": ["team", "founders", "founder", "ceo", "leadership"],
        "traction": ["traction", "metrics", "revenue", "users", "growth", "customers"],
        "product": ["product", "solution", "service", "offering", "what we do"]
    }

    @staticmethod
    def find_column(df_columns: List[str], field_name: str) -> str:
        """Find the best matching column name from variations"""
        possible_names = ExcelParser.COLUMN_MAPPINGS.get(field_name, [field_name])

        # Try exact match first
        for col in df_columns:
            if col in possible_names:
                return col

        # Try partial match
        for col in df_columns:
            for possible in possible_names:
                if possible in col or col in possible:
                    return col

        return None

    @staticmethod
    def parse_excel(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Parse Excel or CSV file

        Args:
            file_bytes: File content as bytes
            filename: Original filename to determine format

        Returns:
            Dict with success status and parsed startups
        """
        try:
            # Determine file type
            if filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file_bytes))
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(file_bytes), engine='openpyxl')
            elif filename.endswith('.xls'):
                df = pd.read_excel(io.BytesIO(file_bytes), engine='xlrd')
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file format: {filename}"
                }

            if df.empty:
                return {
                    "success": False,
                    "error": "File is empty"
                }

            # Normalize column names (lowercase, strip spaces)
            df.columns = df.columns.str.lower().str.strip()
            df_cols = df.columns.tolist()

            # Map columns intelligently
            column_map = {}
            for field in ["name", "sector", "stage", "geography", "ticket_size", "summary",
                         "website", "pdf_link", "team", "traction", "product"]:
                found_col = ExcelParser.find_column(df_cols, field)
                if found_col:
                    column_map[field] = found_col

            logger.info(f"Column mapping: {column_map}")

            startups = []

            for idx, row in df.iterrows():
                try:
                    startup = {
                        "name": str(row.get(column_map.get("name", "name"), "")).strip(),
                        "sector": str(row.get(column_map.get("sector", "sector"), "")).strip(),
                        "stage": str(row.get(column_map.get("stage", "stage"), "")).strip(),
                        "geography": str(row.get(column_map.get("geography", "geography"), "")).strip(),
                        "ticket_size": str(row.get(column_map.get("ticket_size", "ticket_size"), "")).strip(),
                        "summary": str(row.get(column_map.get("summary", "summary"), "")).strip(),
                        "website": str(row.get(column_map.get("website", "website"), "")).strip(),
                        "pdf_link": str(row.get(column_map.get("pdf_link", "pdf_link"), "")).strip(),
                        "team": str(row.get(column_map.get("team", "team"), "")).strip(),
                        "traction": str(row.get(column_map.get("traction", "traction"), "")).strip(),
                        "product": str(row.get(column_map.get("product", "product"), "")).strip()
                    }

                    # Skip empty rows
                    if not startup["name"] or startup["name"] == "nan":
                        continue

                    # Parse ticket size if present
                    if startup["ticket_size"] and startup["ticket_size"] != "nan":
                        startup["parsed_ticket_size"] = ExcelParser.parse_ticket_size(
                            startup["ticket_size"]
                        )

                    startups.append(startup)

                except Exception as e:
                    logger.warning(f"Failed to parse row {idx + 2}: {str(e)}")
                    continue

            if not startups:
                return {
                    "success": False,
                    "error": "No valid startup data found in file"
                }

            return {
                "success": True,
                "startups": startups,
                "total_rows": len(startups)
            }

        except Exception as e:
            logger.error(f"Excel/CSV parsing error: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to parse file: {str(e)}"
            }

    @staticmethod
    def parse_ticket_size(ticket_str: str) -> Dict[str, Any]:
        """
        Parse ticket size string like "$500k-$1M" or "$2M+"
        Returns min and max values in dollars
        """
        try:
            import re

            # Remove spaces and make lowercase
            ticket_str = str(ticket_str).replace(" ", "").lower()

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
