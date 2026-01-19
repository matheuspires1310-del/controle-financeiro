from django.contrib.auth.models import User
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Lancamento(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=255, blank=True)
    recorrente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.valor}"
