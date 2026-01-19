from django.urls import path
from . import views

app_name = "lancamentos"

urlpatterns = [
    path("", views.lista_lancamentos, name="lista"),
    path("<int:id>/editar/", views.editar_lancamento, name="editar"),
    path("<int:id>/excluir/", views.excluir_lancamento, name="excluir"),
]
