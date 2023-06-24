from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class CryptoKey(models.Model):
    key_type = models.IntegerChoices("KeyType", "PUBLIC PRIVATE")
    key_status = models.IntegerChoices("KeyStatus", "ANON KNOWN")
    value = models.BinaryField(unique=True)


class User(models.Model):
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.TextField(blank=True, null=True) #(for now, to make it simple)
    pka = models.OneToOneField(CryptoKey, related_name="pka", on_delete=models.CASCADE)
    ska = models.OneToOneField(CryptoKey, related_name="ska", on_delete=models.CASCADE)

    def __str__(self):
        return self.auth_user
    
    @classmethod
    def get_default(cls):
        userclass, created = cls.objects.get_or_create(
            auth_user = settings.AUTH_USER_MODEL, 
            defaults = dict(likes='No likes provided',
                          pka = models.SET_NULL,
                          ska = models.SET_NULL),
        )
        return userclass.pk


class Event(models.Model):
    author = models.ForeignKey(User, related_name="author", on_delete=models.SET_DEFAULT, default=User.get_default)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    raffle_date = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="members", symmetrical=False)
    pkey_list = models.ManyToManyField(User, symmetrical=False)

    def __str__(self):
        return self.title


class Participant(models.Model):
    user = models.OneToOneField(User, related_name="owner", on_delete=models.CASCADE)
    gifter_pka = models.OneToOneField(CryptoKey, related_name="gifter_pka", null=True, on_delete=models.SET_NULL)
    gifter_prk = models.OneToOneField(CryptoKey, related_name="gifter_prk", null=True, on_delete=models.SET_NULL)
    gifter_srk = models.OneToOneField(CryptoKey, related_name="gifter_srk", null=True, on_delete=models.SET_NULL)
    giftee_pka = models.OneToOneField(CryptoKey, related_name="giftee_pka", null=True, on_delete=models.SET_NULL)
    giftee_id = models.OneToOneField(User, related_name="giftee", on_delete=models.SET_DEFAULT, default=User.get_default)
