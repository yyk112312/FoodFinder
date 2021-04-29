from django.shortcuts import render
import csv
import os
from django.http import HttpResponse
from main_app.models import UserFoodItems
# Create your views here.

def export(request):
    with open('static/userdata/userdata.csv', 'w', newline='') as csvfile:
        fieldnames = ['user','name','quantity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for food in UserFoodItems.objects.all():
            writer.writerow({'user':food.user, 'name':food.name, 'quantity':food.quantity})
        print(food.user)
    return render(request, 'create.html')