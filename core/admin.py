from django.contrib import admin
from .models import Categoria, Lancamento

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'user')


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'valor', 'data', 'categoria', 'user')
    list_filter = ('tipo', 'data')
