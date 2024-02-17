from django.shortcuts import render,redirect
from app.models import User
from django.http import HttpResponse
from app.utils import errorResponse
import time
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User.objects.get(username=username,password=password)
            request.session['username'] = username
            return HttpResponse('登录成功即将跳转到首页')
        except:
            return errorResponse.errorResponse(request,'用户名或密码错误')


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        try:
            User.objects.get(username=username)
        except:
            if not username or not password or not confirmPassword:
                return errorResponse.errorResponse(request,'不允许为空值')
            if password != confirmPassword:
                return errorResponse.errorResponse(request,'两次密码不一致')
            User.objects.create(username=username,password=password,avatar='default.png',createtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return redirect('/app/login')

        return errorResponse.errorResponse(request,'该用户名已存在')


