from django.core.management.base import BaseCommand
from traits.models import Attribute


class Command(BaseCommand):
    help = 'Load dummy traits in the database'

    def handle(self, *args, **options):
        # aphia id 1
        #    - body size = 0.2 - 2.0 mm & life stage = larva
        #    - body size = 2.0 - 200 mm & life stage = adult
        #    - calcification = calcified articulated & life stage = larva
        #    - calcification = calcified non-articulated & life stage = adult

        # aphia id = 2
        #    - body size = 2.0 - 200 mm & life stage = larva
        #    - body size = >200 mm & life stage = adult


        # TODO try to write a query that fetches aphia ids that have body size = 2.0 - 200 mm & life stage = adult
        Attribute.objects.filter(attribute_name='stage')
        # TODO this didn't entirely work:
        aphia_ids = [x.aphia_id for x in
         Attribute.objects.filter(attribute_name='stage', attribute_value='adult', parent__attribute_name='body size',
                                  parent__attribute_value='2.0 - 200 mm')]

