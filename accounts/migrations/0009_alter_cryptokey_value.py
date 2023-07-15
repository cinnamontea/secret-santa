# Generated by Django 4.2.2 on 2023-07-14 02:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_cryptokey_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptokey',
            name='value',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]