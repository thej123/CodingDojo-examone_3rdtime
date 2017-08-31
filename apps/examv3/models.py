from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
import datetime

# Create your models here.

Email_Regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
Name_Regex = re.compile(r'^[a-zA-Z]\w+$')

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        if len(postData['name']) < 3 or len(postData['alias']) < 3:
            errors.append('Name and Alias cannot be fewer than 3 characters')
        if not re.match(Name_Regex, postData['name']) or not re.match(Name_Regex, postData['alias']):
            errors.append('Name and alias can have only letters')
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append('Email has already been registered')
        if not re.match(Email_Regex, postData['email']):
            errors.append('Invalid email')
        if (postData['dob'] > str(datetime.date.today())):
            errors.append('Invalid DOB')
        if len(postData['password']) < 8:
            errors.append('Password is too small')
        if not (postData['password'] == postData['confirm_password']):
            errors.append('Passwords do not match')
        if not errors:
            hashing = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(10))
            user = User.objects.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                # dob=postData['dob'],
                password=hashing,
            )
            return user
        return errors
    
    def validate_login(self, postData):
        errors=[]
        if len(self.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])[0]
            if not (bcrypt.hashpw(postData['password'].encode(), user.password.encode())):
                errors.append('Incorrect password')
        else:
            errors.append('Incorrect Email')
        if errors:
            return errors
        return user

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    # dob = models.DateField(auto_now=False, auto_now_add=False)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()