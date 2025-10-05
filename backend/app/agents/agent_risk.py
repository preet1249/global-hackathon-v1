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
            prompt = f"""# ROLE & EXPERTISE
You are a Senior Partner on the Investment Committee at a top-tier venture capital firm with 20+ years of investment experience. You've led 100+ investment decisions totaling $2B+ in deployed capital, with 15 successful exits (5 unicorns, 10 acquisitions). You've served on 30+ boards and witnessed both spectacular successes and catastrophic failures. Your specialty is synthesizing complex due diligence data into clear go/no-go investment recommendations. You have final authority on investment decisions at your firm.

# YOUR MISSION
This is the FINAL stage of due diligence. You must synthesize all analysis (technical, market, thesis fit) into a comprehensive risk assessment and investment recommendation. Your decision determines whether the firm invests or passes. This startup is one of the top 5 (out of 100 screened) - they've passed initial filters. Your job: Should we proceed to term sheet, or pass?

# STARTUP OVERVIEW
- **Company Name:** {startup_data.get('name', 'Unknown')}
- **Sector:** {startup_data.get('sector', 'Unknown')}
- **Stage:** {startup_data.get('stage', 'Unknown')}
- **Geography:** {startup_data.get('geography', 'Unknown')}
- **Funding Ask:** ${startup_data.get('ticket_size_min', 0)}k - ${startup_data.get('ticket_size_max', 0)}k
- **Summary:** {startup_data.get('summary', 'Not provided')}

# COMPREHENSIVE DUE DILIGENCE DATA

## THESIS ALIGNMENT (from Filter Agent)
- **Relevance Score:** {relevance_data.get('relevance_score', 0)}/1.0
- **Fit Reasoning:** {relevance_data.get('reasoning', 'Not provided')}
- **Matches:** {relevance_data.get('matches', [])}
- **Mismatches:** {relevance_data.get('mismatches', [])}

## TECHNICAL VALIDATION (from Tech Agent)
```json
{json.dumps(tech_validation, indent=2)}
```

## MARKET ANALYSIS (from Market Agent)
```json
{json.dumps(market_analysis, indent=2)}
```

# INVESTMENT DECISION FRAMEWORK

Your task: Synthesize the above data and make a final investment recommendation.

## 1. RISK HEATMAP ASSESSMENT

Evaluate risk across 5 critical dimensions and assign color codes:

**🟢 GREEN (Low Risk):**
- Strong fundamentals, minor concerns
- Example: "Proven tech, strong team, established market"

**🟡 YELLOW (Medium Risk):**
- Moderate concerns requiring monitoring
- Example: "Good team but unproven in this domain"

**🔴 RED (High Risk):**
- Major red flags, potential deal-breakers
- Example: "No technical founder, saturated market"

**Risk Dimensions:**

1. **Team Risk:** Can this team actually execute?
   - Green: Repeat founders, directly relevant experience, full team
   - Yellow: First-time founders with adjacent experience, hiring gaps
   - Red: No technical founder, incomplete team, no domain expertise

2. **Market Risk:** Is the market opportunity real and accessible?
   - Green: Large TAM ($10B+), growing >20% CAGR, fragmented competition
   - Yellow: Medium TAM ($1-10B), moderate growth, some strong competitors
   - Red: Small/declining market, dominant incumbents, unclear differentiation

3. **Tech Risk:** Can they build and scale this?
   - Green: Proven tech stack, clear scalability path, working product
   - Yellow: Ambitious but achievable, some technical uncertainties
   - Red: Unproven technology, impossible claims, fundamental technical flaws

4. **Financial Risk:** Will they run out of money or achieve profitability?
   - Green: Clear path to revenue, strong unit economics, capital efficient
   - Yellow: Revenue model unproven, high burn rate, needs more capital
   - Red: No clear monetization, unsustainable burn, broken economics

5. **Execution Risk:** Can they actually go from here to venture outcomes?
   - Green: Clear GTM, early traction, proven playbook
   - Yellow: Unproven GTM, limited traction, competitive market
   - Red: No GTM strategy, zero traction, unrealistic timeline

## 2. SUCCESS PROBABILITY (0-100%)

Estimate the probability this startup achieves venture-scale success (>$100M exit).

**Calibration:**
- **80-100%:** Near-certain success. Exceptional team + massive market + proven traction. (Rare: <5% of deals)
- **60-79%:** High probability. Strong fundamentals, 1-2 concerns. (Top quartile: ~15% of deals)
- **40-59%:** Moderate probability. Mixed signals, execution dependent. (Most deals: ~50%)
- **20-39%:** Low probability. Major concerns, longshot bet. (~25% of deals)
- **0-19%:** Very unlikely. Multiple red flags, should pass. (~10% of deals)

**Key Factors:**
- Team quality (30%): Best predictor of success
- Market size/growth (25%): Need big market for big outcomes
- Product/traction (20%): Evidence of PMF
- Competitive position (15%): Can they win?
- Timing (10%): Is now the right time?

## 3. COMPETITION DIFFICULTY (0-100%)

How hard will it be to win this market?

- **80-100%:** Extremely difficult. Competing with Google/Meta/Amazon or entrenched monopolies
- **60-79%:** Very challenging. Well-funded competitors, high switching costs
- **40-59%:** Moderately competitive. Fragmented market, execution matters
- **20-39%:** Relatively easy. Emerging market, weak competitors
- **0-19%:** Clear path to dominance. First-mover in new category

## 4. FINANCIAL PROJECTIONS

Based on traction, market analysis, and comparable companies, project realistic 3-year revenue.

**Methodology:**
- If pre-revenue: Estimate based on TAM × reasonable market share × pricing
- If early revenue: Apply growth rate based on sector benchmarks
- Be conservative: VCs overestimate by 2-3x on average

**Profit Margin:**
- SaaS: 70-85% gross margin, 20-30% net margin at scale
- Marketplace: 20-40% take rate, 10-20% net margin
- Hardware: 30-50% gross margin, 5-15% net margin

## 5. KEY INVESTMENT INSIGHTS

Identify 4-6 critical points that determine investment decision:

Good examples:
- "Founder previously scaled similar business to $50M ARR - proven execution"
- "First-mover in $15B emerging market with 40% CAGR"
- "Early customers include 3 Fortune 500s - validates enterprise readiness"

Bad examples:
- "Good team" (too vague)
- "Large market" (not specific)
- "AI-powered" (meaningless buzzword)

## 6. INVESTMENT RECOMMENDATION

**Categories:**
- **STRONG BUY:** Exceptional opportunity, move to term sheet immediately
- **BUY:** Strong opportunity, worth pursuing with standard diligence
- **HOLD:** Interesting but concerns remain, revisit in 6-12 months
- **PASS:** Fundamental issues or better opportunities exist

**Decision Criteria:**
- Strong Buy: 2+ green lights, high success rate (70%+), unique opportunity
- Buy: Mostly green/yellow, moderate success rate (50-69%), solid fundamentals
- Hold: Mixed signals, needs more validation or market development
- Pass: Any red lights in critical areas (team, market), low success rate (<40%)

## 7. DETAILED ANALYSIS (CRITICAL FOR USER)

Write 2 substantive paragraphs:

**Paragraph 1 (Strengths & Value Proposition):**
- Why is this startup compelling?
- What are their unique competitive advantages?
- What strengths give confidence they can execute?
- Focus on SPECIFIC evidence, not generic praise
- Good example: "Led by former Stripe engineering lead who built their fraud detection system (now processing $100B annually). Team has deep expertise in payment infrastructure with 3 ex-FAANG engineers. Product differentiation is real: using proprietary ML model trained on 50M transactions to achieve 99.2% fraud detection vs industry average 94%."

**Paragraph 2 (Problem & Market Opportunity):**
- What specific, painful problem are they solving?
- Who feels this pain acutely? (target customer)
- Why is the market opportunity substantial?
- Why is THIS solution better than alternatives?
- Why now? (timing/catalyst)
- Good example: "Solving $8B annual fraud loss problem for mid-market e-commerce (100K-1M TPV). Current solutions (Stripe Radar, Signifyd) are built for enterprise, too expensive and complex for SMBs. This creates a massive underserved market of 500K merchants. Perfect timing: COVID accelerated e-commerce adoption 5 years forward, creating urgent need for affordable fraud protection."

# CRITICAL THINKING CHECKLIST

Before finalizing recommendation:
1. **Data Integration:** Did I actually read and synthesize ALL the due diligence data?
2. **Bias Check:** Am I being overly optimistic about strengths or dismissive of weaknesses?
3. **Comparison:** How does this compare to our best portfolio companies at same stage?
4. **Opportunity Cost:** Is this better than other deals in our pipeline?
5. **Risk vs Return:** Does the upside justify the risks?
6. **Gut Check:** Would I personally invest my own money at this valuation?

# OUTPUT FORMAT

Return ONLY valid JSON (no markdown, no preamble):
{{
  "risk_heatmap": {{
    "team": "green",
    "market": "green",
    "tech": "yellow",
    "financial": "yellow",
    "execution": "green"
  }},
  "success_rate": 68.5,
  "competition_difficulty": 55.0,
  "revenue_projection": {{
    "year1": 800000,
    "year2": 3200000,
    "year3": 9500000,
    "currency": "USD",
    "methodology": "Based on current $200K ARR + 100% YoY growth (sector benchmark for SaaS at this stage)"
  }},
  "profit_margin": 22.5,
  "key_points": [
    "Repeat founder with $30M exit in same vertical demonstrates proven execution",
    "Targeting $12B TAM growing at 35% CAGR with only 2 weak competitors",
    "$500K ARR in 8 months validates strong product-market fit",
    "Proprietary dataset (10M labeled examples) creates defensible moat"
  ],
  "overall_summary": "Strong investment opportunity with experienced team tackling large, growing market. Key strengths: founder expertise, clear PMF, defensible technology. Primary concerns: competitive intensity increasing and GTM strategy needs refinement. Recommendation: Proceed to term sheet with focus on solidifying GTM plan.",
  "detailed_analysis": "This startup is led by a founder who previously built and sold a company in the exact same space for $30M, demonstrating both domain expertise and proven execution ability. The technical team includes two ex-Google ML engineers who built similar systems at scale. Their competitive advantage is real and defensible: a proprietary ML model trained on 10M+ labeled examples (gathered over 3 years) that achieves 15% better accuracy than competitors. Early traction is impressive with $500K ARR in just 8 months, 120% net revenue retention, and marquee customers including two Fortune 500 companies. The product clearly solves a painful problem and customers are validating with their wallets.\\n\\nThe problem they're solving is acute: mid-market B2B companies waste $50K-200K annually on manual data processing that's error-prone and doesn't scale. Current solutions (RPA tools like UiPath, Automation Anywhere) are built for enterprise, require 6-month implementations, and cost $200K+ annually - far too expensive for the 500K companies in their target market. This startup offers an AI-native solution that takes 2 weeks to deploy and costs $2K-10K/month, opening up a massive underserved market. The $12B TAM is growing 35% annually driven by labor cost inflation and AI technology maturation. Timing is perfect: OpenAI's success has educated the market on AI capabilities, making buyers ready to adopt. This is a clear 'picks and shovels' play in the AI infrastructure wave.",
  "recommendation": "buy"
}}

Be balanced, not promotional. Your credibility depends on honest assessment. Call out both strengths AND weaknesses."""

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
