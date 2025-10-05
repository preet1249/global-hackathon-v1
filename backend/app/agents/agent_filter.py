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
            prompt = f"""# ROLE & EXPERTISE
You are a Senior VC Investment Analyst with 15+ years of experience at top-tier venture capital firms including Sequoia Capital, Andreessen Horowitz, and Accel Partners. You've evaluated 10,000+ startups across 50+ investment decisions totaling $500M+ in deployed capital. You have deep expertise in identifying product-market fit, assessing founder quality, and matching startups to investment thesis criteria.

# YOUR MISSION
Evaluate how well this startup matches our investment thesis and assign a precise relevance score from 0.0 to 1.0. This is the CRITICAL filtering stage where we narrow 100+ startups down to the top 5 for deep due diligence. Your score directly determines which startups get investor attention.

# INVESTMENT THESIS (Our Criteria)
- **Target Sector:** {filters.get('sector', 'Any')}
- **Preferred Stage:** {filters.get('stage', 'Any')}
- **Geographic Focus:** {filters.get('geography', 'Any')}
- **Check Size Range:** ${filters.get('ticket_min', 0)}k - ${filters.get('ticket_max', 'unlimited')}k
- **Strategic Context:** {filters.get('context_text', 'General VC investment - seeking high-growth tech startups with strong unit economics and scalable business models')}

# STARTUP PROFILE
- **Company Name:** {startup_data.get('name', 'Unknown')}
- **Sector/Industry:** {startup_data.get('sector', 'Unknown')}
- **Funding Stage:** {startup_data.get('stage', 'Unknown')}
- **Geography:** {startup_data.get('geography', 'Unknown')}
- **Funding Ask:** ${startup_data.get('ticket_size_min', 0)}k - ${startup_data.get('ticket_size_max', 0)}k
- **Business Summary:** {startup_data.get('summary', '')}
- **Product Description:** {startup_data.get('product', '')}
- **Team:** {startup_data.get('metadata', {}).get('team', 'Not specified')}
- **Traction:** {startup_data.get('metadata', {}).get('traction', 'Not specified')}

# EVALUATION FRAMEWORK

Assess match quality across these dimensions:

**1. Sector Alignment (Weight: 30%)**
- Does the startup operate in our target sector?
- If "Any" sector, prioritize high-growth tech categories (AI, SaaS, FinTech, HealthTech, etc.)
- Consider adjacent sectors that still align with expertise
- Red flag: Sectors we explicitly avoid or low-growth industries

**2. Stage Fit (Weight: 25%)**
- Is this the funding stage we target?
- If "Any" stage, prefer Seed to Series A (proven concept but early enough for high returns)
- Consider: Does their current traction match their stated stage?
- Red flag: Too early (just an idea) or too late (Series C+ looking for small checks)

**3. Geographic Compatibility (Weight: 15%)**
- Can we effectively support this company from our location?
- If "Any" geography, prefer markets we understand
- Consider time zones, regulatory environments, market access
- Red flag: Geographies with regulatory barriers or no local presence

**4. Check Size Match (Weight: 15%)**
- Does our typical check size fit their raise?
- Too small = we can't be meaningful investors
- Too large = we'd be overexposed
- Ideal: Our check is 10-30% of their total raise

**5. Business Quality (Weight: 15%)**
- Product-market fit signals: Do they articulate a clear problem/solution?
- Traction validation: Real revenue/users or just claims?
- Team strength: Relevant experience, technical depth, execution ability?
- Market opportunity: TAM large enough for venture-scale returns?

# SCORING CALIBRATION

**0.9-1.0 (Exceptional Match):**
- Perfect alignment on sector, stage, geography, AND check size
- Strong business fundamentals: clear PMF, impressive traction, stellar team
- Example: AI SaaS startup, Series A, raising $3M, $1M ARR with 15% MoM growth, technical founding team from FAANG

**0.7-0.8 (Strong Match):**
- Aligns on 3/4 key criteria (sector, stage, geo, check size)
- Solid business with 1-2 areas of concern
- Example: Right sector and stage, but geography is stretched OR great company but check size slightly small

**0.5-0.6 (Moderate Match):**
- Aligns on 2/4 criteria OR aligns on all but weak business fundamentals
- Could work but not ideal
- Example: Right sector but wrong stage, or perfect fit but no clear traction yet

**0.3-0.4 (Weak Match):**
- Aligns on only 1/4 criteria
- Multiple red flags
- Example: Interesting company but completely wrong stage and geography

**0.0-0.2 (Poor/No Match):**
- Misaligned on all major criteria
- Clear deal-breakers present
- Example: Consumer goods company when we only do B2B SaaS, or Series D when we only do Seed

# CRITICAL THINKING CHECKLIST

Before finalizing your score, ask yourself:
1. **Thesis Alignment:** If our thesis says "AI startups only", does a "FinTech with some AI features" count? (Be strict on primary sector)
2. **Stage Reality Check:** Does their traction actually match their claimed stage? (A "Series A" with $0 revenue is really pre-seed)
3. **Hidden Strengths:** Does this startup have exceptional qualities that override a weak criteria match? (e.g., founder previously exited for $100M)
4. **Red Flags:** Are there deal-breakers I'm overlooking? (Regulatory issues, problematic cap table, dying market)
5. **Relative Comparison:** If I'm seeing 100 startups today, would this be top 10%? Top 50%? Bottom 25%?

# OUTPUT FORMAT

Return ONLY valid JSON (no markdown, no preamble):
{{
  "relevance_score": 0.75,
  "reasoning": "2-3 sentences explaining the score. Focus on KEY factors: what strongly aligns, what doesn't, and the deciding factor for this specific score.",
  "matches": ["Specific alignment point 1", "Specific alignment point 2", "Specific alignment point 3"],
  "mismatches": ["Specific concern/gap 1", "Specific concern/gap 2"]
}}

**Example Output:**
{{
  "relevance_score": 0.82,
  "reasoning": "Strong match on sector (AI/ML aligns perfectly with thesis) and stage (Series A with solid traction). Check size fits our $1-3M sweet spot. Minor concern on geography (Southeast Asia vs our US focus) but team's Silicon Valley experience mitigates this. Traction is impressive: $800K ARR with 20% MoM growth.",
  "matches": ["AI/ML sector - perfect fit", "Series A with $2M raise - ideal stage", "$800K ARR with strong growth - proven PMF", "Technical founding team with relevant experience"],
  "mismatches": ["Southeast Asia HQ - outside primary geography", "Limited US market presence currently"]
}}

Be precise, be critical, be consistent. This score determines which 5 startups (out of 100) get deep analysis."""

            messages = [{"role": "user", "content": prompt}]

            result = await OpenRouterClient.call_model(
                model_key="gpt5",
                messages=messages,
                max_tokens=500,
                temperature=0.3,
                timeout=30
            )

            if not result.get("success"):
                logger.error(f"Filter agent API error: {result.get('error')}")
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "agent": "filter"
                }

            # Parse JSON response
            content = result.get("content", "").strip()

            if not content:
                logger.error(f"Filter agent returned EMPTY content! Full result: {result}")
                return {
                    "success": False,
                    "error": "API returned empty content",
                    "agent": "filter"
                }

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
