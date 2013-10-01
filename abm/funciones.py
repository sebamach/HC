from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import operator
from django.db.models.fields.related import ForeignKey





def alta(request, clase_name, form_name, modulo, pagina):
	if request.method=='POST':
		formulario=form_name(request.POST)
		for field in formulario:
			field = field.upper
			
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/'+modulo+'/lista/'+clase_name()._meta.verbose_name)
	else:
		formulario=form_name()
	return render_to_response(pagina, {'formulario': formulario, 'nombre': clase_name()._meta.verbose_name_plural,'n': clase_name()._meta.verbose_name}, context_instance=RequestContext(request))


def lista(request, clase_name, pagina):
	datos_lista = clase_name.objects.all()
	
	
	lista_value_objects=[]
	for dato_lista in datos_lista:
		lista_value_object=[]
		for field in dato_lista._meta.fields:
			lista_value_object.append(field.value_to_string(dato_lista))
		lista_value_objects.append(lista_value_object)
	
	
	#field=dir(datos_lista[0]._meta.fields[0])
	
	paginator = Paginator(datos_lista, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		datos = paginator.page(page)
	except PageNotAnInteger:
     
		datos = paginator.page(1)
	except EmptyPage:
       
		datos = paginator.page(paginator.num_pages)		

	return render_to_response(pagina, {'datos': datos,'nombre': clase_name()._meta.verbose_name_plural, 'n': clase_name()._meta.verbose_name, 'fields': clase_name()._meta.fields, 'values_table':lista_value_objects},
							context_instance=RequestContext(request))

def eliminar(request, clase_name, id_domicilio, modulo):
	try:
		dato=clase_name.objects.get(id=id_domicilio)
		dato.delete()
	except Exception:
		pass
	return HttpResponseRedirect('/'+modulo+'/lista/'+clase_name()._meta.verbose_name)
	
def editar(request, id_domicilio, clase_name, form_name, modulo, pagina):

	if request.method=='POST':
		dato = clase_name.objects.get(id=id_domicilio)
		formulario=form_name(request.POST, instance = dato)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/'+modulo+'/lista/'+clase_name()._meta.verbose_name)
	else:
		result = clase_name.objects.get(id=id_domicilio)
		formulario = form_name(instance=result)
	return render_to_response(pagina, {'formulario': formulario, 'nombre': clase_name()._meta.verbose_name_plural,'n': clase_name()._meta.verbose_name}, context_instance=RequestContext(request))

def busqueda(request, clase_name, pagina):
	query = request.GET.get('q', '')
	if query:		
	
		#creo listado de objetos Q, un Q por cada atributo del modelo
		
		search_type = 'startswith'				
		Qs=[]		
		for field in clase_name._meta.fields:	
			if (str(field.get_internal_type).find('ForeignKey')==-1):
				atributo_variable=field.name			
				filter = atributo_variable + '__' + search_type
				Qs.append(Q(**{ filter:query}))
		qset = (
			reduce(operator.or_, Qs)
		)
		
		resultados = clase_name.objects.filter(qset).distinct()
	else:
		resultados = []
		
	paginator = Paginator(resultados, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		datos = paginator.page(page)
	except PageNotAnInteger:
     
		datos = paginator.page(1)
	except EmptyPage:
       
		datos = paginator.page(paginator.num_pages)
	return render_to_response(pagina, {'datos': datos,'nombre': clase_name()._meta.verbose_name_plural,'n': clase_name()._meta.verbose_name},
							context_instance=RequestContext(request))
		
def autocompletar(request, clase_name):
	if request.is_ajax():
		results = []
		q = request.GET.get('term', '') #jquery-ui.autocomplete parameter
		name_list = clase_name.objects.filter(Q(descripcion__startswith = q )|Q(descripcionReducida__startswith = q)).values('id','descripcion', 'descripcionReducida')[:10]
		for descripcion in name_list:
			descripcion_json = {}
			descripcion_json['id'] = descripcion['id']
			descripcion_json['value'] = descripcion['descripcion']
			results.append(descripcion_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
