import random

from django.db import transaction
from django.core.management.base import BaseCommand
from secure_mail.models import User, Message


class Command(BaseCommand):
    help = "Populates database with test users"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing previous data ..")
        User.objects.all().delete()
        Message.objects.all().delete()

        self.stdout.write("Generating users ..")
        User.objects.create_user(username='secure', password='mailer')
        User.objects.create_user(username='alice', password='redqueen')
        User.objects.create_user(username='bob', password='sponge')
        self.stdout.write("Done")

        self.stdout.write("Generating messages ..")
        Message.objects.create(sender='alice', receiver='bob',
                               content='Hello Bob! So glad our messages are safe.')
        Message.objects.create(sender='bob', receiver='alice',
                               content='Agreed, this must be the most secure messaging platform out there!')
        Message.objects.create(sender='secure', receiver='bob',
                               content='Would you like to recommend our service to your colleagues? :)')
        Message.objects.create(sender='bob', receiver='secure',
                               content='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua')
        self.stdout.write("Done")
        self.stdout.write(
            "App can now be run with 'python3 manage.py runserver'")


"""
    sender = models.OneToOneField(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

"""
