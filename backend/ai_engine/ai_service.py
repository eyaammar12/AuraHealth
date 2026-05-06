from .providers import OpenAIProvider
from .prompts import PromptBuilder

class AIEngine:
    def __init__(self, provider=None):
        # Default to OpenAIProvider if no specific provider is passed
        self.provider = provider or OpenAIProvider()

    def analyze_symptoms(self, data: dict, triage_risk: str) -> dict:
        """
        Orchestrates the AI generation process.
        """
        symptoms = data.get("symptoms", [])
        severity = data.get("severity", 5)
        duration = data.get("duration", 1)
        notes = data.get("notes", "")

        # 1. Build the strict prompt
        prompt = PromptBuilder.build_symptom_analysis_prompt(
            symptoms=symptoms,
            severity=severity,
            duration=duration,
            notes=notes,
            triage_risk=triage_risk
        )

        # 2. Call the provider
        result = self.provider.generate_json_response(prompt)
        
        # 3. Apply post-validation or safety overwrites if necessary
        # Ensure disclaimer is present regardless of AI output
        result["disclaimer"] = "This is not medical advice. Consult a healthcare professional for diagnosis and treatment."
        
        # Ensure risk level respects triage high risk
        if triage_risk == "high":
            result["risk_level"] = "high"
            result["doctor_recommendation"] = True

        return result
