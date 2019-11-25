from threading import Thread
from django.db.models.signals import post_save
from .models import Task

from store.management.commands.get_books import run_crawler


def handler_run_scraper(sender, instance, **kwargs):
    if kwargs.get('created'):
        Thread(target=run_crawler, args=(instance, )).start()


post_save.connect(handler_run_scraper, sender=Task)
