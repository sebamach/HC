from django.db import models
from datos2.models import Persona
from django.contrib.auth.models import User


class Perfil (models.Model):
	usuario= models.ForeignKey(User, on_delete=models.PROTECT, unique=True)
	persona= models.ForeignKey(Persona, on_delete=models.PROTECT, unique=True)
	#usuarioCreacion=
	fechaCreacion= models.DateTimeField(auto_now_add=True, editable=True)
	#usuarioModificacion=
	fechaModificacion=models.DateTimeField(auto_now=True, editable=True)
	#audit_log = AuditLog()  
	
	class Admin:
		pass
	class Meta:
		verbose_name_plural = "Perfiles"
	
	


# Create your models here.
