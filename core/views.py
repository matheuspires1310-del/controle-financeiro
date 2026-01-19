from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from decimal import Decimal
from .models import Lancamento
from .forms import LancamentoForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Categoria
from django.http import JsonResponse

@login_required
def dashboard(request):

    # --------------------
    # FORMULÁRIO
    # --------------------
    if request.method == 'POST':
        form = LancamentoForm(request.POST)
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.user = request.user
            lancamento.save()
            return redirect('/?sucesso=1')
    else:
        form = LancamentoForm()

    sucesso = request.GET.get('sucesso')

    # --------------------
    # DATA
    # --------------------
    hoje = date.today()
    mes = hoje.month
    ano = hoje.year

    # --------------------
    # TOTAIS
    # --------------------
    entradas = (
        Lancamento.objects.filter(
            user=request.user,
            tipo='E',
            data__month=mes,
            data__year=ano
        ).aggregate(total=Sum('valor'))['total']
        or Decimal(0)
    )

    saidas = (
        Lancamento.objects.filter(
            user=request.user,
            tipo='S',
            data__month=mes,
            data__year=ano
        ).aggregate(total=Sum('valor'))['total']
        or Decimal(0)
    )

    saldo = entradas - saidas

    # --------------------
    # DIAGNÓSTICO
    # --------------------
    diagnostico = []
    percentual_gastos = Decimal(0)

    if entradas > 0:
        percentual_gastos = (saidas / entradas) * Decimal(100)

        if percentual_gastos >= 70:
            diagnostico.append({
                'tipo': 'danger',
                'mensagem': f'Seus gastos representam {percentual_gastos:.0f}% da renda. Risco alto.'
            })
        elif percentual_gastos >= 50:
            diagnostico.append({
                'tipo': 'warning',
                'mensagem': f'Seus gastos representam {percentual_gastos:.0f}% da renda. Atenção.'
            })
        else:
            diagnostico.append({
                'tipo': 'success',
                'mensagem': f'Seus gastos representam {percentual_gastos:.0f}% da renda. Boa saúde financeira.'
            })

    # --------------------
    # CATEGORIAS
    # --------------------
    categorias = list(
        Lancamento.objects.filter(user=request.user, tipo='S')
        .values('categoria__nome')
        .annotate(total=Sum('valor'))
    )

    # --------------------
    # PERSONALIDADE
    # --------------------
    personalidade = None
    descricao_personalidade = None

    qtd_saidas = Lancamento.objects.filter(
        user=request.user,
        tipo='S',
        data__month=mes,
        data__year=ano
    ).count()

    p = float(percentual_gastos)

    if p >= 80:
        personalidade = "Sobrevivência"
        descricao_personalidade = "Seus gastos consomem quase toda a renda."
    elif p >= 60 and qtd_saidas >= 10:
        personalidade = "Impulsivo Controlado"
        descricao_personalidade = "Você gasta com frequência, mas ainda se controla."
    elif p >= 40:
        personalidade = "Equilibrado"
        descricao_personalidade = "Você mantém bom equilíbrio financeiro."
    elif p < 40 and saldo > 0:
        personalidade = "Planejador"
        descricao_personalidade = "Você planeja bem e prioriza o futuro."
    else:
        personalidade = "Conservador"
        descricao_personalidade = "Você evita riscos financeiros."

    # --------------------
    # GASTOS INVISÍVEIS
    # --------------------
    LIMITE_INVISIVEL = Decimal(30)

    gastos_invisiveis = (
        Lancamento.objects.filter(
            user=request.user,
            tipo='S',
            valor__lte=LIMITE_INVISIVEL,
            data__month=mes,
            data__year=ano
        ).aggregate(total=Sum('valor'))['total']
        or Decimal(0)
    )

    percentual_invisivel = (
        (gastos_invisiveis / saidas) * Decimal(100)
        if saidas > 0 else Decimal(0)
    )

    tem_gastos_invisiveis = gastos_invisiveis > 0

    # --------------------
    # SIMULAÇÃO + IMPACTO ANUAL
    # --------------------
    simulacao = None
    impacto_anual = None

    if categorias:
        maior = max(categorias, key=lambda x: x['total'])

        valor_categoria = maior['total']
        percentual_reducao = Decimal(10)

        economia = valor_categoria * (percentual_reducao / Decimal(100))

        simulacao = {
            'categoria': maior['categoria__nome'],
            'percentual': percentual_reducao,
            'economia': economia.quantize(Decimal('0.01')),
        }

        impacto_anual = {
            'economia_anual': economia * Decimal(12),
            'gasto_atual': saidas * Decimal(12),
            'gasto_ajustado': (saidas - economia) * Decimal(12),
        }

        diagnostico.append({
            'tipo': 'info',
            'mensagem': f'A maior parte dos gastos está em {maior["categoria__nome"]}.'
        })

    # --------------------
    # HUMOR
    # --------------------
    humor = {
        'classe': 'good',
        'emoji': '🙂',
        'texto': 'Você está no controle financeiro.'
    }

    if percentual_gastos >= 70:
        humor = {
            'classe': 'bad',
            'emoji': '😟',
            'texto': 'Seus gastos estão fora de controle.'
        }
    elif percentual_gastos >= 40:
        humor = {
            'classe': 'warn',
            'emoji': '😐',
            'texto': 'Fique atento aos próximos gastos.'
        }

    # --------------------
    # LANÇAMENTOS
    # --------------------
    lancamentos = (
        Lancamento.objects.filter(user=request.user)
        .order_by('-data')[:10]
    )

    # --------------------
    # CONTEXTO
    # --------------------
    context = {
        'entradas': entradas,
        'saidas': saidas,
        'saldo': saldo,
        'form': form,
        'labels_categoria': [c['categoria__nome'] for c in categorias],
        'valores_categoria': [float(c['total']) for c in categorias],
        'tem_grafico': len(categorias) > 1,
        'lancamentos': lancamentos,
        'diagnostico': diagnostico,
        'sucesso': sucesso,
        'simulacao': simulacao,
        'impacto_anual': impacto_anual,
        'gastos_invisiveis': gastos_invisiveis,
        'percentual_invisivel': percentual_invisivel,
        'tem_gastos_invisiveis': tem_gastos_invisiveis,
        'limite_invisivel': LIMITE_INVISIVEL,
        'personalidade': personalidade,
        'descricao_personalidade': descricao_personalidade,
        'humor': humor,
    }

    return render(request, 'dashboard.html', context)


@login_required
def editar_lancamento(request, id):
    lancamento = get_object_or_404(
        Lancamento,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        form = LancamentoForm(request.POST, instance=lancamento)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = LancamentoForm(instance=lancamento)

    return render(request, 'editar_lancamento.html', {
        'form': form,
        'lancamento': lancamento
    })


@login_required
def excluir_lancamento(request, id):
    lancamento = get_object_or_404(
        Lancamento,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        lancamento.delete()

    return redirect('/')


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.filter(user=request.user)
    return render(request, 'categorias/lista.html', {
        'categorias': categorias
    })


@login_required
def criar_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')

        if nome:
            Categoria.objects.create(
                nome=nome.strip(),
                user=request.user  # 🔥 ISSO É O QUE FALTAVA
            )

            return redirect('lista_categorias')

    return render(request, 'categorias/criar.html')



@login_required
def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.save()
        return redirect('lista_categorias')

    return render(request, 'categorias/editar.html', {
        'categoria': categoria
    })


@login_required
def excluir_categoria(request, id):
    categoria = Categoria.objects.get(id=id, user=request.user)
    categoria.delete()
    return redirect('lista_categorias')

@login_required
def lista_lancamentos(request):
    lancamentos = Lancamento.objects.filter(
        user=request.user
    ).order_by('-data')

    return render(request, 'lancamentos.html', {
        'lancamentos': lancamentos
    })

@login_required
def relatorios(request):
    return render(request, 'relatorios.html')


@login_required
def relatorio_mensal(request):
    hoje = date.today()

    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    lancamentos = Lancamento.objects.filter(
        user=request.user,
        data__month=mes,
        data__year=ano
    )

    entradas = lancamentos.filter(tipo='E').aggregate(
        total=Sum('valor')
    )['total'] or 0

    saidas = lancamentos.filter(tipo='S').aggregate(
        total=Sum('valor')
    )['total'] or 0

    saldo = entradas - saidas

    por_categoria = lancamentos.filter(tipo='S') \
        .values('categoria__nome') \
        .annotate(total=Sum('valor')) \
        .order_by('-total')

    context = {
        'mes': mes,
        'ano': ano,
        'entradas': entradas,
        'saidas': saidas,
        'saldo': saldo,
        'por_categoria': por_categoria,
    }

    return render(request, 'relatorios/mensal.html', context)