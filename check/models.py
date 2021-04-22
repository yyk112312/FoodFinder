from django.db import models


class Meals(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FoodType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.IntegerField()
    carbs = models.FloatField()
    fats = models.FloatField()
    protien = models.FloatField()
    per_how_much_gram = models.IntegerField()
    FoodType = models.ForeignKey('FoodType', on_delete=models.CASCADE, null=True)
    MealType = models.ForeignKey('Meals', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name + '-' + self.FoodType.name + '-' + self.MealType.name


class Units(models.Model):
    Ounce = models.IntegerField()
    Grams = models.IntegerField()
    Lb = models.IntegerField()