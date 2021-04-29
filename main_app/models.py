from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class PlanCategory(models.Model):
    title = models.CharField(max_length=40)
    desc = models.TextField()
    image = models.ImageField(default='plan.jpg',upload_to='plan_pics')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Plan Categories'

class MealCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Meal Categories'

class UserFoodItems(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    userid = models.IntegerField(default=0)
    name = models.CharField(max_length=100,null=True)
    meal_cat = models.ForeignKey(MealCategory,on_delete=models.CASCADE,null=True,default="BreakFast")
    quantity = models.PositiveIntegerField(default=0)
    calories = models.FloatField(default=0)
    fats = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    date_added = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User Food Item'

class PastRecords(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    cal_goal = models.PositiveIntegerField(null=True)
    cal_consumed = models.PositiveIntegerField(null=True)
    date_of_record = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.date_of_record} Record"

    class Meta:
        verbose_name = 'Past Record'
