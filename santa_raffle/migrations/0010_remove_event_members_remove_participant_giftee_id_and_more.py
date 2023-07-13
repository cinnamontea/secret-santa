# Generated by Django 4.2.2 on 2023-07-12 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('santa_raffle', '0009_alter_participant_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='members',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='giftee_id',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='giftee_pka',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='gifter_pka',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='gifter_prk',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='gifter_srk',
        ),
        migrations.AddField(
            model_name='participant',
            name='giftee_data',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
