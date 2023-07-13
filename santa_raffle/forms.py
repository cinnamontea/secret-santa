from django import forms
from .models import Event, Participant, CustomUser

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'event_date', )


class ParticipantForm(forms.Form):
    #print(CustomUser.objects.only('username'))
    owner = forms.ModelMultipleChoiceField(CustomUser.objects.only('id', 'username'))
    #owner = forms.TypedChoiceField(choices=CustomUser.objects.values(), label="")

    #class Meta:
    #    model = Participant
    #    fields = ('owner', )