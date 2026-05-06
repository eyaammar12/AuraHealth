import os
import logging
from ai_engine.providers.mock_provider import MockProvider
from ai_engine.providers.gemini_provider import GeminiProvider

# Set up logging
logger = logging.getLogger(__name__)

class AIService:
    """
    Orchestrator for AI Analysis. 
    Switches between different AI providers based on the AI_MODE environment variable.
    """
    
    def __init__(self, override_mode=None):
        # Use override_mode if provided (from API request), otherwise fallback to env variable
        self.mode = (override_mode or os.getenv("AI_MODE", "mock")).lower()
        logger.info(f"Initializing AIService with mode: {self.mode}")
        
        if self.mode == "gemini":
            self.provider = GeminiProvider()
        else:
            self.provider = MockProvider()

    def get_analysis(self, symptoms: list, severity: int, duration: int, notes: str = "") -> dict:
        """
        Calls the selected provider to get the analysis.
        Includes safety enforcement and error handling at the service level.
        """
        try:
            logger.info(f"Requesting analysis from {self.mode} provider...")
            response = self.provider.analyze(symptoms, severity, duration, notes)
            
            # Post-processing: Ensure the safety disclaimer is always present and strong
            response["disclaimer"] = "This is not medical advice. Consult a healthcare professional for diagnosis and treatment."
            
            return response
            
        except Exception as e:
            logger.error(f"Error in AIService while getting analysis: {str(e)}")
            # Safety fallback
            return {
                "possible_conditions": ["Analysis error"],
                "risk_level": "medium",
                "advice": ["We encountered a technical error. Please consult a doctor if you have symptoms of concern."],
                "doctor_recommendation": True,
                "disclaimer": "This is not medical advice. Service error occurred."
            }
