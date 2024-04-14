from app.utils import getPublicData
from mechineLearning import LDA,use_textCNN
import heapq
import time
from datetime import datetime

userData = getPublicData.getAllUsersInfoData()
XcSightData = getPublicData.getAllXcSightInfoData()
XcSightData = list(filter(lambda x: 'hangzhou14' in x.url or 'jiande687' in x.url or 'tonglu688' in x.url or'chunan2249' in x.url, XcSightData))
# CommentsData = getPublicData.getAllCommentsData()
# CommentsTimesortData = getPublicData.getAllCommentsTimesortData()

def getSightById(id):
    for sight in XcSightData:
        if sight.id == id:
            return sight
    return None

# def doTextCNN(id):
#     CommentsTimesort = []
#     comments = []
#     labels = []
#     for i in range(len(CommentsTimesortData)):
#         if(CommentsTimesortData[i].sight_id == id):
#             CommentsTimesort.append(CommentsTimesortData[i])
#     for i in range(len(CommentsTimesort)):
#         comments.append(CommentsTimesort[i].comments)
#         labels.append(CommentsTimesort[i].id)
#     results = use_textCNN.doTextCNN(comments,labels)
#     for i in range(len(CommentsTimesort)):
#         CommentsTimesort[i].positive = results[i]
#         CommentsTimesort[i].save()
#     return CommentsTimesort

def getCommentsById(id):
    # CommentsTimesortData = doTextCNN(id) # 这里本来打算点击一个更新一个，但响应太慢了，打算定时批量更新

    CommentsTimesortData = getPublicData.getAllCommentsTimesortData(id)

    CommentsTimesort = []
    count = 0
    positive = 0
    for i in CommentsTimesortData:
        if i.sight_id == id:
            if count < 10:
                CommentsTimesort.append(i)
            if i.positive == '好评':
                positive = positive + 1
            count = count + 1
    if count > 0:
        positiveRate = round(positive/count*100,2)
    else:
        positiveRate = 0
    return CommentsTimesort,positiveRate