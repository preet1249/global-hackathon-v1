import httpx
import os
import logging
from typing import Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class OpenRouterClient:
    """Client for calling OpenRouter API with different models"""

    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Model configurations from prompt.md
    MODELS = {
        "qwen": {
            "name": "qwen/qwen-2.5-72b-instruct",
            "key": "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"
        },
        "gpt5": {
            "name": "openai/gpt-4o-mini",  # Using gpt-4o-mini as gpt-5-mini might not be available
            "key": "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"
        },
        "deepseek": {
            "name": "deepseek/deepseek-chat",
            "key": "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"
        },
        "gemini": {
            "name": "google/gemini-2.0-flash-thinking-exp:free",
            "key": "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"
        },
        "grok": {
            "name": "x-ai/grok-2-1212",
            "key": "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"
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
        api_key = model_config["key"]

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
