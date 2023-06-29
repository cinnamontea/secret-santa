from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
#from santa_raffle.models import CryptoKey


class CryptoKey(models.Model):
    TypeChoices = models.IntegerChoices("TypeChoices", "PUBLIC PRIVATE")
    StatusChoices = models.IntegerChoices("StatusChoices", "ANON KNOWN")
    
    key_type = models.CharField(choices=TypeChoices.choices, max_length=1, null=True)
    key_status = models.CharField(choices=StatusChoices.choices, max_length=1, null=True)
    value = models.UUIDField(default=uuid.uuid4, editable=False)

    def generate_anon_key(ktype):
        return CryptoKey.objects.create(key_type=ktype, key_status=1) #PUBLIC=1, PRIVATE=2, ANON=1
    
    def generate_pka():
        return CryptoKey.generate_anon_key(1)
    
    def generate_ska():
        return CryptoKey.generate_anon_key(2)


class CustomUser(AbstractUser):
    likes = models.TextField(blank=True, null=True) #(for now, to make it simple)
    pka = models.OneToOneField(CryptoKey, related_name="pka", on_delete=models.CASCADE, editable=False, default=CryptoKey.generate_pka)
    ska = models.OneToOneField(CryptoKey, related_name="ska", on_delete=models.CASCADE, editable=False, default=CryptoKey.generate_ska)

    def __str__(self):
        return self.username