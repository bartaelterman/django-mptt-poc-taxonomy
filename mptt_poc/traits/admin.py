from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from traits.models import Attribute

class AttributeAdmin(MPTTModelAdmin):
    search_fields = ['aphia_id', 'attribute_name']


admin.site.register(Attribute, AttributeAdmin)