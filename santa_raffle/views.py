from django.shortcuts import render, get_object_or_404, redirect
from .forms import EventForm, ParticipantForm, EventMembersForm
from .models import Event, Participant, CustomUser

# Create your views here.

def home_feed(request):
    user = None
    events = None
    context = {}

    if request.user.is_authenticated:
        user = request.user
        participants = user.participant_set.all().order_by('-event__created_date')
        events = participants.values('event__id', 'event__organizer', 'event__title', 'confirmed')
        for e in events:
            e['event__organizer'] = CustomUser.objects.get(id=e['event__organizer'])
        #context['events'] = events
    #return render(request, 'santa_raffle/home_feed.html', context)
    return render(request, 'santa_raffle/home_feed.html', {'events': events} )


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    members = event.get_members_id()

    form = EventMembersForm()
    #form = ParticipantFormSet(queryset=CustomUser.objects.exclude(id=request.user.id))
    return render(request, 'santa_raffle/event_detail.html', 
                  {'event': event,
                   'members': members,
                   'form': form
                   })


def new_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        print(form)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()
            event.members.add(request.user)
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


#def event_invite_form_set(request):
#    formset = ParticipantFormSet(request.POST)
#    return render(request, 'santa_raffle/event_detail.html', {'form': formset})


def event_invites(request, pk):
    print(">>pk:", pk)
    if request.method == "POST":
        invited_event = get_object_or_404(Event, pk=pk)
        print(">>event:", invited_event, invited_event.members, invited_event.members)
        #form = ParticipantFormSet(request.POST)
        #print(request.POST)
        form = EventMembersForm(request.POST)
        if form.is_valid():# and CustomUser.filter(username__iexact=user):
            #for formuser in form.get_queryset():
            #print("formuser:", formuser)
            #user_list = form.data['members']
            for user_id in form.data['members']:
                print(">>user_id:", user_id)
                invited_user = get_object_or_404(CustomUser, pk=user_id)
                participant = None
                if not invited_event.members.contains(invited_user):
                    participant = Participant.objects.create(owner=invited_user, event=invited_event)
                    print(participant, participant.owner, participant.event)
                    #participant = Participant(owner=invited_user, event=invited_event)
                    invited_event.members.add(invited_user)
                #participant.event = event
                #participant.save()
                return redirect('event_detail', pk=invited_event.pk)
    else:
        form = ParticipantForm()
    return render(request, 'santa_raffle/event_detail.html', {'form': form})


def update_confirmation(request, pk, resp):
    if request.method == "POST":
        resp = bool(resp)
        event = get_object_or_404(Event, pk=pk)
        participant = get_object_or_404(Participant, owner=request.user, event=event)
        if resp:
            participant.confirmed = resp
            participant.save()
        else:
            participant.delete()
        return redirect('/')

