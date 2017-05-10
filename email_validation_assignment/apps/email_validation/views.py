from django.shortcuts import render, redirect
from django.contrib import messages
from models import User

def index(request):
	return render(request, 'email_validation/index.html')

def show(request):
    if !logged_in in request.session:
        return redirect('/')
	context = {'users': User.objects.all()}
	return render(request, 'email_validation/success.html', context)

def create(request):
	result = User.objects.register(request.POST['email'])
	if result[0] == False:
		messages.error(request, result[1][0])
		return redirect('/')
	else:
		print result
		print result[1].__dict__
		print result[1].email
		messages.success(request, result[1].email)
		return redirect('/success')
