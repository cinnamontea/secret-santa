# Generated by Django 4.2.2 on 2023-06-30 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_pka_customuser_ska'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pka',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pka', to='accounts.cryptokey'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='ska',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ska', to='accounts.cryptokey'),
        ),
    ]
