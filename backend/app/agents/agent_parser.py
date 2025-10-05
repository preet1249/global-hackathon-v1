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
            prompt = f"""# ROLE & EXPERTISE
You are a Senior Data Extraction Specialist with 10+ years of experience analyzing startup pitch decks at top VC firms like Sequoia Capital, Andreessen Horowitz, and Y Combinator. You've processed 50,000+ pitch decks and have expert-level pattern recognition for extracting structured startup data from unstructured documents.

# YOUR MISSION
Extract complete, accurate, and structured information from this startup pitch deck. This data will be used for AI-powered investment analysis, so accuracy is CRITICAL. Every field you extract directly impacts investment decisions.

# CONTEXT
- This is raw text extracted from a PDF pitch deck
- Quality varies: some decks are professional, others are scrappy
- Information may be scattered across different sections
- Some information might be implied rather than stated explicitly
- Be thorough but conservative - if uncertain, return null rather than guessing

# EXTRACTION GUIDELINES

**Company Name:**
- Look for company/brand name on first pages, headers, or "About Us" sections
- Exclude taglines or product names

**Sector/Industry:**
- Categorize into standard VC sectors: AI/ML, FinTech, HealthTech, EdTech, SaaS, E-commerce, CleanTech, Web3, DeepTech, Enterprise, Consumer, etc.
- If multiple sectors, choose the PRIMARY one
- Be specific (e.g., "AI-powered HealthTech" not just "Technology")

**Funding Stage:**
- Look for explicit mentions: Pre-seed, Seed, Series A/B/C, Growth, etc.
- Infer from context: if raising first $500k = likely Seed, if $5M+ with existing investors = likely Series A+
- If truly unclear, return null

**Geography:**
- Primary market or headquarters location
- Format: "City, Country" or "Country" or "Region" (e.g., "San Francisco, USA", "Singapore", "Southeast Asia")

**Ticket Size (Funding Ask):**
- Extract REQUESTED amount, not current valuation
- Return numbers only (in thousands): $500K = 500, $2M = 2000
- If range stated (e.g., "$1M-$3M"), extract both min and max
- If single number (e.g., "$2M"), set both min and max to same value
- If "$2M+" stated, set min=2000, max=null

**Summary:**
- 2-3 sentences capturing: What they do + Who they serve + Key value proposition
- Focus on BUSINESS, not buzzwords
- Good example: "AI-powered legal document automation platform for mid-size law firms. Reduces contract review time by 80% using NLP. Currently serving 50+ firms with $500K ARR."

**Team:**
- Extract key founders/executives with roles
- Format: ["John Doe (CEO, ex-Google)", "Jane Smith (CTO, PhD MIT)"]
- Include notable previous experience if mentioned
- If no team info, return empty array []

**Traction:**
- Extract CONCRETE metrics: revenue, users, growth rate, partnerships
- Avoid vague statements like "strong growth"
- Good examples: "$500K ARR", "10K users, 25% MoM growth", "Partnerships with Microsoft, AWS"
- If pre-launch/no traction, state: "Pre-revenue" or "In development"

**Product:**
- What does the product/service actually DO?
- 1-2 sentences, focus on functionality not marketing
- Good example: "Mobile app that uses AI to analyze food photos and provide personalized nutrition recommendations"

**Claims:**
- Extract KEY value propositions and claims made
- Focus on quantifiable claims: "80% cost reduction", "10x faster than competitors"
- Include market size claims if stated: "Targeting $50B market"
- Return as array of strings

# QUALITY CHECKS
Before responding, verify:
✓ Company name is clearly identified (not a tagline)
✓ Sector is a standard VC category
✓ Ticket size numbers are reasonable for stated stage
✓ Summary is factual and concise
✓ No placeholder or example data from instructions leaked into output

# INPUT DATA
Pitch Deck Text (first 8000 characters):
{pdf_text[:8000]}

# OUTPUT FORMAT
Return ONLY valid JSON (no markdown blocks, no explanations, just pure JSON):
{{
  "name": "Company Name",
  "sector": "AI/ML",
  "stage": "Seed",
  "geography": "San Francisco, USA",
  "ticket_size_min": 1000,
  "ticket_size_max": 2000,
  "summary": "Clear 2-3 sentence business description with value prop and traction.",
  "team": ["Founder Name (Role, Background)"],
  "traction": "Specific metrics: $X revenue, Y users, Z% growth",
  "product": "What the product does in 1-2 sentences",
  "claims": ["Quantifiable claim 1", "Market claim 2", "Value prop 3"]
}}

If any field is not found in the text, use null (for numbers/strings) or [] (for arrays). Do not guess or fabricate information."""

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
