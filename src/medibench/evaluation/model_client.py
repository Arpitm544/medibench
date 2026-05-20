import logging
import random
import time
from typing import Any

import httpx

from medibench.config import settings

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an expert healthcare data scientist and clinical informatics analyst evaluating the Diabetes 130-US Hospitals (1999-2008) dataset (101,766 hospital encounters).
Provide accurate, precise, and evidence-grounded answers based strictly on the encounter data and epidemiological principles.
Keep numerical answers concise. For categorical queries, give the exact entity name. For operational trade-offs, address confounding and cost-effectiveness."""


class ModelClient:
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        api_key: str | None = None,
        base_url: str | None = None,
        mock_mode: bool = False,
        mock_accuracy: float = 0.85,
    ):
        self.model_name = model_name
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url or settings.OPENAI_BASE_URL
        self.mock_mode = mock_mode or (self.api_key == "mock-key")
        self.mock_accuracy = mock_accuracy

    def query(self, question_text: str, context: str | None = None, expected_ground_truth: str | None = None) -> dict[str, Any]:
        """
        Sends query to the AI model without revealing ground truth.
        """
        start_time = time.time()

        if self.mock_mode:
            # High-fidelity mock model for automated CI and offline evaluations
            time.sleep(random.uniform(0.01, 0.05))  # simulate API latency
            latency_ms = round((time.time() - start_time) * 1000, 2)

            is_correct = random.random() < self.mock_accuracy
            if is_correct and expected_ground_truth is not None:
                # Return the ground truth format with natural language framing
                response_text = f"Based on the hospital encounter analysis, the answer is: {expected_ground_truth}"
            else:
                # Plausible perturbation or generic statement
                response_text = "Based on preliminary dataset screening, the value appears indeterminate or deviated from target."

            return {
                "response": response_text,
                "latency_ms": latency_ms,
                "tokens_used": len(question_text.split()) + len(response_text.split()) + 40,
                "model": self.model_name,
            }

        # Real OpenAI-compatible HTTP call
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question_text},
            ],
            "temperature": 0.0,
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                res = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()
                response_text = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                tokens_used = usage.get("total_tokens", 0)

            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "response": response_text,
                "latency_ms": latency_ms,
                "tokens_used": tokens_used,
                "model": self.model_name,
            }
        except Exception as e:
            logger.warning(f"Live API call failed: {e}. Falling back to mock evaluation response.")
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "response": f"API_ERROR: {e!s}",
                "latency_ms": latency_ms,
                "tokens_used": 0,
                "model": self.model_name,
            }
