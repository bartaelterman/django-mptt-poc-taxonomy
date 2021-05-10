from django.core.management.base import BaseCommand
import csv
import logging
import tqdm

from taxonomy import models


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Load occurrences in csv format in the database'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        reader = csv.reader(open(filename), delimiter='\t')
        header = reader.__next__()
        for row in tqdm.tqdm(reader):
            decimalLatitude = float(row[21])
            decimalLongitude = float(row[22])
            taxonKey = row[33]
            models.Occurrence(taxonKey=taxonKey, x=decimalLongitude, y=decimalLatitude).save()
