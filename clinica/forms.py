#usr/bin/python
# -*- encoding: utf-8 -*-
from django.forms import ModelForm, Select, TextInput, DateTimeInput
from django import forms
from models import *
from datos2.models import Persona
import autocomplete_light
from autocomplete_light_registry import *


class Evolucion_doctorForm(ModelForm):
	fecha = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={ 'id':'datepicker'}))
	
	class Meta:
		model = Evolucion_doctor		
		widgets = {
			'fecha': TextInput(attrs={ 'id':'datepicker'}),
			'diagnostico': autocomplete_light.ChoiceWidget('DiagnosticoAutocomplete'),
		}		
		#fecha = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=DateTimeInput(format="%d-%m-%Y %H:%M"))


    
class Evolucion_enfermeriaForm(ModelForm):
	class Meta:
		model = Evolucion_enfermeria
		widgets = {
			'fecha': TextInput(attrs={ 'id':'datepicker'}),
			'diagnostico': autocomplete_light.ChoiceWidget('DiagnosticoAutocomplete'),
			}	
		
class Prescripciones_medicasForm(ModelForm):
	class Meta:
		model = Prescripciones_medicas
		widgets = {
			'fecha': TextInput(attrs={ 'id':'datepicker'}),
			'diagnostico': autocomplete_light.ChoiceWidget('DiagnosticoAutocomplete'),
			}	
		
class Foja_quirurgicaForm(ModelForm):
	class Meta:
		model = Foja_quirurgica
	widgets = {
			'fecha': TextInput(attrs={ 'id':'datepicker'}),
			'diagnostico': autocomplete_light.ChoiceWidget('DiagnosticoAutocomplete'),
		}	
		
class Formulario_filtro_evolucionForm(forms.Form):
	firmante=forms.ModelChoiceField(Persona.objects.all(),
        widget=autocomplete_light.ChoiceWidget('PersonaAutocomplete'))
	#especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all())
	fecha_desde =  forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={ 'class':'date'}))
	fecha_hasta =  forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={  'class':'date'}))
	diagnostico=forms.ModelChoiceField(Cie10.objects.all(),
									  widget=autocomplete_light.ChoiceWidget('DiagnosticoAutocomplete'))
	especialidad = forms.ModelChoiceField(Especialidad.objects.all(),
									 widget=autocomplete_light.ChoiceWidget('EspecialidadAutocomplete'))   
		#tags = autocomplete_light.TextWidget('TagAutocomplete')

class Formulario_filtro_enfermeriaForm(forms.Form):
	firmante=forms.ModelChoiceField(Persona.objects.all(),
        widget=autocomplete_light.ChoiceWidget('PersonaAutocomplete'))
	#especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all())
	fecha_desde =  forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={ 'class':'date'}))
	fecha_hasta =  forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={  'class':'date'}))


class Formulario_filtro_prescripcionesForm(forms.Form):
	firmante=forms.ModelChoiceField(Persona.objects.all(),
        widget=autocomplete_light.ChoiceWidget('PersonaAutocomplete'))
	#especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all())
	fecha_desde =  forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={ 'class':'date'}))
	fecha_hasta =  forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"],widget=TextInput(attrs={  'class':'date'}))
	diagnostico=forms.ModelChoiceField(Cie10.objects.all(),
									  widget=autocomplete_light.ChoiceWidget('DiagnosticoAutocomplete'))
	especialidad = forms.ModelChoiceField(Especialidad.objects.all(),
									 widget=autocomplete_light.ChoiceWidget('EspecialidadAutocomplete'))   
		#tags = autocomplete_light.TextWidget('TagAutocomplete')
		
