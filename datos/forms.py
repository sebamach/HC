from django.forms import ModelForm, TextInput, Textarea
from django import forms
from models import *


class TituloForm(ModelForm):
	class Meta:
		model = Titulo		
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'observacion': Textarea(),
			
		}
		
		
class EspecialidadForm(ModelForm):
	class Meta:
		model = Especialidad
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'observacion': Textarea(),
			#'titulo':forms.choice{ 'required':'true'},
		}
		
class PaisForm(ModelForm):
	class Meta:
		model = Pais
		widgets = {
			'codigo': TextInput(attrs={ 'required':'true', 'number':'true'}),
			'codigoAlfa2': TextInput(attrs={ 'required':'true'}),
			'codigoAlfa3': TextInput(attrs={ 'required':'true'}),
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}
		
class ProvinciaForm(ModelForm):
	class Meta:
		model = Provincia
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'codigo': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
			
		}

class LocalidadForm(ModelForm):
	class Meta:
		model = Localidad
		widgets = {
			'codigo': TextInput(attrs={ 'required':'true'}),
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}
		
class TipoDomicilioForm(ModelForm):
	class Meta:
		model = TipoDomicilio
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'descripcionReducida': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}

class TipoSexoForm(ModelForm):
	class Meta:
		model = TipoSexo
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'descripcionReducida': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}
		
class TipoDocumentoForm(ModelForm):
	class Meta:
		model = TipoDocumento
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'descripcionReducida': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}

class TipoPersonaForm(ModelForm):
	class Meta:
		model = TipoPersona
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'descripcionReducida': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}
		
class TipoTelefonoForm(ModelForm):
	class Meta:
		model = TipoTelefono
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'descripcionReducida': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}
		
class TipoEstadoCivilForm(ModelForm):
	class Meta:
		model = TipoEstadoCivil
		widgets = {
			'descripcion': TextInput(attrs={ 'required':'true'}),
			'descripcionReducida': TextInput(attrs={ 'required':'true'}),
			'observacion': forms.Textarea,
			
		}

class Cie10Form(ModelForm):
	class Meta:
		model = Cie10	
		widgets = {
			'codigo': TextInput(attrs={ 'required':'true'}),
			'descripcion': TextInput(attrs={ 'required':'true'}),
			
		}
