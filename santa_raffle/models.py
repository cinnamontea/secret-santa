from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser, CryptoKey
import uuid


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(CustomUser, related_name="organizer", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    raffle_date = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(CustomUser, related_name="members", 
                                     through="Participant",
                                     through_fields=("event", "owner"))
    pkey_list = models.ManyToManyField(CryptoKey, symmetrical=False)

    def __str__(self):
        return self.title
        
    def create_event(self):
        created_date = timezone.now()
        self.save()
    
    def save(self, *args, **kwargs):
        if self.organizer is not None:
            # save this item
            super(Event,self).save(*args, **kwargs)
            # and create a participant connected to the user and this event
            Participant.objects.create(owner=self.organizer, event=self)
            # finally, add user as an event member
            self.members.add(self.organizer)


class Participant(models.Model):
    owner = models.ForeignKey(CustomUser, related_name="owner", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="event", on_delete=models.CASCADE)
    gifter_pka = models.OneToOneField(CryptoKey, related_name="gifter_pka", null=True, on_delete=models.SET_NULL)
    gifter_prk = models.OneToOneField(CryptoKey, related_name="gifter_prk", null=True, on_delete=models.SET_NULL)
    gifter_srk = models.OneToOneField(CryptoKey, related_name="gifter_srk", null=True, on_delete=models.SET_NULL)
    giftee_pka = models.OneToOneField(CryptoKey, related_name="giftee_pka", null=True, on_delete=models.SET_NULL)
    giftee_id = models.OneToOneField(CustomUser, related_name="giftee", null=True, on_delete=models.SET_NULL)