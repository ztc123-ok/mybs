from app.utils import getPublicData
import heapq
import time
from datetime import datetime

userData = getPublicData.getAllUsersInfoData()
XcSightData = getPublicData.getAllXcSightInfoData()
XcSightData = list(filter(lambda x: 'hangzhou14' in x.url or 'jiande687' in x.url or 'tonglu688' in x.url or'chunan2249' in x.url, XcSightData))

def getSortHotTableData():
    sortedObjects = sorted(list(XcSightData), key=lambda obj: obj.heat_score, reverse=True)
    hotData = []
    for i in range(len(sortedObjects)):
        try:
            sortedObjects[i].photos = sortedObjects[i].photos.split(",")[0].split("\"")[1]
        except:
            pass
        hotData.append(sortedObjects[i])
    # print(top_10)
    return hotData