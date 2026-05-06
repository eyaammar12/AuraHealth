import random
from .base_provider import BaseAIProvider

class MockProvider(BaseAIProvider):
    """
    Mock AI Provider for testing and local development.
    Generates realistic-looking responses without calling an external API.
    """
    
    def analyze(self, symptoms: list, severity: int, duration: int, notes: str = "") -> dict:
        # Determine risk level based on severity
        if severity < 4:
            risk_level = "low"
        elif severity <= 7:
            risk_level = "medium"
        else:
            risk_level = "high"
            
        # Realistic conditions map
        condition_map = {
            "headache": ["Tension Headache", "Migraine", "Dehydration"],
            "fever": ["Common Cold", "Influenza", "Viral Infection"],
            "cough": ["Bronchitis", "Allergies", "Common Cold"],
            "chest pain": ["Muscle Strain", "Acid Reflux", "Angina (Seek Care)"],
            "fatigue": ["Anemia", "Sleep Deprivation", "Viral Syndrome"]
        }
        
        possible_conditions = []
        for s in symptoms:
            s_lower = s.lower()
            if s_lower in condition_map:
                possible_conditions.extend(condition_map[s_lower])
        
        # Unique and limit to 3
        possible_conditions = list(set(possible_conditions))[:3]
        if not possible_conditions:
            possible_conditions = ["General Viral Syndrome", "Non-specific symptoms"]

        return {
            "possible_conditions": possible_conditions,
            "risk_level": risk_level,
            "advice": [
                "Monitor your symptoms closely over the next 24 hours.",
                "Maintain adequate hydration and rest.",
                "Avoid strenuous activity until symptoms improve."
            ],
            "doctor_recommendation": risk_level == "high",
            "disclaimer": "This is not medical advice. Always consult with a qualified healthcare professional."
        }
