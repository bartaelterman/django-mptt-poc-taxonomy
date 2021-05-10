from django.core.management.base import BaseCommand
import csv
import logging
import pandas as pd

from taxonomy import models


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Load data in csv format in the database'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        taxon_csv = pd.read_csv(filename, quotechar='"', quoting=csv.QUOTE_ALL,
                                dtype={
                                    'AphiaID': str,
                                    'AphiaID_accepted': str})
        taxon_csv.dropna(subset=['AphiaID', 'AphiaID_accepted'], inplace=True)
        taxon_csv.rename(columns={'AphiaID': 'taxonKey', 'AphiaID_accepted': 'acceptedTaxonKey'}, inplace=True)
        taxon_csv.fillna('', inplace=True)
        models.Taxon.t_objects.update_with_worms_csv_rows(taxon_csv.itertuples())