from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q


def alta(request, clase_name, form_name, modulo, pagina):
	if request.method=='POST':
		formulario=form_name(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/'+modulo+'/lista/'+clase_name()._meta.verbose_name)
	else:
		formulario=form_name()
	return render_to_response(pagina, {'formulario': formulario, 'nombre': clase_name()._meta.verbose_name_plural,'n': clase_name()._meta.verbose_name}, context_instance=RequestContext(request))


def lista(request, clase_name, pagina):
	datos = clase_name.objects.all()
	return render_to_response(pagina, {'datos': datos,'nombre': clase_name()._meta.verbose_name_plural,'n': clase_name()._meta.verbose_name},
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
	return render_to_response(pagina, {'formulario': formulario}, context_instance=RequestContext(request))
