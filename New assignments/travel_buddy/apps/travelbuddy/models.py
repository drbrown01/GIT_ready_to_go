from __future__ import unicode_literals
import bcrypt
import hashlib
import re
from datetime import datetime
from ..login.models import User
from django.db import models

# Create your models here.
class TripManager(models.Manager):
    def get_all_data(self, session_id): #this is coming from travel_index
        user_info = User.objects.all()
        item_info = self.all(),
        current_user = User.objects.get_current(session_id)
        wishlist =  Trip.objects.find_wishlist(session_id)
        other_people_wl = self.other_wishlist(session_id)

        all_data = {
            'user_info' : user_info,
            'item_info' : item_info,
            'current_user' : current_user,
            'wishlist' : wishlist,
            'other_wishlist' : other_people_wl
        }
        print(all_data['current_user'].first_name)
        return all_data

    def make_item(self, postData, session_id):
        current_user_obj = User.objects.get(id=session_id)#session_id is an entire object
        self.create(
        destination = postData['item_name'],
        plan = postData['trip_description'],
        start_date = postData['start_date'],
        end_date = postData['end_date'],
        created_by = current_user_obj #this is entering the appropriate fields for the item we created
        )
        new_item_id = self.filter().latest('id')#this will get the item's id that we just created in the lines above
        print(new_item_id)
        print(postData['item_name'])
        self.add_wishlist(new_item_id.id, current_user_obj)
        #new_item_id will be item_id in add_wishlist, same for current_user_obj, it will be user_id. ORDER MATTERS!

    def add_wishlist(self,item_id, user_id):
        print(user_id)
        print (item_id)

        item_obj = self.get(id=item_id)
        item_obj.wishlist.add(user_id)

        #.add is for M2M, .create is for Foreign Key/entering something into a db
        #this is the user object from make_item/other places
       #since we are passing in the full item object and user object, we don't need to query for the wishlist.
       #so it will add to our wishlist entry in our item table
    def find_wishlist(self, session_id):
        return self.filter(wishlist__id=session_id)
        #wishlist for current user

    def other_wishlist(self,session_id):
        return self.exclude(wishlist__id=session_id)
        #wishlist for other users

    def get_item_id(self, item_id):
        return self.get(id=item_id)
        #we need to return so item_id can be send to my views, which then be sent to html
    def get_wishers(self, item_id):
        return User.objects.filter(wishlist_list=item_id)
        #this will find everyone who has the item in their wishlist

    def delete_me(self, item_id):
        self.filter(id=item_id).delete()

    def remove_me(self, item_id, user_id):
        item_obj = self.get(id=item_id)
        item_obj.wishlist.remove(user_id)

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField(max_length=1000)
    created_by = models.ForeignKey(User, related_name="trips_added")
    wishlist = models.ManyToManyField(User, related_name = "wishlist_list")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
