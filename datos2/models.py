from django.db import models
from datos.models import *
from django.contrib.auth.models import User
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog


class Persona (models.Model):
	nombre = models.CharField("NOMBRE", max_length=30)
	apellido = models.CharField("APELLIDO", max_length=30)
	sexo = models.ForeignKey(TipoSexo, on_delete=models.PROTECT)
	estado_civil = models.ForeignKey(TipoEstadoCivil, on_delete=models.PROTECT)
	tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
	numero_documento = models.IntegerField()
	pais_nacimiento = models.ForeignKey(Pais, on_delete=models.PROTECT)
	provincia_nacimiento = models.ForeignKey(Provincia, on_delete=models.PROTECT, null=True, blank=True)
	localidad_nacimiento = models.ForeignKey(Localidad, on_delete=models.PROTECT, null=True, blank=True)
	fecha_de_nacimiento = models.DateField("FECHA DE NACIMIENTO")
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.apellido+', '+self.nombre +' ('+str(self.numero_documento)+')'
		
	class meta:
		unique_together =[("tipo_documento","numero_documento")]
		ordering = ['apellido','nombre'] 
		
class Telefono (models.Model):
	tipo_telefono = models.ForeignKey(TipoTelefono, on_delete=models.PROTECT)
	codigo_area = models.CharField("CODIGO DE AREA", max_length=20)
	numero = models.CharField("NUMERO TELEFONICO", max_length=20)
	observacion = models.TextField("OBSERVACION", blank=True)
	persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.codigo_area+'-'+self.numero		

		
class Domicilio (models.Model):	
	tipo_domicilio = models.ForeignKey(TipoDomicilio, on_delete=models.PROTECT)
	direccion = models.CharField("DIRECCION", max_length=50)
	localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
	observacion = models.TextField("OBSERVACION", blank=True)
	persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return self.direccion
		
class FotoPerfil (models.Model):
	foto = models.ImageField(upload_to = 'fotitos')
	persona = models.ForeignKey(Persona)		
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
class DatosProfesionales (models.Model):
	persona = models.ForeignKey(Persona)
	especialidad = models.ForeignKey(Especialidad)
	matriculap = models.CharField("Matricula Provincial",blank =True, max_length = 6, unique=True)
	matriculan = models.CharField("Matricula Provincial",blank =True, max_length = 6, unique=True)
	email=	models.EmailField("Correo Electronico")
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)


	

	
