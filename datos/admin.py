from django.contrib import admin
from datos.models import TipoTelefono
from audit_log.models import *


	

	
class TipoTelefonoAdmin(admin.ModelAdmin):
	fields = ['descripcion','descripcionReducida','observacion']
	list_display = ('descripcion','descripcionReducida','observacion')
	

	

admin.site.register(TipoTelefono, TipoTelefonoAdmin)

