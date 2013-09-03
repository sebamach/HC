from django.conf.urls import patterns, include, url


"""
from datos.models import Profesion
from django.conf.urls.defaults import *
from django.views.generic import *
"""

from views import *
from datos.views import *
from datos2.views import *
from usuarios.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
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
		
	
	url(r'^datos/alta/([a-z]+)$', 'datos.views.alta_'),
	url(r'^datos/lista/([a-z]+)$', 'datos.views.lista_'),
	url(r'^datos/editar/([a-z]+)/(\d+)$', 'datos.views.editar_'),
	url(r'^datos/eliminar/([a-z]+)/(\d+)$', 'datos.views.eliminar_'),
	url(r'^datos/busqueda/([a-z]+)$', 'datos.views.busqueda_'),
	
	url(r'^datos2/alta/persona$',alta_persona),
	url(r'^datos2/editar/persona/(\d+)$',editar_persona),
	url(r'^datos2/alta/([a-z]+)$', 'datos2.views.alta_'),
	url(r'^datos2/lista/([a-z]+)$', 'datos2.views.lista_'),
	url(r'^datos2/editar/([a-z]+)/(\d+)$', 'datos2.views.editar_'),
	url(r'^datos2/eliminar/([a-z]+)/(\d+)$', 'datos2.views.eliminar_'),
	url(r'^datos2/busqueda/([a-z]+)$', 'datos2.views.busqueda_'),
	
	url(r'^usuarios/alta/$', nuevo_usuario),	
	url(r'^usuarios/salir/$', logout_view),
	url(r'^usuarios/lista/usuario/$', 'usuarios.views.lista_'),		
	url(r'^usuarios/bloqueo/([a-z]+)/(\d+)$', 'usuarios.views.bloqueo_usuario'),
	url(r'password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'pass_reset.html'}),
	url(r'^password-changed/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'succes.html'}),
    
	
)




