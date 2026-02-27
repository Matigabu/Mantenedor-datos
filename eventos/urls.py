from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.registrar_evento, name="registrar_evento"),
    path("registrar/", views.registrar_evento, name="registrar_evento_alt"),
    path("validar-ot-fracttal/", views.validar_ot_fracttal, name="validar_ot_fracttal"),
    path("<int:pk>/seguimiento/", views.ver_seguimiento_fracttal, name="ver_seguimiento_fracttal"),
]