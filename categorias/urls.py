from django.urls import path
from . import views

app_name = "categorias"

urlpatterns = [
    path("", views.lista_categorias, name="lista"),
    path("criar/", views.criar_categoria, name="criar"),
    path("<int:id>/editar/", views.editar_categoria, name="editar"),
    path("<int:id>/excluir/", views.excluir_categoria, name="excluir"),
]
