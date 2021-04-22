from django.urls import path
from . import views

urlpatterns = [
 path('', views.checkcal , name='cal'),
 path('diet', views.DietPlan, name='diet'),
]
