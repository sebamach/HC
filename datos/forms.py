from django.forms import ModelForm
from django import forms
from models import *


class TituloForm(ModelForm):
	class Meta:
		model = Titulo
		
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
