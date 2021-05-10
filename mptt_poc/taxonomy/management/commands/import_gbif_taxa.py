from django.core.management.base import BaseCommand
import logging

from taxonomy import models


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Load data in JSON format in the database'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        json_rows = open(filename).readlines()
        parent = models.Taxon.objects.get(taxon_key=3)
        models.Taxon.t_objects.update_with_gbif_json_rows(json_rows, parent)