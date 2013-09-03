from abm.funciones import *
from models import *
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.forms.models import modelformset_factory
from stronghold.decorators import public
from django.contrib.auth.decorators import permission_required
from django.forms import ModelForm, TextInput, Textarea

nombresFormularios={unicode("persona"):PersonaForm,
					unicode("telefono"):TelefonoForm,
					unicode("domicilio"):DomicilioForm}
					
nombresModelos={unicode("persona"):Persona,
				unicode("telefono"):Telefono,
				unicode("domicilio"):Domicilio}



def alta_persona(request):
	if request.user.has_perm('datos.add_'+'persona'):
		DomicilioFormSet=modelformset_factory(Domicilio, form=DomicilioForm, extra=10, exclude=('persona','observacion',))	
		#TelefonoFormSet=modelformset_factory(Telefono, form=TelefonoForm, extra=10, exclude=('persona','observacion',))	
		if request.method=='POST':
			formulario1=PersonaForm(request.POST)			
			formulario2=DomicilioFormSet(request.POST, queryset=Domicilio.objects.none(),prefix='domicilios',initial=[{'tipo_domicilio': u'legal','direccion': u'hola','localidad': u'rawson'}])
		##	formulario3=TelefonoFormSet(request.POST, queryset=Telefono.objects.none(),prefix='telefonos',initial=[{'tipo_telefono': u'legal','codigo_area': u'hola','numero': u'rawson'}])
			if (formulario1.is_valid() and formulario2.is_valid()):
				domicilios=formulario2.save(commit=False)
				telefonos=formulario3.save(commit=False)
				persona=formulario1.save()				
				
				for domicilio in domicilios:
					domicilio.persona=persona
					domicilio.save()
				
				for telefono in telefonos:
					telefono.persona=persona
					telefono.save()
				
					
				return HttpResponseRedirect('/datos2/lista/persona')
		else:
			formulario1=PersonaForm()
			formulario2=DomicilioFormSet(queryset=Domicilio.objects.none(),prefix='domicilios',initial=[{'tipo_domicilio': u'legal','direccion': u'hola','localidad': u'rawson'}])
			#formulario3=TelefonoFormSet(queryset=Telefono.objects.none(),prefix='telefonos',initial=[{'tipo_telefono': u'legal','codigo_area': u'hola','numero': u'rawson'}])
		return render_to_response('formulario_personas.html', {'formulario': formulario1, 'formulario2': formulario2, 'nombre': Persona._meta.verbose_name_plural, 'n': Persona._meta.verbose_name,}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		

def alta_(request, modelo):
	if request.user.has_perm('datos.add_'+modelo):
		return alta(request,nombresModelos[modelo],nombresFormularios[modelo],"datos2",'formulario_datos2.html')
	else:
		return HttpResponseRedirect('/403')
		
def lista_(request,modelo):
	return lista(request,nombresModelos[modelo],'lista_datos2.html')

	
def editar_(request, modelo, id_profesion):
	if request.user.has_perm('datos.change_'+modelo):
		return editar(request, id_profesion, nombresModelos[modelo], nombresFormularios[modelo],"datos2",'formulario_datos2.html') 
	else:
		return HttpResponseRedirect('/403')
		
def eliminar_(request, modelo, id_domicilio):
	if request.user.has_perm('datos.delete_'+modelo):
		return eliminar(request,  nombresModelos[modelo], id_domicilio,"datos2")
	else:
		return HttpResponseRedirect('/403')
		

def editar_persona(request, id_persona):
	if request.user.has_perm('datos.add_'+'persona'):
		DomicilioFormSet=modelformset_factory(Domicilio, extra=0, form=DomicilioForm, exclude=('persona','observacion',))	
		TelefonoFormSet=modelformset_factory(Telefono, form=TelefonoForm, extra=0, exclude=('persona','observacion',))	
		if request.method=='POST':
			persona = Persona.objects.get(id=id_persona)
			formulario1=PersonaForm(request.POST, instance = persona)			
			queryset=Domicilio.objects.all()
			formulario2=DomicilioFormSet(request.POST, queryset=queryset.filter(persona = persona),prefix='domicilios',initial=[{'tipo_domicilio': u'legal','direccion': u'hola','localidad': u'rawson'}])
			queryset=Telefono.objects.all()
			formulario3=TelefonoFormSet(request.POST, queryset=queryset.filter(persona = persona),prefix='telefonos',initial=[{'tipo_telefono': u'legal','codigo_area': u'hola','numero': u'rawson'}])
			if (formulario1.is_valid() and formulario2.is_valid()):
				domicilios=formulario2.save(commit=False)
				telefonos=formulario3.save(commit=False)
				persona=formulario1.save()				
				
				for domicilio in domicilios:
					domicilio.persona=persona
					domicilio.save()
				
				for telefono in telefonos:
					telefono.persona=persona
					telefono.save()
				
					
				return HttpResponseRedirect('/datos2/lista/persona')
		else:
			persona = Persona.objects.get(id=id_persona)
			formulario1=PersonaForm(instance = persona)
			queryset=Domicilio.objects.all()			
			formulario2=DomicilioFormSet(queryset = queryset.filter(persona = persona),prefix='domicilios')
			queryset=Telefono.objects.all()
			formulario3=TelefonoFormSet(queryset=queryset.filter(persona = persona),prefix='telefonos',initial=[{'tipo_telefono': u'legal','codigo_area': u'hola','numero': u'rawson'}])			
		return render_to_response('formulario_edit_personas.html', {'formulario': formulario1, 'formulario2': formulario2, 'formulario3': formulario3, 'nombre': Persona._meta.verbose_name_plural, 'n': Persona._meta.verbose_name,}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		
def busqueda_(request,modelo):
	return busqueda(request,nombresModelos[modelo],'lista_datos2.html')
		
