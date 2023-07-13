from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_feed, name='home_feed'),
    path('event/<uuid:pk>/', views.event_detail, name='event_detail'),
]