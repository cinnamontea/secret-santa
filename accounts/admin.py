# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import CustomUser, CryptoKey
from santa_raffle.models import * #Event, Participant


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username","pubkey"]


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ["organizer", "title", "created_date", "raffle_date", "event_date", ]
    exclude = ("raffle_date", "created_date", "pkey_list",)


class ParticipantAdmin(admin.ModelAdmin):
    model = Participant
    list_display = ["owner", "event", "confirmed"]
    #exclude = ("gifter_pka", "gifter_prk", "gifter_srk", "giftee_pka", "giftee_id",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(CryptoKey)
admin.site.register(Message)