from rest_framework import serializers

class AnalyzeInputSerializer(serializers.Serializer):
    """
    Validates input data for the symptom analysis endpoint.
    """
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=1,
        help_text="A list of symptoms reported by the user."
    )
    severity = serializers.IntegerField(
        min_value=1, 
        max_value=10,
        help_text="Symptom severity on a scale of 1-10."
    )
    duration = serializers.IntegerField(
        min_value=1,
        help_text="Duration of symptoms in days."
    )
    notes = serializers.CharField(
        required=False, 
        allow_blank=True, 
        max_length=1000,
        help_text="Optional additional notes from the user."
    )
