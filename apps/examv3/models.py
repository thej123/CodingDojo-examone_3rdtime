from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
import datetime

# Create your models here.

Name_Regex = re.compile(r'^[a-zA-Z]\w+$')

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        if len(postData['name']) < 3 or len(postData['username']) < 3:
            errors.append('Name and Username cannot be fewer than 3 characters')
        if not re.match(Name_Regex, postData['name']) or not re.match(Name_Regex, postData['username']):
            errors.append('Name and Username can have only letters')
        if len(postData['password']) < 8:
            errors.append('Password is too small')
        if not (postData['password'] == postData['confirm_password']):
            errors.append('Passwords do not match')
        if not errors:
            hashing = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(10))
            user = User.objects.create(
                name=postData['name'],
                username=postData['username'],
                password=hashing,
            )
            return user
        return errors
    
    def validate_login(self, postData):
        errors=[]
        if len(self.filter(username=postData['username'])) > 0:
            user = self.filter(username=postData['username'])[0]
            if not (bcrypt.hashpw(postData['password'].encode(), user.password.encode())):
                errors.append('Incorrect password')
        else:
            errors.append('Incorrect Username')
        if errors:
            return errors
        return user

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def validate_trip(self, postData):
        errors=[]
        if len(postData['destination']) < 1:
            errors.append('Please enter Destination of the trip')
        if len(postData['description']) < 1:
            errors.append('Please enter Description of the trip')
        if (postData['travel_date_from'] < str(datetime.date.today())):
            errors.append('Travel dates should be future-dated')
        if (postData['travel_date_to'] < postData['travel_date_from']):
            errors.append("'Travel Date To' should not be before the 'Travel Date From'")
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField(auto_now=False, auto_now_add=False)
    travel_date_to = models.DateField(auto_now=False, auto_now_add=False)
    trip_creater = models.ForeignKey(User, related_name='trip_created')
    trip_joiners = models.ManyToManyField(User, related_name='trips_goingto')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()