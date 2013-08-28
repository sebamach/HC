from django.forms import ModelForm, TextInput
from django import forms
from models import *


class TituloForm(ModelForm):
	class Meta:
		model = Titulo
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			#'descripcion': TextInput(attrs={ 'class': '{required:true, maxlength:5}' }),
		}
		
class EspecialidadForm(ModelForm):
	class Meta:
		model = Especialidad
		
class PaisForm(ModelForm):
	class Meta:
		model = Pais
		
class ProvinciaForm(ModelForm):
	class Meta:
		model = Provincia

class LocalidadForm(ModelForm):
	class Meta:
		model = Localidad
		
class TipoDomicilioForm(ModelForm):
	class Meta:
		model = TipoDomicilio

class TipoSexoForm(ModelForm):
	class Meta:
		model = TipoSexo
		
class TipoDocumentoForm(ModelForm):
	class Meta:
		model = TipoDocumento

class TipoPersonaForm(ModelForm):
	class Meta:
		model = TipoPersona
		
class TipoTelefonoForm(ModelForm):
	class Meta:
		model = TipoTelefono
		
class TipoEstadoCivilForm(ModelForm):
	class Meta:
		model = TipoEstadoCivil
