from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth.models import User
from django.contrib import messages, auth
import hashlib
# Create your views here.


def index(request):
    return render(request, 'dmgcapp/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/dmgcapp/')
        else:
            messages.info(request, '아이디 혹은 비밀번호가 잘못되었습니다')
            return redirect('login')
    else:
        return render(request, 'dmgcapp/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/dmgcapp/')


def signup(request):
    if request.method == 'POST':
        if Account.objects.filter(username=request.POST['username']).values():
            messages.info(request, '이미 존재하는 아이디 입니다.')
            return redirect('signup')

        # 비밀번호가 10자리 미만으로 구성 될 경우
        elif len(request.POST['password1']) < 10:
            messages.info(request, '비밀번호는 10자 이상으로 설정해주세요')
            return redirect('signup')

        # 비밀번호가 서로 일치 하지 않는 경우
        elif request.POST['password1'] != request.POST['password2']:
            messages.info(request, '비밀번호가 서로 일치하지 않습니다. 확인해 주세요')
            return redirect('signup')

        # 비밀번호가 서로 일치 할 경우
        elif request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            password = request.POST['password1']
            password_crypt = hashlib.sha256(password.encode('utf-8')).hexdigest()
            nickname = request.POST['nickname']
            email = request.POST['email']
            user = Account(username=username,
                         password=password_crypt,
                         nickname=nickname,
                         email=email)
            user.save()
            User.objects.create_user(username=username,
                                     password=password)
            return redirect('/dmgcapp/')
    else:
        return render(request, 'dmgcapp/signup.html')

def foodlist(request):
    key_id = "6f79706705224d619099/"
    service_id = "I0750/"
    datatype = 'json/'
    start_idx = "1/"
    end_idx = "5"
    front_url = "http://openapi.foodsafetykorea.go.kr/api/"
    url = front_url + key_id + service_id + datatype + start_idx + end_idx


    return render(request, 'dmgcapp/foodlist.html')
