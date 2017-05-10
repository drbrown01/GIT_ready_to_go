from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class EmailManager(models.Manager):
	def register(self, email):
		errors = []
		if len(email) == 0:
			errors.append("Email is required")
		elif not EMAIL_REGEX.match(email):
			errors.append("Email not valid")
		if len(errors) > 0:
			return (False, errors)
		else:
			print("inside else of models" )
			email = User.objects.create(email=email)
			print email
			email.save()
			return(True, email)

class User(models.Model):
	email = models.CharField(max_length=100)
	created_at = models.DateField(auto_now_add = True)
	updated_at = models.DateField(auto_now = True)
	objects = EmailManager()
