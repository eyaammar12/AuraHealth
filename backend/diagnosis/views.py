from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai

@api_view(['POST'])
def analyze_symptoms(request):
    symptoms = request.data.get("symptoms")

    prompt = f"""
    Tu es un assistant médical éducatif.
    Un utilisateur décrit ces symptômes : {symptoms}

    1. Donne 3 hypothèses possibles (sans diagnostic certain)
    2. Donne des conseils généraux
    3. Ajoute un avertissement de consulter un médecin
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return Response({
        "result": response["choices"][0]["message"]["content"]
    })