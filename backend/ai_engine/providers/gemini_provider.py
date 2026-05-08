import os
import json
import logging
import google.generativeai as genai
from .base_provider import BaseAIProvider

# Set up logging
logger = logging.getLogger(__name__)

def analyze_with_gemini(data: dict) -> dict:
    """
    Perform medical symptom analysis using Google Gemini AI.
    Returns a strict JSON response.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is not set.")
        return {
            "error": "Gemini API key missing.",
            "disclaimer": "This is not medical advice. Technical error occurred."
        }

    try:
        genai.configure(api_key=api_key)
        # Using gemini-flash-latest as it is confirmed to have quota and work in this environment.
        model = genai.GenerativeModel('gemini-flash-latest')

        symptoms = data.get("symptoms", [])
        severity = data.get("severity", "unknown")
        duration = data.get("duration", "unknown")
        notes = data.get("notes", "")

        # Structured Prompt - Focused on fast JSON generation
        prompt = f"""
        Role: Medical triage assistant.
        Input: Symptoms: {', '.join(symptoms) if isinstance(symptoms, list) else symptoms}, Severity: {severity}/10, Duration: {duration} days, Notes: {notes}
        
        Rules: No diagnosis, no medication.
        Risk levels: 'low', 'medium', 'high'.
        
        Output exact JSON structure:
        {{
          "possible_conditions": ["..."],
          "risk_level": "...",
          "advice": ["..."],
          "doctor_recommendation": boolean,
          "disclaimer": "..."
        }}
        """

        # Optimized call with JSON mode
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        raw_text = response.text.strip()
        
        # Parse JSON
        result = json.loads(raw_text)

        # Schema Validation
        required_keys = ["possible_conditions", "risk_level", "advice", "doctor_recommendation", "disclaimer"]
        for key in required_keys:
            if key not in result:
                logger.warning(f"Gemini response missing key: {key}")
                # Inject default if missing
                if key == "possible_conditions": result[key] = ["Non-specific symptoms"]
                if key == "risk_level": result[key] = "medium"
                if key == "advice": result[key] = ["Monitor symptoms", "Consult a professional if symptoms worsen"]
                if key == "doctor_recommendation": result[key] = True
                if key == "disclaimer": result[key] = "This is not medical advice."

        # Cap possible_conditions to max 3
        if isinstance(result.get("possible_conditions"), list):
            result["possible_conditions"] = result["possible_conditions"][:3]

        return result

    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error from Gemini: {e}. Raw text: {raw_text if 'raw_text' in locals() else 'N/A'}")
        return get_fallback_response("Invalid response format from AI.")
    except Exception as e:
        logger.error(f"Error in Gemini Provider: {str(e)}")
        return get_fallback_response(f"An unexpected error occurred: {str(e)}")

def get_fallback_response(error_msg: str) -> dict:
    """Returns a safe fallback response in case of errors."""
    return {
        "possible_conditions": ["Analysis unavailable"],
        "risk_level": "medium",
        "advice": [
            "We were unable to process your request at this moment.",
            "Please monitor your symptoms closely.",
            "Consult a medical professional if you have concerns."
        ],
        "doctor_recommendation": True,
        "disclaimer": "This is not medical advice. Analysis failed due to technical reasons.",
        "error_context": error_msg
    }

class GeminiProvider(BaseAIProvider):
    """
    Implementation of Google Gemini AI Provider.
    Uses the google-generativeai SDK.
    """
    def analyze(self, symptoms: list, severity: int, duration: int, notes: str = "") -> dict:
        data = {
            "symptoms": symptoms,
            "severity": severity,
            "duration": duration,
            "notes": notes
        }
        return analyze_with_gemini(data)
