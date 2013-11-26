from django.conf.urls import patterns, include, url
from django.conf import settings


"""
from datos.models import Profesion
from django.conf.urls.defaults import *
from django.views.generic import *
"""

from views import *
from datos.views import *
from datos2.views import *
from usuarios.views import *
from clinica.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
admin.autodiscover()

#profesion_info = {"model": Profesion}


urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
	url(r'^403/$', 'HC.views.sin_permiso'),
	url(r'^login/$', login_usuario),
    # url(r'^HC/', include('HC.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	#(r'^profesiones/create/$', create_update.create_object, profesion_info),
	
	url(r'^carga/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
		
	
	url(r'^datos/alta/([a-z]+)$', 'datos.views.alta_'),
	url(r'^datos/lista/([a-z]+)$', 'datos.views.lista_'),
	url(r'^datos/editar/([a-z]+)/(\d+)$', 'datos.views.editar_'),
	url(r'^datos/eliminar/([a-z]+)/(\d+)$', 'datos.views.eliminar_'),
	url(r'^datos/busqueda/([a-z]+)$', 'datos.views.busqueda_'),
	url(r'^datos/lista/get_name/([a-z]+)/$', 'datos.views.autocompletar_', ),	
	
	
	#url(r'^datos2/alta/persona$',alta_persona),
	#url(r'^datos2/editar/persona/(\d+)$',editar_persona),
	url(r'^datos2/alta/telefono$', 'datos2.views.alta_telefono'),
	url(r'^datos2/alta/domicilio$', 'datos2.views.alta_domicilio'),
	url(r'^datos2/cargar_imagen$', 'datos2.views.cargar_imagen'),
	url(r'^datos2/alta/([a-z]+)$', 'datos2.views.alta_'),	
	url(r'^datos2/lista/([a-z]+)$', 'datos2.views.lista_'),
	url(r'^datos2/editar/([a-z]+)/(\d+)$', 'datos2.views.editar_'),
	url(r'^datos2/eliminar/([a-z]+)/(\d+)$', 'datos2.views.eliminar_'),
	url(r'^datos2/busqueda/([a-z]+)$', 'datos2.views.busqueda_'),
	url(r'^datos2/seleccionar/([a-z]+)/(\d+)$', 'datos2.views.seleccionar'),
	url(r'^datos2/lista/get_name/([a-z]+)/$', 'datos2.views.autocompletar_', ),
	url(r'^datos2/profesional/$', 'datos2.views.cargar_datos_profesionales', ),
	
	url(r'^usuarios/alta/$', nuevo_usuario),	
	url(r'^usuarios/salir/$', logout_view),
	url(r'^usuarios/lista/usuario/$', 'usuarios.views.lista_'),		
	url(r'^usuarios/bloqueo/([a-z]+)/(\d+)$', 'usuarios.views.bloqueo_usuario'),
	url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'pass_reset.html'}),
	url(r'password_changed/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'succes.html',}),
	url(r'^activar/$', 'usuarios.views.activar_usuario'),
	url(r'^usuarios/matriz_coordenadas/$', generar_matriz_html),
	url(r'^usuarios/matriz_coordenadas_pdf/$', generar_matriz_pdf),
    
	url(r'^clinica/lista/evolucion$', 'clinica.views.listar_evolucion'),
	url(r'^clinica/alta/evolucion$', 'clinica.views.alta_evolucion'),
	url(r'^clinica/lista/enfermeria$', 'clinica.views.listar_enfermeria'),
	url(r'^clinica/alta/enfermeria$', 'clinica.views.alta_enfermeria'),
    
	   # include the lookup urls
    (r'^admin/lookups/', include(ajax_select_urls)),
    (r'^admin/', include(admin.site.urls)),
    
    
    
	
)




