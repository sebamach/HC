# Create your views here.
from models import *
from forms import *
from abm.funciones import *
from django.contrib.auth.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from stronghold.decorators import public
from django.contrib.auth.decorators import permission_required

def nuevo_usuario(request):
	if request.user.has_perm('usuarios.add_usuario'):
		if request.method=='POST':
			formulario_user=UserCreationForm(request.POST)
			formulario_perfil = PerfilForm(request.POST)
			if formulario_user.is_valid() and formulario_perfil.is_valid():
				usuario = formulario_user.save()
				perfil = formulario_perfil.save(commit=False)
				perfil.usuario = usuario
				perfil.save()			
				return lista(request,User,'lista_usuarios.html')
		else:
			formulario_user=UserCreationForm()
			formulario_perfil=PerfilForm()
		return render_to_response('formulario_usuarios.html', {'formulario': formulario_user, 'formulario_perfil': formulario_perfil, 'nombre': "Usuarios",'n': "usuario", 'modulo': "usuario"}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		
	

def lista_(request):
	return lista(request,User,'lista_usuarios.html')
	

def editar_(request, modelo, id_user):
	if request.user.has_perm('usuarios.change_usuario'):
		return editar(request, id_user, User, Perfil,"usuarios",'formulario_datos.html') 
	else:
		return HttpResponseRedirect('/403')
		
@permission_required('usuarios.can_change','/403')
def bloqueo_usuario(request,modelo,id_user):
	dato= User.objects.get(id=id_user)
	if dato.is_active == 1:
		dato.is_active =0
	else:
		dato.is_active=1
	dato.save()
	return lista(request,User,'lista_usuarios.html')
	
@public
def login_usuario(request):
	if request.method=='POST':
		formulario= AuthenticationForm(request.POST)
		usuario= request.POST['username']
		clave= request.POST['password']
		acceso=authenticate(username=usuario,password=clave)
		if acceso is not None:
			if acceso.is_active:
				login(request,acceso)
				return HttpResponseRedirect('/')
			
			
	else:
		formulario=AuthenticationForm()
	return render_to_response('login_usuarios.html', {'formulario': formulario}, context_instance=RequestContext(request))
	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

	
