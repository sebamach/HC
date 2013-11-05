from django.forms import ModelForm
from django import forms

from models import *


class PerfilForm(ModelForm):
	class Meta:
		model = Perfil
		

class TarjetaForm(ModelForm):
	class Meta:
		model = Tarjeta		

class PartialUsuarioForm(ModelForm):
	class Meta:
		model = User
		exclude = ('password', 'first_name','last_name','email','is_staff', 'is_active','date_joined','last_login','is_superuser',)	


# Create your models here.
