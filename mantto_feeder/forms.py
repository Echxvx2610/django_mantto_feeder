from django import forms
from .models import FeederParaReparar,PartesFeeder,PartesRequeridas


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class FeederParaRepararForm(forms.ModelForm):
    class Meta:
        model = FeederParaReparar
        fields = ['feeder_id', 'tamano', 'color', 'falla', 'parte', 'cantidad_refaccion', 'tecnico']

class PartesFeederForm(forms.ModelForm):
    class Meta:
        model = PartesFeeder
        fields = ['numero_parte', 'nombre', 'costo', 'stock_minimo', 'cantidad', 'estado']
        
        
class PartesRequeridasForm(forms.ModelForm):
    class Meta:
        model = PartesRequeridas
        fields = ['feeder_id', 'numero_parte', 'nombre', 'costo', 'cantidad']