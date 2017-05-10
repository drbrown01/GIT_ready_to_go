from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from ..travelbuddy.models import Trip

# Create your views here.

def login_index(request):
    total_users = User.objects.get_all()
    context = {
        'all_users': total_users
    }
    print context
    return render(request, 'login/index.html', context)

def register(request):
    error_arr_message = User.objects.validate(request.POST)
    if len(error_arr_message) > 0: #if my error_arr_message is not empty...
        for message in error_arr_message: #loop through the array and add them all to "messages" and it is what we use in our html
            messages.add_message(request, messages.ERROR, message)
        return redirect ('/')
    if User.objects.username_exist(request.POST):
        messages.add_message(request, messages.ERROR, "Username already exits!")
        return redirect ('/')
    User.objects.register(request.POST) #pass the POST dictionary to the UserManager register method
    request.session['user_id'] = User.objects.set_session(request.POST) #this will log in the user without making go through the login form
    print (request.session['user_id'])
    return redirect ('travel_ns:travel_index')

def login(request):
    if "user_id" in request.session: #this says is the user_id key (from the login method when we set the session) in session?
        messages.add_message(request, messages.ERROR, "You are already logged in!")
        return redirect('travel_ns:travel_index')

    login_attempt = User.objects.login_user(request.POST) #this says go to User, then it's objects, then the method login_user
    if not User.objects.username_exist(request.POST): #did they input an email that's in the database?
        messages.add_message(request, messages.ERROR, "Username is incorrect!")
        return redirect('/')
        #now we check to see if the password matches the email with the code below!
    if not login_attempt: #aka if login_attempt == False
        messages.add_message(request, messages.ERROR, "Password is incorrect!")
        return redirect('/')
    #now let's set the session!
    request.session['user_id'] = User.objects.set_session(request.POST) #this sets the session so we can access this user's info as long as they are logged in
    print (request.session['user_id']) #user_id is a key that we just created. this will go to list_app views for the index!
    return redirect('travel_ns:travel_index') #reroute to my success page
# Create your views here.
