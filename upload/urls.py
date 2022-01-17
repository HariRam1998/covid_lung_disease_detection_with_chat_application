from django.contrib import admin
from django.urls import path, re_path, include
from . import views

# app_name = 'main'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.user_home, name='user_home'),
    path('lung/', views.covidlung, name= 'covidlung'),
    path('register/', views.register, name= 'user_register'),
    path('login/', views.login1, name= 'user_login'),
    path('logout/', views.logoutfun, name= 'logout'),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
    ]
