from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_feed, name='home_feed'),
    path('event/<uuid:pk>/', views.event_detail, name='event_detail'),
    path('event/new', views.new_event, name='new_event'),
    path('event/<uuid:pk>/edit/', views.edit_event, name='edit_event'),
]