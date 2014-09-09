from django.db import models

# Create your models here.

'''
Created on 07/09/2014

@author: jamerson
'''

class ShortenedLink(models.Model):
    identifier = models.CharField(max_length = 10)
    original_link = models.CharField(max_length = 500)
    
class User(models.Model):
    name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 50)