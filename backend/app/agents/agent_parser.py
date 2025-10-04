from app.agents.openrouter_client import OpenRouterClient
from typing import Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class ParserAgent:
    """
    Agent 1: Input & Preprocessing
    Uses Qwen3-VL to parse PDF content and extract structured startup data
    """

    @staticmethod
    async def parse_pdf_content(pdf_text: str, pdf_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse PDF content and extract startup information

        Args:
            pdf_text: Extracted text from PDF
            pdf_data: Full PDF parsing result with tables

        Returns:
            Structured startup data or error
        """
        try:
            prompt = f"""You are analyzing a startup pitch deck. Extract the following information from the provided text.
If information is not found, return null for that field. Be precise and factual.

Extract:
- name: Company name
- sector: Industry/sector (e.g., AI, FinTech, HealthTech)
- stage: Funding stage (e.g., Pre-seed, Seed, Series A)
- geography: Location/market
- ticket_size_min: Minimum funding amount requested (number only)
- ticket_size_max: Maximum funding amount requested (number only)
- summary: Brief 2-3 sentence summary of the company
- team: Key team members and their roles
- traction: Current metrics, users, revenue
- product: What the product/service does
- claims: Key claims made in the deck

Pitch Deck Text:
{pdf_text[:8000]}

Return ONLY valid JSON in this exact format:
{{
  "name": "...",
  "sector": "...",
  "stage": "...",
  "geography": "...",
  "ticket_size_min": null or number,
  "ticket_size_max": null or number,
  "summary": "...",
  "team": ["..."],
  "traction": "...",
  "product": "...",
  "claims": ["..."]
}}"""

            messages = [{"role": "user", "content": prompt}]

            result = await OpenRouterClient.call_model(
                model_key="qwen",
                messages=messages,
                max_tokens=1500,
                temperature=0.3,
                timeout=30
            )

            if not result.get("success"):
                logger.error(f"Parser agent failed: {result.get('error')}")
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "agent": "parser"
                }

            # Parse JSON response
            content = result.get("content", "").strip()

            # Try to extract JSON from response
            try:
                # Remove markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                parsed_data = json.loads(content)

                return {
                    "success": True,
                    "data": parsed_data,
                    "agent": "parser",
                    "model": result.get("model")
                }

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from parser agent: {str(e)}")
                logger.error(f"Content was: {content}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response: {str(e)}",
                    "raw_content": content,
                    "agent": "parser"
                }

        except Exception as e:
            logger.error(f"Parser agent exception: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": "parser"
            }
