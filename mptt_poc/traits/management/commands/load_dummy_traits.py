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
        a1 = Attribute(
            aphia_id='1',
            attribute_name='body size',
            attribute_value='0.2 - 2.0 mm'
        )
        a1.save()

        a2 = Attribute(
            attribute_name='stage',
            attribute_value='larva',
            parent=a1
        )
        a2.save()

        a3 = Attribute(
            aphia_id='1',
            attribute_name='body size',
            attribute_value='2.0 - 200 mm'
        )
        a3.save()

        a4 = Attribute(
            attribute_name='stage',
            attribute_value='adult',
            parent=a3
        )
        a4.save()

        a5 = Attribute(
            aphia_id='1',
            attribute_name='calcification',
            attribute_value='calcified articulated'
        )
        a5.save()

        a6 = Attribute(
            attribute_name='stage',
            attribute_value='larva',
            parent=a5
        )
        a6.save()

        a7 = Attribute(
            aphia_id='1',
            attribute_name='calcification',
            attribute_value='calcified non-articulated'
        )
        a7.save()

        a8 = Attribute(
            attribute_name='stage',
            attribute_value='adult',
            parent=a7
        )
        a8.save()

        # aphia id = 2
        #    - body size = 2.0 - 200 mm & life stage = larva
        #    - body size = >200 mm & life stage = adult
        a9 = Attribute(
            aphia_id='2',
            attribute_name='body size',
            attribute_value='2.0 - 200 mm'
        )
        a9.save()

        a10 = Attribute(
            attribute_name='stage',
            attribute_value='larva',
            parent=a9
        )
        a10.save()

        a11 = Attribute(
            aphia_id='1',
            attribute_name='body size',
            attribute_value='>200 mm'
        )
        a11.save()

        a12 = Attribute(
            attribute_name='stage',
            attribute_value='adult',
            parent=a11
        )
        a12.save()
