from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

def logout_view(request):
    logout(request)
    return redirect("home")

def signup_view(requset):
    if requset.method=='POST':
        print(requset.POST)
        username = requset.POST['username']
        password = requset.POST['password']
        firstname = requset.POST['firstname']
        lastname = requset.POST['lastname']
        email = requset.POST['email']
        height = requset.POST['height']
        weight = requset.POST['weight']
        food = requset.POST['food']
        area = requset.POST['area']

        user = User.objects.create_user(username,email,password)
        user.last_name=lastname
        user.first_name=firstname
        user.height=height
        user.weight=weight
        user.food=food
        user.area=area
        user.save()
        return redirect("home")
    return render(requset,"users/signup.html")