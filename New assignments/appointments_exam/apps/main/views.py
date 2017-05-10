from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import pytz
from pytz import timezone
from .models import *
utc = pytz.utc
central = pytz.timezone('US/Central')
# Create your views here.
def index(request):
	todays_tasks = []
	future_tasks = []
	tasks = Task.objects.filter(user=User.objects.filter(id=1)).order_by('time')
	today = central.localize(datetime.today()).date()
	for task in tasks:
		if task.time.date() == today:
			todays_tasks.append(task)
		elif task.time.date() > today:
			future_tasks.append(task)

	context = {
		'current_user': User.objects.filter(id=1),
		'todays_tasks': todays_tasks,
		'future_tasks': future_tasks,
	}
	return render(request, 'main/index.html', context)

def destroy_task(request, task_id):
	task = Task.objects.filter(id = task_id).first()
	if task:
		task.delete()
	return redirect("/")

def edit_task(request, task_id):
	task = Task.objects.filter(id=task_id).first()
	context = {
		'task': task,
		#before we can display date/time we need to convert from UTC to CST
		'task_date': task.time.astimezone(central).strftime('%Y-%m-%d'),
		'task_time': task.time.astimezone(central).strftime('%H:%M'),
	}
	return render(request, 'main/edit_task.html', context)

def update_task(request, task_id):
	task = Task.objects.filter(id=task_id).first()
	if task:
		check = Task.objects.validate_task(request.POST, task)
		if check[0]:
			task.task = request.POST.get('task')
			task.status = request.POST.get('status')
			task.time = check[1]
			task.save()
			return redirect('/')
		else:
			for message in check[1]:
				messages.error(request, message)
			return redirect("/tasks/{}".format(task_id))

def create_task(request):
	if request.method == 'POST':
		task = Task.objects.validate_task(request.POST)
		if task[0]:
			Task.objects.create(
				task = request.POST.get('task'),
				time = task[1],
				status = 'Pending',
				user = User.objects.filter(id=1)
			)
		else:
			for message in task[1]:
				messages.error(request, message)
	return redirect('/')

# Create your views here.
