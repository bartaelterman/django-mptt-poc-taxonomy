from django.core.management.base import BaseCommand
import logging

from taxonomy import models


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Drop the taxa in the database'

    def handle(self, *args, **options):
        models.Taxon.t_objects.delete_all()
