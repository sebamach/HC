from django.db import models
from datos2.models import *
from datos.models import *
from django.contrib.auth.models import User
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog
from django.utils.formats import get_format

# Create your models here.


#hoja de evolucion de internado (doctor)
class Evolucion_doctor(models.Model):
	persona = models.ForeignKey(Persona, editable=False)
	fecha = models.DateTimeField ()
	diagnostico=models.ForeignKey(Cie10, blank=True)
	prescripcion = models.TextField("PRESCRIPCIONES Y ORDENES", blank=True)
	firma	= models.ForeignKey(User, editable= False)##no editable se uso para probar con admin
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	audit_log = AuditLog()
	class Meta:
		ordering = ['-fechaCreacion']
		unique_together =[("persona","fecha","prescripcion",'firma')]

	
#hoja de evolucion de internado (enfermeros)		
class Evolucion_enfermeria(models.Model):
	persona = models.ForeignKey(Persona, editable=False)
	fecha = models.DateTimeField ()
	prescripcion = models.TextField("PRESCRIPCIONES Y ORDENES", blank=True)
	firma	= models.ForeignKey(User, editable= False)##no editable se uso para probar con admin
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	audit_log = AuditLog()
	
	class Meta:
		ordering = ['-fechaCreacion']
		unique_together =[("persona","fecha","prescripcion",'firma')]
		
	
	
#hoja de prescripciones y ordenes medicas (enfermeros)
class Prescripciones_medicas(models.Model):
	persona = models.ForeignKey(Persona, editable=False)
	fecha = models.DateTimeField ()
	diagnostico=models.ForeignKey(Cie10, blank=True)
	prescripcion = models.TextField("PRESCRIPCIONES Y ORDENES MEDICAS", blank=True)
	firma	= models.ForeignKey(User, editable= False)##no editable se uso para probar con admin
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	audit_log = AuditLog()
	class Meta:
		ordering = ['-fechaCreacion']
		unique_together =[("persona","fecha","prescripcion",'firma')]
	
		
#foja quirurgica		
class Foja_quirurgica (models.Model):
	riesgo = (	('G', 'Grave'),	('M', 'Mediano'),	('L', 'Leve')	)	
	transfusion = (    ('S', 'Suero'),    ('P', 'Plasma')    )	
	sino = (    ('S', 'Si'),    ('N', 'No'),   )	
    
    
	persona = models.ForeignKey(Persona, editable=False, related_name='paciente')
	fecha_inicio = models.DateTimeField ()
	fecha_fin = models.DateTimeField ()
	firma_cirujano	= models.ForeignKey(User,related_name='firmante', verbose_name='CIRUJANO')
	ayudantes = models.ManyToManyField(Persona)
	anestesia_empleada= models.CharField(max_length=100)
	anestesista= models.ForeignKey(Persona, related_name ='anestesista')
	pre_anestesia= models.CharField(blank = True,max_length=100)
	hora_pre_anestesia = models.DateTimeField ()
	diagnostico_pre_operatorio = models.ForeignKey(Cie10, related_name='pre')
	riesgo_operatorio= models.CharField(choices=riesgo, default='L',max_length=100)
	transfusion_intraoperatoria = models.CharField(choices=transfusion, default='S',max_length=100)
	plan_quirurgico= models.CharField(max_length=100)
	operacion_practicada= models.CharField(max_length=100)
	detalles_operatorios= models.TextField(max_length=100)
	material_de_sutura=  models.CharField(max_length=100)
	drenajes = models.CharField(max_length=100)
	diagnostico_post_operatorio = models.ForeignKey(Cie10, related_name='post')
	descripcion_macroscopica= models.CharField(max_length=100)
	envia_material = models.CharField(choices=sino, default='N',max_length=100)
	fechaCreacion= models.DateTimeField(auto_now_add=True)
	fechaModificacion=models.DateTimeField(auto_now=True, null=True)
	audit_log = AuditLog()
	
	
	class Meta:
		ordering = ['fecha_inicio']
		verbose_name_plural = "Fojas Quirurgicas"
		verbose_name = "foja_quirurgica"
		


