from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:id>/excluir/', views.excluir_categoria, name='excluir_categoria'),

    # Lançamentos
    path('lancamento/<int:id>/editar/', views.editar_lancamento, name='editar_lancamento'),
    path('lancamento/<int:id>/excluir/', views.excluir_lancamento, name='excluir_lancamento'),
    path('lancamentos/', views.lista_lancamentos, name='lista_lancamentos'),

    path('relatorios/', views.relatorio_mensal, name='relatorio_mensal'),
    ]
