"""
Servicios para la lógica de negocio, incluyendo interacción con LLMs.
"""
import os
import json
from openai import OpenAI


class ReputationAnalysisService:
    """
    Servicio encargado de la lógica de análisis de reputación online.

    Esta clase encapsula la interacción con modelos de lenguaje (LLMs) a través
    de la API de Groq/OpenAI para realizar análisis de sentimiento y generar
    informes detallados.
    """
    def __init__(self):
        self.model_llm = "openai/gpt-oss-120b"
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )


    def analyze_reputation(self, query):
        """
        Realiza un análisis rápido de reputación para una consulta dada.

        Limpia la consulta, construye un prompt optimizado y solicita al LLM un análisis
        en formato JSON estricto.

        Args:
            query (str): El nombre de la empresa, persona o entidad a analizar.

        Returns:
            dict: Un diccionario con el 'sentimiento_general', 'puntuacion_salud_marca'
                  y 'resumen_ejecutivo'. Retorna un diccionario con clave 'error' si falla.
        """
        if len(query) > 50:
            query = query[:50]

        query = query.replace("_", " ").replace("-", " ")

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
        prompt_final = prompt_template.format(query=query)

        try:
            completion = self.client.chat.completions.create(
                model=self.model_llm,
                messages=[{"role": "user", "content": prompt_final}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            content = completion.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error Groq: {e}")
            return {"error": f"Error al conectar con Groq: {e}"}


    def generate_report_data(self, query):
        """
        Genera datos estructurados para un informe PDF exhaustivo.

        Solicita al LLM un análisis profundo que incluye desglose de sentimiento,
        fuentes principales, puntos críticos y recomendaciones estratégicas.
        Los datos retornados están listos para ser renderizados en una plantilla HTML/PDF.

        Args:
            query (str): El nombre de la entidad a analizar.

        Returns:
            dict: Un diccionario complejo con la estructura necesaria para el reporte PDF.
        
        Raises:
            Exception: Si ocurre un error durante la generación o el parseo de datos.
        """
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
        prompt_final = prompt_template.format(query=query)

        try:
            completion = self.client.chat.completions.create(
                model=self.model_llm,
                messages=[{"role": "user", "content": prompt_final}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            content = completion.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error generando reporte PDF: {e}")
            raise e
