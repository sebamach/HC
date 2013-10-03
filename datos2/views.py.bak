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

import datetime



nombresFormularios={unicode("persona"):PersonaForm,
					unicode("telefono"):TelefonoForm,
					unicode("partialtelefono"):PartialTelefonoForm,
					unicode("domicilio"):DomicilioForm,
					unicode("partialdomicilio"):PartialDomicilioForm,
					unicode("fotoperfil"):FotoPerfilForm,}
					
nombresModelos={unicode("persona"):Persona,
				unicode("telefono"):Telefono,
				unicode("domicilio"):Domicilio,
				unicode("fotoperfil"):FotoPerfil,
				}



def alta_persona(request):
	if request.user.has_perm('datos.add_'+'persona'):
		#DomicilioFormSet=modelformset_factory(Domicilio, form=DomicilioForm, extra=10, exclude=('persona','observacion',))	
		#TelefonoFormSet=modelformset_factory(Telefono, form=TelefonoForm, extra=10, exclude=('persona','observacion',))	
		if request.method=='POST':
			formulario1=PersonaForm(request.POST)			
		#	formulario2=DomicilioFormSet(request.POST, queryset=Domicilio.objects.none(),prefix='domicilios',initial=[{'tipo_domicilio': u'legal','direccion': u'hola','localidad': u'rawson'}])
		##	formulario3=TelefonoFormSet(request.POST, queryset=Telefono.objects.none(),prefix='telefonos',initial=[{'tipo_telefono': u'legal','codigo_area': u'hola','numero': u'rawson'}])
			if (formulario1.is_valid() ):#and formulario2.is_valid()):
				#domicilios=formulario2.save(commit=False)
				#telefonos=formulario3.save(commit=False)
				formulario1.save()				
				
				#for domicilio in domicilios:
				#	domicilio.persona=persona
				#	domicilio.save()
				
				#for telefono in telefonos:
				#	telefono.persona=persona
				#	telefono.save()
				
					
				return HttpResponseRedirect('/datos2/lista/persona')
		else:
			formulario1=PersonaForm()
			#formulario2=DomicilioFormSet(queryset=Domicilio.objects.none(),prefix='domicilios',initial=[{'tipo_domicilio': u'legal','direccion': u'hola','localidad': u'rawson'}])
			#formulario3=TelefonoFormSet(queryset=Telefono.objects.none(),prefix='telefonos',initial=[{'tipo_telefono': u'legal','codigo_area': u'hola','numero': u'rawson'}])
		return render_to_response('formulario_personas.html', {'formulario': formulario1,  'nombre': Persona._meta.verbose_name_plural, 'n': Persona._meta.verbose_name,}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		

def alta_(request, modelo):
	if request.user.has_perm('datos.add_'+modelo):
		return alta(request,nombresModelos[modelo],nombresFormularios[modelo],"datos2",'formulario_datos2.html')
	else:
		return HttpResponseRedirect('/403')

	
		
def alta(request, clase_name, form_name, modulo, pagina):
	if request.method=='POST':
		formulario=Telefono(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/'+modulo+'/lista/'+clase_name()._meta.verbose_name)
	else:
		formulario=form_name()
	return render_to_response(pagina, {'formulario': formulario, 'nombre': clase_name()._meta.verbose_name_plural,'n': clase_name()._meta.verbose_name}, context_instance=RequestContext(request))
		
		
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
			if formulario1.is_valid():
				persona=formulario1.save()				
				return HttpResponseRedirect("/datos2/seleccionar/persona/"+request.session['persona'])
		else:
			persona = Persona.objects.get(id=id_persona)
			formulario1=PersonaForm(instance = persona)
			
		return render_to_response('formulario_edit_personas.html', {'formulario': formulario1, 'nombre': Persona._meta.verbose_name_plural, 'n': Persona._meta.verbose_name,}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		
def busqueda_(request,modelo):
	return busqueda(request,nombresModelos[modelo],'lista_datos2.html')
		
def autocompletar_(request,modelo):
	return autocompletar(request,nombresModelos[modelo])
	
def autocompletar_nombre_apellido(request,modelo):
	return autocompletar(request,nombresModelos[modelo])
	
def seleccionar(request,modelo, id_persona):
	dato=Persona.objects.get(id=id_persona)
	fotoperfil=FotoPerfil.objects.filter(persona=dato)
	if fotoperfil:
		foto = fotoperfil[0].foto
	else:
		foto = ""
	domicilios= Domicilio.objects.filter(persona = dato)
	telefonos= Telefono.objects.filter(persona = dato)
	delta = datetime.date.today() - dato.fecha_de_nacimiento
	delta = datetime.date.fromordinal(delta.days).year
	request.session['persona'] = id_persona
	return render_to_response('persona.html',{'dato':dato, 'edad':delta, 'domicilios':domicilios,'telefonos':telefonos, 'foto':foto},context_instance=RequestContext(request))

	
	
def alta_telefono(request):
	if request.user.has_perm('datos.add_'+'telefono'):
		if request.method=='POST':
			formulario=PartialTelefonoForm(request.POST)
			if formulario.is_valid():
				telefono=formulario.save(commit=False)
				telefono.persona= Persona.objects.get(id=request.session['persona'])
				telefono.save()
				return HttpResponseRedirect('/datos2/seleccionar/persona/'+request.session['persona'])
				
		else:
			formulario=PartialTelefonoForm()
		return render_to_response('formulario_datos2.html', {'formulario': formulario, 'nombre': Telefono._meta.verbose_name_plural,'n': Telefono()._meta.verbose_name}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/datos2/seleccionar/persona/'+request.session['persona'])
	
def alta_domicilio(request,id_persona):
	if request.user.has_perm('datos.add_'+'domicilio'):
		if request.method=='POST':
			formulario=PartialDomicilioForm(request.POST)
			if formulario.is_valid():
				domicilio=formulario.save(commit=False)
				domicilio.persona= Persona.objects.get(id=id_persona)
				domicilio.save()
			return HttpResponseRedirect('/datos2/seleccionar/persona/'+id_persona)
		else:
			formulario=PartialDomicilioForm()
				
		return alta(request,nombresModelos['domicilio'],nombresFormularios['partialdomicilio'],"datos2",'formulario_datos2.html')
		
def cargar_imagen(request):
	if request.user.has_perm('datos.add_'+'domicilio'):
		if request.method=='POST':
			formulario=FotoPerfilForm(request.POST, request.FILES)
			if formulario.is_valid():
				fotoperfil=formulario.save(commit=False)
				fotoperfil.persona= Persona.objects.get(id=request.session['persona'])
				fotoperfil.save()
				return HttpResponseRedirect('/datos2/seleccionar/persona/'+request.session['persona'])
		else:
			formulario=FotoPerfilForm()
		return render_to_response('formulario_datos2.html', {'formulario': formulario, 'nombre': 'fotos','n': 'foto'}, context_instance=RequestContext(request))
		
	
