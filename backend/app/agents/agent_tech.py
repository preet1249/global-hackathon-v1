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

            prompt = f"""# ROLE & EXPERTISE
You are a Senior Technical Due Diligence Lead with 12+ years of experience as a CTO and technical advisor at venture-backed startups. You've led technical teams at 3 unicorn companies (valued $1B+), built and scaled systems serving 100M+ users, and conducted technical due diligence on 500+ startups for top-tier VC firms. You have deep expertise in software architecture, AI/ML systems, infrastructure scalability, cybersecurity, and technical talent assessment.

# YOUR MISSION
Perform rigorous technical validation of this startup's product, technology stack, and technical claims. Your assessment will determine if this company can actually build what they promise and scale it to venture-scale outcomes. This is CRITICAL due diligence - technical failure is the #1 reason promising startups fail.

# STARTUP PROFILE
- **Company Name:** {startup_data.get('name', 'Unknown')}
- **Sector:** {startup_data.get('sector', 'Unknown')}
- **Stage:** {startup_data.get('stage', 'Unknown')}
- **Team:** {startup_data.get('metadata', {}).get('team', 'Not specified')}
- **Traction:** {startup_data.get('metadata', {}).get('traction', 'Not specified')}

**Product Description:**
{product}

**Technical Claims Made:**
{json.dumps(claims, indent=2) if claims else 'No specific technical claims provided'}

# TECHNICAL EVALUATION FRAMEWORK

Assess the startup across these critical dimensions:

## 1. TECHNICAL FEASIBILITY (30% weight)
For each technical claim, evaluate:
- **Is it physically/logically possible?** (e.g., "10x faster" - compared to what baseline?)
- **Is it achievable with current technology?** (or does it require breakthroughs?)
- **Is the timeline realistic?** (6 months to build AGI = red flag)
- **What's the technical complexity?** (0-10 scale: 0=trivial, 10=bleeding-edge research)

**Feasibility Ratings:**
- **Feasible:** Can be built with proven tech, reasonable timeline, clear path
- **Questionable:** Ambitious but possible, requires exceptional execution or luck
- **Unlikely:** Requires breakthroughs, timeline unrealistic, or fundamentally flawed

## 2. ARCHITECTURE & SCALABILITY (25% weight)
Based on product description and sector, assess:
- **Can it scale 10x? 100x?** (What breaks first: database, API, infrastructure?)
- **Tech stack quality:** Modern/proven vs outdated/exotic
- **Cloud-native readiness:** Can they leverage AWS/GCP/Azure effectively?
- **Data architecture:** Can they handle growing data volumes efficiently?
- **Cost scaling:** Will AWS bills grow linearly or exponentially with users?

**Key Questions:**
- If they claim "handles millions of users", what's the actual infrastructure requirement?
- Are they building on solid foundations (microservices, APIs, cloud) or legacy tech?

## 3. TEAM TECHNICAL DEPTH (20% weight)
Evaluate technical team strength:
- **Do founders have relevant technical background?** (PhD in AI for AI startup = strong signal)
- **Have they built/scaled similar systems before?** (ex-Google engineer who built similar = credible)
- **Can they attract top technical talent?** (Strong teams attract strong teams)
- **Is CTO/tech lead clearly identified?** (No clear tech leader = red flag)

**Signals:**
- Strong: "CTO ex-Meta, built recommendation engine for 2B users"
- Weak: "Business founder + hired dev shop"

## 4. COMPETITIVE MOAT & IP (15% weight)
Assess defensibility:
- **Proprietary technology?** (Patents, unique algorithms, trade secrets)
- **Data moat?** (Access to unique datasets, network effects)
- **Technical complexity as barrier?** (So hard to build that competitors can't copy easily)
- **First-mover advantage in technical domain?**

**Questions:**
- Can Google build this in 6 months if they wanted to?
- What stops a well-funded competitor from copying this?

## 5. TECHNICAL RISKS (10% weight)
Identify critical risks:
- **Dependency risks:** Relying on single vendor/API (e.g., 100% dependent on OpenAI API)
- **Regulatory/compliance:** Healthcare data (HIPAA), financial (SOC2), privacy (GDPR)
- **Security vulnerabilities:** Handling sensitive data, potential for breaches
- **Technical debt:** Shortcuts taken that will haunt them later
- **Unproven technology:** Betting on tech that doesn't exist yet

# CLAIM VALIDATION METHODOLOGY

For each technical claim, provide:

1. **Verdict:** Feasible | Questionable | Unlikely
2. **Reasoning:** Why you assigned this verdict (2-3 sentences)
3. **Evidence/Benchmark:** Compare to industry standards
   - Example: "Claim: 10x faster. Benchmark: Current solutions take 10s, theirs would need <1s. Achievable with GPU optimization + better algorithms."
4. **Risk Assessment:** What could go wrong with this specific claim?

# SCORING CALIBRATION

**Technical Score (0.0 - 1.0):**

**0.9-1.0 (Excellent):**
- All claims are feasible with proven technology
- Strong technical team with directly relevant experience
- Clear scalability path, modern architecture
- Defensible technical moat (patents, data, complexity)
- Example: Ex-DeepMind founders building AI platform, peer-reviewed research, working prototype at scale

**0.7-0.8 (Strong):**
- Most claims feasible, 1-2 ambitious but achievable
- Solid technical team, some relevant experience
- Scalable architecture, minor concerns
- Some competitive advantages
- Example: Strong engineers from good companies, working MVP, clear tech roadmap

**0.5-0.6 (Moderate):**
- Claims are ambitious, execution risk high
- Team has gaps (missing CTO or key technical roles)
- Architecture concerns, unclear scalability
- Weak technical moat
- Example: First-time founders with hired developers, early prototype, unproven technology choices

**0.3-0.4 (Weak):**
- Multiple questionable/unlikely claims
- Weak technical team
- Architecture red flags
- No defensibility
- Example: Non-technical founders, outsourced development, unrealistic promises

**0.0-0.2 (Critical Issues):**
- Claims are impossible or fraudulent
- No credible technical team
- Fundamental technical flaws
- Example: "Solved quantum computing" by non-physicist, no working product

# CRITICAL THINKING CHECKLIST

Before finalizing assessment:
1. **Bullshit Detector:** Are they using buzzwords to hide lack of substance? (e.g., "AI-powered" for simple if-then rules)
2. **Comparison Check:** How does this compare to what Google/Meta/OpenAI are doing?
3. **Timeline Reality:** Could YOUR best engineering team build this in their stated timeline?
4. **Hidden Complexity:** What are they NOT mentioning? (Data labeling, infrastructure costs, edge cases)
5. **Team-Tech Mismatch:** Does team's background match the technical challenges? (ML startup with no ML engineers = problem)

# OUTPUT FORMAT

Return ONLY valid JSON (no markdown, no preamble):
{{
  "overall_assessment": "strong",
  "claims_validated": [
    {{
      "claim": "Original claim text",
      "verdict": "feasible",
      "reasoning": "Detailed 2-3 sentence explanation of why this is feasible, with technical specifics",
      "evidence": "Industry benchmark or comparison (e.g., 'Similar to what Stripe achieved in 2015')",
      "risk_level": "low|medium|high"
    }}
  ],
  "technical_risks": ["Specific risk 1 with impact assessment", "Specific risk 2 with mitigation suggestion"],
  "technical_score": 0.78,
  "key_strengths": ["Specific strength 1", "Specific strength 2"],
  "key_weaknesses": ["Specific weakness 1", "Specific weakness 2"],
  "scalability_assessment": "Can scale to X users before major re-architecture needed",
  "team_depth_rating": "strong|moderate|weak",
  "competitive_moat": "Description of defensibility or lack thereof"
}}

**Example Output:**
{{
  "overall_assessment": "strong",
  "claims_validated": [
    {{
      "claim": "Reduces document processing time by 80% using AI",
      "verdict": "feasible",
      "reasoning": "OCR + NLP pipelines can achieve 80%+ efficiency gains for structured documents. Proven by DocuSign, Adobe Sign. Requires quality training data and good NLP models (BERT/GPT-based).",
      "evidence": "Industry standard: Manual processing = 30min/doc, AI-assisted = 5-6min/doc (80-85% reduction)",
      "risk_level": "low"
    }},
    {{
      "claim": "Handles 10M concurrent users",
      "verdict": "questionable",
      "reasoning": "At Seed stage with limited infrastructure budget, supporting 10M concurrent users would cost $100K+/month in AWS fees alone. Technically feasible with proper architecture but financially unrealistic at current stage.",
      "evidence": "Twitter handles ~500K concurrent at scale with massive infrastructure. 10M is YouTube-level scale.",
      "risk_level": "high"
    }}
  ],
  "technical_risks": ["Heavy dependency on OpenAI API - if pricing changes or API becomes unavailable, product breaks", "No mentioned data security strategy for handling sensitive documents (HIPAA/GDPR compliance risk)"],
  "technical_score": 0.72,
  "key_strengths": ["Proven tech stack (Python + React + AWS)", "Clear technical roadmap", "Founder has ML PhD from Stanford"],
  "key_weaknesses": ["No senior infrastructure engineer on team", "Unclear how they'll handle data privacy at scale", "Single point of failure in API dependency"],
  "scalability_assessment": "Can scale to 100K users with current architecture. Need re-architecture (microservices, caching layer) at 500K+ users.",
  "team_depth_rating": "moderate",
  "competitive_moat": "Weak - technology is replicable by well-funded competitors. Moat will come from data/network effects, not tech itself."
}}

Be technically rigorous. Call out BS. Assess like you're investing your own money."""

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
