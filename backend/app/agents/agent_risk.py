from app.agents.openrouter_client import OpenRouterClient
from typing import Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class RiskAgent:
    """
    Agent 5: Risk Assessment & Summary
    Uses Grok to generate risk heatmap, predictions, and final summary
    """

    @staticmethod
    async def assess_risk_and_predict(
        startup_data: Dict[str, Any],
        tech_validation: Dict[str, Any],
        market_analysis: Dict[str, Any],
        relevance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive risk assessment and predictions

        Args:
            startup_data: Basic startup info
            tech_validation: Results from tech agent
            market_analysis: Results from market agent
            relevance_data: Results from filter agent

        Returns:
            Risk heatmap, success rate, revenue projections, key points
        """
        try:
            prompt = f"""You are a senior VC analyst. Based on comprehensive due diligence, generate final assessment.

Startup: {startup_data.get('name', 'Unknown')}
Sector: {startup_data.get('sector')}

TECHNICAL ASSESSMENT:
{json.dumps(tech_validation, indent=2)}

MARKET ASSESSMENT:
{json.dumps(market_analysis, indent=2)}

THESIS MATCH:
Score: {relevance_data.get('relevance_score', 0)}
Reasoning: {relevance_data.get('reasoning', '')}

Generate final investment assessment with:

1. Risk Heatmap (rate each as: green/yellow/red)
   - Tech risk
   - Market risk
   - Financial risk
   - Compliance risk

2. Success Rate (0-100): Probability of achieving stated goals

3. Competition Difficulty (0-100): How hard is this market to win

4. Revenue Projection (3 years): Realistic estimates

5. Profit Margin: Expected % at scale

6. Key Points (3-6 bullets): Critical insights

7. Overall Summary: Investment recommendation

8. Detailed Analysis (2 paragraphs):
   - Paragraph 1: Why this startup is good, unique value proposition, competitive advantages
   - Paragraph 2: What problem they're solving, market opportunity, why this specific solution stands out

Return ONLY valid JSON:
{{
  "risk_heatmap": {{
    "tech": "green|yellow|red",
    "market": "green|yellow|red",
    "finance": "green|yellow|red",
    "compliance": "green|yellow|red"
  }},
  "success_rate": 75.5,
  "competition_difficulty": 65.0,
  "revenue_projection": {{
    "year1": 500000,
    "year2": 2000000,
    "year3": 5000000,
    "currency": "USD"
  }},
  "profit_margin": 25.5,
  "key_points": [
    "Strong technical team with proven track record",
    "Large TAM in growing market",
    "Early traction validates product-market fit"
  ],
  "overall_summary": "Brief investment recommendation with reasoning",
  "detailed_analysis": "Two detailed paragraphs explaining why this is good and what they're solving. First paragraph focuses on strengths and competitive advantages. Second paragraph explains the problem space and market opportunity.",
  "recommendation": "strong_buy|buy|hold|pass"
}}"""

            messages = [{"role": "user", "content": prompt}]

            result = await OpenRouterClient.call_model(
                model_key="grok",
                messages=messages,
                max_tokens=1500,
                temperature=0.5,
                timeout=60
            )

            if not result.get("success"):
                return {
                    "success": False,
                    "error": result.get("error"),
                    "agent": "risk"
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
                    "risk_heatmap": parsed_data.get("risk_heatmap", {}),
                    "success_rate": parsed_data.get("success_rate", 50.0),
                    "competition_difficulty": parsed_data.get("competition_difficulty", 50.0),
                    "revenue_projection": parsed_data.get("revenue_projection", {}),
                    "profit_margin": parsed_data.get("profit_margin", 0.0),
                    "key_points": parsed_data.get("key_points", []),
                    "overall_summary": parsed_data.get("overall_summary", ""),
                    "detailed_analysis": parsed_data.get("detailed_analysis", ""),
                    "recommendation": parsed_data.get("recommendation", "hold"),
                    "agent": "risk",
                    "model": result.get("model")
                }

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from risk agent: {str(e)}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response: {str(e)}",
                    "raw_content": content,
                    "agent": "risk"
                }

        except Exception as e:
            logger.error(f"Risk agent exception: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": "risk"
            }
