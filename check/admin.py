from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Meals)
admin.site.register(FoodType)
admin.site.register(Food)