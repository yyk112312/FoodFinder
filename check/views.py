from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import *


# Create your views here.

def home(request):
    # When the user clicks on the website, the homepage shows up
    if request.method == 'GET':
        form = CalorieCal(initial={'HeightChoice': 'CM'})
        return render(request, 'main/check.html', {'form': form})

    # If the user fills and submits the form
    if request.method == 'POST':
        form = CalorieCal(request.POST)
        # Taking Inputs from user in Post method
        if form.is_valid():
            Age = form.cleaned_data['Age']
            Weight = float(form.cleaned_data['Weight'])
            Height = form.cleaned_data['Height']
            Height_feet = form.cleaned_data['Height_1st']
            Height_inches = form.cleaned_data['Height_2nd']
            Gender = form.cleaned_data['Gender']
            Activity = form.cleaned_data['Activity']

            if Height_feet is not None:
                Height_feet = float(Height_feet)
            if Height_inches is not None:
                Height_inches = float(Height_inches)

            # Choices for weight and height
            WeightChoice = form.cleaned_data['WeightChoice']

            HeightChoice = form.cleaned_data['HeightChoice']

            if (HeightChoice == 'Feet' and Gender == 'Male' and WeightChoice == 'LB'):
                Height_feet = (Height_feet * 12)
                Height_metric = Height_feet + Height_inches

                BMR = (Weight * 4.536) + (Height_metric * 14.88) - (Age * 5) + (5)

            if (HeightChoice == 'Feet' and Gender == 'Male' and WeightChoice == 'KG'):
                Height_feet = (Height_feet * 12)
                Height_metric = Height_feet + Height_inches

                BMR = (Weight * 10) + (Height_metric * 14.88) - (Age * 5) + (5)

            elif (HeightChoice == 'Feet' and Gender == 'Female' and WeightChoice == 'LB'):
                Height_feet = (Height_feet * 12)
                Height_metric = Height_feet + Height_inches
                BMR = round((Weight * 4.536) + (Height_metric * 15.88) - (Age * 5) - (161))

            elif (HeightChoice == 'Feet' and Gender == 'Female' and WeightChoice == 'KG'):
                Height_feet = (Height_feet * 12)
                Height_metric = Height_feet + Height_inches
                BMR = round((Weight * 10) + (Height_metric * 15.88) - (Age * 5) - (161))

            # Calculation According to gender
            elif (HeightChoice == 'CM' and Gender == 'Male' and WeightChoice == 'KG'):
                BMR = round((Weight * 10) + (Height * 6.25) - (Age * 5) + (5))
            elif (HeightChoice == 'CM' and Gender == 'Female' and WeightChoice == 'KG'):
                BMR = round((Weight * 10) + (Height * 6.25) - (Age * 5) - (161))

            elif (HeightChoice == 'CM' and Gender == 'Male' and WeightChoice == 'LB'):
                BMR = round((Weight * 4.536) + (Height * 6.25) - (Age * 5) + (5))
            elif (HeightChoice == 'CM' and Gender == 'Female' and WeightChoice == 'LB'):
                BMR = round((Weight * 4.536) + (Height * 6.25) - (Age * 5) - (161))

            # Calculation According to Activity Level

            if (Activity == '1'):
                Calories = (BMR * 1.3)
            elif (Activity == '2'):
                Calories = (BMR * 1.5)
            elif (Activity == '3'):
                Calories = (BMR * 1.7)

            # Drop down for checking if its for Loosing weight or gaining muscle
            TypeOfCal = form.cleaned_data['CalType']

            # Cutting Calories
            if (TypeOfCal == 'Losing Weight'):
                Calorie = round(Calories - 250)
            elif (TypeOfCal == 'Gaining Muscle'):
                # Surplus Calories
                Calorie = round(Calories + 250)

            if (WeightChoice == 'KG'):
                # Macros For Metric
                Proteins = round(Weight * 2.2, 2)
                Fats = round(Proteins * 0.4, 2)

                CalFromProteins = Proteins * 4
                CalFromFats = Fats * 9

                CalFromCarbs = Calories - CalFromFats - CalFromProteins
                Carbs = round(CalFromCarbs / 4, 2)

            elif (WeightChoice == 'LB'):
                Proteins = round(Weight)
                Fats = round(Proteins * 0.4, 2)

                CalFromProteins = Proteins * 4
                CalFromFats = Fats * 9

                CalFromCarbs = Calories - CalFromFats - CalFromProteins

                Carbs = round(CalFromCarbs / 4, 2)
    context = {'form': form, 'Calorie': Calorie, 'Proteins': Proteins, 'Carbs': Carbs, 'Fats': Fats}
    return render(request, 'main/check.html', context)


def DietPlan(request):
    Calories = float(request.POST['Calories'])
    Proteins = float(request.POST['Proteins'])
    Carbs = float(request.POST['Carbs'])
    Fats = float(request.POST['Fats'])

    breakfast_cal, breakfast_protein, breakfast_carbs, \
    breakfast_fats = percentage(20, calories=Calories, protein=Proteins, \
                                carbs=Carbs, fats=Fats)

    lunch_cal, lunch_protein, lunch_carbs, \
    lunch_fats = percentage(40, calories=Calories, protein=Proteins, \
                            carbs=Carbs, fats=Fats)

    dinner_cal = lunch_cal
    dinner_protein = lunch_protein
    dinner_carbs = lunch_carbs
    dinner_fats = lunch_fats

    temp_cal = breakfast_cal

    find_cal = Food.objects.filter(MealType=1).all()
    sum_cal = 0  # This is to be used in finding out total calories of total breakfast

    selectedBreakfast = []
    # select_breakfast = Food.objects.filter(MealType__name__contains='Breakfast')
    for var in find_cal:
        Carbohydrates = Food.objects.filter(MealType__name__contains='Breakfast').aggregate(Sum('carbs'))
        Fat = Food.objects.filter(MealType__name__contains='Breakfast').aggregate(Sum('fats'))
        Protein = Food.objects.filter(MealType__name__contains='Breakfast').aggregate(Sum('protien'))
        break

    # Takes out the calories
    for item in find_cal:
        food_breakfast = macros(carbs=item.carbs, fats=item.fats, proteins=item.protien)
        sum_cal = food_breakfast + sum_cal
    print("Sum is", sum_cal)
    print("20% of breakfast cal is", temp_cal)
    # Have to get sum of food_breakfast

    if (sum_cal <= temp_cal):
        selectedBreakfast.append(item)
        temp_cal = temp_cal - sum_cal
        print(temp_cal)
    else:
        print("Else")

        # elif(sum_cal >= temp_cal):
        #     select_breakfast.append(item)
        #     temp_cal = temp_cal - sum_cal
        #     print(temp_cal)
    # if(temp_cal>=sum):
    #     selectedBreakfast.append([sum])
    #     temp_cal=temp_cal-sum
    # print(selectedBreakfast)

    return render(request, 'main/DietPlan.html', {"breakfast": find_cal})


def percentage(percentage, **macros):
    return (macros['calories'] * percentage) / 100, \
           (macros['protein'] * percentage) / 100, \
           (macros['carbs'] * percentage) / 100, \
           (macros['fats'] * percentage) / 100


def macros(**kcal):
    return (kcal['carbs'] * 4) + (kcal['fats'] * 9) + (kcal['proteins'] * 4)