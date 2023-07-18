from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_feed, name='home_feed'),
    path('event/<uuid:pk>/', views.event_detail, name='event_detail'),
    path('event/new', views.new_event, name='new_event'),
    path('event/<uuid:pk>/edit/', views.edit_event, name='edit_event'),
    path('event/<uuid:pk>/invited/', views.event_invites, name='event_invites'),
    path('event/<uuid:pk>/confirm/<int:resp>', views.update_confirmation, name='update_confirmation'),
    path('event/<uuid:pk>/start/', views.start_raffle, name='start_raffle'),
    path('event/<uuid:event_pk>/getmsgs', views.get_messages, name='getmsgs'),
    path('event/sendmsg', views.send_message, name='sendmsg'),
]