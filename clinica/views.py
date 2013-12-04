#usr/bin/python
# -*- encoding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from clinica.models import *
from datos2.models import *
from datos.models import *
from usuarios.models import *
from django.contrib.auth.decorators import *
from abm.funciones import *
from forms import *
import time
from datetime import datetime
from usuarios.forms import CoordenadasForm
from usuarios.views import *

@user_passes_test(lambda u: u.groups.filter(name__startswith='HOJA').count() <> 0, login_url='/403')
def listar_evolucion(request):
	"""
	retorna un template con los posteos realizados por DOCTORES en la hoja de Evolucion
	de doctores
	
	"""
	objetos = Evolucion_doctor.objects.filter(persona= request.session['persona'])	
	perfil = Perfil.objects.get(usuario = request.user)
	dato_profesional = DatosProfesionales.objects.get(persona= perfil.persona)
	request.session['coordenadas']=generar_coordenadas()
	formc=CoordenadasForm()
	queryset = Q()
	
	filtro = Formulario_filtro_evolucionForm(request.POST) 
	try:
		firmante = request.POST['firmante']
	except:
		firmante = ''
	try:
		especialidad = request.POST['especialidad']
		
	except:
		especialidad=''
		
	try:
		f_desde = request.POST['fecha_desde']
	except:
		pass
	try:
		f_hasta = request.POST['fecha_hasta']
	except:
		f_hasta=datetime.today()
	try:
		diagnostico = request.POST['diagnostico']
	except:
		diagnostico=''
	
	if especialidad <>'':
		objetos=  objetos.filter (firma__datos_profesionales__especialidad = especialidad)
		messages.add_message(request, messages.ERROR, 'especialidad' )
	if firmante <> '':
		queryset.add(Q(firma=firmante), Q.AND)
		messages.add_message(request, messages.ERROR, 'firmante' )
	
	if diagnostico <> '':
		queryset.add(Q(diagnostico=diagnostico), Q.AND)
		messages.add_message(request, messages.ERROR, 'diagnostico' )

	objetos = objetos.filter(queryset)
#########################################
#creo paginador dentro del arreglo
	paginator = Paginator(objetos, 3) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		datos = paginator.page(page)
	except PageNotAnInteger:     
		datos = paginator.page(1)
	except EmptyPage:       
		datos = paginator.page(paginator.num_pages)		
	persona= request.session['persona']
	return render_to_response('hoja_base.html',
	{'titulo':'Evolucion En Internado',
	'datos': datos,
	'dato_profesional':dato_profesional,
	'form':  Evolucion_doctorForm, 'action':'/clinica/alta/evolucion',
	'hoja':'EVOLUCION',
	'evolucion': 'active',
	'filtro': Formulario_filtro_evolucionForm(request.POST),
	'accion_filtro':'/clinica/lista/evolucion',	
	'formc': formc},
	 context_instance=RequestContext(request))


@user_passes_test(lambda u: u.groups.filter(name='HOJA MEDICA').count() == 1 , login_url='/403')
def alta_evolucion(request):
	#instancio los parametros para la funcion de alta
	if request.method=='POST':
		form=Evolucion_doctorForm(request.POST)
		coordenada = request.POST["valor"]
		matriz = request.session['matriz']
		fila= request.session['coordenadas']['fila']
		columna = request.session['coordenadas']['columna']
	
		if coordenada.upper()== matriz[int(fila)][int(columna)]: 
			if form.is_valid():
				form = form.save(commit = False)
				form.persona = request.session['persona']
				perfil = Perfil.objects.get(usuario = request.user)
				form.firma= perfil.persona				
				try:
					form.save()
					messages.add_message(request, messages.ERROR, 'Se dio de ALTA el registro ' )
				except Exception, e:
					messages.add_message(request, messages.ERROR, 'Error al intentar guardar '+ str(e) )
			else:
				for errores in form.errors:
					messages.add_message(request, messages.ERROR, 'No se pudo de dar de alta por datos invalidos  ' + errores )
			return listar_evolucion(request)
		else:
			messages.add_message(request, messages.ERROR, coordenada.upper() + ' son distintas '+ matriz[int(fila)][int(columna)] )
			
	else:
		form=Evolucion_doctorForm(request)
		messages.add_message(request, messages.ERROR, coordenada + ' salio por el GET  '+ matriz[int(fila)][int(columna)] )
	return listar_evolucion(request)
 


"""
evolucion de internado enfermero
"""	
@user_passes_test(lambda u: u.groups.filter(name__startswith='HOJA').count() <> 0, login_url='/403')
def listar_enfermeria(request):
	"""
	retorna un template con los posteos realizados por ENFERMEROS en la hoja de Evolucion
	de enfermeria
	
	"""
	objetos = Evolucion_enfermeria.objects.filter(persona= request.session['persona'])	
	perfil = Perfil.objects.get(usuario = request.user)
	dato_profesional = DatosProfesionales.objects.get(persona= perfil.persona)
	request.session['coordenadas']=generar_coordenadas()
	formc=CoordenadasForm()
	queryset = Q()
	
	filtro = Formulario_filtro_enfermeriaForm(request.POST) 
	try:
		firmante = request.POST['firmante']
	except:
		firmante = ''
	try:
		especialidad = request.POST['especialidad']
		
	except:
		especialidad=''
		
	try:
		f_desde = request.POST['fecha_desde']
	except Exception, e:
		messages.add_message(request, messages.ERROR, str(e) )
	try:
		f_hasta = request.POST['fecha_hasta']
	except:
		f_hasta=datetime.today()
	try:
		diagnostico = request.POST['diagnostico']
	except:
		diagnostico=''
	
	if especialidad <>'':
		objetos=  objetos.filter (firma__datos_profesionales__especialidad = especialidad)
		messages.add_message(request, messages.ERROR, 'especialidad' )
	if firmante <> '':
		queryset.add(Q(firma=firmante), Q.AND)
		messages.add_message(request, messages.ERROR, 'firmante' )
	
	if diagnostico <> '':
		queryset.add(Q(diagnostico=diagnostico), Q.AND)
		messages.add_message(request, messages.ERROR, 'diagnostico' )

	objetos = objetos.filter(queryset)
#########################################
#creo paginador dentro del arreglo
	paginator = Paginator(objetos, 3) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		datos = paginator.page(page)
	except PageNotAnInteger:     
		datos = paginator.page(1)
	except EmptyPage:       
		datos = paginator.page(paginator.num_pages)		
	persona= request.session['persona']
	return render_to_response('hoja_base.html',
	{'titulo':'Evolucion Enfermeria',
	'datos': datos,
	'dato_profesional':dato_profesional,
	'form':  Evolucion_enfermeriaForm, 'action':'/clinica/alta/evolucion',
	'hoja':'EVOLUCION ENFERMERIA',
	'enfermeria': 'active',
	'filtro': Formulario_filtro_enfermeriaForm(request.POST),
	'accion_filtro':'/clinica/lista/enfermeria',	
	'formc': formc},
	 context_instance=RequestContext(request))




@user_passes_test(lambda u: u.groups.filter(name='HOJA ENFERMERIA').count() == 1 , login_url='/403')
def alta_enfermeria(request):
	#instancio los parametros para la funcion de alta
	if request.method=='POST':
		form=Evolucion_enfermeriaForm(request.POST)
			
		if form.is_valid():
			form = form.save(commit = False)
			form.persona = request.session['persona']
			perfil = Perfil.objects.get(usuario = request.user)
			form.firma= perfil.persona		
			try:
				form.save()
				messages.add_message(request, messages.ERROR, 'Se dio de ALTA el registro ' )
			except:
				pass
			
			
			return listar_enfermeria(request)
	else:
		form=Evolucion_enfermeriaForm()
		listar_enfermeria(request)
	return listar_enfermeria(request)
	

"""
Prescripciones Medicas
"""	
@user_passes_test(lambda u: u.groups.filter(name__startswith='HOJA').count() <> 0, login_url='/403')
def listar_prescripcion(request):
	"""
	retorna un template con los posteos realizados por medicos en la hoja de Prescripciones medicas
	
	"""
	objetos = Prescripciones_medicas.objects.filter(persona= request.session['persona'])	
	perfil = Perfil.objects.get(usuario = request.user)
	dato_profesional = DatosProfesionales.objects.get(persona= perfil.persona)
	request.session['coordenadas']=generar_coordenadas()
	formc=CoordenadasForm()
	queryset = Q()
	
	filtro = Formulario_filtro_prescripcionesForm(request.POST) 
	try:
		firmante = request.POST['firmante']
	except:
		firmante = ''
	try:
		especialidad = request.POST['especialidad']
		
	except:
		especialidad=''
		
	try:
		f_desde = request.POST['fecha_desde']
	except:
		pass
	try:
		f_hasta = request.POST['fecha_hasta']
	except:
		f_hasta=datetime.today()
	try:
		diagnostico = request.POST['diagnostico']
	except:
		diagnostico=''
	
	if especialidad <>'':
		objetos=  objetos.filter (firma__datos_profesionales__especialidad = especialidad)
		messages.add_message(request, messages.ERROR, 'especialidad' )
	if firmante <> '':
		queryset.add(Q(firma=firmante), Q.AND)
		messages.add_message(request, messages.ERROR, 'firmante' )
	
	if diagnostico <> '':
		queryset.add(Q(diagnostico=diagnostico), Q.AND)
		messages.add_message(request, messages.ERROR, 'diagnostico' )

	objetos = objetos.filter(queryset)
#########################################
#creo paginador dentro del arreglo
	paginator = Paginator(objetos, 3) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		datos = paginator.page(page)
	except PageNotAnInteger:     
		datos = paginator.page(1)
	except EmptyPage:       
		datos = paginator.page(paginator.num_pages)		
	persona= request.session['persona']
	return render_to_response('hoja_base.html',
	{'titulo':'Evolucion Enfermeria',
	'datos': datos,
	'dato_profesional':dato_profesional,
	'form':  Prescripciones_medicasForm, 'action':'/clinica/alta/prescripcion',
	'hoja':'PRESCRIPCIONES MEDICAS',
	'prescripciones': 'active',
	'filtro': Formulario_filtro_prescripcionesForm(request.POST),
	'accion_filtro':'/clinica/lista/prescripcion',	
	'formc': formc},
	 context_instance=RequestContext(request))




@user_passes_test(lambda u: u.groups.filter(name='HOJA').count() == 1 , login_url='/403')
def alta_prescripcion(request):
	#instancio los parametros para la funcion de alta
	if request.method=='POST':
		form=Evolucion_prescripcionForm(request.POST)
			
		if form.is_valid():
			form = form.save(commit = False)
			form.persona = request.session['persona']
			perfil = Perfil.objects.get(usuario = request.user)
			form.firma= perfil.persona		
			try:
				form.save()
				messages.add_message(request, messages.ERROR, 'Se dio de ALTA el registro ' )
			except:
				pass
			
			
			return listar_prescripcion(request)
	else:
		form=Evolucion_prescripcionForm()
		listar_prescripcion(request)
	return listar_prescripcion(request)
	
	
	



