from mptt.models import MPTTModel, TreeManager, TreeForeignKey
from django.db import models


class Attribute(MPTTModel):
    aphia_id = models.CharField(max_length=100)
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['aphia_id']

    def __str__(self):
        return f'{self.aphia_id} {self.attribute_name}'