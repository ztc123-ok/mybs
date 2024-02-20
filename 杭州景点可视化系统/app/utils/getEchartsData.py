from app.utils import getPublicData
import datetime

XcSightData = getPublicData.getAllXcSightInfoData()
XcSightData = list(filter(lambda x: 'hangzhou14' in x.url or 'jiande687' in x.url or 'tonglu688' in x.url or'chunan2249' in x.url, XcSightData))
WestlakeData = getPublicData.getAllWestlakesInfoData()

def districtCharData():
    dataDic = {}
    hangzhou_districts = getPublicData.hangzhou_districts
    for sight in XcSightData:
        for district in hangzhou_districts:
            if district in sight.address:
                if district in dataDic:
                    dataDic[district] += 1
                else:
                    dataDic[district] = 1
    return list(dataDic.keys()),list(dataDic.values())

def districtHotData(district):
    hotDic = {}
    for sight in XcSightData:
        if district in sight.address or district == '全部':
            if str(sight.heat_score) in hotDic:
                hotDic[str(sight.heat_score)] += 1
            else:
                hotDic[str(sight.heat_score)] = 1
    resultData = []
    for key,value in hotDic.items():
        resultData.append({
            'name':key,
            'value':value,
        })
    print(resultData)
    return resultData

def districtScoreData(district):
    ScoreDic = {}
    for sight in XcSightData:
        if district in sight.address or district == '全部':
            if str(sight.comment_score) in ScoreDic:
                ScoreDic[str(sight.comment_score)] += 1
            else:
                ScoreDic[str(sight.comment_score)] = 1
    resultData = []
    for key,value in ScoreDic.items():
        resultData.append({
            'name':key,
            'value':value,
        })
    print(resultData)
    return resultData

def passengerCharData(sight_name):
    sightList = []
    passengerDic = {}
    for sight in WestlakeData:
        if sight.sight_name not in sightList:
            sightList.append(sight.sight_name)
        if sight.sight_name == sight_name:
            passengerDic[str(sight.mydate)] = float(sight.passenger_number)
    print(list(passengerDic.keys()))
    print(list(passengerDic.values()))
    return sightList,list(passengerDic.keys()),list(passengerDic.values())