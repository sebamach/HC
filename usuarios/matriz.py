#usr/bin/python
# -*- encoding: utf-8 -*-
from stronghold.decorators import public
from django.contrib.auth.decorators import permission_required
import string
import random
from django.core.mail import EmailMessage 

class matriz():
	__init__ ():
		
	def generar ():
		coor_generator
		
		
	def __coor_generator(size=2, chars=string.ascii_uppercase + string.digits):
			return ''.join(random.choice(chars) for x in range(size))
			