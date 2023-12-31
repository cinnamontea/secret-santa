# Generated by Django 4.2.2 on 2023-07-13 20:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('santa_raffle', '0011_participant_confirmed_alter_participant_giftee_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='user_members', through='santa_raffle.Participant', to=settings.AUTH_USER_MODEL),
        ),
    ]
