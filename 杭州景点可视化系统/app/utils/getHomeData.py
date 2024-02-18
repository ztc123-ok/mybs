from app.utils import getPublicData
import heapq

XcSightData = getPublicData.getAllXcSightInfoData()
XcSightData = list(filter(lambda x: 'hangzhou14' in x.url, XcSightData))

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

def getSortData():
    sortedObjects = sorted(list(XcSightData), key=lambda obj: obj.heat_score, reverse=True)
    hotTop10Data = sortedObjects[:10]
    for i in range(len(hotTop10Data)):
        hotTop10Data[i].photos = hotTop10Data[i].photos.split(",")[0].strip()
    # print(top_10)
    return hotTop10Data
