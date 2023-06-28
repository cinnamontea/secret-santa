from django.conf import settings
from django.db import models
from django.utils import timezone
#from django.contrib.auth import get_user_model
from accounts.models import *
import uuid

BaseUser = CustomUser

'''
class User(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    likes = models.TextField(blank=True, null=True) #(for now, to make it simple)
    pka = models.OneToOneField(CryptoKey, related_name="pka", on_delete=models.CASCADE)
    ska = models.OneToOneField(CryptoKey, related_name="ska", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.base_user)
    
    @classmethod
    def get_default(cls):
        userclass, created = cls.objects.get_or_create(
            base_user = settings.AUTH_USER_MODEL, 
            defaults = dict(likes='No likes provided',
                            pka = models.SET_NULL,
                            ska = models.SET_NULL),
        )
        return userclass.pk
'''


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(BaseUser, related_name="organizer", on_delete=models.SET_DEFAULT, null=True),#default=models.SET_DEFAULT)#, default=User.get_default)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    raffle_date = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(BaseUser, related_name="members", 
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
    owner = models.OneToOneField(BaseUser, related_name="owner", on_delete=models.CASCADE)
    event = models.OneToOneField(Event, related_name="event", on_delete=models.CASCADE)#, default=Event.get_default)
    gifter_pka = models.OneToOneField(CryptoKey, related_name="gifter_pka", null=True, on_delete=models.SET_NULL)
    gifter_prk = models.OneToOneField(CryptoKey, related_name="gifter_prk", null=True, on_delete=models.SET_NULL)
    gifter_srk = models.OneToOneField(CryptoKey, related_name="gifter_srk", null=True, on_delete=models.SET_NULL)
    giftee_pka = models.OneToOneField(CryptoKey, related_name="giftee_pka", null=True, on_delete=models.SET_NULL)
    giftee_id = models.OneToOneField(BaseUser, related_name="giftee", null=True, on_delete=models.SET_NULL)#, default=models.SET_DEFAULT)#, default=User.get_default)
