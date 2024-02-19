from django.urls import path
from app import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logOut/', views.logOut, name='logOut'),
    path('home/',views.home,name='home'),
    path('changeSelfInfo/',views.changeSelfInfo,name='changeSelfInfo'),
    path('changePassword/',views.changePassword,name='changePassword'),
]