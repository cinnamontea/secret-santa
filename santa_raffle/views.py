from django.shortcuts import render
from django.utils import timezone
from .models import Event

# Create your views here.

def home_feed(request):
    #my_events = Event.objects.filter(organizer=)
    events = Event.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'santa_raffle/home_feed.html', {'events': events} )