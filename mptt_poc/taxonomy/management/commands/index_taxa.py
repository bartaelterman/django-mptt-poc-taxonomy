from django.core.management.base import BaseCommand
import logging

from taxonomy import models


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Index the taxa to optimize taxon-based search'

    def handle(self, *args, **options):
        models.Taxon.t_objects.index_for_search()
