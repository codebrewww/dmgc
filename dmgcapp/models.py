from django.db import models

# Create your models here.


class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    goalCalories = models.CharField(max_length=20)
    goalCaloriesRatio = models.CharField(max_length=20)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    gender = models.CharField(max_length=20)
    goalStepCount = models.CharField(max_length=20)
    birthday = models.CharField(max_length=20, null=True)


'''
class TodayCalories(models.Model):
    userId = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='userId')
    calories = models.CharField(max_length=20)
    mealTime = models.CharField(max_length=20)
    foodName = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
'''