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