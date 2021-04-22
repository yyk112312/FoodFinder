from django.contrib.auth.models import User
from django import forms
from .models import *

class FoodDetailsForm(forms.ModelForm):

    class Meta:
        model = UserFoodItems
        fields = ['meal_cat','quantity']
        labels = {
            'meal_cat': ('Meal Category')
        }

class UpdateFoodItem(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(UpdateFoodItem, self).__init__(*args, **kwargs)
       self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = UserFoodItems
        fields = ['name','meal_cat','quantity']
        labels = {
            'meal_cat': ('Meal Category')
        }