from django.urls import path
from .views import analyze_symptoms

urlpatterns = [
    path("analyze/", analyze_symptoms),
]