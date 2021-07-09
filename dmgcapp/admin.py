from django.contrib import admin
from .models import Account, TodayCalories

# Register your models here.

admin.site.register(Account)
admin.site.register(TodayCalories)