from django.db import models
from datos2.models import Persona
from django.contrib.auth.models import User
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog



class Perfil (models.Model):
	usuario= models.ForeignKey(User, on_delete=models.PROTECT, unique=True)
	persona= models.ForeignKey(Persona, on_delete=models.PROTECT, unique=True)
	ultimoUsuario = models.ForeignKey(User, editable=False, related_name="CREADOR")
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	class Admin:
		pass
	
		
	
class Tarjeta (models.Model):
	usuario= models.ForeignKey(User, on_delete=models.PROTECT, unique=True,related_name='propietario')
	cordenadas= models.TextField();
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
# Create your models here.
