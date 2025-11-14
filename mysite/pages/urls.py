# load a view when the user visits the root URL
from django.urls import path
from . import views
from .views import DesignPageView, RunPageView, DebugPageView

urlpatterns = [
    path("", views.home, name="home"),
    path("design/", DesignPageView.as_view(), name="design"),
    path("run/", RunPageView.as_view(), name="run"),
    path("debug/", DebugPageView.as_view(), name="debug"),
]
