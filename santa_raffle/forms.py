from django import forms
from .models import Event, Participant

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'event_date', )


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = ('owner', )