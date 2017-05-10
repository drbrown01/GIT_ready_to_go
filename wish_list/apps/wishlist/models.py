from __future__ import unicode_literals

from django.db import models
import re, bcrypt
# Create your models here.

class UserManager(models.Manager):
	def loginvalid(self, request, email, password):
		print "login valid!"
		print email
		print password
		error = []

		if email:
			user = Users.objects.filter(email=email)
			if user:
				user = Users.objects.get(email = email)
				if bcrypt.hashpw(password.encode('utf-8'), user.hashedpw.encode('utf-8')) == user.hashedpw:
					return True
				else:
					error.append("Password incorrect")
			else:
				error.append("User does not exist")
		else:
			error.append("Please enter an email")
		return error


	def registervalid(self, name, username, email, password, repass):
		print "register valid!"
		error = []

		#Check all field is filled
		if name and email and password and repass and username:
			print "good job everything is filled in"

			if Users.objects.filter(email=email):
				error.append("User already exist! Please login instead!")
				return error

			if re.search(r'^[a-zA-Z]+$', name) == False or len(name)<2:
				error.append("Name invalid! Must be at least 8 characters long and consist of only letters")

			if Users.objects.filter(email=email):
				error.append("User already exist! Please login instead!")

			if re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', email) == None:
				error.append("Email invalid")

			if len(password) < 8:
				error.append("Password must be longer than 8 character!")

			if repass != password:
				error.append("Password entries do not match")

		else:
			print "dude fill it in"
			error.append("Please fill in all the blanks")

		return error


#vertify item
class ItemManager(models.Manager):
	def existitem(self, item, thisuser):
		if item:
			if Items.objects.filter(item=item):
				thisitem = Items.objects.get(item=item)
				addtowish = thisitem.user.add(thisuser)
			else:
				thisitem = Items.objects.create(item=item, creator=thisuser)
				addtowish = thisitem.user.add(thisuser)
			return thisitem
		else:
			return False






class Users(models.Model):
	name = models.CharField(max_length=45)
	username = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	hashedpw = models.CharField(max_length=225)
	created_at = models.DateTimeField(auto_now_add = True)

	objects = UserManager()

class Items(models.Model):
	item = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add = True)
	added_at = models.DateTimeField(auto_now= True)
	creator =  models.ForeignKey('Users', models.DO_NOTHING, related_name="itemcreater")
	user = models.ManyToManyField('Users')

	objects = ItemManager()
