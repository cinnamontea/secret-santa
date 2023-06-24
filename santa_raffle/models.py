from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class CryptoKey(models.Model):
    class KeyType(models.IntegerChoices):
        PUBLIC = 0;     PRIVATE = 1
    
    class KeyStatus(models.IntegerChoices):
        ANON = 0;       KNOWN = 1
    
    type = models.BinaryField(choices=KeyType)
    status = models.BinaryField(choices=KeyStatus)
    value = models.PositiveBigIntegerField(unique=True)


class User(models.Model):
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.TextField(blank=True, null=True) #(for now, to make it simple)
    pka = models.OneToOneField(CryptoKey)
    ska = models.OneToOneField(CryptoKey)

    def __str__(self):
        return self.auth_user


class Event(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    raffle_date = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(User, symmetrical=False)
    pkey_list = models.ManyToManyField(User, symmetrical=False)

    def __str__(self):
        return self.title


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gifter_pka = models.OneToOneField(CryptoKey, null=True)
    gifter_prk = models.OneToOneField(CryptoKey, null=True)
    gifter_srk = models.OneToOneField(CryptoKey, null=True)
    giftee_pka = models.OneToOneField(CryptoKey, null=True)
    giftee_id = models.OneToOneField(User)