from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('greet/<str:name>', views.greeting, name='greet'),

    path('secondgreet/<str:name>', views.second_greeting, name='greet'),

]