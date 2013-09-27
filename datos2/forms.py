from django.forms import ModelForm, Select, TextInput
from django import forms
from models import *

class PersonaForm(ModelForm):
	class Meta:
		model = Persona
		
class DomicilioForm(ModelForm):
	class Meta:
		model = Domicilio		
		widgets = {
			'tipo_domicilio': Select(attrs={ 'class':'input-small'}),
			'direccion': TextInput(attrs={ 'class':'input-medium'}),
			'localidad': Select(attrs={ 'class':'input-small'}),
		}
		
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
