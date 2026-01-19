from django import forms
from .models import Lancamento

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['tipo', 'valor', 'data', 'categoria', 'descricao', 'recorrente']
        widgets = {
            'tipo': forms.RadioSelect(choices=Lancamento.TIPO_CHOICES),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ex: 150,00'
            }),
            'data': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional'
            }),
            'recorrente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if not tipo:
            raise forms.ValidationError('Selecione Entrada ou Saída.')
        return tipo