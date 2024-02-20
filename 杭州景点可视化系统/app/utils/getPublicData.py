from app.models import XcSight, User,Westlake,XcComments,XcCommentsTimesort
import time

hangzhou_districts = [
    "上城区",
    "下城区",
    "江干区",
    "拱墅区",
    "西湖区",
    "滨江区",
    "萧山区",
    "余杭区",
    "临安区",
    "富阳区",
    "建德市",
    "桐庐县",
    "淳安县"
]

def getAllXcSightInfoData():
    return XcSight.objects.all()


def getAllUsersInfoData():
    return User.objects.all()

def getAllWestlakesInfoData():
    WestlakeData = sorted(Westlake.objects.all(), key=lambda x: x.mydate)
    return WestlakeData

def getAllCommentsData():
    return XcComments.objects.all()

def getAllCommentsTimesortData():
    CommentsTimesortData = sorted(XcCommentsTimesort.objects.all(), key=lambda x: x.comments_time ,reverse=True)
    return CommentsTimesortData

