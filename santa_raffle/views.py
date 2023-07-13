from django.shortcuts import render, get_object_or_404, redirect
from .forms import EventForm, ParticipantForm
from .models import Event, Participant, CustomUser

# Create your views here.

def home_feed(request):
    user = None
    events = None
    context = {}

    if request.user.is_authenticated:
        user = request.user
        participant = user.participant_set.all().order_by('event__created_date')
        events = participant.values('event__id', 'event__organizer', 'event__title')
        for e in events:
            e['event__organizer'] = CustomUser.objects.get(id=e['event__organizer'])
        context['events'] = events
    #return render(request, 'santa_raffle/home_feed.html', context)
    return render(request, 'santa_raffle/home_feed.html', {'events': events} )


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    members = event.get_members_id()
    return render(request, 'santa_raffle/event_detail.html', 
                  {'event': event,
                   'members': members,
                   })


def new_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'santa_raffle/event_edit.html', {'form': form})


def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'santa_raffle/event_edit.html', {'form': form})

