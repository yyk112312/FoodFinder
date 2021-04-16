from django.db import models

class Exercise(models.Model):
    name = models.CharField('운동 및 활동', max_length=50)
    calories1 = models.IntegerField('51kg', default=0)
    calories2 = models.IntegerField('71kg', default=0)
    calories3 = models.IntegerField('81kg', default=0)
    calories4 = models.IntegerField('95kg', default=0)
    hour = models.FloatField('한시간 당 소모 칼로리', default=0)
    eximg = models.ImageField('운동이미지', blank='True')

    def __str__(self):
        return self.name

