import pandas as pd
from .models import Lancamento, Categoria

def importar_excel(user, arquivo):
    df = pd.read_excel(arquivo)

    for _, row in df.iterrows():
        categoria, _ = Categoria.objects.get_or_create(
            nome=row['Categoria'],
            user=user
        )

        Lancamento.objects.create(
            user=user,
            tipo=row['Tipo'],
            valor=row['Valor'],
            data=row['Data'],
            categoria=categoria,
            descricao=row.get('Descricao', '')
        )
