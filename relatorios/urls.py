from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path("", views.relatorio_mensal, name="mensal"),
]
