#usr/bin/python
# -*- encoding: utf-8 -*-

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
from django.contrib.auth.decorators import *
import string
import random
from django.core.mail import EmailMessage 
from django.db import transaction
from cPickle import loads, dumps
#import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def coor_generator(size=2, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def coor_generator2(size=1, chars=string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@transaction.commit_on_success
@user_passes_test(lambda u: u.groups.filter(name='USUARIOS').count() == 1 , login_url='/403')	
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
					usuario = User.objects.create_user(generar_username(request), '', str(clave))
					usuario.is_active=False
					usuario.is_superuser=False
					usuario.set_password = clave
					usuario.save()
					perfil = formulario_perfil.save(commit=False)
					tarjeta = tarjeta.save(commit=False)
					perfil.usuario = usuario
					perfil.persona = request.session['persona']
					perfil.ultimoUsuario = request.user
					tarjeta.usuario = usuario
					tarjeta.ultimoUsuario = request.user
					tarjeta.cordenadas = dumps(matriz)
					try:
						tarjeta.save()
						perfil.save()
						#destino = DatosProfesionales.objects.get(persona=perfil.persona)
						#enviar_correo('Creacion de Usuario', clave , 'ciberarcadia@hotmail.com', request)
						mensaje='Se enviaron datos de usuario por mail '+  clave
					
					except Exception, e:
						mensaje	='No se pudo crear usuario' + str(e)
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
		
def generar_username(request):
	inicial = request.session['persona'].nombre[:1]	
	apellido = request.session['persona'].apellido.replace(" ", "")
	pre_username = inicial + apellido
	lista = User.objects.filter(username__startswith=pre_username).order_by('-username')
	if lista.count()<>0:		
		last_username = lista[0].username.encode('utf-8')
		digito=re.findall('\d+', last_username)
		try:
			numero=int(digito[0])+1
		except:
			numero=1
		username = pre_username + str(numero)
	else:
		username = pre_username	
	return username
		
	
@user_passes_test(lambda u: u.groups.filter(name='USUARIOS').count() == 1 , login_url='/403')
def lista_usuarios(request):	
	"""
	llama a la funcion de lista con los parametros correspondientes al nombre de modelo recibido;
	estos son el modelo, el template a renderizar y los parametros a renderizar
	que son el nombre en plural y singular del modelo
	"""
	model = User
	model_plural_name = model()._meta.verbose_name_plural
	model_name = model()._meta.verbose_name
	parametros = {}
	parametros['name'] = model_name
	parametros['plural_name'] = model_plural_name
	parametros['fields'] = model()._meta.fields
	objetos = model.objects.all()
	return lista(request, objetos,'lista_usuarios.html', parametros)
	
@user_passes_test(lambda u: u.groups.filter(name='USUARIOS').count() == 1 , login_url='/403')
def editar_(request, modelo, id_user):
	if request.user.has_perm('usuarios.change_usuario'):
		return editar(request, id_user, User, Perfil,"usuarios",'formulario_datos.html') 
	else:
		return HttpResponseRedirect('/403')
		
@user_passes_test(lambda u: u.groups.filter(name='USUARIOS').count() == 1 , login_url='/403')
def bloqueo_usuario(request, id_user):
	dato= User.objects.get(id=id_user)
	if dato.is_active == 1:
		dato.is_active =0
	else:
		dato.is_active=1
	dato.save()
	return HttpResponseRedirect('/usuarios/lista/usuario/')
	
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
				if not usuario=='admin':
					tarjeta = Tarjeta.objects.get(usuario=request.user)
					matriz = loads(tarjeta.cordenadas.encode('utf-8'))
					request.session['matriz']=matriz
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

def generar_coordenadas():
	coordenadas={}
	coordenadas['fila']= coor_generator2()
	coordenadas['columna']= coor_generator2()
	coordenadas['letra']= chr(65+ int(coordenadas['columna']))
	return coordenadas
	

def generar_matriz():
	matriz=[]
	for i in range (10):
		matriz.append([])
		for j in range (10):
			matriz[i].append(coor_generator())
	return matriz
	
def generar_matriz_ascii(matriz):
	string=""
	for k in range (10):
		string = string + "  " + str(k)
	string = string + '\n'
	for i in range (10):		
		if i<>0 or i<>9:
			string = string + '\n'
		string = string + str(i) + " "
		for j in range (10):
			string = string + matriz[i][j] + " "
	return string
	
def generar_matriz_html(request):
	letras={}
	for k in range (10):
		letras [k]=chr(65+k)
		
		
	return render_to_response('tabla_matriz.html',{"letras":letras},context_instance=RequestContext(request) )
	
def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def generar_matriz_pdf(request):
    html = render_to_string('tabla_matriz.html', {'pagesize':'A4'}, context_instance=RequestContext(request))
    return generar_pdf(html)
	

def enviar_correo (asunto, mensaje, destino, request):
	html = render_to_string('tabla_matriz.html', {'pagesize':'A4'}, context_instance=RequestContext(request))
	out = StringIO.StringIO()
	pdf = pisa.CreatePDF(StringIO.StringIO(html), out)
	email = EmailMessage(asunto, mensaje, to=[destino])
	#Agregamos una variable 'email' y le pasamos los valores del Asunto, Mensaje y el correo destinatario
	email.attach('agreement.pdf', out.getvalue(), 'application/pdf')
	email.send()
	
def activar_usuario (request):
	usuario =  request.user
	usuario.is_active= True
	
	usuario.save()
	messages.add_message(request, messages.ERROR, 'listo ya esta activado ' + str(usuario) )
	return HttpResponseRedirect('/')
