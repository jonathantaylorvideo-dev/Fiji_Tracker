import json
import time
from datetime import datetime
from typing import Optional
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from core.config import settings
from core.logger import get_logger
from models.voice_payload import VoicePayload

logger = get_logger()

class GeminiVoiceParser:
    """Parses raw audio transcripts into structured VoicePayload objects using the Google GenAI SDK."""

    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            logger.warning("GEMINI_API_KEY is not configured in settings.")
            self.model = None
            return

        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config={"response_mime_type": "application/json"}
            )
            logger.info("GeminiVoiceParser initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.model = None

    def parse_transcript(self, transcript: str, max_retries: int = 3) -> Optional[VoicePayload]:
        """Parses a raw transcript string into a validated VoicePayload with exponential backoff retry logic."""
        if not self.model:
            logger.error("Gemini model is uninitialized. Cannot process transcript.")
            return None

        system_instruction = (
            "You are a specialized infrastructure analysis assistant. Extract structured details "
            "from the provided voice transcript and output ONLY valid JSON matching this schema: "
            '{"asset_type": string, "latitude": float, "longitude": float, "severity": int (1-5), '
            '"description": string, "timestamp": ISO8601 datetime string, "confidence_score": float (0.0-1.0)}.'
        )

        prompt = f"{system_instruction}\n\nTranscript: {transcript}"

        delay = 1.0
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Invoking Gemini API for transcript parsing (Attempt {attempt}/{max_retries})...")
                response = self.model.generate_content(prompt)

                if not response or not response.text:
                    raise ValueError("Received empty response payload from Gemini API.")

                raw_data = json.loads(response.text)

                if isinstance(raw_data.get("timestamp"), str):
                    raw_data["timestamp"] = datetime.fromisoformat(raw_data["timestamp"].replace("Z", "+00:00"))

                payload = VoicePayload(**raw_data)
                logger.info("Successfully parsed and validated voice payload.")
                return payload

            except (GoogleAPIError, Exception) as e:
                logger.warning(f"Gemini API invocation failed on attempt {attempt}: {e}")
                if attempt == max_retries:
                    logger.error("Max retries reached. Failed to parse voice transcript payload.")
                    return None
                time.sleep(delay)
                delay *= 2.0

        return None