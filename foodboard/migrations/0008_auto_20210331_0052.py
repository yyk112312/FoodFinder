# Generated by Django 3.1.6 on 2021-03-30 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodboard', '0007_auto_20210331_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodclass',
            name='cabor',
            field=models.FloatField(default=0, verbose_name='탄수화물'),
        ),
        migrations.AlterField(
            model_name='foodclass',
            name='fat',
            field=models.FloatField(default=0, verbose_name='지방'),
        ),
        migrations.AlterField(
            model_name='foodclass',
            name='protein',
            field=models.FloatField(default=0, verbose_name='단백질'),
        ),
    ]
