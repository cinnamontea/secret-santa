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


class EventMembersFormSet(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('members', )
    
    def __init__(self, confirmed_mems, *args, **kwargs):
        super(EventMembersFormSet, self).__init__(*args, **kwargs)
        qs = CustomUser.objects.exclude(id__in=confirmed_mems)
        self.fields['members'].queryset = qs
        self.fields['members'].label = ""

