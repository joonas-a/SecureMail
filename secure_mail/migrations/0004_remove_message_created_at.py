# Generated by Django 4.2.5 on 2023-09-26 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_mail', '0003_alter_message_sender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='created_at',
        ),
    ]
