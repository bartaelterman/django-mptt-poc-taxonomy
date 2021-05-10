from django.shortcuts import render
from taxonomy import models


def get_occurrences_by_taxon_query(request):
    q = request.GET.get('q', '')
    print(q)
    context = {
    }
    if q:
        occ, searched_taxa, taxa_w_desc = models.get_occurrence_by_taxon_name(q)
        context['occ'] = occ
        context['taxa'] = searched_taxa
        context['taxa_w_d'] = taxa_w_desc
    return render(request, 'occurrences.html', context)

