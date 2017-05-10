from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ALPHA_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX1 = re.compile(r'.*?\d')
PASSWORD_REGEX2 = re.compile(r'.*?[A-Z]')
PASSWORD_REGEX3 = re.compile(r'.*?[a-z]')
PASSWORD_REGEX4 = re.compile(r'.*?[\$\!\?\%\&]')
# .*?\d    checks for at least one digit
# .*?[A-Z] checks for at least one uppercase letter
# .*?[a-z] checks for at least one lowercase letter
# .*?[!?%&_] checks for at least one special character

class UserManager(models.Manager):
	def register(self, user):
		print user
		errors = []
		if len(user['first_name']) < 2:
			errors.append({'message':'First name must be at least 2 characters', 'tag': 'first_name'})
		elif not ALPHA_REGEX.match(user['first_name']):
			errors.append({'message':'First name can only contain letters', 'tag': 'first_name'})
		if len(user['last_name']) < 2:
			errors.append({'message':'Last name must be at least 2 characters', 'tag': 'last_name'})
		elif not ALPHA_REGEX.match(user['last_name']):
			errors.append({'message':'Last name can only contain letters', 'tag': 'last_name'})
		if len(user['username']) < 1:
			errors.append({'message':'Username cannot be blank', 'tag': 'username'})
		elif User.objects.filter(username = user['username']).exists():
			errors.append({'message':'Username is taken', 'tag': 'username'})
		if len(user['email']) < 1:
			errors.append({'message':'Email cannot be blank', 'tag': 'email'})
		elif not EMAIL_REGEX.match(user['email']):
			errors.append({'message':'Email not valid', 'tag': 'email'})
		if len(user['password']) < 1:
			errors.append({'message':'Password cannot be blank', 'tag': 'password'})
		elif len(user['password']) < 8:
			errors.append({'message':'Password must be at least 8 characters', 'tag': 'password'})
		elif not PASSWORD_REGEX1.match(user['password']):
			errors.append({'message':'Password must contain at least 1 number', 'tag': 'password'})
		elif not PASSWORD_REGEX2.match(user['password']):
			errors.append({'message':'Password must contain at least 1 Uppercase letter', 'tag': 'password'})
		elif not PASSWORD_REGEX3.match(user['password']):
			errors.append({'message':'Password must contain at least 1 lowercase letter', 'tag': 'password'})
		elif not PASSWORD_REGEX4.match(user['password']):
			errors.append({'message':'Password must contain at least 1 special character i.e. $!?%&', 'tag': 'password'})
		elif user['password'] != user['confirm_password']:
			errors.append({'message':'Passwords do not match', 'tag': 'password'})
		if len(user['birthdate']) < 1:
			errors.append({'message':'Birthdate is required', 'tag': 'birthdate'})
		else:
			birthday = datetime.strptime(user['birthdate'], '%Y-%m-%d')
			today = datetime.now()
			age = today - timedelta(days=4748)
			if today < birthday:
				errors.append({'message':"You can't be born in the future!", 'tag': 'birthdate'})
			elif age < birthday:
				errors.append({'message':'You must be at least 13 years of age to register', 'tag': 'birthdate'})
		if len(errors) > 0:
			return (False, errors)
		else:
			newUser = {
				'first_name': user['first_name'],
				'last_name': user['last_name'],
				'username': user['username'],
				'email': user['email'],
				'password': bcrypt.hashpw(user['password'].encode(), bcrypt.gensalt()),
				'birthdate': user['birthdate']
			}
			user = User.objects.create(**newUser)
			user.save()
			return (True, "registered", user.username)

	def login(self, user):
		if len(user['email']) < 1 or len(user['password']) < 1:
			return (False, {'message':'Make sure email and password fields are filled in', 'tag': 'login'})
		try:
			logUser = User.objects.get(email=user['email'])
		except:
			return (False, {'message':'Invalid email or password', 'tag': 'login'})
		if logUser.password == bcrypt.hashpw(user['password'].encode(), logUser.password.encode()):
			return (True, "logged in", logUser.username)
		else:
			return (False, {'message':'Invalid email or password', 'tag': 'login'})

class User(models.Model):
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	username = models.CharField(max_length=45)
	email = models.EmailField(max_length=254)
	password = models.CharField(max_length=254)
	birthdate = models.DateField(auto_now=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
