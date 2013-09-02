from abm.funciones import *
from models import *
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from stronghold.decorators import public
from django.contrib.auth.decorators import permission_required


def menu(request):
	return render_to_response('index.html')




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
				unicode("tipoestadocivil"):TipoEstadoCivil}




				
			


def alta_(request, modelo):
	#if request.user.has_module_perms('datos'):
	if request.user.has_perm('datos.add_'+modelo):
		return alta(request,nombresModelos[modelo],nombresFormularios[modelo],"datos",'formulario_datos.html')
	else:
		return HttpResponseRedirect('/403')

def lista_(request,modelo):
	return lista(request,nombresModelos[modelo],'lista_datos.html')

def editar_(request, modelo, id_profesion):
	if request.user.has_perm('datos.change_'+modelo):
		return editar(request, id_profesion, nombresModelos[modelo], nombresFormularios[modelo],"datos",'formulario_datos.html') 
	else:
		return HttpResponseRedirect('/403')


def eliminar_(request, modelo, id_domicilio):
	if request.user.has_perm('datos.delete_tipotelefono'):
		return eliminar(request,  nombresModelos[modelo], id_domicilio,"datos")	
	else:
		return HttpResponseRedirect('/403')


def busqueda_(request,modelo):
	return busqueda(request,nombresModelos[modelo],'lista_datos.html')
