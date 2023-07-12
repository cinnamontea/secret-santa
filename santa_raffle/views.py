from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event

# Create your views here.

def home_feed(request):
    events = Event.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'santa_raffle/home_feed.html', {'events': events} )

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    members = event.get_members_id()

    return render(request, 'santa_raffle/event_detail.html', 
                  {'event': event,
                   'members': members,
                   })