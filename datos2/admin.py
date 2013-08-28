from django.contrib import admin
from datos2.models import Persona

class PersonaAdmin(admin.ModelAdmin):
	fields = ['nombre','apellido']
	list_display = ('nombre','apellido')
	
	

admin.site.register(Persona, PersonaAdmin)
