from django.shortcuts import render,redirect
from app.models import User
from django.http import HttpResponse
from app.utils import errorResponse,getHomeData
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
            return redirect('/app/home')
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
            User.objects.create(username=username,password=password,avatar='avatar/default.png',createtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return redirect('/app/login')

        return errorResponse.errorResponse(request,'该用户名已存在')

def logOut(request):
    request.session.clear()
    return redirect('/app/login')

def home(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    sightNumber,commentsLenMax,commentsName,heatScoreMax,heatScoreName = getHomeData.getHomeTagData()
    hotTop10Data = getHomeData.getSortData()
    return render(request,'home.html',{
        'userInfo':userInfo,
        'sightNumber':sightNumber,
        'commentsLenMax':commentsLenMax,
        'commentsName':commentsName,
        'heatScoreName':heatScoreName,
        'heatScoreMax':heatScoreMax,
        'hotTop10Data':hotTop10Data,
    })