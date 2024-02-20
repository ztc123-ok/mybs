from app.utils import getPublicData
import heapq
import time
from datetime import datetime

userData = getPublicData.getAllUsersInfoData()
XcSightData = getPublicData.getAllXcSightInfoData()
XcSightData = list(filter(lambda x: 'hangzhou14' in x.url or 'jiande687' in x.url or 'tonglu688' in x.url or'chunan2249' in x.url, XcSightData))
CommentsData = getPublicData.getAllCommentsData()
CommentsTimesortData = getPublicData.getAllCommentsTimesortData()
def getSightById(id):
    for sight in XcSightData:
        if sight.id == id:
            return sight
    return None

def getCommentsById(id):
    CommentsTimesort = []
    flag = 0
    for i in CommentsTimesortData:
        if i.sight_id == id:
            CommentsTimesort.append(i)
            flag = flag + 1
        if flag == 10:
            break
    return CommentsTimesort