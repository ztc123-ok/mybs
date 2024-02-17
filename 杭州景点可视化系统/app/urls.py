from django.urls import path
from app import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
]