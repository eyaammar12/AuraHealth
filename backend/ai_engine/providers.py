import os
import json
from abc import ABC, abstractmethod
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_json_response(self, prompt: str) -> dict:
        """
        Takes a prompt and returns a strictly parsed JSON dictionary.
        """
        pass

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        # Assumes OPENAI_API_KEY is in environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    def generate_json_response(self, prompt: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a medical pre-diagnosis assistant. You must output ONLY valid JSON without markdown wrapping."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                timeout=15.0  # Timeout handling
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"OpenAI API Error: {str(e)}")
            raise Exception("Failed to communicate with AI provider")
