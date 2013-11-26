from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
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
		exclude = ('username','password', 'first_name','last_name','email','is_staff', 'is_active','date_joined','last_login','is_superuser','user_permissions',)	
	
class CoordenadasForm(forms.Form):
	valor = forms.CharField(max_length=2)
	

# Create your models here.
