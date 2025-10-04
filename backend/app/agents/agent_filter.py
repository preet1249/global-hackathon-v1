from app.agents.openrouter_client import OpenRouterClient
from typing import Dict, Any, List
import logging
import json

logger = logging.getLogger(__name__)

class FilterAgent:
    """
    Agent 2: Thesis Matcher
    Uses GPT-5 mini to filter startups against VC investment thesis
    """

    @staticmethod
    async def calculate_relevance(startup_data: Dict[str, Any], filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate relevance score for a startup based on VC thesis

        Args:
            startup_data: Parsed startup information
            filters: VC investment criteria (sector, stage, geography, ticket size, context)

        Returns:
            Relevance score (0-1) and reasoning
        """
        try:
            prompt = f"""You are a VC investment analyst. Rate how well this startup matches the investment criteria.

Investment Criteria:
- Sector: {filters.get('sector', 'Any')}
- Stage: {filters.get('stage', 'Any')}
- Geography: {filters.get('geography', 'Any')}
- Ticket Size: ${filters.get('ticket_min', 0)}k - ${filters.get('ticket_max', 'unlimited')}k
- Context: {filters.get('context_text', 'General VC investment')}

Startup Information:
- Name: {startup_data.get('name', 'Unknown')}
- Sector: {startup_data.get('sector', 'Unknown')}
- Stage: {startup_data.get('stage', 'Unknown')}
- Geography: {startup_data.get('geography', 'Unknown')}
- Ticket Size: ${startup_data.get('ticket_size_min', 0)}k - ${startup_data.get('ticket_size_max', 0)}k
- Summary: {startup_data.get('summary', '')}
- Product: {startup_data.get('product', '')}

Rate the match on a scale of 0.0 to 1.0 where:
- 1.0 = Perfect match with all criteria
- 0.7-0.9 = Strong match
- 0.4-0.6 = Moderate match
- 0.1-0.3 = Weak match
- 0.0 = No match

Provide ONLY valid JSON:
{{
  "relevance_score": 0.85,
  "reasoning": "Brief explanation of why this score",
  "matches": ["what matches"],
  "mismatches": ["what doesn't match"]
}}"""

            messages = [{"role": "user", "content": prompt}]

            result = await OpenRouterClient.call_model(
                model_key="gpt5",
                messages=messages,
                max_tokens=500,
                temperature=0.3,
                timeout=30
            )

            if not result.get("success"):
                logger.error(f"Filter agent failed: {result.get('error')}")
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "agent": "filter"
                }

            # Parse JSON response
            content = result.get("content", "").strip()

            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                parsed_data = json.loads(content)

                return {
                    "success": True,
                    "relevance_score": parsed_data.get("relevance_score", 0.0),
                    "reasoning": parsed_data.get("reasoning", ""),
                    "matches": parsed_data.get("matches", []),
                    "mismatches": parsed_data.get("mismatches", []),
                    "agent": "filter",
                    "model": result.get("model")
                }

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from filter agent: {str(e)}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response: {str(e)}",
                    "raw_content": content,
                    "agent": "filter"
                }

        except Exception as e:
            logger.error(f"Filter agent exception: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": "filter"
            }
