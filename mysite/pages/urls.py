# load a view when the user visits the root URL
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
