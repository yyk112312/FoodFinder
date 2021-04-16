from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms


class User(AbstractUser):
    height = models.IntegerField('키', null=True)
    weight = models.IntegerField('몸무게', null=True)
    food = models.CharField('선호하는음식', max_length=10,null=True)
    area = models.CharField('사는 지역', max_length=10,default='')




