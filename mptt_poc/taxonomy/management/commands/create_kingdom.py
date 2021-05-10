from django.core.management.base import BaseCommand
import logging

from taxonomy import models


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Drop the taxa in the database'

    def handle(self, *args, **options):
        taxon = models.Taxon(taxon_key=3,
                             scientific_name='Bacteria',
                             accepted_taxon_key=3,
                             taxon_rank='KINGDOM')
        taxon.save()
