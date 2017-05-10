from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Trip
from datetime import date
from ..login.models import User


# Create your views here.

def travel_index(request):
    session_id = request.session['user_id']#this is from the register/login set_session
    all_data = Trip.objects.get_all_data(session_id)

    print(request.session['user_id'])
    context = {
        'all_data' : all_data,
    }
    print(all_data)
    return render(request, 'travelbuddy/dashboard.html', context)

def add_item(request):
    return render(request, 'travelbuddy/add_trip.html')

def create_item(request):
    if len(request.POST['item_name'])< 2:
        messages.add_message(request, messages.ERROR, "Please enter a valid destination! It must be at least 2 characters long and have no numbers!")
        return redirect ('travel_ns:add')
    # if request.POST['start_date'] < request.session['created_at']:
    #     messages.add_message(request, messages.ERROR, "Your trip must be in the future!")
    #     return redirect ('/')
    if request.POST['end_date'] < request.POST['start_date']:
        messages.add_message(request, messages.ERROR, "Your trip end date must be after your start date!")
        return redirect ('travel_ns:add')
    Trip.objects.make_item(request.POST, request.session['user_id'])
    return redirect('travel_ns:travel_index')

def view_item(request, item_id):
    wishers = Trip.objects.get_wishers(item_id)
    this_item = Trip.objects.get_item_id(item_id)
    context = {
        'this_item' : this_item,
        'wishers' : wishers
    }
    print (context['this_item'])
    return render(request, 'travelbuddy/show_trip.html', context)

def add_wishlist(request, item_id):
    item_id=item_id
    user_id=request.session['user_id']
    print (user_id)
    Trip.objects.add_wishlist(item_id, user_id)
    return redirect('travel_ns:travel_index')

def delete_item(request, item_id):
    Trip.objects.delete_me(item_id)
    return redirect('travel_ns:travel_index')

def remove_item(request, item_id):
    Trip.objects.remove_me(item_id, request.session['user_id'])
    return redirect('trip_ns:travel_index')

def logout(request):
    request.session.flush() #this clears all the sessions!
    return redirect('login_ns:user_index')

# Create your views here.
