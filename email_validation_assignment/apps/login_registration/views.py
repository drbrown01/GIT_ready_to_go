from django.shortcuts import render, redirect
from django.contrib import messages
from models import User

def index(request):
	return render(request, 'login_registration/index.html')

def create(request):
	result = User.objects.register(request.POST)
	if result[0] == False:
		for error in result[1]:
			messages.error(request, error['message'], extra_tags = error['tag'])
		return redirect('user_signin')
	else:
		request.session['logged_in'] = result[3]
		request.session['alias'] = result[2]
		messages.success(request, result[1])
		return redirect('books_index')

def login(request):
	result = User.objects.login(request.POST)
	if result[0] == False:
		messages.error(request, result[1]['message'], extra_tags=result[1]['tag'])
		return redirect('user_signin')
	else:
		request.session['logged_in'] = result[3]
		request.session['alias'] = result[2]
		messages.success(request, result[1])
		return redirect('books_index')

def logout(request):
	request.session.pop('logged_in')
	request.session.pop('alias')
	return redirect('/')

def show(request, id):
	print id
	user = User.objects.get(id=id)
	context = {
		'user': user
	}
	return render(request, 'login_registration/show.html', context)
