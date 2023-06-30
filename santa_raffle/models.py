from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser, CryptoKey
import uuid

#BaseUser = CustomUser


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(CustomUser, related_name="organizer", on_delete=models.SET_DEFAULT, null=True),#default=models.SET_DEFAULT)#, default=User.get_default)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    raffle_date = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(CustomUser, related_name="members", 
                                     through="Participant",
                                     through_fields=("event", "owner"))#, symmetrical=False)
    pkey_list = models.ManyToManyField(CryptoKey, symmetrical=False)

    def __str__(self):
        return self.title
    
    @classmethod
    def get_default(cls):
        eventclass, created = cls.objects.get_or_create(
            id = uuid.uuid4,
            defaults = dict(organizer = models.SET_NULL,#SET_DEFAULT,
                          title='Deleted Event',
                          raffle_date = models.SET_NULL,
                          event_date = models.SET_NULL,
                          members = models.SET_DEFAULT,
                          pkey_list = models.SET_NULL),
        )
        return eventclass.pk
    
    def create_event(self):
        created_date = timezone.now()


class Participant(models.Model):
    owner = models.OneToOneField(CustomUser, related_name="owner", on_delete=models.CASCADE)
    event = models.OneToOneField(Event, related_name="event", on_delete=models.CASCADE)#, default=Event.get_default)
    gifter_pka = models.OneToOneField(CryptoKey, related_name="gifter_pka", null=True, on_delete=models.SET_NULL)
    gifter_prk = models.OneToOneField(CryptoKey, related_name="gifter_prk", null=True, on_delete=models.SET_NULL)
    gifter_srk = models.OneToOneField(CryptoKey, related_name="gifter_srk", null=True, on_delete=models.SET_NULL)
    giftee_pka = models.OneToOneField(CryptoKey, related_name="giftee_pka", null=True, on_delete=models.SET_NULL)
    giftee_id = models.OneToOneField(CustomUser, related_name="giftee", null=True, on_delete=models.SET_NULL)#, default=models.SET_DEFAULT)#, default=User.get_default)
