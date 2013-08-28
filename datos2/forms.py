from django.forms import ModelForm, Select, TextInput
from django import forms
from models import *

class PersonaForm(ModelForm):
	class Meta:
		model = Persona
		
class DomicilioForm(ModelForm):
	class Meta:
		model = Domicilio

class PartialDomicilioForm(ModelForm):
	class Meta:
		model = Domicilio
		exclude = ('persona','observacion')

class ClonableDomicilioForm(ModelForm):
	class Meta:
		model = Domicilio
		exclude = ('persona','observacion')
		widgets = {
			'tipo_domicilio': Select(attrs={'id': "id_domicilios-#index#-direccion", 'name': "id_domicilios-#index#-direccion",}),
			'direccion': TextInput(attrs={'id': "id_domicilios-#index#-direccion", 'name': "id_domicilios-#index#-direccion",}),
			'localidad': Select(attrs={'id': "id_domicilios-#index#-direccion", 'name': "id_domicilios-#index#-direccion",}),
		}
		
class TelefonoForm(ModelForm):
	class Meta:
		model = Telefono

class PartialTelefonoForm(ModelForm):
	class Meta:
		model = Telefono
		exclude = ('persona','observacion')