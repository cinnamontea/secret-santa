from django.shortcuts import render, get_object_or_404, redirect
from .forms import EventForm, EventMembersForm, EventMembersFormSet
from .models import Event, Participant, Message, CustomUser
from django.http import JsonResponse
from django.utils import timezone
import json
from .crypto import aesctr, rsaoaep, strongrand

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
        # For now, redirect the user to the home page.
        return redirect('home_feed')
    
    # This access is safe because we already checked that the current user is a participant of the event.
    p = event.participant_set.get(owner=user)

    # EventMembersFormSet populates the list of invitable people:
    form = EventMembersFormSet(members.values_list('owner__id'))
    return render(request, 'santa_raffle/event_detail.html', 
                  {'event': event,
                   'members': members,
                   'form': form,
                   'participant': p,
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
        # Check that the event hasn't been raffled yet.
        req3 = not event.raffle_date
        if req1 and req2 and req3:
            # DO RAFFLE

            # Fix the list of participants.
            ps = [p for p in event.participant_set.all()]
            n = len(ps)
            # Shuffle it.
            sps = strongrand.shufflelist(ps)

            # Generate a random event key for each participant. It will be used to encrypt the event secrets of each participant.
            # We generate the list before because in each iteration we'll need the event key of our gifter in order to encrypt some info.
            # Check out the code below to get a better understanding of what's going on.
            # The keys themselves will be encrypted with the public RSA key of the corresponding participant, so that only they can recover the event key.
            ekeys = [aesctr.generateKey256() for _ in range(n)]

            for i, p in enumerate(sps):
                gifter = sps[(i-1)%n]  # p's secret santa is the participant that appears before in the list.
                giftee = sps[(i+1)%n]  # dual argument
                
                # Retrieve the event key of the current participant and their gifter.
                p_ek = ekeys[i]
                p_gifter_ek = ekeys[(i-1)%n]
                
                # Get p's public RSA key, use it to encrypt this participant's event key, and save the result.
                p_pubk = rsaoaep.import_pk_string(p.owner.pubkey)
                p.event_key = rsaoaep.encrypt(p_ek, p_pubk)

                # We will encrypt all the info that belongs to this participant with their event key.
                p.giftee_id = aesctr.encrypt(giftee.owner.username, p_ek)
                
                # For each pair gifter/giftee, assign a chat ID and generate a symmetric key to encrypt chat messages.
                # Since the participants have already been shuffled, we can assign chat IDs in order starting from 0. We'll use index i.
                # Chat IDs are only unique for an Event.
                
                chat_key = aesctr.generateKey256()
                p.gifter_chat_id = aesctr.encrypt(str(i), p_ek)
                p.gifter_chat_key = aesctr.encrypt(chat_key, p_ek)
                # Encrypt the info of p's gifter with their event key, otherwise they won't be able to retrieve this info.
                gifter.giftee_chat_id = aesctr.encrypt(str(i), p_gifter_ek)
                gifter.giftee_chat_key = aesctr.encrypt(chat_key, p_gifter_ek)
                gifter.save()

                # We only set the data for p's gifter. Because the next iteration will set p's giftee_chat_id and key.

                p.save()

            event.raffle_date = timezone.now()
            event.save()
        return redirect('event_detail', pk=event.pk)
    else:
        return render(request, 'santa_raffle/event_detail.html')
    

def get_messages(request, event_pk):
    if not request.user.is_authenticated:
        return JsonResponse({})
    
    if request.method == "GET":
        event = get_object_or_404(Event, pk=event_pk)
        msgs = event.message_set.all().order_by('timestamp')
        ser_msgs = []
        for msg in msgs:
            ser_msgs.append({
                'chat_id': msg.chat_id,
                'timestamp': msg.timestamp,
                'msg': msg.msg
            })
        return JsonResponse({'success': True, 'msgs': ser_msgs})
    else:
        return JsonResponse({})
    

def send_message(request):
    if not request.user.is_authenticated:
        return JsonResponse({})
    
    if request.method == "POST":
        body=json.loads(request.body)
        event_pk = body.get('event_pk')
        chat_id = body.get('chat_id')
        msg = body.get('msg')
        event = get_object_or_404(Event, pk=event_pk)
        m = Message(event=event, chat_id=chat_id, timestamp=timezone.now(), msg=msg)
        m.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({})
