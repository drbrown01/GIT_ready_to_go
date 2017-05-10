from django.shortcuts import render, redirect
from . import models
from .models import Users, Items
import bcrypt
from django.contrib import messages
# Create your views here.

def index(request):

	return render(request, 'wishlist/index.html')


def home(request):
	if 'user_id' not in request.session:
		messages.error(request, 'Please login to visit your wishlist!')
		return redirect('/')
	else:
		thisuser = models.Users.objects.get(id = request.session['user_id'])
		userlist = models.Items.objects.filter(user=thisuser)
		allitem = models.Items.objects.exclude(user=thisuser).order_by('-added_at')

		context={
			"thisuser" : thisuser,
			"items" : userlist,
			'allitem' : allitem
		}
		print(K *500)
		return render(request, 'wishlist/home.html', context)



def additem(request):

	return render(request, 'wishlist/additem.html')

def displayitem(request, id):
	if models.Items.objects.filter(id=id):
		thisitem = models.Items.objects.get(id=id)
		users = thisitem.user.all()
		context = {
			'thisitem' : thisitem,
			"users" : users
		}
		return render(request, 'wishlist/item.html', context)
	else:
		return redirect('/home')




def additemprocess(request):

	if request.POST:
		thisuser = models.Users.objects.get(id = request.session['user_id'])
		print thisuser.name
		thisitem = models.Items.objects.existitem(item=request.POST['item'], thisuser = thisuser)
		print thisitem

		if thisitem == False:
			messages.error(request, 'Item name cannot be blank!')
			return redirect('/additem')

	return redirect('/home')

def deleteitem(request, id):
	models.Items.objects.filter(id=id).delete()
	return redirect('/home')

def removeitem(request, id):
	thisitem = models.Items.objects.get(id=id)
	thisuser = models.Users.objects.get(id = request.session['user_id'])
	removeuser = thisitem.user.remove(thisuser)

	return redirect('/home')

def addthis(request, id):
	thisitem = models.Items.objects.get(id=id)
	thisuser = models.Users.objects.get(id = request.session['user_id'])
	removeuser = thisitem.user.add(thisuser)
	return redirect('/home')




#LOGIN REGS
def login(request):
	email=request.POST.get('email')
	password=request.POST.get('password')

	#check if existing user or input error
	existuser = models.Users.objects.loginvalid(request,email, password)
	if existuser == True:
		print "user exist"
		user_id = models.Users.objects.get(email = email).id
		request.session['user_id'] = user_id
		context = {
			'username' : email,
			'status' : "logged in"
		}
		return redirect('/home')
	##DISPLAY MSGED TO SHOW ERROR
	messages.error(request, existuser)
	return redirect('/')

def register(request):
	#GET USER INPUT
	name=request.POST.get('name')
	username=request.POST.get('username')
	email = request.POST.get('email')
	password=request.POST.get('password')
	repassword=request.POST.get('re_password')
	newuser = models.Users.objects.registervalid(name, username, email, password, repassword)

	if not newuser:
		hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		newuser = models.Users.objects.create(name=name, username=username, email=email, hashedpw=hashed)
		user_id = models.Users.objects.get(email = email).id
		request.session['user_id'] = user_id
		return redirect('/home')

	for ind in range (0, len(newuser)):
		messages.error(request, newuser[ind])
	return redirect('/')


def log_out(request):
	request.session.pop('user_id')
	return redirect('/')
