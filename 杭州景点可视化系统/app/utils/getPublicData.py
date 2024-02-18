from app.models import XcSight, User


def getAllXcSightInfoData():
    return XcSight.objects.all()


def getAllUsersInfoData():
    return User.objects.all()
