#usr/bin/python
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def index (request):
	return render_to_response('index.html', context_instance=RequestContext(request))
def sin_permiso (request):
	return render_to_response('403.html')
