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
			
		parametros = {}
		parametros['name'] = model_name
		parametros['plural_name'] = model_plural_name
		return render_to_response('formulario_personas.html', {'formulario': formulario1,  'parametros': parametros,}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		

def alta_(request, model_name):
	"""
	llama a la funcion de alta con los parametros correspondientes al nombre de modelo recibido;
	estos son el modelo, el template a renderizar, el template de redireccion y los parametros a renderizar
	que son el nombre en plural y singular del modelo
	"""
	if request.user.has_perm('datos.add_'+model_name):
		try:
			model = nombresModelos[model_name]
		except KeyError:
			return HttpResponseRedirect('/404')
		model_plural_name = model()._meta.verbose_name_plural
		model_name = model()._meta.verbose_name
		template_to_redirect='/'+'datos2'+'/lista/'+model_name
		parametros = {}
		parametros['name'] = model_name
		parametros['plural_name'] = model_plural_name
		return alta(request,nombresFormularios[model_name],'formulario_datos2.html',template_to_redirect,parametros)
	else:
		return HttpResponseRedirect('/403')
		
def lista_(request,model_name):	
	"""
	llama a la funcion de lista con los parametros correspondientes al nombre de modelo recibido;
	estos son el modelo, el template a renderizar y los parametros a renderizar
	que son el nombre en plural y singular del modelo
	"""
	try:
		model = nombresModelos[model_name]
	except KeyError:
		return HttpResponseRedirect('/404')
	model_plural_name = model()._meta.verbose_name_plural
	model_name = model()._meta.verbose_name
	parametros = {}
	parametros['name'] = model_name
	parametros['plural_name'] = model_plural_name
	parametros['fields'] = model()._meta.fields
	objetos = model.objects.all()
	return lista(request, objetos,'lista_datos2.html', parametros)

def busqueda_(request,model_name):
	"""
	llama a la funcion de busqueda con los parametros correspondientes al nombre de modelo recibido;
	estos son el modelo, el template a renderizar, el id del input de busqueda, y los parametros a renderizar
	que son el nombre en plural y singular del modelo
	"""

	if request.POST.get('q', ''):
		valor = request.session['valor'] = request.POST.get('q', '')
	else:
		if request.session.get('valor', ''):
			valor = request.session['valor']
		else:
			valor = request.session['valor'] = ''
	
	try:
		model = nombresModelos[model_name]
	except KeyError:
		return HttpResponseRedirect('/404')

	if valor:			
		#creo listado de objetos Q, un Q por cada atributo del modelo, Q es una query atributo__starswith__=valor
		search_type = 'startswith'				
		Qs=[]		
		for field in model._meta.fields:	
			if (str(field.get_internal_type).find('ForeignKey')==-1):
				atributo_variable=field.name			
				filter = atributo_variable + '__' + search_type
				Qs.append(Q(**{ filter:valor}))
		qset = (
			reduce(operator.or_, Qs)
		)		
		objetos = model.objects.filter(qset).distinct()
	else:
		objetos = []

	model_plural_name = model()._meta.verbose_name_plural
	model_name = model()._meta.verbose_name
	parametros = {}
	parametros['name'] = model_name
	parametros['plural_name'] = model_plural_name
	parametros['fields'] = model()._meta.fields
	return lista(request, objetos,'lista_datos2.html', parametros)

	
def editar_(request, model_name, id):
	"""
	llama a la funcion de editar con los parametros correspondientes al nombre de modelo recibido;
	estos son el modelo, el template a renderizar y de redireccion, el id del objeto a editar, y los parametros a renderizar
	que son el nombre en plural y singular del modelo
	"""
	if request.user.has_perm('datos.change_'+model_name):
		try:
			model = nombresModelos[model_name]
		except KeyError:
			return HttpResponseRedirect('/404')
		model_plural_name = model()._meta.verbose_name_plural
		model_name = model()._meta.verbose_name
		parametros = {}
		parametros['name'] = model_name
		parametros['plural_name'] = model_plural_name
		parametros['fields'] = model()._meta.fields
		template_to_redirect='/'+'datos2'+'/lista/'+model_name
		return editar(request, model, nombresFormularios[model_name], id, template_to_redirect, "formulario_datos2.html", parametros) 
	else:
		return HttpResponseRedirect('/403')
		
def eliminar_(request, model_name, id):
	"""
	llama a la funcion de eliminar con los parametros correspondientes al nombre de modelo recibido,
	estos son el modelo y el id del objeto a eliminar
	"""	
	if request.user.has_perm('datos.delete_tipotelefono'):
		try:
			model = nombresModelos[model_name]
		except KeyError:
			return HttpResponseRedirect('/404')
		template_to_redirect = '/'+'datos2'+'/lista/'+model()._meta.verbose_name
		return eliminar(request, model, id, template_to_redirect)
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

		
def autocompletar_(request,model_name):
	try:
		model = nombresModelos[model_name]
	except KeyError:
		return HttpResponseRedirect('/404')
	return autocompletar(request,model)

	
def seleccionar(request,modelo, id_persona):
	dato=Persona.objects.get(id=id_persona)
	fotos=FotoPerfil.objects.filter(persona=dato)
	if fotos:
		fotos = fotos[fotos.count()-1]
	domicilios= Domicilio.objects.filter(persona = dato)
	telefonos= Telefono.objects.filter(persona = dato)
	delta = datetime.date.today() - dato.fecha_de_nacimiento
	delta = datetime.date.fromordinal(delta.days).year
	request.session['persona'] = dato
	return render_to_response('persona.html',{'dato':dato, 'edad':delta -1, 'domicilios':domicilios,'telefonos':telefonos, 'fotos':fotos},context_instance=RequestContext(request))	
	

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
	
def alta_domicilio(request):
	if request.user.has_perm('datos.add_'+'domicilio'):
		if request.method=='POST':
			formulario=PartialDomicilioForm(request.POST)
			if formulario.is_valid():
				domicilio=formulario.save(commit=False)
				domicilio.persona= Persona.objects.get(id=id_persona)
				domicilio.save()
				return HttpResponseRedirect('/datos2/seleccionar/persona/'+request.session['persona'])
		else:
			formulario=PartialDomicilioForm()
		return render_to_response('formulario_datos2.html', {'formulario': formulario, 'nombre': Telefono._meta.verbose_name_plural,'n': Telefono()._meta.verbose_name}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/datos2/seleccionar/persona/'+request.session['persona'])
		
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
		
def cargar_datos_profesionales(request):
	sucesos=[]
	if request.method=='POST':
		formulario=DatosProfesionalesForm(request.POST)
		if formulario.is_valid():
			profesional=formulario.save(commit=False)
			profesional.persona= Persona.objects.get(id=request.session['persona'])
			profesional.save()
			sucesos.append("Datos Profesionales asignados correctamente")
			return HttpResponseRedirect('/datos2/seleccionar/persona/'+request.session['persona'])
	else:
		formulario=DatosProfesionalesForm()
	return render_to_response('formulario_datos2.html', {'sucesos': sucesos,'formulario': formulario, 'nombre': 'datosProfesional','n': 'datoProfesional'}, context_instance=RequestContext(request))
