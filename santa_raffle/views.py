from django.shortcuts import render, get_object_or_404, redirect
from .forms import EventForm, EventMembersForm, EventMembersFormSet
from .models import Event, Participant, CustomUser, CryptoKey
from django.utils import timezone
from random import shuffle
from .crypto import aesctr, rsaoaep

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

    # IDEA: We could check if the authenticated user (if any) is a participant of the event.
    # This could be used to prevent access to the details of events of which the user is not a participant,
    # and to keep non-authenticated users from accessing the details of arbitrary events.
    user = request.user
    if not user.is_authenticated or len(event.participant_set.filter(owner=user)) == 0:
        # Take the user to a «This event doesn't exist or you are not a participant.» page.
        pass

    # EventMembersFormSet populates the list of invitable people:
    form = EventMembersFormSet(members.values_list('owner__id'))
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


def event_invites(request, pk):
    if request.method == "POST":
        invited_event = get_object_or_404(Event, pk=pk)

        # EventMembersForm receives the exact same fields as Set, but collects responses:
        form = EventMembersForm(request.POST)
        if form.is_valid():
            for user_id in form.data['members']:
                invited_user = get_object_or_404(CustomUser, pk=user_id)
                participant = None
                if not invited_event.members.contains(invited_user):
                    participant = Participant.objects.create(owner=invited_user, event=invited_event)
                    invited_event.members.add(invited_user)
                return redirect('event_detail', pk=invited_event.pk)
    else:
        form = EventMembersForm()
    return render(request, 'santa_raffle/event_detail.html', {'form': form})


def update_confirmation(request, pk, resp):
    # TO-DO: still needs to receive the user's key to add it to pkey_list!
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


def start_raffle(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        participants = event.participant_set.all()

        # Check that the user has permission:
        req1 = request.user == event.organizer
        # And that all users have accepted:
        req2 = True
        for participant in participants:
            req2 = req2 and participant.confirmed
        if req1 and req2:
            # DO RAFFLE

            # Fix the list of participants.
            ps = [p for p in event.participant_set.all()]
            n = len(ps)
            # Suffle it.
            shuffle(ps)

            for i, p in enumerate(ps):
                gifter = ps[(i-1)%n]  # p's secret santa is the participant that appears before in the list.
                giftee = ps[(i+1)%n]  # dual argument
                # Generate a random event key. It will be used to encrypt the event secrets of this participant.
                # The key itself will be encrypted with p's public RSA key, so that only they can recover the event key.
                ekey = aesctr.generateKey256()
                
                # Get p's public RSA key, use it to encrypt the event key, and save the result.
                p_pubk = rsaoaep.import_pk_string(p.owner.pubkey)
                p.event_key = rsaoaep.encrypt(ekey, p_pubk)

                # We will encrypt everything else with p's event key.
                p.giftee_id = aesctr.encrypt(giftee.owner.username, ekey)
                p.giftee_pka = aesctr.encrypt(giftee.owner.pubkey, ekey)
                p.gifter_pka = aesctr.encrypt(gifter.owner.pubkey, ekey)
                p.save()

            """ # -------TEMP CODE----------
            # for now, pkeys'll be generated randomly (to have something to sort)
            n_mems = len(participants)
            while len(event.pkey_list.all()) != n_mems:
                key_list = [CryptoKey.objects.create() for _ in range(n_mems)]
                [event.pkey_list.add(key) for key in key_list]
            
            # create shuffled list of indexes:
            order_list = [*range(n_mems)]
            shuffle(order_list)
            # set shuffled 'order' indexes:
            for i,k in enumerate(event.pkey_list.all()):
                k.order = order_list[i]
                k.save()
            # -------TEMP CODE---------- """
            event.raffle_date = timezone.now()
            event.save()
        return redirect('event_detail', pk=event.pk)
    else:
        return render(request, 'santa_raffle/event_detail.html')
