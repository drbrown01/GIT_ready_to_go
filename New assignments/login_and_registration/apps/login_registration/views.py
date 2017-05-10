from django.shortcuts import render, redirect
from django.contrib import messages
from models import User

def index(request):
	if not 'logged_in' in request.session or request.session['logged_in'] == False:
		return redirect('/login')
	return render(request, 'login_registration/index.html')

def signin(request):
	return render(request, 'login_registration/login.html')

def create(request):
	result = User.objects.register(request.POST)
	if result[0] == False:
		for error in result[1]:
			messages.error(request, error['message'], extra_tags = error['tag'])
		return redirect('/login')
	else:
		request.session['logged_in'] = True
		request.session['username'] = result[2]
		messages.success(request, result[1])
		return redirect('/')

def login(request):
	result = User.objects.login(request.POST)
	if result[0] == False:
		messages.error(request, result[1]['message'], extra_tags=result[1]['tag'])
		return redirect('/login')
	else:
		request.session['logged_in'] = True
		request.session['username'] = result[2]
		messages.success(request, result[1])
		return redirect('/')

def logout(request):
	request.session['logged_in'] = False
	request.session.pop('username')
	return redirect('/')
# Create your views here.
