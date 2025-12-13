import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


# Create your views here.
def home(request):
    """ Inicia la pagina principal """
    context = {
        "greeting": "Descubre tu reputación con la IA",
        "options": [
            ">> Input único. Barra de busqueda donde poner _Nombre_de_empresa_ o _Persona_",
            "Multiconsulta. El sistema envía el prompt a 3 modelos seleccionados simultaneamente",
            "Analisis de sentimiento básico: Positiva, Neutra o Negativa",
            "Puntuación de salud de marca (ej 8/10)",
            "Resumen ejecutivo. Usa un modelo pequeño y barato para generar las tres opiones y generar resumen de 2 lineas",
            "-----------",
            "A partir de aquí hay que pagar: Generar informe PDF completo con toda la información del análisis"
        ],
    }
    return render(request, "pages/home.html", context)


# Análisis de reputación
def analyze(request):
    """ Recibe el nombre de la empresa o persona. A continuación lo analiza """
    query = request.POST.get("query")
    api_key = os.environ.get("OPENAI_API_KEY")

    print(api_key)

    return HttpResponse("ok")
