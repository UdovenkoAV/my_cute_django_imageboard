from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [path('<slug:board_slug>/', views.thread_list, name='thread_list'),
               path('<slug:board_slug>/<int:id>/', views.thread_detail, name='thread_detail'),
               path('', views.index, name='index')]
