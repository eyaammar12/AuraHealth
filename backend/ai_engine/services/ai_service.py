import logging
from ai_engine.providers.gemini_provider import GeminiProvider

# Set up logging
logger = logging.getLogger(__name__)

class AIService:
    """
    Orchestrator for AI Analysis. 
    Uses GeminiProvider for all analyses.
    """
    
    def __init__(self):
        logger.info("Initializing AIService with Gemini provider")
        self.mode = "gemini"
        self.provider = GeminiProvider()

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
