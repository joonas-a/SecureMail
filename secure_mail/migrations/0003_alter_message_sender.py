# Generated by Django 4.2.5 on 2023-09-26 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secure_mail', '0002_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.CharField(max_length=50),
        ),
    ]