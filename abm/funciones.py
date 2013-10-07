from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import operator
from django.db.models.fields.related import ForeignKey


def alta(request, formulario, template_to_render, template_to_redirect,parametros):
	"""
	renderiza el formulario en el template de formulario con los parametros recibidos
	valida formulario con datos recibidos del request POST, los guarda y redirige a template de redireccion
	"""
	if request.method=='POST':
		form=formulario(request.POST)
			
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(template_to_redirect)
	else:
		form=formulario()
	return render_to_response(template_to_render, {'formulario': form, 'parametros': parametros}, context_instance=RequestContext(request))


def lista(request, objetos, template_to_render, parametros):
	"""
	retorna un template con los valores por atributo de los objetos del modelo correspondiente, y los parametros recibidos
	"""	
	#creo "tabla de valores" del modelo, un arreglo conteniendo un arreglo por objecto, que contiene 
	#los valores de los atributos del modelo, para ser recorrido facilmente en el template
	registros=[]
	for objeto in objetos:
		valores=[]
		for field in objeto._meta.fields:
			valores.append(getattr(objeto,field.name))
		registros.append(valores)

	#creo paginador dentro del arreglo
	paginator = Paginator(registros, 5) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		datos = paginator.page(page)
	except PageNotAnInteger:     
		datos = paginator.page(1)
	except EmptyPage:       
		datos = paginator.page(paginator.num_pages)		

	return render_to_response(template_to_render, {'datos': datos, 'parametros': parametros,},
		context_instance=RequestContext(request))


def eliminar(request, modelo, id, template_to_redirect):
	"""
	elimina objeto del modelo recibido por parametro, correspondiente con el id recibido, redirige hacia template
	"""
	try:
		dato=modelo.objects.get(id=id)
		dato.delete()
	except Exception:
		pass
	return HttpResponseRedirect(template_to_redirect)
	
def editar(request, modelo, formulario, id, template_to_redirect, template_to_render, parametros):
	"""
	edita objeto del modelo recibido por parametro, correspondiente con el id recibido, redirige hacia template
	"""
	if request.method=='POST':
		dato = modelo.objects.get(id=id)
		formulario=formulario(request.POST, instance = dato)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect(template_to_redirect)
	else:
		result = modelo.objects.get(id=id)
		formulario = formulario(instance=result)
	return render_to_response(template_to_render, {'formulario': formulario,'parametros':parametros}, context_instance=RequestContext(request))


		
def autocompletar(request, modelo):
	if request.is_ajax():
		results = []
		query = request.GET.get('term', '') #jquery-ui.autocomplete parameter
		principal=modelo._meta.fields[1].name
		search_type = 'startswith'
		filter = principal + '__' + search_type			
		
		name_list = modelo.objects.filter(Q(**{filter:query}))#.values('id','descripcion', 'descripcionReducida')
		for descripcion in name_list:			
			descripcion_json = {}
			descripcion_json['id'] = descripcion.id			
			descripcion_json['value'] = getattr(descripcion,principal)
			results.append(descripcion_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
