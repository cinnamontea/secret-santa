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
    objects = CryptoKeyManager()
    value = models.UUIDField(default=uuid.uuid4, editable=False)
    order = models.PositiveSmallIntegerField(name="order", default=0)


class CustomUser(AbstractUser):
    likes = models.TextField(blank=True, null=True) #(for now, to make it simple)
 
    def __str__(self):
        return self.username
