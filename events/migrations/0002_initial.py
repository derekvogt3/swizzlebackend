# Generated by Django 4.1 on 2022-09-06 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firebase_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(through='events.Invitation', to=settings.AUTH_USER_MODEL),
        ),
    ]