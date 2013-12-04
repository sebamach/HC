#usr/bin/python
# -*- encoding: utf-8 -*-
from abm.funciones import *
from models import *
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from stronghold.decorators import public
from django.contrib.auth.decorators import *
#from dajax.core import Dajax
#from dajaxice.decorators import dajaxice_register
#from dajaxice.utils import deserialize_form

nombresFormularios={unicode("titulo"):TituloForm,
					unicode("especialidad"):EspecialidadForm,
					unicode("pais"):PaisForm,
					unicode("provincia"):ProvinciaForm,
					unicode("localidad"):LocalidadForm,
					unicode("tiposexo"):TipoSexoForm,
					unicode("tipodocumento"):TipoDocumentoForm,
					unicode("tipopersona"):TipoPersonaForm,
					unicode("tipodomicilio"):TipoDomicilioForm,
					unicode("tipotelefono"):TipoTelefonoForm,
					unicode("cie"):Cie10Form,
					unicode("tipoestadocivil"):TipoEstadoCivilForm}
					
nombresModelos={unicode("titulo"):Titulo,
				unicode("especialidad"):Especialidad,
				unicode("pais"):Pais,
				unicode("provincia"):Provincia,
				unicode("localidad"):Localidad,
				unicode("tiposexo"):TipoSexo,
				unicode("tipodocumento"):TipoDocumento,
				unicode("tipopersona"):TipoPersona,
				unicode("tipodomicilio"):TipoDomicilio,
				unicode("tipotelefono"):TipoTelefono,
				unicode("cie"):Cie10,
				unicode("tipoestadocivil"):TipoEstadoCivil}



@user_passes_test(lambda u: u.groups.filter(name='PARAMETROS').count() == 1, login_url='/403')
def alta_(request, model_name):
	"""
	llama a la funcion de alta con los parametros correspondientes al nombre de modelo recibido;
	estos son el modelo, el template a renderizar, el template de redireccion y los parametros a renderizar
	que son el nombre en plural y singular del modelo
	"""
	#if request.user.has_module_perms('datos'):
	if request.user.has_perm('datos.add_'+model_name):
		model = nombresModelos[model_name]
		model_plural_name = model()._meta.verbose_name_plural
		model_name = model()._meta.verbose_name
		template_to_redirect='/'+'datos'+'/lista/'+model_name
		parametros = {}
		parametros['name'] = model_name
		parametros['plural_name'] = model_plural_name
		return alta(request,nombresFormularios[model_name],'formulario_datos.html',template_to_redirect,parametros)
	else:
		return HttpResponseRedirect('/403')

def lista_(request,model_name):	
	"""
	llama a la funcion de lista con los parametros correspondientes al nombre de modelo recibido;
	estos son el modelo, el template a renderizar y los parametros a renderizar
	que son el nombre en plural y singular del modelo
	"""
	model = nombresModelos[model_name]
	model_plural_name = model()._meta.verbose_name_plural
	model_name = model()._meta.verbose_name
	parametros = {}
	parametros['name'] = model_name
	parametros['plural_name'] = model_plural_name
	parametros['fields'] = model()._meta.fields
	objetos = model.objects.all()
	return lista(request, objetos,'lista_datos.html', parametros)


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
	
	model = nombresModelos[model_name]

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
	return lista(request, objetos,'lista_datos.html', parametros)
	
@user_passes_test(lambda u: u.groups.filter(name='PARAMETROS').count() == 1, login_url='/403')
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
		template_to_redirect='/'+'datos'+'/lista/'+model_name
		return editar(request, model, nombresFormularios[model_name], id, template_to_redirect, "formulario_datos.html", parametros) 
	else:
		return HttpResponseRedirect('/403')

@user_passes_test(lambda u: u.groups.filter(name='PARAMETROS').count() == 1, login_url='/403')
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
		template_to_redirect = '/'+'datos'+'/lista/'+model()._meta.verbose_name
		return eliminar(request, model, id, template_to_redirect)
	else:
		return HttpResponseRedirect('/403')

def autocompletar_(request,model_name):
	try:
		model = nombresModelos[model_name]
	except KeyError:
		return HttpResponseRedirect('/404')
	return autocompletar(request,model)



