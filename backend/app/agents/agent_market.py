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
            prompt = f"""# ROLE & EXPERTISE
You are a Senior Market Research and Strategy Analyst with 14+ years of experience at top-tier management consulting firms (McKinsey, BCG, Bain) and venture capital firms. You've conducted 300+ market analyses for startups raising $1B+ combined, specialized in TAM/SAM/SOM sizing, competitive intelligence, and go-to-market strategy. You have deep expertise in identifying market opportunities, assessing competitive dynamics, and evaluating business model viability across tech sectors.

# YOUR MISSION
Conduct comprehensive market analysis for this startup to determine if the market opportunity is large enough for venture-scale returns and if this company can capture meaningful market share. Your assessment determines whether investors should pursue this opportunity or pass due to market limitations.

# STARTUP PROFILE
- **Company Name:** {startup_data.get('name', 'Unknown')}
- **Sector:** {startup_data.get('sector', 'Unknown')}
- **Geography:** {startup_data.get('geography', 'Unknown')}
- **Stage:** {startup_data.get('stage', 'Unknown')}
- **Funding Ask:** ${startup_data.get('ticket_size_min', 0)}k - ${startup_data.get('ticket_size_max', 0)}k

**Business Summary:**
{startup_data.get('summary', 'Not provided')}

**Product Description:**
{startup_data.get('product', 'Not provided')}

**Current Traction:**
{startup_data.get('metadata', {}).get('traction', 'No traction data provided')}

**Team Background:**
{startup_data.get('metadata', {}).get('team', 'Not specified')}

# MARKET ANALYSIS FRAMEWORK

Evaluate across these critical dimensions:

## 1. MARKET SIZING (TAM/SAM/SOM) - 30% weight

**Total Addressable Market (TAM):**
- What's the maximum revenue opportunity if this company achieved 100% market share?
- Calculate bottom-up: (# of potential customers) × (annual spend per customer)
- For venture scale, TAM should be $1B+ (ideally $10B+)
- Example: "Enterprise email security: 500K companies × $50K/year = $25B TAM"

**Serviceable Addressable Market (SAM):**
- What portion of TAM can this company realistically target given geography, product limitations, go-to-market capabilities?
- Typically 10-30% of TAM
- Example: "Focusing on US + Europe SMBs (50K-500 employees) = $5B SAM"

**Serviceable Obtainable Market (SOM):**
- What market share can they realistically capture in 3-5 years?
- For early stage: 1-5% of SAM is realistic
- Example: "Capturing 3% of SAM in 5 years = $150M revenue opportunity"

**Market Size Assessment:**
- Too small (<$1B TAM): Not venture-scalable
- Medium ($1-10B TAM): Viable but competitive
- Large (>$10B TAM): Excellent opportunity if can execute

## 2. MARKET DYNAMICS & TRENDS - 25% weight

**Growth Rate:**
- Is the market growing, flat, or declining?
- Ideal: >20% CAGR (compound annual growth rate)
- Declining markets are red flags unless there's disruption

**Market Trends:**
- What macro trends support this business? (AI adoption, remote work, regulatory changes, consumer behavior shifts)
- Are trends accelerating or decelerating?
- Example: "Enterprise AI adoption growing 40% YoY, driven by GPT success"

**Market Timing:**
- Why now? What changed to make this possible/necessary?
- Too early = market not ready
- Too late = market already saturated
- Perfect timing = inflection point (new tech, new regulation, new behavior)

**Market Maturity:**
- Nascent: High risk, high reward, undefined
- Growing: Sweet spot for venture
- Mature: Harder to disrupt, lower multiples
- Declining: Avoid unless clear disruption angle

## 3. COMPETITIVE LANDSCAPE - 25% weight

**Direct Competitors:**
- Who else is solving the EXACT same problem for the SAME customers?
- List 3-5 key players with brief description
- Assess their strengths: funding, market share, product quality

**Indirect Competitors:**
- Alternative solutions (different approach to same problem)
- Incumbents (current way customers solve this)
- DIY/Status quo (doing nothing is often the real competitor)

**Competitive Advantages:**
- Why will customers choose THIS startup over competitors?
- Moats: Network effects, proprietary data, IP/patents, brand, regulatory barriers, switching costs
- Be skeptical: "Better UI" is NOT a strong moat

**Competitive Disadvantages:**
- Where are they weak vs competitors?
- First-mover disadvantage? Well-funded competitors? Incumbent dominance?

**Market Positioning:**
- Niche specialist vs full-stack generalist?
- Premium vs budget?
- Horizontal (all industries) vs vertical (one industry)?

## 4. GO-TO-MARKET (GTM) STRATEGY - 15% weight

**Customer Acquisition:**
- How do they plan to acquire customers?
- Channels: Sales team, inbound marketing, partnerships, product-led growth
- CAC (Customer Acquisition Cost): Can they acquire customers profitably?

**Sales Cycle:**
- Enterprise: 6-18 month cycles, high touch, expensive
- SMB: 1-3 month cycles, mid touch
- Self-serve: Minutes to days, low touch, scalable

**Unit Economics:**
- LTV (Lifetime Value) should be 3x+ CAC
- LTV = (Average revenue per customer) × (Gross margin) × (1/Churn rate)
- Red flag: High CAC with low retention

**Distribution Power:**
- Do they have unfair advantages in distribution? (Founder's network, strategic partnerships, viral loops)

## 5. FINANCIAL VIABILITY - 5% weight

**Revenue Model:**
- How do they make money? (SaaS subscription, transaction fees, marketplace take rate, usage-based)
- Is it recurring and predictable?

**Path to Profitability:**
- Can they become profitable with reasonable scale?
- Or will they need massive scale before breaking even?

**Capital Efficiency:**
- Can they reach $1M ARR on <$2M raised? (Strong signal)
- Or do they need $10M+ to prove anything? (Concerning)

# MARKET SCORING CALIBRATION (0.0 - 1.0)

**0.9-1.0 (Exceptional Market):**
- TAM >$10B, growing >30% annually
- Clear market trends supporting growth
- Weak/fragmented competition
- Strong GTM strategy with proven traction
- Example: AI infrastructure tools in 2023, vertical SaaS in underserved industries

**0.7-0.8 (Strong Market):**
- TAM $5-10B, growing 15-25% annually
- Positive trends, some competition
- Viable GTM with early customer validation
- Example: B2B SaaS in established but growing categories

**0.5-0.6 (Moderate Market):**
- TAM $1-5B, growing <15% annually
- Mixed trends, significant competition
- Unproven GTM, limited traction
- Example: Incremental improvements in mature markets

**0.3-0.4 (Weak Market):**
- TAM <$1B or declining market
- Strong incumbents dominating
- Unclear GTM or high CAC
- Example: Consumer apps in saturated categories

**0.0-0.2 (Poor Market):**
- No clear TAM or dying market
- Impossible to compete
- Fundamentally broken economics
- Example: Competing with free Google products

# CRITICAL THINKING CHECKLIST

Before finalizing:
1. **TAM Reality Check:** Is the TAM real or inflated with unrealistic assumptions?
2. **Competition Honesty:** Am I underestimating how hard it is to compete with [Big Tech Company]?
3. **Timing Truth:** Is "why now" compelling or just hopeful?
4. **Economics Test:** Can this business ever make money at scale?
5. **VC Fit:** Even if this works, can it return the fund (need $100M+ exit)?

# OUTPUT FORMAT

Return ONLY valid JSON (no markdown, no preamble):
{{
  "market_analysis": {{
    "tam_estimate": "$XB - Specific TAM calculation with methodology",
    "sam_estimate": "$XB - SAM breakdown",
    "som_estimate": "$XM - Realistic 5-year revenue target",
    "growth_rate": "X% CAGR with supporting evidence",
    "market_trends": ["Specific trend 1 with data", "Specific trend 2"],
    "market_maturity": "nascent|growing|mature|declining",
    "market_timing": "Assessment of why now is the right time",
    "market_risks": ["Specific risk 1", "Specific risk 2"]
  }},
  "competitor_map": {{
    "direct_competitors": ["Competitor 1 (funded $XM, YK users)", "Competitor 2 (public, $XB revenue)"],
    "indirect_competitors": ["Alternative solution 1", "Incumbent 2"],
    "competitive_advantages": ["Specific advantage 1 with defensibility", "Advantage 2"],
    "competitive_disadvantages": ["Specific weakness vs competitors 1", "Weakness 2"],
    "market_position": "Description of how they're positioned vs competition"
  }},
  "financial_check": {{
    "revenue_potential": "high|medium|low",
    "revenue_model": "Description of how they monetize",
    "unit_economics_assessment": "LTV/CAC analysis if data available",
    "burn_rate_assessment": "healthy|concerning|critical",
    "path_to_profitability": "clear|unclear|unlikely",
    "capital_efficiency": "strong|moderate|weak",
    "financial_risks": ["Specific financial risk 1", "Risk 2"]
  }},
  "market_score": 0.78,
  "key_insight": "One critical market insight that determines investment viability"
}}

**Example Output:**
{{
  "market_analysis": {{
    "tam_estimate": "$15B - 300K US enterprises × $50K annual cybersecurity spend",
    "sam_estimate": "$4.5B - Targeting mid-market (500-5000 employees) = 90K companies",
    "som_estimate": "$135M - Capturing 3% of SAM in 5 years is realistic given traction",
    "growth_rate": "28% CAGR - Cybersecurity spending growing due to increased threats and compliance requirements",
    "market_trends": ["Zero-trust adoption accelerating (Gartner: 60% of orgs by 2025)", "Remote work driving cloud security needs", "Regulatory pressure (GDPR, CCPA) mandating investment"],
    "market_maturity": "growing",
    "market_timing": "Perfect timing: Major breaches (SolarWinds, MOVEit) driving budget allocation + mature cloud infrastructure enabling deployment",
    "market_risks": ["Economic downturn could reduce security budgets", "Potential M&A consolidation (Palo Alto, CrowdStrike acquiring competitors)"]
  }},
  "competitor_map": {{
    "direct_competitors": ["SentinelOne (public, $500M ARR, endpoint focus)", "CrowdStrike (public, $2B ARR, market leader)", "Wiz ($100M ARR, cloud-native, fast growing)"],
    "indirect_competitors": ["Traditional firewalls (Cisco, Fortinet)", "DIY security teams using open source tools"],
    "competitive_advantages": ["First to combine endpoint + cloud in single platform", "AI detection with 99.8% accuracy (benchmarked vs competitors)", "Pricing 40% below CrowdStrike for SMB segment"],
    "competitive_disadvantages": ["No brand recognition vs established players", "Smaller sales team (15 vs CrowdStrike's 1000+)", "Limited integrations compared to incumbents"],
    "market_position": "Positioned as 'CrowdStrike for mid-market' - enterprise-grade tech at SMB prices"
  }},
  "financial_check": {{
    "revenue_potential": "high",
    "revenue_model": "SaaS subscription: $50-200 per endpoint/month, annual contracts",
    "unit_economics_assessment": "Strong early signals: $120K ACV, $30K CAC = 4:1 LTV/CAC with 90% gross margin",
    "burn_rate_assessment": "healthy",
    "path_to_profitability": "clear",
    "capital_efficiency": "strong",
    "financial_risks": ["High upfront R&D costs for AI models", "Price competition from well-funded competitors could compress margins"]
  }},
  "market_score": 0.84,
  "key_insight": "Massive market ($15B TAM) with strong tailwinds, but success depends on execution against well-funded competitors. Window of opportunity exists in under-served mid-market segment before incumbents move down-market."
}}

Be rigorous. Use real data when possible. Call out when TAM is inflated or competition is underestimated."""

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
