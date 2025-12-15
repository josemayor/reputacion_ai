import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template.loader import get_template
from xhtml2pdf import pisa

from openai import OpenAI

MODEL_LLM = "openai/gpt-oss-120b"


# Create your views here.
def home(request):
    """ Inicia la pagina principal """
    return render(request, "pages/home.html")


# Análisis de reputación
def analyze(request):
    """ Recibe el nombre de la empresa o persona. A continuación lo analiza """
    query = request.POST.get("query")
    global MODEL_LLM

    # limitación del tamaño de la cadena, a 50 caracteres
    if len(query) > 50:
        query = query[:50]

    # Limpieza del texto, para eliminar caracteres especiales
    query = query.replace("_", " ")
    query = query.replace("-", " ")

    # A la cadena de query le agregamos el prompt
    prompt_template = """
Eres un experto en análisis de reputación online y monitoreo de marca. Tu regla más importante es no inventar NUNCA
información. Si no estás absolutamente seguro de una respuesta, debes indicarlo claramente y abstenerte de especular
o proporcionar detalles que no puedas verificar en tus datos de entrenamiento. Analiza la reputación online
actual de {query} basándote en información pública disponible en internet, redes sociales (especialmente X/Twitter,
LinkedIn, Facebook, Instagram), foros (como Reddit), noticias recientes, reseñas en sitios como Google Reviews,
Trustpilot o similares, y cualquier mención relevante.
Devuelve ÚNICAMENTE tu respuesta en el siguiente formato JSON estricto, sin texto adicional antes o después:

{{
  "sentimiento_general": "positivo" | "neutro" | "negativo",
  "puntuacion_salud_marca": número entre 0 y 10 (donde 0 es reputación extremadamente dañada y 10 es excelente),
  "resumen_ejecutivo": "Breve resumen de 2-3 líneas máximo que describa el estado actual de la reputación online de {query}.
   Debe ser objetivo, conciso y destacar los aspectos más relevantes (positivos, negativos o mixtos)."
}}

Reglas importantes:
- El sentimiento_general debe ser solo una de estas tres opciones: "positivo", "neutro" o "negativo".
- La puntuación debe ser un número entero o decimal (ej: 7.5).
- El resumen_ejecutivo debe tener máximo 3 líneas (aprox. 100-150 palabras) y ser profesional.
- Considera solo información reciente (últimos 12-24 meses prioritariamente) y fuentes públicas confiables.
- Si la información es escasa o contradictoria, refleja eso en la puntuación y resumen.
"""

    groq_api_key = os.environ.get("GROQ_API_KEY")

    client = OpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    prompt_final = prompt_template.format(query=query)

    try:
        completion = client.chat.completions.create(
            model=MODEL_LLM,
            messages=[{"role": "user", "content": prompt_final}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        content = completion.choices[0].message.content

    except Exception as e:
        print(f"Error Groq: {e}")
        content = f"Error al conectar con Groq: {e}"

    data = json.loads(content)

    return render(request, "pages/results.html", {"data": data, "query": query})


def generate_pdf(request):
    if request.method == "POST":
        query = request.POST.get("query")
        global MODEL_LLM
        
        # Prompt más detallado para el informe PDF
        prompt_template = """
        Eres un experto analista de reputación corporativa. Tu regla más importante es no inventar NUNCA información. Si no
        estás absolutamente seguro de una respuesta, debes indicarlo claramente y abstenerte de especular o proporcionar
        detalles que no puedas verificar en tus datos de entrenamiento. Genera un informe detallado y profesional sobre
        la reputación online de {query}.
        El informe debe estar estructurado en HTML para ser convertido a PDF.
        
        Estructura esperada del JSON (MANTÉN ESTRICTAMENTE ESTE FORMATO):
        {{
            "titulo": "Informe de Reputación Online: {query}",
            "fecha": "La fecha de hoy",
            "informacion_general": "Información general sobre {query} ¿quien es? ¿qué hace? ¿donde está ubicado?",
            "resumen_ejecutivo": "Un resumen ejecutivo detallado de 4-5 párrafos.",
            "analisis_sentimiento": {{
                "positivo_pct": int (0-100),
                "negativo_pct": int (0-100),
                "neutro_pct": int (0-100),
                "explicacion": "Explicación detallada del desglose de sentimiento."
            }},
            "fuentes_principales": [
                "Fuente 1 (ej: Twitter) - Resumen de hallazgos",
                "Fuente 2 (ej: Noticias) - Resumen de hallazgos",
                "Fuente 3 (ej: Foros) - Resumen de hallazgos"
            ],
            "puntos_criticos": [
                "Punto crítico 1 (positivo o negativo)",
                "Punto crítico 2",
                "Punto crítico 3"
            ],
            "recomendaciones": [
                "Recomendación estratégica 1. Desarrolla con explicaciones y consejos detallados para ayudar a mejorar la reputación online de {query}",
                "Recomendación estratégica 2. Desarrolla con explicaciones y consejos detallados para ayudar a mejorar la reputación online de {query}",
                "Recomendación estratégica 3. Desarrolla con explicaciones y consejos detallados para ayudar a mejorar la reputación online de {query}"
            ]
        }}
        """

        groq_api_key = os.environ.get("GROQ_API_KEY")
        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        prompt_final = prompt_template.format(query=query)
        
        try:
            completion = client.chat.completions.create(
                model=MODEL_LLM,
                messages=[{"role": "user", "content": prompt_final}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            content = completion.choices[0].message.content
            report_data = json.loads(content)
        except Exception as e:
            print(f"Error generando reporte PDF: {e}")
            return HttpResponse(f"Error generando reporte: {e}", status=500)

        # Renderizar el template HTML con los datos
        template_path = 'pages/pdf_template.html'
        context = {'report': report_data}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{query}.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)
        
        # Crear PDF
        pisa_status = pisa.CreatePDF(
           html, dest=response
        )
        
        if pisa_status.err:
           return HttpResponse('Hubo errores al generar el PDF <pre>' + html + '</pre>')
            
        return response
    
    return HttpResponse("Método no permitido", status=405)
