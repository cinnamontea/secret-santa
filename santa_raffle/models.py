from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser, CryptoKey
import uuid


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # possibly better to use ints xD
    organizer = models.ForeignKey(CustomUser, related_name="organizer", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    raffle_date = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(CustomUser, related_name="members", blank=True,
                                     through="Participant",
                                     through_fields=("event", "owner"))
    #members = models.ManyToManyField(CustomUser, through="Participant", related_name="user_members", blank=True)#, on_delete=models.SET_NULL)
    pkey_list = models.ManyToManyField(CryptoKey, symmetrical=False)

    def __str__(self):
        return self.title
        
    def create_event(self):
        created_date = timezone.now()
        self.save()
    
    def get_members_id(self):
        return self.participant_set.values('owner__id', 'owner__username', 'confirmed')
    
    def save(self, *args, **kwargs):
        if self.organizer is not None and self.members is None: #not self.participant_set.filter(owner=self.organizer):
            # create a participant connected to the user and this event
            Participant.objects.update_or_create(owner=self.organizer, event=self, confirmed=True)
            #self.members.add(self.organizer)
            # add user as an event member
            #self.members = self.organizer
            # manytomany works as list but add doesn't work,
            # foreignkey doesn't work as list >:c 
        # save this item
        super(Event,self).save(*args, **kwargs)


class Participant(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    #gifter_pka = models.OneToOneField(CryptoKey, related_name="gifter_pka", null=True, on_delete=models.SET_NULL)
    #gifter_prk = models.OneToOneField(CryptoKey, related_name="gifter_prk", null=True, on_delete=models.SET_NULL)
    #gifter_srk = models.OneToOneField(CryptoKey, related_name="gifter_srk", null=True, on_delete=models.SET_NULL)
    #giftee_pka = models.OneToOneField(CryptoKey, related_name="giftee_pka", null=True, on_delete=models.SET_NULL)
    giftee_data = models.TextField(max_length=200, null=True, blank=True)
