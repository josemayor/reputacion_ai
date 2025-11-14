from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


# Create your views here.
def home(request):
    context = {
        "greeting": "Thank you for visiting.",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
        ],
    }
    return render(request, "pages/home.html", context)


class DesignPageView(TemplateView):
    template_name = "pages/design-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["greeting"] = "Thank you for visiting."
        return context


class RunPageView(TemplateView):
    template_name = "pages/run-page.html"


class DebugPageView(TemplateView):
    template_name = "pages/debug-page.html"
