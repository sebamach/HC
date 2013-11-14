#FFFFFF# Create your views here.
from models import *
from datos2.models import *
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
import string
import random
from django.core.mail import EmailMessage 
from django.db import transaction


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def coor_generator(size=2, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))



@transaction.commit_on_success	
def nuevo_usuario(request):
	clave=''
	errores=[]
	mensaje=''
	matriz=[]
	if request.user.has_perm('usuarios.add_usuario'):
		if request.method=='POST':
			formulario_user=PartialUsuarioForm(request.POST)
			formulario_perfil=PerfilForm()
			tarjeta = TarjetaForm()
			if formulario_user.is_valid():
				matriz = generar_matriz()
				clave = id_generator()
				if not Perfil.objects.filter(persona=request.session['persona']):
					usuario = User.objects.create_user(request.POST['username'], '', str(clave))
					usuario.is_active=False
					usuario.is_superuser=True
					usuario.set_password = clave
					usuario.save()
					perfil = formulario_perfil.save(commit=False)
					tarjeta = tarjeta.save(commit=False)
					perfil.usuario = usuario
					perfil.persona = request.session['persona']
					perfil.ultimoUsuario = request.user
					tarjeta.usuario = usuario
					tarjeta.ultimoUsuario = request.user
					tarjeta.cordenadas = matriz
					try:
						tarjeta.save()
						perfil.save()
						#destino = DatosProfesionales.objects.get(persona=perfil.persona)
						#enviar_correo('Creacion de Usuario', clave , 'ciberarcadia@hotmail.com')
						mensaje='Se enviaron datos de usuario por mail '+  clave
					
					except:
						mensaje	='No se pudo crear usuario'
					messages.add_message(request, messages.ERROR, mensaje )	
					return HttpResponseRedirect('/datos2/seleccionar/persona/'+str(request.session['persona'].id))
				else:
					messages.add_message(request, messages.ERROR, 'Ya Existe un usuairo para esa persona' )
			else:
				messages.add_message(request, messages.ERROR, 'Nombre de Usuario NO VALIDO' )
			return render_to_response('formulario_usuarios.html', {'formulario': PartialUsuarioForm,  'nombre': "Usuarios",'n': "usuario", 'modulo': "usuario", 'errores':errores}, context_instance=RequestContext(request))
		else:
			formulario_user=PartialUsuarioForm()
			
		return render_to_response('formulario_usuarios.html', {'errores':errores,'formulario': PartialUsuarioForm,  'nombre': "Usuarios",'n': "usuario", 'modulo': "usuario",}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		
	

def lista_(request):
	return lista(request,User,'lista_usuarios.html',parametros=['hola'])
	

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
				login(request,acceso)
				return HttpResponseRedirect('/password_change/')
			
	else:
		formulario=AuthenticationForm()
	return render_to_response('login_usuarios.html', {'formulario': formulario}, context_instance=RequestContext(request))
	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def generar_matriz():
	matriz=[]
	for i in range (10):
		matriz.append([])
		for j in range (10):
			matriz[i].append(coor_generator())
	return matriz

def enviar_correo (asunto, mensaje, destino):
	email = EmailMessage(asunto, mensaje, to=[destino])
	#Agregamos una variable 'email' y le pasamos los valores del Asunto, Mensaje y el correo destinatario
	email.send()
	
def activar_usuario (request):
	usuario =  request.user
	usuario.is_active= True
	
	usuario.save()
	messages.add_message(request, messages.ERROR, 'listo ya esta activado ' + str(usuario) )
	return HttpResponseRedirect('/')
