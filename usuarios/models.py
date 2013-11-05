from django.db import models
from datos2.models import Persona
from django.contrib.auth.models import User
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog



class Perfil (models.Model):
	usuario= models.ForeignKey(User, on_delete=models.PROTECT, unique=True)
	persona= models.ForeignKey(Persona, on_delete=models.PROTECT, unique=True)
	
	fechaCreacion= models.DateTimeField(auto_now_add=True, editable=True)
	fechaModificacion=models.DateTimeField(auto_now=True, editable=True)
	
	class Admin:
		pass
	
		
	
class Tarjeta (models.Model):
	usuario= models.ForeignKey(User, on_delete=models.PROTECT, unique=True,related_name='propietario')
	cordenadas= models.TextField();
	ultimoUsuario = models.ForeignKey(User, editable=False, blank = True)
	fechaCreacion= models.DateTimeField(auto_now_add=True, editable=True)
	fechaModificacion=models.DateTimeField(auto_now=True, editable=True, null=True)
# Create your models here.
