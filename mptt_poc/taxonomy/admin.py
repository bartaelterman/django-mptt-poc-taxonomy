from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from taxonomy.models import Occurrence, Taxon


class TaxonAdmin(MPTTModelAdmin):
    search_fields = ['taxon_key']


admin.site.register(Occurrence)
admin.site.register(Taxon, TaxonAdmin)