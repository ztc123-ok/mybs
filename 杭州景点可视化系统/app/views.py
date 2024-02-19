from django.shortcuts import render,redirect
from app.models import User
from django.http import HttpResponse
from app.utils import errorResponse,getHomeData,getPublicData,getChangeSelfInfoData,getTableData
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
    hotTop10Data = getHomeData.getSortHot()
    year, mon, day = getHomeData.getNowTime()
    geoData = getHomeData.getGeoData()
    userBarCharData = getHomeData.getUserCreateTimeData()
    scoreTop10Data = getHomeData.getSortScore()
    return render(request,'home.html',{
        'userInfo':userInfo,
        'sightNumber':sightNumber,
        'commentsLenMax':commentsLenMax,
        'commentsName':commentsName,
        'heatScoreName':heatScoreName,
        'heatScoreMax':heatScoreMax,
        'hotTop10Data':hotTop10Data,
        'scoreTop10Data':scoreTop10Data,
        'nowTime':{
            'year':year,
            'mon':mon,
            'day':day,
        },
        'geoData':geoData,
        'userBarCharData':userBarCharData,
    })

def changeSelfInfo(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    if request.method == 'POST':
        getChangeSelfInfoData.changeSelfInfo(username,request.POST,request.FILES)
        userInfo = User.objects.get(username=username)
    return render(request,'changeSelfInfo.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
    })

def changePassword(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    if request.method == 'POST':
        res = getChangeSelfInfoData.getChangePassword(userInfo,request.POST)
        if res != None:
            return errorResponse.errorResponse(request,res)
    return render(request,'changePassword.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
    })

def tableData(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    tableData = getTableData.getSortHotTableData()

    # global page_end, page_start
    try:
        # 获取url中的page值，并将默认值设置为1
        page = int(request.GET.get('page', 1))
        # print(page, type(page))
        if page < 1:
            page = 1
    except Exception:
        page = 1
    # print(page)

    # 每页显示的数量
    page_num = 7

    # 计算总页码数
    # divmod为len(user_list) / page_num，整数为total_num，余数为remainder
    total_num, remainder = divmod(len(tableData), page_num)
    if remainder != 0:
        total_num += 1
    # print(total_num)

    # 每页显示的总页码数
    max_page_num = 7

    # 每页显示总页码数一半数
    half_num = max_page_num // 2
    # 实际总页码数 < 页面总页码数
    if total_num < max_page_num:
        # 页码起始值
        page_start = 1
        # 页码终止值
        page_end = total_num
    # 实际总页码数 > 页面总页码数
    else:
        # 处理左边极值
        if page - half_num < 1:
            page_start = 1
            page_end = max_page_num
        # 处理右边极值
        elif page + half_num > total_num:
            page_start = total_num - max_page_num + 1
            page_end = total_num
        else:
            page_start = page - half_num
            page_end = page + half_num

    html_list = []
    if page == 1:
        html_list.append('<li class="page-item disabled"><a class="page-link">上一页</a></li>')
    else:
        html_list.append(
        '<li class="page-item"><a class="page-link" href="?page=%s" aria-label="上一页"><span aria-hidden="true">&laquo;</span></a></li>' % (page - 1))
    for i in range(page_start, page_end + 1):
        if page == i:
            html_list.append('<li class="page-item active" aria-current="page"><a class="page-link" href="?page=%s">%s</a></li>' % (i, i))
        else:
            html_list.append('<li class="page-item"><a class="page-link" href="?page=%s">%s</a></li>' % (i, i))
    if page == total_num:
        html_list.append('<li class="page-item disabled"><a class="page-link">下一页</a></li>')
    else:
        html_list.append(
        '<li class="page-item"><a class="page-link" href="?page=%s" aria-label="下一页"><span aria-hidden="true">&raquo;</span></a></li>' % (page + 1)
        )
    html_list = ''.join(html_list)

    # 起始
    # start = 0
    start = (page - 1) * page_num
    # 终止
    # end = 7
    end = page * page_num

    return render(request,'tableData.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
        'tableData':tableData[start: end],
        'html_list': html_list,
    })

def getDetail(request,id):
    print("id",id)


def districtChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    return render(request,'districtChar.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
    })