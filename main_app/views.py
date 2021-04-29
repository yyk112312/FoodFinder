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
    apikey="9a0cd871b41e45a39e17"
    startRow=1
    endRow=15
    if request.method == "POST" and form_id1:
        globals()['food_item'] = []
        food = request.POST.get("food_item")
        if food:
            url = "http://openapi.foodsafetykorea.go.kr/api/"+ apikey+"/I2790/json/"+str(startRow)+"/"+str(endRow)+"/DESC_KOR="+food
            # response = requests.get('https://api.nutritionix.com/v1_1/search/mcdonalds?results=0:20&fields=item_name,brand_name,item_id,nf_calories&appId=16aee158&appKey=746d5b3d7c4fc8e9120d126c95405665').json()
            response = requests.post(url)
            data = json.loads(response.content)
            #print(data)
            dataset = data['I2790']

            #namedata = data['DESC_KOR']
            #print(finaldata['DESC_KOR','NUTR_CONT1','NUTR_CONT2','NUTR_CONT3'])

            try:
                finaldata = dataset['row']
                for i in range(len(finaldata)):
                    query = finaldata[i]
                    food_name = query['DESC_KOR']
                    food_cal = query['NUTR_CONT1']
                    food_pro = query['NUTR_CONT3']
                    food_fat = query['NUTR_CONT4']
                    food_carb = query['NUTR_CONT2']
                    food_qua = query['SERVING_SIZE']


            except:
                messages.warning(request, "음식이 존재하지 않습니다!!!")
                return redirect('select_food')

            food_item.append(query)




            context = {"data": data, "form": form, "food_name": food_name, "food": food, "food_cal":food_cal,"food_pro":food_pro,"food_fat":food_fat,"food_carb":food_carb, 'finaldata':finaldata, 'food_qua':food_qua}
            return render(request, 'main_app/select_food.html', context)
    elif request.method == "POST" and form_id2:
        form = FoodDetailsForm(request.POST)
        try:
            for i in range(len(globals()['food_item'])):

                f_name = globals()['food_item'][i]['DESC_KOR']
                f_cal = globals()['food_item'][i]['NUTR_CONT1']
                f_pro = globals()['food_item'][i]['NUTR_CONT3']
                f_fat = globals()['food_item'][i]['NUTR_CONT4']
                f_carb = globals()['food_item'][i]['NUTR_CONT2']

        except:
            messages.warning(request, "음식을 검색해보세요!!!")
            return redirect('select_food')

        if form.is_valid():
            quan = form.cleaned_data.get('quantity')
            meal = form.cleaned_data.get('meal_cat')

            if quan == 0:
                messages.warning(request, "수량을 입력해주세요!!!")
                return redirect('select_food')

            f_obj = UserFoodItems(userid=request.user.id, user=request.user, name=f_name, meal_cat=meal, quantity=quan, calories=f_cal,
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