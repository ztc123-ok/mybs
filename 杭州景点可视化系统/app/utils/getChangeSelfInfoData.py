from app.models import XcSight, User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def changeSelfInfo(username,formData,file):
    user = User.objects.get(username=username)
    user.address = formData['address']
    user.sex = formData['sex']
    if formData['textarea']:
        user.textarea = formData['textarea']
    if file.get('avatar') != None:
        print(file.get('avatar').name)
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'avatar'))

        # 保存文件到MEDIA_ROOT，并获取保存后的文件名
        filename = fs.save(file.get('avatar').name,file.get('avatar'))
        user.avatar = 'avatar/'+filename
    user.save()

def getChangePassword(userInfo,passwordInfo):
    oldPwd = passwordInfo['oldPassword']
    newPwd = passwordInfo['newPassword']
    newPwdConfirm = passwordInfo['newPasswordConfirm']
    user = User.objects.get(username=userInfo.username)

    if oldPwd != userInfo.password:
        return "原始密码不正确"
    if newPwd != newPwdConfirm:
        return "两次密码输入不一致"

    user.password = newPwd
    user.save()
