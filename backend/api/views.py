from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnalyzeInputSerializer
from ai_engine.services.ai_service import AIService
from triage.services import TriageService

class AnalyzeAPIView(APIView):
    """
    Endpoint for symptom analysis and pre-diagnosis.
    POST /api/analyze/
    """
    
    def post(self, request):
        serializer = AnalyzeInputSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            # 1. Triage Check (Rule-based)
            triage_score = TriageService.calculate_risk_score(
                data['symptoms'], 
                data['severity']
            )
            
            # 2. AI Analysis
            ai_service = AIService()
            analysis_result = ai_service.get_analysis(
                symptoms=data['symptoms'],
                severity=data['severity'],
                duration=data['duration'],
                notes=data.get('notes', '')
            )
            
            # Force high risk if triage flagged it
            if triage_score == "high":
                analysis_result["risk_level"] = "high"
                analysis_result["doctor_recommendation"] = True

            return Response(analysis_result, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
