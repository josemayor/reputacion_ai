"""
Configuración de URLs para la aplicación de páginas.
"""
from django.urls import path
from .views import HomeView, AnalyzeView, GeneratePDFView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("analyze", AnalyzeView.as_view(), name="analyze"),
    path("generate-pdf", GeneratePDFView.as_view(), name="generate_pdf"),
]
