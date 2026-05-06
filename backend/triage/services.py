class TriageService:
    """
    Service for initial rule-based risk assessment.
    Runs before or in parallel with AI analysis to flag critical issues.
    """
    
    CRITICAL_SYMPTOMS = ["chest pain", "shortness of breath", "severe bleeding", "unconsciousness"]

    @staticmethod
    def calculate_risk_score(symptoms: list, severity: int) -> str:
        """
        Flags high risk based on specific critical symptoms or extreme severity.
        """
        symptoms_lower = [s.lower() for s in symptoms]
        
        # Immediate high risk for critical symptoms
        for critical in TriageService.CRITICAL_SYMPTOMS:
            if critical in symptoms_lower:
                return "high"
                
        # High risk for extreme severity
        if severity > 8:
            return "high"
            
        return "normal"
