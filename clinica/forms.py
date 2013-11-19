from django.forms import ModelForm, Select, TextInput, DateTimeInput
from django import forms
from models import *

class Evolucion_doctorForm(ModelForm):
	fecha = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={ 'id':'datepicker'}))
	
	class Meta:
		model = Evolucion_doctor		
		widgets = {
			'fecha': TextInput(attrs={ 'id':'datepicker'}),
		}		
		#fecha = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=DateTimeInput(format="%d-%m-%Y %H:%M"))


class Evolucion_enfermeriaForm(ModelForm):
	class Meta:
		model = Evolucion_enfermeria
		
class Prescripciones_medicasForm(ModelForm):
	class Meta:
		model = Prescripciones_medicas
		
class Foja_quirurgicaForm(ModelForm):
	class Meta:
		model = Foja_quirurgica
		
"""		
class PartialDomicilioForm(ModelForm):
	class Meta:
		model = Domicilio
		exclude = ('persona','observacion')
		
class TelefonoForm(ModelForm):
	class Meta:
		model = Telefono
		widgets = {
			'tipo_telefono': Select(attrs={ 'class':'input-small'}),
			'codigo_area': TextInput(attrs={ 'class':'input-small'}),
			'numero': TextInput(attrs={ 'class':'input-medium'}),
		}

class PartialTelefonoForm(ModelForm):
	class Meta:
		model = Telefono
		exclude = ('persona','observacion')		
		
from django.forms.models import BaseModelFormSet

class BaseDomicilioFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseDomicilioFormSet, self).add_fields(form, index)
        # customize your fields .. e.g. to change the size of a InputText
        self.fields['tipo_domicilio'].widget.attrs['class'] = 'span1'

class FotoPerfilForm(ModelForm):
	class Meta:
		model = FotoPerfil
		exclude = ('persona')
		
class DatosProfesionalesForm(ModelForm):
	class Meta:
		model = DatosProfesionales
		exclude = ('persona')
"""
