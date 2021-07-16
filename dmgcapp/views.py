from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, TodayCalories
from django.contrib.auth.models import User
from django.contrib import messages, auth
from math import *
from datetime import datetime, timedelta, date
import hashlib
import json
import requests
# Create your views here.


def index(request):
    today = datetime.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day
    today_string = str(today_year)

    if 1 <= today_month <= 9:
        today_string += ("0"+str(today_month))
    else:
        today_string += str(today_month)
    if 1 <= today_day <= 9:
        today_string += ("0"+str(today_day))
    else:
        today_string += str(today_day)

    today_string = int(today_string)
    return render(request, 'dmgcapp/index.html', {
        "today_year": today_year,
        "today_month": today_month,
        "today_day": today_day,
        "today_string": today_string,
    })


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/dmgcapp/')
        else:
            messages.error(request, '아이디 혹은 비밀번호가 잘못되었습니다')
            return redirect('login')
    else:
        return render(request, 'dmgcapp/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/dmgcapp/')


def signup(request):
    if request.method == 'POST':
        if Account.objects.filter(username=request.POST['username']).values():
            messages.error(request, '이미 존재하는 아이디 입니다.')
            return redirect('signup')

        # 비밀번호가 10자리 미만으로 구성 될 경우
        elif len(request.POST['password1']) < 10:
            messages.error(request, '비밀번호는 10자 이상으로 설정해주세요')
            return redirect('signup')

        # 비밀번호가 서로 일치 하지 않는 경우
        elif request.POST['password1'] != request.POST['password2']:
            messages.error(request, '비밀번호가 서로 일치하지 않습니다. 확인해 주세요')
            return redirect('signup')

        # 비밀번호가 서로 일치 할 경우
        elif request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            password = request.POST['password1']
            password_crypt = hashlib.sha256(password.encode('utf-8')).hexdigest()
            nickname = request.POST['nickname']
            email = request.POST['email']
            goalCalories = request.POST.get('goalCalories')
            goalCaloriesRatio = request.POST.get('goalCaloriesRatio')
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            gender = request.POST.get('gender')
            birthday = request.POST.get('birthday')
            birthday_year = ""
            birthday_month = ""
            birthday_day = ""
            if birthday:
                birthday_year = str(birthday[0:4])
                birthday_month = str(birthday[5:7])
                birthday_day = str(birthday[8:10])
            birthday = birthday_year + birthday_month + birthday_day
            user = Account(
                username=username,
                password=password_crypt,
                nickname=nickname,
                email=email,
                goalCalories=goalCalories,
                goalCaloriesRatio=goalCaloriesRatio,
                height=height,
                weight=weight,
                gender=gender,
                birthday=birthday
            )
            user.save()
            User.objects.create_user(username=username,
                                     password=password)
            return redirect('/dmgcapp/')
    else:
        return render(request, 'dmgcapp/signup.html')


def search(request, today_string):
    # 날짜 계산
    today = datetime.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day
    today_datetime = datetime(today_year, today_month, today_day)
    month_day_list = []
    day_string = 0

    # 3일 전부터 1일 전
    for i in range(3, 0, -1):
        one_day = today_datetime - timedelta(days=i)
        day_string = str(one_day.year)
        if 1 <= one_day.month <= 9:
            day_string += ("0" + str(one_day.month))
        else:
            day_string += str(one_day.month)

        if 1 <= one_day.day <= 9:
            day_string += ("0" + str(one_day.day))
        else:
            day_string += str(one_day.day)
        day_string = int(day_string)
        temp = [one_day.month, one_day.day, day_string]
        month_day_list.append(temp)

    # 오늘
    today_string = str(today_year)
    if 1 <= today_month <= 9:
        today_string += ("0" + str(today_month))
    else:
        today_string += str(today_month)
    if 1 <= today_day <= 9:
        today_string += ("0" + str(today_day))
    else:
        today_string += str(today_day)

    today_string = int(today_string)
    month_day_list.append([today_month, today_day, today_string])

    # 1일 후 부터 3일 후
    for i in range(1, 4):
        one_day = today_datetime + timedelta(days=i)
        day_string = str(one_day.year)
        if 1 <= one_day.month <= 9:
            day_string += ("0" + str(one_day.month))
        else:
            day_string += str(one_day.month)

        if 1 <= one_day.day <= 9:
            day_string += ("0" + str(one_day.day))
        else:
            day_string += str(one_day.day)

        day_string = int(day_string)
        temp = [one_day.month, one_day.day, day_string]
        month_day_list.append(temp)
    try:
        if request.method == "POST":

            '''
            key_id = "6f79706705224d619099/"
            service_id = "I2790/"
            datatype = 'json/'
            start_idx = "1/"
            end_idx = "5"
            '''

            if request.POST.getlist('nutr'):
                new_food_data = request.POST.getlist('nutr')
                path_day_string = int(request.path[16:])
                day_object_year = int(request.path[16:20])
                day_object_month = int(request.path[20:22])
                day_object_day = int(request.path[22:24])
                day_object = date(day_object_year, day_object_month, day_object_day)
                for i in range(len(new_food_data)):
                    temp_contained_food_name = ""
                    temp_contained_calories_amount = 0
                    temp_contained_carbohydrate = 0
                    temp_contained_protein = 0
                    temp_contained_fat = 0
                    temp_contained_food_code = ""

                    temp_data_list = list(new_food_data[i].split("+"))
                    if temp_data_list[0]:
                        temp_contained_food_name = temp_data_list[0]
                    if temp_data_list[1]:
                        temp_contained_calories_amount = temp_data_list[1]
                    if temp_data_list[2]:
                        temp_contained_carbohydrate = temp_data_list[2]
                    if temp_data_list[3]:
                        temp_contained_protein = temp_data_list[3]
                    if temp_data_list[4]:
                        temp_contained_fat = temp_data_list[4]
                    if temp_data_list[5]:
                        temp_contained_food_code = temp_data_list[5]

                    username = request.user
                    user_id = Account.objects.filter(username=username).values_list()[0][0]
                    today_nutr = TodayCalories(
                        userId=Account.objects.get(id=user_id),
                        foodName=temp_contained_food_name,
                        calories=temp_contained_calories_amount,
                        carb=temp_contained_carbohydrate,
                        prot=temp_contained_protein,
                        fat=temp_contained_fat,
                        date=day_object,
                        foodCode=temp_contained_food_code,
                    )
                    today_nutr.save()
                return redirect('/dmgcapp/search/%d' % path_day_string)

            url = "http://openapi.foodsafetykorea.go.kr/api/6f79706705224d619099/I2790/json/1/100/DESC_KOR=%s"         # 검색어 - 제품명
            search_food_name = request.POST.get('search')

            # 음식 이름에 공백이 있으면 api 호출이 정상 작동 하지 않음
            # 따라서 공백을 '_'로 바꾸어 주는 작업 진행
            if search_food_name is not None and ' ' in search_food_name:
                search_food_name = search_food_name.replace(' ', '_')

            if search_food_name:
                url = "http://openapi.foodsafetykorea.go.kr/api/6f79706705224d619099/" \
                            "I2790/json/1/1000/DESC_KOR=%s" % search_food_name

            # 검색어 - 제조사
            search_company = request.POST.get('search2')

            # 제조사에 공백이 있으면 api 호출이 정상 작동 하지 않음
            # 따라서 공백을 '_'로 바꾸어 주는 작업 진행
            if search_company is not None and ' ' in search_company:
                search_company = search_company.replace(' ', '_')
            if search_company:
                url = "http://openapi.foodsafetykorea.go.kr/api/6f79706705224d619099/" \
                            "I2790/json/1/1000/MAKER_NAME=%s" % search_company

            # 검색어 - 제조사 & 제품명
            if search_company is not None and search_food_name is not None:
                if ' ' in search_company:
                    search_company = search_company.replace(' ', '_')
                if ' ' in search_food_name:
                    search_food_name = search_food_name.replace(' ', '_')
            if search_company and search_food_name:
                url = "http://openapi.foodsafetykorea.go.kr/api/6f79706705224d619099/" \
                            "I2790/json/1/1000/MAKER_NAME=%s&DESC_KOR=%s" % (search_company, search_food_name)

            temp_data = requests.get(url).json()
            json_data = temp_data.get('I2790').get('row')
            food_info_list = []
            for i in range(len(json_data)):
                # 음식이름
                food_name = json_data[i]['DESC_KOR']
                # 칼로리
                calories = json_data[i]['NUTR_CONT1']
                # 탄수화물
                carbohydrate = json_data[i]['NUTR_CONT2']
                # 단백질
                protein = json_data[i]['NUTR_CONT3']
                # 지방
                fat = json_data[i]['NUTR_CONT4']
                # 당류
                sugars = json_data[i]['NUTR_CONT5']
                # 총 내용량
                food_size = json_data[i]['SERVING_SIZE']
                # 제조사명
                maker_name = json_data[i]['MAKER_NAME']
                # 조사년도
                research_year = json_data[i]['RESEARCH_YEAR']
                # 포화지방산
                saturated_fatty_acid = json_data[i]['NUTR_CONT8']
                # 식품코드
                food_code = json_data[i]['FOOD_CD']
                temp_food_info_list = [maker_name, food_name, research_year,
                                       food_size, calories, carbohydrate,
                                       protein, fat, saturated_fatty_acid, sugars, food_code]

                food_info_list.append(temp_food_info_list)


            return render(request, 'dmgcapp/search.html', {
                "today_string": today_string,
                "month_day_list": month_day_list,
                "day_string": day_string,
                "food_info_list": food_info_list,
                "calories": calories,
            })
    except:
        messages.error(request, '검색어를 다시 한번 확인해 주세요')
        return redirect('/dmgcapp/search/%d' % today_string)

    else:
        return render(request, 'dmgcapp/search.html', {
            "today_string": today_string,
            "month_day_list": month_day_list,
            "day_string": day_string,
        })


def profile(request):
    temp_username = request.user
    temp_list = Account.objects.filter(username=temp_username).values_list()
    username = temp_list[0][1]
    nickname = temp_list[0][3]
    email = temp_list[0][4]
    goal_calories = temp_list[0][5]
    goal_calories_ratio = temp_list[0][6]
    height = temp_list[0][7]
    weight = temp_list[0][8]
    gender = temp_list[0][9]
    if gender == 'male':
        gender = '남자'
    elif gender == 'female':
        gender = '여자'
    goal_step_count = temp_list[0][10]
    birthday = temp_list[0][11]
    year = birthday[:4]
    month = birthday[4:6]
    day = birthday[6:8]
    return render(request, 'dmgcapp/profile.html', {
        'temp_list': temp_list,
        'username': username,
        'nickname': nickname,
        'email': email,
        'goal_calories': goal_calories,
        'goal_calories_ratio': goal_calories_ratio,
        'height': height,
        'weight': weight,
        'gender': gender,
        'goal_step_count': goal_step_count,
        'year': year,
        'month': month,
        'day': day
    })


def profile_edit(request):
    temp_username = request.user
    temp_list = Account.objects.filter(username=temp_username).values_list()
    user_id = temp_list[0][0]
    username = temp_list[0][1]
    nickname = temp_list[0][3]
    email = temp_list[0][4]
    goal_calories = temp_list[0][5]
    goal_calories_ratio = temp_list[0][6]
    height = temp_list[0][7]
    weight = temp_list[0][8]
    gender = temp_list[0][9]
    goal_step_count = temp_list[0][10]
    birthday = temp_list[0][11]

    if request.method == 'POST':
        new_username = request.POST['username']
        new_nickname = request.POST['nickname']
        new_email = request.POST['email']
        new_goal_calories = request.POST['goalCalories']
        new_goal_calories_ratio = request.POST['goalCaloriesRatio']
        new_height = request.POST['height']
        new_weight = request.POST['weight']
        new_gender = request.POST['gender']
        new_goal_step_count = request.POST['goalStepCount']
        temp_birthday = request.POST['birthday']
        year = temp_birthday[0:4]
        month = temp_birthday[5:7]
        day = temp_birthday[8:10]
        new_birthday = year+month+day

        is_new_username = Account.objects.filter(username=new_username).values_list()
        if is_new_username:
            if is_new_username[0][0] != user_id:
                messages.info(request, '이미 존재하는 아이디 입니다.')
                return redirect('profile_edit')

        new_account = Account.objects.get(id=user_id)
        new_account.username = new_username
        new_account.nickname = new_nickname
        new_account.email = new_email
        new_account.goalCalories = new_goal_calories
        new_account.goalCaloriesRatio = new_goal_calories_ratio
        new_account.height = new_height
        new_account.weight = new_weight
        new_account.gender = new_gender
        new_account.goalStepCount = new_goal_step_count
        new_account.birthday = new_birthday
        new_account.save()

        user = request.user
        user.username = new_username
        user.save()
        return redirect('/dmgcapp/')

    else:
        return render(request, 'dmgcapp/profile_edit.html', {
            'username': username,
            'nickname': nickname,
            'email': email,
            'goal_calories': goal_calories,
            'goal_calories_ratio': goal_calories_ratio,
            'height': height,
            'weight': weight,
            'gender': gender,
            'goal_step_count': goal_step_count,
            'birthday': birthday,
        })


def calculator(request, today_string):
    # 날짜 계산
    today = datetime.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day
    today_datetime = datetime(today_year, today_month, today_day)
    month_day_list = []
    day_string = 0

    # 3일 전부터 1일 전
    for i in range(3, 0, -1):
        one_day = today_datetime - timedelta(days=i)
        day_string = str(one_day.year)
        if 1 <= one_day.month <= 9:
            day_string += ("0" + str(one_day.month))
        else:
            day_string += str(one_day.month)

        if 1 <= one_day.day <= 9:
            day_string += ("0" + str(one_day.day))
        else:
            day_string += str(one_day.day)
        day_string = int(day_string)
        temp = [one_day.month, one_day.day, day_string]
        month_day_list.append(temp)

    # 오늘
    today_string = str(today_year)
    if 1 <= today_month <= 9:
        today_string += ("0" + str(today_month))
    else:
        today_string += str(today_month)
    if 1 <= today_day <= 9:
        today_string += ("0" + str(today_day))
    else:
        today_string += str(today_day)

    today_string = int(today_string)
    month_day_list.append([today_month, today_day, today_string])

    # 1일 후 부터 3일 후
    for i in range(1, 4):
        one_day = today_datetime + timedelta(days=i)
        day_string = str(one_day.year)
        if 1 <= one_day.month <= 9:
            day_string += ("0" + str(one_day.month))
        else:
            day_string += str(one_day.month)

        if 1 <= one_day.day <= 9:
            day_string += ("0" + str(one_day.day))
        else:
            day_string += str(one_day.day)

        day_string = int(day_string)
        temp = [one_day.month, one_day.day, day_string]
        month_day_list.append(temp)

    if request.method == "POST":
        delete_check_list = request.POST.getlist('nutr')

        username = request.user
        day_object_year = int(request.path[20:24])
        day_object_month = int(request.path[24:26])
        day_object_day = int(request.path[26:28])
        day_object = date(day_object_year, day_object_month, day_object_day)
        user_id = Account.objects.filter(username=username).values_list()[0][0]

        for food_code in delete_check_list:
            TodayCalories.objects.filter(userId=user_id, date=day_object, foodCode=food_code).delete()

        food_info_list = TodayCalories.objects.filter(userId=user_id, date=day_object).values_list()
        parsed_food_info_list = []
        today_calories = 0
        today_carb = 0
        today_prot = 0
        today_fat = 0
        for i in range(len(food_info_list)):
            calories = food_info_list[i][2]
            food_name = food_info_list[i][3]
            carb = food_info_list[i][4]
            prot = food_info_list[i][5]
            fat = food_info_list[i][6]
            food_code = food_info_list[i][7]
            date_object = food_info_list[i][8]
            year = date_object.year
            month = date_object.month
            day = date_object.day

            today_calories += float(calories)
            today_carb += float(carb)
            today_prot += float(prot)
            today_fat += float(fat)

            temp_list = [calories, food_name, carb, prot, fat,
                         food_code, year, month, day]
            parsed_food_info_list.append(temp_list)

        return render(request, 'dmgcapp/calculator.html', {
            'today_string': today_string,
            'food_info_list': food_info_list,
            'parsed_food_info_list': parsed_food_info_list,
            'today_calories': today_calories,
            'today_carb': today_carb,
            'today_prot': today_prot,
            'today_fat': today_fat,
            'day_object': day_object,
            "month_day_list": month_day_list,
        })

    else:
        username = request.user
        day_object_year = int(request.path[20:24])
        day_object_month = int(request.path[24:26])
        day_object_day = int(request.path[26:28])
        day_object = date(day_object_year, day_object_month, day_object_day)
        user_id = Account.objects.filter(username=username).values_list()[0][0]
        food_info_list = TodayCalories.objects.filter(userId=user_id, date=day_object).values_list()
        parsed_food_info_list = []

        today_calories = 0
        today_carb = 0
        today_prot = 0
        today_fat = 0
        for i in range(len(food_info_list)):
            calories = food_info_list[i][2]
            food_name = food_info_list[i][3]
            carb = food_info_list[i][4]
            prot = food_info_list[i][5]
            fat = food_info_list[i][6]
            food_code = food_info_list[i][7]
            date_object = food_info_list[i][8]
            year = date_object.year
            month = date_object.month
            day = date_object.day

            today_calories += float(calories)
            today_carb += float(carb)
            today_prot += float(prot)
            today_fat += float(fat)

            temp_list = [calories, food_name, carb, prot, fat,
                         food_code, year, month, day]
            parsed_food_info_list.append(temp_list)

        return render(request, 'dmgcapp/calculator.html', {
            'today_string': today_string,
            'food_info_list': food_info_list,
            'parsed_food_info_list': parsed_food_info_list,
            'today_calories': today_calories,
            'today_carb': today_carb,
            'today_prot': today_prot,
            'today_fat': today_fat,
            'day_object': day_object,
            "month_day_list": month_day_list,
        })


def summary(request, today_string):
    # 날짜 계산
    today = datetime.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day
    today_datetime = datetime(today_year, today_month, today_day)
    month_day_list = []
    day_string = 0

    # 3일 전부터 1일 전
    for i in range(3, 0, -1):
        one_day = today_datetime - timedelta(days=i)
        day_string = str(one_day.year)
        if 1 <= one_day.month <= 9:
            day_string += ("0" + str(one_day.month))
        else:
            day_string += str(one_day.month)

        if 1 <= one_day.day <= 9:
            day_string += ("0" + str(one_day.day))
        else:
            day_string += str(one_day.day)
        day_string = int(day_string)
        temp = [one_day.month, one_day.day, day_string]
        month_day_list.append(temp)

    # 오늘
    today_string = str(today_year)
    if 1 <= today_month <= 9:
        today_string += ("0" + str(today_month))
    else:
        today_string += str(today_month)
    if 1 <= today_day <= 9:
        today_string += ("0" + str(today_day))
    else:
        today_string += str(today_day)

    today_string = int(today_string)
    month_day_list.append([today_month, today_day, today_string])

    # 1일 후 부터 3일 후
    for i in range(1, 4):
        one_day = today_datetime + timedelta(days=i)
        day_string = str(one_day.year)
        if 1 <= one_day.month <= 9:
            day_string += ("0" + str(one_day.month))
        else:
            day_string += str(one_day.month)

        if 1 <= one_day.day <= 9:
            day_string += ("0" + str(one_day.day))
        else:
            day_string += str(one_day.day)

        day_string = int(day_string)
        temp = [one_day.month, one_day.day, day_string]
        month_day_list.append(temp)

    if request.method == 'GET':
        username = request.user
        user_id = Account.objects.filter(username=username).values_list()[0][0]
        day_object_year = int(request.path[17:21])
        day_object_month = int(request.path[21:23])
        day_object_day = int(request.path[23:25])
        day_object = date(day_object_year, day_object_month, day_object_day)
        food_info_list = TodayCalories.objects.filter(userId=user_id, date=day_object).values_list()
        parsed_food_info_list = []

        today_calories = 0
        today_carb = 0
        today_prot = 0
        today_fat = 0
        for i in range(len(food_info_list)):
            calories = food_info_list[i][2]
            food_name = food_info_list[i][3]
            carb = food_info_list[i][4]
            prot = food_info_list[i][5]
            fat = food_info_list[i][6]
            food_code = food_info_list[i][7]
            date_object = food_info_list[i][8]
            year = date_object.year
            month = date_object.month
            day = date_object.day

            today_calories += float(calories)
            today_carb += float(carb)
            today_prot += float(prot)
            today_fat += float(fat)

            temp_list = [calories, food_name, carb, prot, fat,
                         food_code, year, month, day]
            parsed_food_info_list.append(temp_list)

        return render(request, 'dmgcapp/summary.html', {
            "month_day_list": month_day_list,
            "food_info_list": food_info_list,
            "today_carb": today_carb,
            "today_prot": today_prot,
            "today_fat": today_fat,
            "today_calories": today_calories,
        })
    elif request.method == 'POST':
        pass


def setting(request):
    pass
