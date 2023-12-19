from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Ticket, Trabajador, Atencion

class AtencionFinalizados(forms.Form):
    class Meta:
        model = Atencion
        fields = ['id_ticket']

    def __init__(self, *args, **kwargs):
        super(AtencionFinalizados, self).__init__(*args, **kwargs)
        self.fields['id_ticket'].widget.attrs['readonly'] = True

class BusquedaForm(forms.Form):
    fecha_inicial = forms.DateField(
        label='Fecha Inicial',error_messages={'required': ''},
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
    )
    fecha_final = forms.DateField(
        label='Fecha Final',error_messages={'required': ''},
        widget=forms.TextInput(attrs={'placeholder': ''}),
    )
    
class IngresoForm(forms.ModelForm):
    areas = Trabajador.objects.values_list('area', 'area').distinct()
    area = forms.ChoiceField(choices=areas, label='Área')
    class Meta:
        model = Ticket
        fields = ['nombre_usuario', 'area', 'descripcion']

class ActualizarForm(forms.ModelForm):
    estados = [
        ('Por atender', 'Por atender'),
        ('En atención', 'En atención'),
        ('Atendido', 'Atendido')
    ]
    estado = forms.ChoiceField(choices = estados, label='Estado')

    class Meta:
        model = Atencion
        fields = ['id_ticket', 'solucion', 'estado']

    def __init__(self, *args, **kwargs):
        super(ActualizarForm, self).__init__(*args, **kwargs)
        self.fields['id_ticket'].widget.attrs['readonly'] = True
