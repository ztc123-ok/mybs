from app.utils import getPublicData
import heapq
import time
from datetime import datetime

userData = getPublicData.getAllUsersInfoData()
XcSightData = getPublicData.getAllXcSightInfoData()
XcSightData = list(filter(lambda x: 'hangzhou14' in x.url or 'jiande687' in x.url or 'tonglu688' in x.url or'chunan2249' in x.url, XcSightData))

# 获取主页数据
def getHomeTagData():
    sightNumber = 0
    commentsLenMax = 0
    commentsName = ''
    heatScoreMax = 0
    heatScoreName = ''
    for sight in XcSightData:
        sightNumber = sightNumber + 1
        if sight.comment_count > commentsLenMax:
            commentsLenMax = sight.comment_count
            commentsName = sight.name
        if sight.heat_score > heatScoreMax:
            heatScoreMax = sight.heat_score
            heatScoreName = sight.name
    return sightNumber,commentsLenMax,commentsName,heatScoreMax,heatScoreName

# 获取热度前10的景点
def getSortData():
    sortedObjects = sorted(list(XcSightData), key=lambda obj: obj.heat_score, reverse=True)
    hotTop10Data = sortedObjects[:10]
    for i in range(len(hotTop10Data)):
        try:
            hotTop10Data[i].photos = hotTop10Data[i].photos.split(",")[0].split("\"")[1]
        except:
            pass
    # print(top_10)
    return hotTop10Data

# 获取当前时间
def getNowTime():
    timeFormat = time.localtime()
    year = timeFormat.tm_year
    mon = timeFormat.tm_mon
    day = timeFormat.tm_mday
    return year,mon,day

# 获取地图统计数据
def getGeoData():
    dataDic = {}
    hangzhou_districts = getPublicData.hangzhou_districts
    for sight in XcSightData:
        for district in hangzhou_districts:
            if district in sight.address:
                if district in dataDic:
                    dataDic[district] += 1
                else:
                    dataDic[district] = 1
    resultData = []
    for key,value in dataDic.items():
        resultData.append({
            'name':key,
            'value':value,
        })
    print(resultData)
    return resultData

def getUserCreateTimeData():
    dataDic = {}
    for user in userData:
        createtime = str(user.createtime.date())
        if dataDic.get(createtime,-1) == -1:
            dataDic[createtime] = 1
        else:
            dataDic[createtime] = dataDic[createtime] + 1
    resultData = []
    for key,value in dataDic.items():
        resultData.append({
            'name':key,
            'value':value,
        })
    print(resultData)
    return resultData

