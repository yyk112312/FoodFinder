from django.db import models

class Foodclass(models.Model):
    name = models.CharField('식품명', max_length=50, unique=False)
    once = models.FloatField('1회 제공량', default=0)
    cabor = models.FloatField('탄수화물', default=0)
    protein = models.FloatField('단백질', default=0)
    fat = models.FloatField('지방', default=0)
    def __str__(self):
        return self.name