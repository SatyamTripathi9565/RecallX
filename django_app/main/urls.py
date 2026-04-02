from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),      # main page
    path('chat/', views.chat), # AI chat
]