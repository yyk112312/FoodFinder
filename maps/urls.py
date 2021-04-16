from django.contrib import admin
from django.urls import path
from django.conf.urls import url

import maps.views
from FoodFinder import views

urlpatterns = [
    path('', maps.views.index, name='index'),
]