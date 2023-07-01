from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CryptoKeyManager(models.Manager):
    def _create_key(self, ktype, kstatus):
        new_key = self.create(key_type=ktype, key_status=kstatus) # implicit new_key.save()
        return new_key
    
    def create_pka(self):
        return self._create_key(ktype=1, kstatus=1)
    
    def create_ska(self):
        return self._create_key(ktype=2, kstatus=1)


class CryptoKey(models.Model):
    TypeChoices = models.IntegerChoices("TypeChoices", "PUBLIC PRIVATE")
    StatusChoices = models.IntegerChoices("StatusChoices", "ANON KNOWN")
    objects = CryptoKeyManager()
    
    key_type = models.CharField(choices=TypeChoices.choices, max_length=1, null=True)
    key_status = models.CharField(choices=StatusChoices.choices, max_length=1, null=True)
    value = models.UUIDField(default=uuid.uuid4, editable=False)


class CustomUser(AbstractUser):
    likes = models.TextField(blank=True, null=True) #(for now, to make it simple)
    pka = models.OneToOneField(CryptoKey, related_name="pka", on_delete=models.CASCADE, null=True, editable=False)
    ska = models.OneToOneField(CryptoKey, related_name="ska", on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Do custom logic here (key creation in this case)
        if self.pka is None and self.ska is None:
            self.pka = CryptoKey.objects.create_pka()
            self.ska = CryptoKey.objects.create_ska()
            # Run default save() method
            super(CustomUser,self).save(*args, **kwargs)