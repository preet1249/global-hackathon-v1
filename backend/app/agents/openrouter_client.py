import httpx
import os
import logging
from typing import Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class OpenRouterClient:
    """Client for calling OpenRouter API with different models"""

    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Model configurations - API key from environment variable
    MODELS = {
        "qwen": {
            "name": "qwen/qwen3-30b-a3b-instruct-2507"
        },
        "gpt5": {
            "name": "openai/gpt-4o-mini"
        },
        "deepseek": {
            "name": "deepseek/deepseek-chat-v3.1"
        },
        "gemini": {
            "name": "google/gemini-2.5-flash-lite-preview-09-2025"
        },
        "grok": {
            "name": "x-ai/grok-4-fast"
        }
    }

    @staticmethod
    async def call_model(
        model_key: str,
        messages: list,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        timeout: int = 90
    ) -> Dict[str, Any]:
        """
        Call OpenRouter API with specific model

        Args:
            model_key: Key from MODELS dict (qwen, gpt5, deepseek, gemini, grok)
            messages: List of message dicts [{"role": "user", "content": "..."}]
            max_tokens: Max response tokens
            temperature: Sampling temperature
            timeout: Request timeout in seconds

        Returns:
            Dict with response or error
        """
        if model_key not in OpenRouterClient.MODELS:
            return {
                "success": False,
                "error": f"Unknown model key: {model_key}"
            }

        model_config = OpenRouterClient.MODELS[model_key]
        model_name = model_config["name"]
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            return {
                "success": False,
                "error": "OPENROUTER_API_KEY environment variable not set"
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    OpenRouterClient.OPENROUTER_API_URL,
                    headers=headers,
                    json=payload
                )

                if response.status_code != 200:
                    logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"API returned {response.status_code}: {response.text}",
                        "model": model_name
                    }

                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

                return {
                    "success": True,
                    "content": content,
                    "model": model_name,
                    "usage": result.get("usage", {})
                }

        except asyncio.TimeoutError:
            logger.error(f"Timeout calling {model_name}")
            return {
                "success": False,
                "error": f"Request timeout after {timeout}s",
                "model": model_name
            }
        except Exception as e:
            logger.error(f"Error calling {model_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "model": model_name
            }
