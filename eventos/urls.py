from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.registrar_evento, name="registrar_evento"),
    path("registrar/", views.registrar_evento, name="registrar_evento_alt"),
]