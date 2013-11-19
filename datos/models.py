from django.db import models
from django.contrib.auth.models import User
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog

# Create your models here.

"""
MODELADO DE DATOS PARA LA PARAMETRIA DE LA APLICACION DE HISTORIAS CLINICAS
"""




# modelo de profesion

class Titulo(models.Model):
	descripcion = models.CharField("DESCRIPCION",max_length=20, unique=True)
	descripcionReducida = models.CharField("ALIAS",max_length=5, blank=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return self.descripcion +" ("+ self.descripcionReducida +")"
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(Profesion, self).save()"""
	class Admin:
		pass
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Titulos"
		
# modelo de especialidad con clave foranea a la profesion que pertenece, se restringe la eliminacion es cascada

class Especialidad(models.Model):
	descripcion = models.CharField("DESCRIPCION", max_length=20)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, blank=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	titulo = models.ForeignKey(Titulo, on_delete=models.PROTECT)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return self.descripcion  +" ("+ self.titulo.descripcionReducida +")"
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(Especialidad, self).save()"""
	class Meta:
		unique_together =[("descripcion","titulo")]
		ordering = ['descripcion']
		verbose_name_plural = "Especialidades"

# modelo de pais segun la norma ISO	3166-1

class Pais(models.Model):
	codigo = models.IntegerField("CODIGO", unique= True)
	codigoAlfa2 = descripcion = models.CharField("COD. 2 LETRAS" , max_length=2)
	codigoAlfa3 = descripcion = models.CharField("COD. 3 LETRAS", max_length=3)
	descripcion = descripcion = models.CharField("DESCRIPCION", max_length=20)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.codigoAlfa2 = self.codigoAlfa2.upper()
		self.codigoAlfa3 = self.codigoAlfa3.upper()
		self.descripcion = self.descripcion.upper()
		self.observacion = self.observacion.upper()
		super(Pais, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Paises"

# modelo de provincias	
	
class Provincia(models.Model):
	codigo = models.CharField("LETRA DE PROV.", max_length=1,unique=True)
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, blank=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.codigo = self.codigo.upper()
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(Provincia, self).save()"""
	class Meta:
		ordering = ['descripcion']

# modelo de localidades

class Localidad(models.Model):
	codigo = models.CharField("CODIGO POSTAL", max_length=5,unique=True)
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, blank=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.codigo = self.codigo.upper()
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(Localidad, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Localidades"

# modelo de Tipo de Sexo

class TipoSexo(models.Model):
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, unique=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.observacion = self.observacion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		super(TipoSexo, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural="Tipos de sexo"
		verbose_name = "tiposexo"
		
# modelo de Tipo de Documento

class TipoDocumento(models.Model):
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, unique=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return self.descripcionReducida
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(TipoDocumento, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Tipos de documentos"
		verbose_name = "tipodocumento"

# modelo de tipo de persona

class TipoPersona(models.Model):
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, unique=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(TipoPersona, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Tipos de personas"
		verbose_name = "tipopersona"
		
# modelo de tipo de domicilio
		
class TipoDomicilio(models.Model):
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, unique=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(TipoDomicilio, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Tipos de domicilios"
		verbose_name = "tipodomicilio"
		
# modelo de tipo de telefono
		
class TipoTelefono(models.Model):
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, unique=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(TipoTelefono, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Tipos de telefono"
		verbose_name = "tipotelefono"

class TipoEstadoCivil(models.Model):
	descripcion = models.CharField("DESCRIPCION", max_length=20, unique=True)
	descripcionReducida = models.CharField("DESCRIPCION REDUCIDA", max_length=5, unique=True)
	observacion = models.TextField("OBSERVACION", blank=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(TipoTelefono, self).save()"""
	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = "Tipos de estado civil"
		verbose_name = "tipoestadocivil"


#cie10 codigos en cod4 solamente
class Cie10(models.Model):
	codigo = models.CharField (max_length=4, unique=True)
	descripcion= models.CharField (max_length=100, unique=True)
	ultimoUsuario = models.ForeignKey(User, editable=False)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.descripcion
	"""def save(self):
		self.descripcion = self.descripcion.upper()
		self.descripcionReducida = self.descripcionReducida.upper()
		self.observacion = self.observacion.upper()
		super(TipoTelefono, self).save()"""
	class Meta:
		ordering = ['codigo']
		verbose_name_plural = "Codigos CIE 10"
		verbose_name = "cie"

