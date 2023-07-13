from django import forms
from .models import Event, Participant, CustomUser

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'event_date', )

class EventMembersForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('members', )


class ParticipantForm(forms.ModelForm):
    #print(CustomUser.objects.only('username'))
    #owner = forms.ModelMultipleChoiceField(CustomUser.objects.only('id', 'username'),
    #                                       required=True, label='')
    #owner = forms.TypedChoiceField(choices=CustomUser.objects.values(), label="")

    class Meta:
        model = Participant
        fields = ('owner', )
        #widgets = {'owner', forms.SelectMultiple()}
