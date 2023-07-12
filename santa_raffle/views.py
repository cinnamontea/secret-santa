from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event, Participant, CustomUser

# Create your views here.

def home_feed(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    participant = user.participant_set.all().order_by('event__created_date')
    events = participant.values('event__id', 'event__organizer', 'event__title')
    for e in events:
        e['event__organizer'] = CustomUser.objects.get(id=e['event__organizer'])
    return render(request, 'santa_raffle/home_feed.html', {'events': events} )


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    members = event.get_members_id()
    return render(request, 'santa_raffle/event_detail.html', 
                  {'event': event,
                   'members': members,
                   })