from __future__ import unicode_literals

from django.db import models
import re, bcrypt
from datetime import datetime
# elif datetime.strptime(birthday,'%Y-%m-%d')>datetime.now():
#             return (False, "Birthday is invalid")
NO_NUM_REGEX = re.compile(r'^[^0-9]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def register(self,post_data):
        error_msgs=[]
        if User.objects.filter(email=post_data['email']).exists():
            error_msgs.append('Email already registered')
        if len(post_data['name']) < 2:
            error_msgs.append('Name is too short')
        elif not NO_NUM_REGEX.match(post_data['name']):
            error_msgs.append('Theres numbers in your name')
        if len(post_data['alias']) < 2:
            error_msgs.append('Alias name is too short')
        elif not NO_NUM_REGEX.match(post_data['alias']):
            error_msgs.append('Numbers in alias is not allowed')
        if not EMAIL_REGEX.match(post_data['email']):
            error_msgs.append('Your email is not valid')
        if len(post_data['birthday']) <= 0:
            error_msgs.append('Birthday is empty')
        if datetime.strptime(post_data['birthday'],'%Y-%m-%d')>datetime.now():
            error_msgs.append('From the future?')
        if len(post_data['password']) < 8:
            error_msgs.append('Password length is too short')
        elif post_data['password'] != post_data['cpassword']:
            error_msgs.append('Password does not match')

        if error_msgs:
            return {'error' : error_msgs}
        else:
            password = post_data['password']
            pwhash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            user = User.objects.create(name=post_data['name'],alias=post_data['alias'],email=post_data['email'],password=pwhash,dateofbirth=post_data['birthday'])
            return {'the_user' : user}


    def login(self,post_data):
        error_msgs = []
        isuser = User.objects.filter(email=post_data['email'])
        if isuser.count() < 1:
            error_msgs.append('Email does not exists. Please Register')
            return {'error' : error_msgs}
        user = User.objects.get(email=post_data['email'])
        password = user.password
        if bcrypt.hashpw(post_data['password'].encode('utf-8'),password.encode('utf-8')) == password:
            return {'the_user' : user }
        else:
            error_msgs.append('incorrect password')
            return {'error' : error_msgs}

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dateofbirth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class QuoteManager(models.Manager):
    def qval(self,post_data):
        error_msgs=[]
        if len(post_data['quote_by']) < 3:
            error_msgs.append('Quote By is too short')
        if len(post_data['message']) < 10:
            error_msgs.append('Message is too short')

        if error_msgs:
            return {'error' : error_msgs}
        else:
            ##################################
            ###adding quote inside of views###
            ##################################
            # user = User.objects.get(id=request.session['logged_in'])
            # quote = Quote.objects.create(name=post_data['quote_by'],content=post_data['message'],user=user)
            return {'the_quote' : 'success'}


class Quote(models.Model):
    name = models.CharField(max_length=45)
    content = models.TextField()
    user = models.ForeignKey(User, related_name='quote_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Favorite(models.Model):
    quote = models.ForeignKey(Quote, related_name='favorite_quote')
    user = models.ForeignKey(User, related_name='favorite_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
