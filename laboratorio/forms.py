from django import forms
from .models import Usuario, PruebaLaboratorio

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'puesto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto': forms.Select(attrs={'class': 'form-control'}),
        }

class PruebaForm(forms.ModelForm):
    class Meta:
        model = PruebaLaboratorio
        fields = ['tipo_prueba', 'cantidad']
        widgets = {
            'tipo_prueba': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }