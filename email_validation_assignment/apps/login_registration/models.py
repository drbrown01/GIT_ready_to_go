from __future__ import unicode_literals

from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, user):
		print user
		errors = []
		if len(user['name']) < 1:
			errors.append({'message':'Name field cannot be blank', 'tag': 'name'})
		if len(user['alias']) < 1:
			errors.append({'message':'Alias cannot be blank', 'tag': 'alias'})
		elif User.objects.filter(alias = user['alias']).exists():
			errors.append({'message':'Alias is taken', 'tag': 'alias'})
		if len(user['email']) < 1:
			errors.append({'message':'Email cannot be blank', 'tag': 'email'})
		elif not EMAIL_REGEX.match(user['email']):
			errors.append({'message':'Email not valid', 'tag': 'email'})
		if len(user['password']) < 1:
			errors.append({'message':'Password cannot be blank', 'tag': 'password'})
		elif len(user['password']) < 8:
			errors.append({'message':'Password must be at least 8 characters', 'tag': 'password'})
		elif user['password'] != user['confirm_password']:
			errors.append({'message':'Passwords do not match', 'tag': 'password'})
		if len(errors) > 0:
			return (False, errors)
		else:
			newUser = {
				'name': user['name'],
				'alias': user['alias'],
				'email': user['email'],
				'password': bcrypt.hashpw(user['password'].encode(), bcrypt.gensalt())
			}
			user = User.objects.create(**newUser)
			user.save()
			return (True, "registered", user.alias, user.id)

	def login(self, user):
		if len(user['email']) < 1 or len(user['password']) < 1:
			return (False, {'message':'Make sure email and password fields are filled in', 'tag': 'login'})
		try:
			logUser = User.objects.get(email=user['email'])
		except:
			return (False, {'message':'Invalid email or password', 'tag': 'login'})
		if logUser.password == bcrypt.hashpw(user['password'].encode(), logUser.password.encode()):
			return (True, "logged in", logUser.alias, logUser.id)
		else:
			return (False, {'message':'Invalid email or password', 'tag': 'login'})

class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=45)
	email = models.EmailField(max_length=254)
	password = models.CharField(max_length=254)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()
