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
        participant = user.participant_set.all().order_by('-event__created_date')
        events = participant.values('event__id', 'event__organizer', 'event__title')
        for e in events:
            e['event__organizer'] = CustomUser.objects.get(id=e['event__organizer'])
        context['events'] = events
    #return render(request, 'santa_raffle/home_feed.html', context)
    return render(request, 'santa_raffle/home_feed.html', {'events': events} )


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    members = event.get_members_id()
    form = ParticipantForm()
    return render(request, 'santa_raffle/event_detail.html', 
                  {'event': event,
                   'members': members,
                   'form': form
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

def event_invite_form(request):
    form = ParticipantForm(request.POST)
    return render(request, 'santa_raffle/event_detail.html', {'form': form})

def event_invites(request, pk):
    print(">>pk:", pk)
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        form = ParticipantForm(request.POST)
        print(">>form:", form)
        if form.is_valid():# and CustomUser.filter(username__iexact=user):
                participant = form.save(commit=False)
                print(participant)
                participant.event = event
                participant.save()
                return redirect('event_detail', pk=event.pk)
    else:
        form = ParticipantForm()
    return render(request, 'santa_raffle/event_detail.html', {'form': form})

#def user_search(request, keyword):
#    queryset_list = CustomUser.objects.filter(username__contains=keyword)
#    return render(request, 'santa_raffle/event_invites.html', {'form': queryset_list})