import fitz  # PyMuPDF
import pdfplumber
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    """Parse PDF files and extract text, images, tables"""

    @staticmethod
    def extract_text_pymupdf(pdf_path: str) -> Dict[str, Any]:
        """
        Extract text from PDF using PyMuPDF
        Returns structured JSON with page-wise chunks
        """
        try:
            doc = fitz.open(pdf_path)
            pages_data = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                # Extract images info
                images = page.get_images()

                pages_data.append({
                    "page_number": page_num + 1,
                    "text": text.strip(),
                    "image_count": len(images)
                })

            doc.close()

            # Combine all text
            full_text = "\n\n".join([p["text"] for p in pages_data if p["text"]])

            return {
                "success": True,
                "pages": pages_data,
                "full_text": full_text,
                "total_pages": len(pages_data),
                "method": "pymupdf"
            }

        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "method": "pymupdf"
            }

    @staticmethod
    def extract_tables_pdfplumber(pdf_path: str) -> Dict[str, Any]:
        """
        Extract tables from PDF using pdfplumber
        """
        try:
            tables_data = []

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            tables_data.append({
                                "page": page_num + 1,
                                "data": table
                            })

            return {
                "success": True,
                "tables": tables_data,
                "table_count": len(tables_data),
                "method": "pdfplumber"
            }

        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "method": "pdfplumber"
            }

    @staticmethod
    def parse_pdf(pdf_path: str) -> Dict[str, Any]:
        """
        Main parsing function - combines text and table extraction
        Returns structured JSON ready for AI processing
        """
        try:
            # Extract text
            text_result = PDFParser.extract_text_pymupdf(pdf_path)

            # Extract tables
            table_result = PDFParser.extract_tables_pdfplumber(pdf_path)

            if not text_result.get("success"):
                return {
                    "success": False,
                    "error": text_result.get("error", "Unknown error in text extraction")
                }

            return {
                "success": True,
                "text_data": text_result,
                "table_data": table_result,
                "full_text": text_result.get("full_text", ""),
                "pages": text_result.get("pages", []),
                "tables": table_result.get("tables", [])
            }

        except Exception as e:
            logger.error(f"PDF parsing failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
