# Generated by Django 4.1 on 2022-09-09 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessage',
            old_name='event_settings',
            new_name='message_text',
        ),
    ]
