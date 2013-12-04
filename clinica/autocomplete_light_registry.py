#usr/bin/python
# -*- encoding: utf-8 -*-
import autocomplete_light
from models import *



autocomplete_light.register(User, name='PersonaAutocomplete',
    choices=Persona.objects.all(),
	search_fields = ['^nombre', 'apellido'],
	 autocomplete_js_attributes={
        'minimum_characters': 3,
        'placeholder': 'Tipee la Persona',})
        
autocomplete_light.register(Cie10, name='DiagnosticoAutocomplete',
    choices=Cie10.objects.all(),
	search_fields = ['^codigo', 'descripcion'],
	 autocomplete_js_attributes={
        'minimum_characters': 3,
        'placeholder': 'Tipee el Diagnostico',})
        
autocomplete_light.register(Especialidad, name='EspecialidadAutocomplete',
    choices=Especialidad.objects.all(),
	search_fields = ['^descripcion', 'descripcion'],
	 autocomplete_js_attributes={
        'minimum_characters': 3,
        'placeholder': 'Tipee la Especialidad',})
        
autocomplete_light.register(Pais, name='PaisAutocomplete',
    choices=Pais.objects.all(),
	search_fields = ['^descripcion', 'descripcion'],
	 autocomplete_js_attributes={
        'minimum_characters': 3,
        'placeholder': 'Tipee el Pais',})
        
autocomplete_light.register(Provincia, name='ProvinciaAutocomplete',
    choices=Provincia.objects.all(),
	search_fields = ['^descripcion', 'descripcion'],
	 autocomplete_js_attributes={
        'minimum_characters': 3,
        'placeholder': 'Tipee la Provincia o Estado',})
        
autocomplete_light.register(Localidad, name='LocalidadAutocomplete',
    choices=Localidad.objects.all(),
	search_fields = ['^descripcion', 'descripcion'],
	 autocomplete_js_attributes={
        'minimum_characters': 3,
        'placeholder': 'Tipee la Localidad',})

autocomplete_light.register(Titulo, name='TituloAutocomplete',
    choices=Titulo.objects.all(),
	search_fields = ['^descripcion', 'descripcion'],
	 autocomplete_js_attributes={
        'minimum_characters': 3,
        'placeholder': 'Tipee el Titulo',})

