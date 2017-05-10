from __future__ import unicode_literals
from datetime import datetime
import pytz
from pytz import timezone
from django.db import models
utc = pytz.utc
central = pytz.timezone('US/Central')
# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class TaskManager(models.Manager):
	def validate_task(self, post, task=None):
		errors = []
		#get current date/time and let python know its CST
		today = central.localize(datetime.today())
		#convert current date/time to UTC
		today = today.astimezone(utc)
		#create timestamp from form, localize to central, then convert to UTC
		task_date_time = central.localize(datetime.combine(datetime.strptime(post.get('date'), "%Y-%m-%d"), datetime.strptime(post.get('time'), "%H:%M").time())).astimezone(utc)
		if task_date_time < today:
			errors.append('Date must not be in the past.')
		#does this date/time already exist?
		found_task = Task.objects.filter(time=task_date_time).first()
		if found_task and found_task != task:
			errors.append('You may only have task for a specific time and date')
		if len(errors) == 0:
			return (True, task_date_time)
		else:
			return (False, errors)

class Task(models.Model):
	task = models.TextField()
	time = models.DateTimeField()
	status = models.CharField(max_length=20)
	user = models.ForeignKey(User, related_name='tasks')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TaskManager()
