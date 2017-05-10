from __future__ import unicode_literals
import bcrypt
import hashlib
import re
import datetime


from django.db import models

# Create your models here.

class UserManager(models.Manager):
    def get_all(self):
        total_users = User.objects.all()
        return total_users
    def get_current(self, user_id):
        current_user = User.objects.get(id=user_id)
        print(current_user)
        return current_user

    def validate (self, postData):
    #this method ensures that what the user inputs is valid

        regex_name = re.compile(r'^[a-zA-Z\s]{3,100}$') #{minum length, maximum length}
        error_arr = []
    # error = 0 #this is to check if everything below passes! It can also be used as a boolean
        if not regex_name.match(postData['first_name']):
            error_arr.append("Please enter a valid name! It must be 3 characters long and have no numbers!")
        if not postData['password'] == postData['confirm']: #if these don't match up
            error_arr.append("Your passwords do not match!")
        if len(postData['password']) < 8:
            error_arr.append("Your password must be at least 8 characters long!")
        if self.username_exist(postData): #take postData and pass it to the emailExist method
            error_arr.append("You have already registered with this username!")

        return error_arr

    def username_exist(self, postData):
        findUsername = User.objects.filter(username=postData['username'])
        if findUsername: #this line equates to: if findEmail has value, or is true
            return True #if it is true, the email already exists
        else:
            return False #if false, it will become registered

    def register(self, postData):
        self.create( #we want to create one row in Users that has all these fields so we keep it together
            first_name = postData['first_name'],
            username = postData['username'],
            password = bcrypt.hashpw(postData['confirm'].encode(), bcrypt.gensalt())
        )

    def login_user(self, postData):
        user_info = self.filter(username=postData['username']) #find the User row that contains the entered email
        if not user_info: #if user_info is false...
            return False #if the email isn't there, get outta here!
        print ('- First instance of user_info -')
        print (user_info) #so we can see if it's the correct user we're talking about
        #user_info currently gives you an array which has a dictionary inside
        user_info = user_info[0] #traverse to the first index in the list
        print ('- Second instance of user_info -')
        print (user_info) #now we get object!
        pw_hash = user_info.password.encode() #this set pw_hash to equal the password for the user object we just printed in the terminal
        if pw_hash == bcrypt.hashpw(postData['password'].encode(), pw_hash): #the second pw_hash is being used to check if it matches the postData password
            return True
        return False

    def set_session(self, postData): #with this method, we will be retrieving an id and sending to our views.py
        #we already know that the inputed email exists, so now we want to find associated user info with the line below
        #Also, since we know that we will be getting a list with one item, we can skip setting this to find_user[0] and say .first() instead
        find_user = self.filter(username=postData['username']).first()
        return find_user.id #this sends returns the id value

class User(models.Model):
    first_name = models.CharField(max_length=100)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    confirm = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
# Create your models here.
