""" Load a view when the user visits the root URL """
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze", views.analyze, name="analyze"),
    path("generate-pdf", views.generate_pdf, name="generate_pdf"),
]
