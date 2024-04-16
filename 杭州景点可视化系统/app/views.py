from django.shortcuts import render,redirect
from app.models import User,TaskSetting,TextCNN,XcSight
from django.http import HttpResponse
from app.utils import errorResponse,getHomeData,getPublicData,getChangeSelfInfoData,getTableData,getEchartsData,getDetailData
import time
import re
from machineLearning import textCNN,use_textCNN
from spider import update_sight
from machineLearning import LDA
from app.task import mytask

# 哈哈哈，线程居然可以放在这启动
mytask.doTask()

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
    sightText = 'None'
    # global page_end, page_start
    try:
        # 获取url中的page值，并将默认值设置为1
        page = int(request.GET.get('page', 1))
        sightText = request.GET.get('sightText', 'None')
        tableData = getTableData.getSortHotTableData(sightText)
        # print(page, type(page))
        if page < 1:
            page = 1
    except Exception:
        page = 1
    # print(page)

    if request.method == 'POST':
        sightText = request.POST.get('sightText')
        tableData = getTableData.getSortHotTableData(sightText)

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
        '<li class="page-item"><a class="page-link" href="?page=%s&sightText=%s" aria-label="上一页"><span aria-hidden="true">&laquo;</span></a></li>' % (page - 1,sightText))
    for i in range(page_start, page_end + 1):
        if page == i:
            html_list.append('<li class="page-item active" aria-current="page"><a class="page-link" href="?page=%s&sightText=%s">%s</a></li>' % (i, sightText ,i))
        else:
            html_list.append('<li class="page-item"><a class="page-link" href="?page=%s&sightText=%s">%s</a></li>' % (i,sightText ,i))
    if page == total_num:
        html_list.append('<li class="page-item disabled"><a class="page-link">下一页</a></li>')
    else:
        html_list.append(
        '<li class="page-item"><a class="page-link" href="?page=%s&sightText=%s" aria-label="下一页"><span aria-hidden="true">&raquo;</span></a></li>' % (page + 1,sightText)
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
        'sightText':sightText,
    })

def getDetail(request,id):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    sight = getDetailData.getSightById(id)
    CommentsTimesort,positiveRate = getDetailData.getCommentsById(id)
    try:
        sight.photos = sight.photos.split(",")[0].split("\"")[1]
    except:
        pass
    try:
        topicWords = sight.topic.split(";")[0].split(" ")
        senceWords = sight.topic.split(";")[1].split(" ")
    except:
        # print("正在处理景点 ",sight.id," 的主题词")
        # topic = LDA.doLDA(id)
        # sight.topic = topic
        # sight.save()
        # topicWords = topic.split(";")[0].split(" ")
        # senceWords = topic.split(";")[1].split(" ")
        topicWords = "这个景点太冷门了"
        senceWords = "这个景点太冷门了"

    return render(request, 'detail.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
        'sight':sight,
        'LDA':{
            'topicWords':topicWords,
            'senceWords':senceWords,
        },
        'CommentsTimesort':CommentsTimesort,
        'positiveRate':positiveRate,
    })


def districtChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    Xdata,ydata = getEchartsData.districtCharData()
    return render(request,'districtChar.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
        'districtCharData':{
            'Xdata':Xdata,
            'ydata':ydata,
        }
    })

def rateChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    districtList = ["全部"] + getPublicData.hangzhou_districts
    hotList = getEchartsData.districtHotData("全部")
    scoreList = getEchartsData.districtScoreData("全部")
    choose = "全部"
    if request.method == 'POST':
        hotList = getEchartsData.districtHotData(request.POST.get('district'))
        scoreList = getEchartsData.districtScoreData(request.POST.get('district'))
        choose = request.POST.get('district')

    return render(request,'rateChar.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
        'districtList':districtList,
        'hotList':hotList,
        'scoreList':scoreList,
        'choose':choose,
    })

def passengerChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    sightName = "灵隐飞来峰"
    if request.method == 'POST':
        sightName = request.POST.get('sightName')
    sightList, XData, yData = getEchartsData.passengerCharData(sightName)
    return render(request,'passengerChar.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
        'sightList': sightList,
        'sightName': sightName,
        'echartsData':{
            'XData':XData,
            'yData':yData,
        },
    })

def taskSetting(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    taskInfo = TaskSetting.objects.get(id=1)
    if request.method == 'POST':
        update_type = str(request.POST.get('update_type'))
        update_time = request.POST.get('update_time')
        print("update_type",update_type)
        # 更新定时任务
        if update_type == "0":
            if not request.POST.get('update_time'):
                update_time = taskInfo.update_time
            pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
            if re.match(pattern, update_time):
                taskInfo.update_time = update_time
                if request.POST.get('spider_type'):
                    taskInfo.spider_type = request.POST.get('spider_type')
                if request.POST.get('machine_type'):
                    taskInfo.machine_type = request.POST.get('machine_type')
                taskInfo.save()
            else:
                return errorResponse.errorResponse(request,'定时任务时间设置有误 00:00')
        # 更新景点评论
        elif update_type == "1":
            if request.POST.get('sight_id'):
                sight_id = request.POST.get('sight_id')
                print("正在更新一个景点的评论。。。", sight_id)
                sightInfo = XcSight.objects.get(id=sight_id)
                update_sight.update_sight(sightInfo.url)
        # 标注特定景点
        elif update_type == "2":
            if request.POST.get('sight_id'):
                sight_id = request.POST.get('sight_id')
                print("正在标注一个景点评论的情感。。。", sight_id)
                use_textCNN.textCNNOne(sight_id)
    taskInfo = TaskSetting.objects.get(id=1)
    return render(request,'taskSetting.html',{
        'userInfo': userInfo,
        'taskInfo':taskInfo,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
    })

def modelSetting(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    textCNN_parameter = TextCNN.objects.get(best_use=1)
    model_rating = {
        'accuracy': '待评估',
        'precisions': '待评估',
        'recall': '待评估',
        'specificity': '待评估',
        'new_parameter': {id: ''},
    }
    if request.method == 'POST':
        if not request.POST.get('embedding'):
            embedding = int(textCNN_parameter.embedding)
        else:
            embedding = int(request.POST.get('embedding'))
        if not request.POST.get('epoch'):
            epoch = int(textCNN_parameter.epoch)
        else:
            epoch = int(request.POST.get('epoch'))
        if not request.POST.get('learning_rate'):
            learning_rate = float(textCNN_parameter.learning_rate)
        else:
            learning_rate = float(request.POST.get('learning_rate'))
        if not request.POST.get('max_len'):
            max_len = int(textCNN_parameter.max_len)
        else:
            max_len = int(request.POST.get('max_len'))
        if not request.POST.get('batch_size'):
            batch_size = int(textCNN_parameter.batch_size)
        else:
            batch_size = int(request.POST.get('batch_size'))
        hidden_num = 2

        # 区分该post请求是 更新模型操作 还是 训练模型操作
        if request.POST.get('update_model'):
            print(request.POST.get('update_model'),request.POST.get('update_id'))
            with open('machineLearning/textCNN_new.pt', 'rb') as file1:
                content = file1.read()
            with open('machineLearning/textCNN.pt', 'wb') as file2:
                file2.write(content)
            with open('machineLearning/word_2_index_new.json', 'rb') as file1:
                content = file1.read()
            with open('machineLearning/word_2_index.json', 'wb') as file2:
                file2.write(content)
            textCNN_parameter.best_use = 0
            textCNN_parameter.save()
            update_parameter = TextCNN.objects.get(id=request.POST.get('update_id'))
            update_parameter.best_use = 1
            update_parameter.save()
        else:
            accuracy,precisions,recall,specificity = textCNN.train_model(embedding,epoch,learning_rate,max_len,batch_size,hidden_num)
            model_rating['accuracy'] = accuracy
            model_rating['precisions'] = precisions
            model_rating['recall'] = recall
            model_rating['specificity'] = specificity
            new_parameter = TextCNN.objects.create(embedding=embedding, epoch=epoch, learning_rate=learning_rate,
                                max_len=max_len,batch_size=batch_size,hidden_num=hidden_num,accuracy=accuracy,precisions=precisions,
                                   recall=recall,specificity=specificity,best_use=0)
            model_rating['new_parameter'] = new_parameter
            print("id",new_parameter.id)
    textCNN_parameter = TextCNN.objects.get(best_use=1)
    return render(request,'modelSetting.html',{
        'userInfo': userInfo,
        'textCNN_parameter': textCNN_parameter,
        'model_rating': model_rating,
        'nowTime': {
            'year': year,
            'mon': mon,
            'day': day,
        },
    })
