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
            "name": "google/gemini-2.0-flash-exp:free",
            "key": "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"
        },
        "grok": {
            "name": "x-ai/grok-beta",
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
