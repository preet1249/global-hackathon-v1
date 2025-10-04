from app.agents.openrouter_client import OpenRouterClient
from typing import Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class TechAgent:
    """
    Agent 3: Tech Validator
    Uses DeepSeek to validate technical claims
    """

    @staticmethod
    async def validate_tech(startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate technical claims made by the startup

        Args:
            startup_data: Startup information with claims

        Returns:
            Technical validation results
        """
        try:
            claims = startup_data.get('claims', [])
            product = startup_data.get('product', '')

            prompt = f"""You are a technical due diligence expert. Analyze the technical claims made by this startup.

Startup: {startup_data.get('name', 'Unknown')}
Sector: {startup_data.get('sector', 'Unknown')}

Product Description:
{product}

Technical Claims:
{json.dumps(claims, indent=2)}

Validate each claim and provide:
1. Feasibility assessment (feasible/questionable/unlikely)
2. Evidence or benchmark comparisons
3. Technical risks or red flags

Return ONLY valid JSON:
{{
  "overall_assessment": "strong|moderate|weak",
  "claims_validated": [
    {{
      "claim": "original claim",
      "verdict": "feasible|questionable|unlikely",
      "reasoning": "why",
      "evidence": "benchmark or comparison"
    }}
  ],
  "technical_risks": ["risk1", "risk2"],
  "technical_score": 0.75,
  "key_strengths": ["strength1"],
  "key_weaknesses": ["weakness1"]
}}"""

            messages = [{"role": "user", "content": prompt}]

            result = await OpenRouterClient.call_model(
                model_key="deepseek",
                messages=messages,
                max_tokens=1500,
                temperature=0.4,
                timeout=90
            )

            if not result.get("success"):
                return {
                    "success": False,
                    "error": result.get("error"),
                    "agent": "tech"
                }

            content = result.get("content", "").strip()

            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                parsed_data = json.loads(content)

                return {
                    "success": True,
                    "tech_validation": parsed_data,
                    "agent": "tech",
                    "model": result.get("model")
                }

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from tech agent: {str(e)}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response: {str(e)}",
                    "raw_content": content,
                    "agent": "tech"
                }

        except Exception as e:
            logger.error(f"Tech agent exception: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": "tech"
            }
