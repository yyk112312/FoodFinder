from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, ProfilePictureUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main_app.models import *
from .models import *
from main_app.models import *
from django.utils import timezone
from datetime import date, timedelta


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("main")
    else:
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                messages.success(request, '계정이 생성되었습니다.' + user + '!')
                return redirect("login")
        else:
            form = UserRegisterForm()
        context = {"form": form}
        return render(request, "users/register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("main")
    else:
        if request.method == "POST":
            usrnme = request.POST.get('username')
            pswd = request.POST.get('password')
            user = authenticate(request, username=usrnme, password=pswd)
            if user is not None:
                login(request, user)
                cal_goal = user.profile.calorie_goal
                if cal_goal:
                    return redirect('main')
                else:
                    return redirect('plan_category')
            else:
                messages.info(request, '사용자 이름 또는 암호가 잘못되었습니다!')

        return render(request, "users/login.html")


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def details_form(request, id):
    if request.user.is_authenticated and request.user.profile.calorie_goal:
        return redirect("main")
    else:
        flag = 0
        plan_chosen = PlanCategory.objects.get(pk=id)
        if request.method == "POST":
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            lifestyle = request.POST.get('lifestyle')
            if int(age) <= 0 or int(age) >= 130:
                messages.info(request, '잘못입력되었습니다')
                flag = 1
            if float(height) <= 0 or float(height) >= 250:
                messages.info(request, '잘못입력되었습니다')
                flag = 1
            if float(weight) <= 0 or float(weight) >= 180:
                messages.info(request, '잘못입력되었습니다')
                flag = 1
            if gender is None:
                messages.info(request, '성별을 선택해 주세요')
                flag = 1
            if flag == 0:
                p_obj = Profile.objects.get(user=request.user)
                p_obj.plan = plan_chosen
                p_obj.age = age
                p_obj.gender = gender
                p_obj.height = height
                p_obj.weight = weight
                p_obj.lifestyle = lifestyle

                p_obj.save()
                return redirect('set_target_wt')
            else:
                return redirect('filling_details', id=id)
        else:
            context = {'plan': plan_chosen}
            return render(request, "users/details_form.html", context)


@login_required(login_url='login')
def target_wt(request):
    if request.user.is_authenticated and request.user.profile.calorie_goal:
        return redirect("home")
    else:
        p_obj = Profile.objects.get(user=request.user)
        plan_chosen = p_obj.plan
        h = p_obj.height
        w = p_obj.weight
        ht = float(h)
        wt = float(w)
        bmi = round((wt / ((ht * ht) / 10000)), 2)
        if bmi < 18.5:
            bmi_cat = "UnderWeight"
        elif 18.5 <= bmi <= 25:
            bmi_cat = "Normal"
        elif bmi > 25:
            bmi_cat = "OverWeight"
        gender = p_obj.gender
        if gender == "female":
            ideal_wt = 45.5 + (0.91 * (ht - 152.4))
        else:
            ideal_wt = 50 + (0.91 * (ht - 152.4))
        ideal_wt_low = round(ideal_wt - 5)
        ideal_wt_high = round(ideal_wt + 5)

        if request.method == "POST":
            target_weight = request.POST.get('target_weight')
            if ideal_wt - 10 <= float(target_weight) <= ideal_wt + 10:
                p_obj.ideal_wt = round(ideal_wt, 2)
                p_obj.target_wt = target_weight
                p_obj.save()
                return redirect('calorie_goal')
            else:
                messages.info(request, '올바른 목표 가중치를 입력하세요')
        context = {'plan_chosen': plan_chosen, 'height': ht, 'weight': wt, 'bmi': bmi, 'bmi_cat': bmi_cat,
                   'ideal_wt_low': ideal_wt_low, 'ideal_wt_high': ideal_wt_high}
        return render(request, "users/set_target_wt.html", context)


@login_required(login_url='login')
def calorie_goal(request):
    if request.user.is_authenticated and request.user.profile.calorie_goal:
        return redirect("main")
    else:
        p_obj = Profile.objects.get(user=request.user)
        gender = p_obj.gender
        h = p_obj.height
        w = p_obj.weight
        ht = float(h)
        wt = float(w)
        age = p_obj.age
        lifestyle = p_obj.lifestyle
        plan = str(p_obj.plan)

        if gender == "Male":
            bmr = (10 * wt) + (6.25 * ht) - (5 * age) + 5
        else:
            bmr = (10 * wt) + (6.25 * ht) - (5 * age) - 161

        if lifestyle == "Sedentary or light activity":
            cal_goal = bmr * 1.53
        elif lifestyle == "Active or moderately active":
            cal_goal = bmr * 1.76
        else:
            cal_goal = bmr * 2.25

        cal_goal = round(cal_goal)
        print(cal_goal)
        if plan == "음식 칼로리 확인":
            cal_goal = cal_goal - 300
        elif plan == "다이어트":
            cal_goal = cal_goal - 700
        p_obj.calorie_goal = cal_goal
        p_obj.save()
        context = {'cal_goal': cal_goal}
        return render(request, "users/calorie_goal.html", context)


def profile(request):
    all_food_items_today = UserFoodItems.objects.filter(user=request.user, date_added=date.today())
    past_seventh_day = date.today() - timedelta(days=7)

    records = PastRecords.objects.filter(date_of_record__gte=past_seventh_day, date_of_record__lte=date.today(),
                                         user=request.user)
    if request.method == "POST":
        p_form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, '정상적으로 등록되었습니다.')
            return redirect('profile')
    else:
        p_form = ProfilePictureUpdateForm(instance=request.user.profile)
        context = {'p_form': p_form, 'food_items': all_food_items_today, 'records': records}
    return render(request, 'users/profile.html', context)