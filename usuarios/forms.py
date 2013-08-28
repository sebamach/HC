from django.forms import ModelForm
from django import forms
from models import *


class PerfilForm(ModelForm):
	class Meta:
		model = Perfil
		exclude = ('usuario',)
	
	


# Create your models here.
