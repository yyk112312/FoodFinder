from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from users.models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
import requests
import json
from datetime import date, timedelta


# Create your views here.
@login_required(login_url='login')
def home(request):
    p_obj = Profile.objects.get(user=request.user)
    food_items = UserFoodItems.objects.filter(user=request.user, date_added=date.today())
    breakfast_items = UserFoodItems.objects.filter(user=request.user, date_added=date.today(), meal_cat=1)
    lunch_items = UserFoodItems.objects.filter(user=request.user, date_added=date.today(), meal_cat=2)
    eve_snack_items = UserFoodItems.objects.filter(user=request.user, date_added=date.today(), meal_cat=3)
    dinner_items = UserFoodItems.objects.filter(user=request.user, date_added=date.today(), meal_cat=4)

    prev_day = date.today() - timedelta(days=1)
    prev_day_items = UserFoodItems.objects.filter(user=request.user, date_added=prev_day)
    last_item_of_day = UserFoodItems.objects.filter(user=request.user).last()

    try:
        if date.today() > last_item_of_day.date_added and last_item_of_day.date_added == prev_day:
            cal_for_prevday = 0
            for i in prev_day_items:
                cal_for_prevday += i.calories * i.quantity
            cal_for_prevday = round(cal_for_prevday)
            prev_day_obj = PastRecords.objects.filter(user=request.user).last()
            if prev_day_obj.date_of_record != prev_day:
                rec_obj = PastRecords(user=request.user, cal_goal=request.user.profile.calorie_goal,
                                      cal_consumed=cal_for_prevday, date_of_record=prev_day)
                rec_obj.save()
    except:
        pass

    cal_consumed = 0
    for i in food_items:
        cal_consumed += (i.calories * i.quantity)
    cal_consumed = round(cal_consumed)

    msg = "하루 남은 칼로리는.."
    try:
        cal_rem = int(p_obj.calorie_goal) - cal_consumed

        if cal_rem == 0:
            msg = "오늘 목표를 달성했습니다!!! 칼로리를 남기지 마세요~~!!"
            cal_rem = ""

        if cal_rem < 0:
            msg = "오늘 칼로리 목표를 초과했습니다."
            cal_rem = ""
        context = {'profile': p_obj, 'cal_consumed': cal_consumed, 'cal_rem': cal_rem, 'food_items': food_items,
                   'b_items': breakfast_items, 'l_items': lunch_items, 'eve_items': eve_snack_items,
                   'din_items': dinner_items, 'message': msg}
        return render(request, 'main_app/home_page.html', context)
    except:
        return render(request, 'main_app/home_page.html')


@login_required(login_url='login')
def plan_category(request):
    if request.user.is_authenticated and request.user.profile.calorie_goal:
        return redirect("home")
    else:
        plans = PlanCategory.objects.all()
        context = {'plans': plans}
        return render(request, 'main_app/plan_category.html', context)


@login_required(login_url='login')
def select_food(request):
    form = FoodDetailsForm()
    form_id1 = request.POST.get("first", False)
    form_id2 = request.POST.get("second", False)

    if request.method == "POST" and form_id1:
        globals()['food_item'] = []
        food = request.POST.get("food_item")
        if food:
            ARGS = {
                "appId": "16aee158",
                "appKey": "746d5b3d7c4fc8e9120d126c95405665",
                "query": food,
                "fields": [
                    "item_name",
                    "nf_serving_size_qty",
                    "nf_serving_size_unit",
                    "nf_calories",
                    "nf_protein",
                    "nf_total_fat",
                    "nf_total_carbohydrate"
                ],
            }
            url = "https://api.nutritionix.com/v1_1/search/"
            # response = requests.get('https://api.nutritionix.com/v1_1/search/mcdonalds?results=0:20&fields=item_name,brand_name,item_id,nf_calories&appId=16aee158&appKey=746d5b3d7c4fc8e9120d126c95405665').json()
            response = requests.post(url, json=ARGS)
            data = json.loads(response.content.decode('utf-8'))
            try:
                query = data["hits"][:1]
            except:
                messages.warning(request, "음식이 존재하지 않습니다!!!")
                return redirect('select_food')

            food_item.append(query[0])

            food_name = query[0]['fields']['item_name']
            context = {"data": query, "form": form, "food_name": food_name, "food": food}
            return render(request, 'main_app/select_food.html', context)
    elif request.method == "POST" and form_id2:
        form = FoodDetailsForm(request.POST)
        try:
            f_name = globals()['food_item'][0]['fields']['item_name']
            f_cal = globals()['food_item'][0]['fields']['nf_calories']
            f_pro = globals()['food_item'][0]['fields']['nf_protein']
            f_fat = globals()['food_item'][0]['fields']['nf_total_fat']
            f_carb = globals()['food_item'][0]['fields']['nf_total_carbohydrate']
        except:
            messages.warning(request, "음식을 검색해보세요!!!")
            return redirect('select_food')

        if form.is_valid():
            quan = form.cleaned_data.get('quantity')
            meal = form.cleaned_data.get('meal_cat')

            if quan == 0:
                messages.warning(request, "수량을 입력해주세요!!!")
                return redirect('select_food')

            f_obj = UserFoodItems(user=request.user, name=f_name, meal_cat=meal, quantity=quan, calories=f_cal,
                                  fats=f_fat, proteins=f_pro, carbs=f_carb)
            f_obj.save()

            messages.success(request, '성공적으로 추가되었습니다.')
            return redirect('select_food')
        context = {"form": form}
        return render(request, 'main_app/select_food.html', context)
    return render(request, 'main_app/select_food.html', {"form": form})


@login_required(login_url='login')
def updatefooditem(request, id):
    food = UserFoodItems.objects.get(id=id)
    form = UpdateFoodItem(instance=food)
    if request.method == "POST":
        form = UpdateFoodItem(request.POST, instance=food)
        if form.is_valid():
            quan = form.cleaned_data.get('quantity')
            meal = form.cleaned_data.get('meal_cat')

            if quan == 0:
                messages.warning(request, "수량을 입력해주세요!!!")
                return redirect('update_food_item', id=id)
            else:
                food.quantity = quan
                food.meal_cat = meal
                food.save()
                messages.success(request, '성공적으로 추가되었습니다')
                return redirect('profile')
    context = {'form': form}
    return render(request, 'main_app/update_food.html', context)


@login_required(login_url='login')
def deletefooditem(request, id):
    food = UserFoodItems.objects.get(id=id)
    if request.method == "POST":
        food.delete()
        messages.info(request, '삭제되었습니다!')
        return redirect('profile')
    context = {'food': food}
    return render(request, 'main_app/delete_food.html', context)