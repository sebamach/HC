# Create your views here.
from django.template import RequestContext
from clinica.models import *
from datos2.models import *
from datos.models import *
from usuarios.models import *
from abm.funciones import *
from forms import *

def listar_evolucion_doctor(request):
	"""
	retorna un template con los posteos realizados por DOCTORES en la hoja de Evolucion
	de doctores
	
	"""
	objetos = Evolucion_doctor.objects.filter(persona= request.session['persona'])	
	perfil = Perfil.objects.get(usuario=2)
	dato_profesional = DatosProfesionales.objects.get(persona= perfil.persona)
	
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
	return render_to_response('hoja_base.html', {'titulo':'Evolucion En Internado','datos': datos, 'dato_profesional':dato_profesional, 'form':  Evolucion_doctorForm, 'persona':persona},
		context_instance=RequestContext(request))



def alta_evolucion_internado(request):
	#instancio los parametros para la funcion de alta
	if request.method=='POST':
		form=Evolucion_doctorForm(request.POST)
			
		if form.is_valid():
			form = form.save(commit = False)
			form.persona = request.session['persona']
			form.save()
			messages.add_message(request, messages.ERROR, 'Se dio de ALTA el registro ' )
			
			return listar_evolucion_doctor(request)
	else:
		form=Evolucion_doctorForm()
		listar_evolucion_doctor(request)
	return listar_evolucion_doctor(request)

	
	
	
	

