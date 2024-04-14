from django.urls import path
from app import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logOut/', views.logOut, name='logOut'),
    path('home/',views.home,name='home'),
    path('changeSelfInfo/',views.changeSelfInfo,name='changeSelfInfo'),
    path('changePassword/',views.changePassword,name='changePassword'),
    path('tableData/',views.tableData,name='tableData'),
    path('getDetail/<int:id>',views.getDetail,name='getDetail'),
    path('districtChar/',views.districtChar,name='districtChar'),
    path('rateChar/',views.rateChar,name='rateChar'),
    path('passengerChar/',views.passengerChar,name='passengerChar'),
    path('taskSetting/',views.taskSetting,name='taskSetting'),
]