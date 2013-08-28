from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


def index (request):
	return render_to_response('index.html')
def sin_permiso (request):
	return render_to_response('403.html')
