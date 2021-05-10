
TAXON_RANKS = {
    'kingdom': 0,
    'phylum': 1,
    'class': 2,
    'order': 3,
    'family': 4,
    'genus': 5,
    'subgenus': 6,
    'species': 7,
    'subspecies': 8,
    'variety': 9,
    'form': 10,
    'unranked': 11
}


def sort_by_rank(taxon_lines):
    return sorted(taxon_lines, key=lambda x: TAXON_RANKS[x['rank'].lower()])