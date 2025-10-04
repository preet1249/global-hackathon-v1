from app.agents.openrouter_client import OpenRouterClient
from typing import Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class MarketAgent:
    """
    Agent 4: Market & Financial Analyst
    Uses Gemini to analyze market, competitors, and financials
    """

    @staticmethod
    async def analyze_market(startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market opportunity and financial projections

        Args:
            startup_data: Startup information

        Returns:
            Market analysis and financial assessment
        """
        try:
            prompt = f"""You are a market research and financial analyst. Analyze this startup's market opportunity.

Startup: {startup_data.get('name', 'Unknown')}
Sector: {startup_data.get('sector', 'Unknown')}
Geography: {startup_data.get('geography', 'Unknown')}

Summary:
{startup_data.get('summary', '')}

Product:
{startup_data.get('product', '')}

Traction:
{startup_data.get('traction', 'None reported')}

Analyze:
1. Total Addressable Market (TAM)
2. Market growth rate and trends
3. Potential competitors
4. Market risks
5. Financial health indicators

Return ONLY valid JSON:
{{
  "market_analysis": {{
    "tam_estimate": "market size estimate",
    "growth_rate": "estimated annual growth %",
    "market_trends": ["trend1", "trend2"],
    "market_risks": ["risk1", "risk2"]
  }},
  "competitor_map": {{
    "direct_competitors": ["comp1", "comp2"],
    "indirect_competitors": ["comp3"],
    "competitive_advantages": ["advantage1"],
    "competitive_disadvantages": ["disadvantage1"]
  }},
  "financial_check": {{
    "revenue_potential": "high|medium|low",
    "burn_rate_assessment": "healthy|concerning|critical",
    "path_to_profitability": "clear|unclear|uncertain",
    "financial_risks": ["risk1"]
  }},
  "market_score": 0.75
}}"""

            messages = [{"role": "user", "content": prompt}]

            result = await OpenRouterClient.call_model(
                model_key="gemini",
                messages=messages,
                max_tokens=1500,
                temperature=0.4,
                timeout=90
            )

            if not result.get("success"):
                return {
                    "success": False,
                    "error": result.get("error"),
                    "agent": "market"
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
                    "market_analysis": parsed_data.get("market_analysis", {}),
                    "competitor_map": parsed_data.get("competitor_map", {}),
                    "financial_check": parsed_data.get("financial_check", {}),
                    "market_score": parsed_data.get("market_score", 0.5),
                    "agent": "market",
                    "model": result.get("model")
                }

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from market agent: {str(e)}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response: {str(e)}",
                    "raw_content": content,
                    "agent": "market"
                }

        except Exception as e:
            logger.error(f"Market agent exception: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": "market"
            }
