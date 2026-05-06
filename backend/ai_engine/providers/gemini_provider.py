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
        # Using gemini-1.5-flash for faster response and cost-efficiency
        model = genai.GenerativeModel('gemini-1.5-flash')

        symptoms = data.get("symptoms", [])
        severity = data.get("severity", "unknown")
        duration = data.get("duration", "unknown")
        notes = data.get("notes", "")

        # Structured Prompt
        prompt = f"""
        Role: You are a highly accurate medical triage AI assistant.
        Task: Analyze the following patient symptoms and provide preliminary information.
        
        Patient Input:
        - Symptoms: {', '.join(symptoms) if isinstance(symptoms, list) else symptoms}
        - Severity (1-10): {severity}
        - Duration: {duration} days
        - Patient Notes: {notes}

        Constraints & Safety Rules:
        1. STRICTLY NO DIAGNOSIS. Use phrases like "Possible conditions to discuss with a doctor".
        2. NO MEDICATION RECOMMENDATIONS. Do not suggest drugs or dosages.
        3. ADVICE: Focus on self-care (rest, hydration) and when to seek professional help.
        4. RISK ASSESSMENT: 
           - 'low': Minor symptoms, can wait.
           - 'medium': Persistent or uncomfortable symptoms, see a doctor soon.
           - 'high': Severe symptoms, potential emergency, seek immediate care.
        5. DOCTOR RECOMMENDATION: Boolean based on the risk level.

        Output Format:
        You must return a valid JSON object only. Do not include markdown formatting or any other text.
        Structure:
        {{
          "possible_conditions": ["Condition A", "Condition B", "Condition C"],
          "risk_level": "low" | "medium" | "high",
          "advice": ["Step 1", "Step 2", "Step 3"],
          "doctor_recommendation": true | false,
          "disclaimer": "This is not medical advice. Consult a healthcare professional for diagnosis and treatment."
        }}
        """

        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        # Robust JSON cleaning (Gemini often wraps in code blocks)
        clean_text = raw_text
        if "```json" in raw_text:
            clean_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            clean_text = raw_text.split("```")[1].split("```")[0].strip()

        # Parse JSON
        result = json.loads(clean_text)

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
