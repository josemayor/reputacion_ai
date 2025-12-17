"""
Vistas para la gestión de páginas, análisis de reputación y la generación
de los reportes.
"""
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import TemplateView, View

from .services import ReputationAnalysisService



class HomeView(TemplateView):
    """
    Renderiza la página de inicio de la aplicación.
    
    Hereda de TemplateView para servir un archivo HTML estático.
    """
    template_name = "pages/home.html"


class AnalyzeView(View):
    """
    Gestiona el análisis de reputación de una entidad (empresa o persona).
    """
    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud POST para realizar el análisis de reputación.

        Recibe una consulta ('query') del formulario, utiliza el servicio de
        análisis para obtener métricas de sentimiento, y renderiza la plantilla
        de resultados con los datos obtenidos.

        Args:
            request: La solicitud HTTP.

        Returns:
            HttpResponse: La plantilla 'pages/results.html' renderizada con los
            datos del análisis.
        """
        query = request.POST.get("query")

        service = ReputationAnalysisService()
        data = service.analyze_reputation(query)

        return render(request, "pages/results.html", {"data": data, "query": query})


class GeneratePDFView(View):
    """
    Gestiona la generación y descarga de informes en formato PDF.
    """
    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud POST para generar un informe PDF detallado.

        Recibe una consulta ('query'), solicita datos estructurados al servicio
        de análisis, renderiza una plantilla HTML específica para PDF y la
        convierte a un archivo PDF descargable.

        Args:
            request: La solicitud HTTP.

        Returns:
            HttpResponse: Un archivo PDF adjunto o un mensaje de error si la
            generación falla.
        """
        query = request.POST.get("query")

        service = ReputationAnalysisService()

        try:
            report_data = service.generate_report_data(query)
        except Exception as e:
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
