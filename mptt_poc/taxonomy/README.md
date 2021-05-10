# Loading data

There's code in here to load data both from WoRMS and from GBIF.
Check out the management commands `import_gbif_taxa`,
`import_occurrences` and `import_worms_taxa`.

# Models

- Occurrence
- Taxon
- AcceptedTaxon
- TaxonManager

# Views

`get_occurrences_by_taxon_query`, which renders
the `occurrences.html` template. Check out the
projects urls.py file to see where this view is
accessible.

Basically, this view allows you to search taxa and
occurrences.