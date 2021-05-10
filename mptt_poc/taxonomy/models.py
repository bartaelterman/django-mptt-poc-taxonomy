import json
import logging
import tqdm

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.aggregates import ArrayAgg
from mptt.models import MPTTModel, TreeForeignKey
from taxonomy.taxonomy import sort_by_rank


class Occurrence(models.Model):
    taxonKey = models.CharField(max_length=100, blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.x}:{self.y} ({self.taxonKey})'


class AcceptedTaxon(models.Model):
    """
    After loading all Taxa, you can "index" the taxa to "optimize search" (see
    the index_taxa management command).
    This will created AcceptedTaxon objects. Every such object is an accepted
    taxon according to WoRMS. Other taxa (hence, that are not accepted) are
    considered synonyms. Their names are added to the accepted taxon in the
    synonyms array.
    """
    scientific_name = models.CharField(max_length=250, unique=True)
    taxon_rank = models.CharField(max_length=100)
    taxon_key = models.CharField(max_length=100, unique=True)
    synonym_taxon_keys = ArrayField(models.CharField(max_length=150), blank=True, null=True)
    synonyms = ArrayField(models.CharField(max_length=150), blank=True, null=True)


class TaxonManager(models.Manager):
    @staticmethod
    def log_changed_fields(taxon, taxon_fields_changed):
        field_logs = [f'{k}: {v["old"]} -> {v["new"]}' for k, v in taxon_fields_changed.items()]
        logging.info(f'Taxon id {taxon.pk}, taxon_key {taxon.taxon_key}.\tUpdated fields: {", ".join(field_logs)}')

    def names_by_taxon_key(self):
        return self.values('accepted_taxon_key').annotate(names=ArrayAgg('scientific_name', distinct=True),
                                                          taxon_keys=ArrayAgg('taxon_key', distinct=True)).all()

    def index_for_search(self):
        """
        Created AcceptedTaxon objects which can function as an index
        for the search.
        """
        logging.info('Deleting all AcceptedTaxon objects')
        AcceptedTaxon.objects.all().delete()
        nr_objects_created = 0
        names_by_taxon_key = self.names_by_taxon_key()
        for names_obj in names_by_taxon_key:
            accepted_taxon = self.get(taxon_key=names_obj['accepted_taxon_key'])
            AcceptedTaxon(scientific_name=accepted_taxon.scientific_name,
                          taxon_rank=accepted_taxon.taxon_rank,
                          taxon_key=accepted_taxon.taxon_key,
                          synonyms=names_obj['names'],
                          synonym_taxon_keys=names_obj['taxon_keys']
                          ).save()
            nr_objects_created += 1
        logging.info(f'{nr_objects_created} AcceptedTaxon objects created')

    def delete_all(self):
        all = self.all()
        logging.warning(f'deleting {len(all)} existing taxa.')
        all.delete()

    def write_obj_to_json_lines(self, objects, filename):
        with open(filename, 'w+') as out:
            for line in objects:
                out.write(json.dumps(line) + '\n')

    def update_with_gbif_json_rows(self, json_rows, parent):
        children = parent.children.all()
        logging.warning(f'Delete {len(children)} children of parent {parent}')
        children.delete()
        taxa_to_process = [json.loads(x) for x in json_rows]
        # Sort by taxon rank first. To make sure parents exist when loading new taxa
        taxa_to_process = sort_by_rank(taxa_to_process)

        unaccepted = []
        failed = []
        success = []
        index = {parent.taxon_key: parent}
        print(index)

        for row in tqdm.tqdm(taxa_to_process):
            if row['taxonomicStatus'] != 'ACCEPTED':
                unaccepted.append(row)
                continue
            if str(row['parentKey']) not in index:
                row['failedReason'] = 'parent not found'
                failed.append(row)
                continue

            parent = index[str(row['parentKey'])]
            try:
                taxon = Taxon(
                    taxon_key=row['key'],
                    scientific_name=row['scientificName'],
                    accepted_taxon_key=row['key'],
                    taxon_rank=row['rank'],
                    parent=parent
                )

                taxon.save()
                index[str(row['key'])] = taxon
                success.append(row)
            except Exception as e:
                # Create a parent if needed. It will be updated when we encounter that taxon in the input
                # Parent does not exist yet. We'll have to try this taxon again later
                row['failedReason'] = str(e)
                failed.append(row)
        logging.info(f'Successfully created {len(success)} taxa.')
        self.write_obj_to_json_lines(unaccepted, 'unaccepted.json')
        logging.info(f'Skipped {len(unaccepted)} unaccepted taxa. Check unaccepted.json')
        self.write_obj_to_json_lines(failed, 'failed.json')
        logging.info(f'Skipped {len(failed)} failed taxa. Check failed.json')

    def update_with_worms_csv_rows(self, csv_rows):
        """
        Update the taxa in the database with a list of
        rows coming from a csv.
        If a taxon does not exist, it will be created. If
        it already exists, it will be updated.
        Since taxon_key and accepted_taxon_key are required
        in our database, taxa without one of those will be
        skipped.
        :return:
        """
        for row in csv_rows:
            try:
                taxon = self.get(taxon_key=row.taxonKey)
                taxon_fields_changed = {}
                if taxon.scientific_name != row.ScientificName:
                    taxon_fields_changed['scientific_name'] = {'new': row.ScientificName, 'old': taxon.scientific_name}
                    taxon.scientific_name = row.ScientificName
                if taxon.taxon_rank != row.taxonRank:
                    taxon_fields_changed['taxon_rank'] = {'new': row.taxonRank, 'old': taxon.taxon_rank}
                    taxon.taxon_rank = row.taxonRank
                if taxon.accepted_taxon_key != row.acceptedTaxonKey:
                    taxon_fields_changed['accepted_taxon_key'] = {'new': row.acceptedTaxonKey,
                                                                 'old': taxon.accepted_taxon_key}
                    taxon.accepted_taxon_key = row.acceptedTaxonKey
                if len(taxon_fields_changed) > 0:
                    taxon.save()
                    self.log_changed_fields(taxon, taxon_fields_changed)
            except Taxon.DoesNotExist:
                taxon = Taxon(
                    taxon_key=row.taxonKey,
                    scientific_name=row.ScientificName,
                    accepted_taxon_key=row.acceptedTaxonKey,
                    taxon_rank=row.taxonRank
                )
                taxon.save()
                logging.info(f'Taxon id {taxon.pk}, taxonKey {taxon.taxon_key} added.')


class Taxon(MPTTModel):
    scientific_name = models.CharField(max_length=250)
    taxon_rank = models.CharField(max_length=100)
    taxon_key = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    accepted_taxon_key = models.CharField(max_length=100)
    t_objects = TaxonManager()

    class MPTTMeta:
        order_insertion_by = ['scientific_name']

    def __str__(self):
        return f'{self.scientific_name} ({self.taxon_rank})'


def flatten_and_unique_list_of_lists(l):
    out = set()
    for sublist in l:
        for item in sublist:
            out.add(item)
    return list(out)


def get_occurrence_by_taxon_name(q):
    searched_taxa = Taxon.objects.filter(scientific_name__icontains=q)
    taxa_with_descendants_list = [x.get_descendants(include_self=True) for x in searched_taxa]
    taxa_with_descendants = flatten_and_unique_list_of_lists(taxa_with_descendants_list)
    taxon_keys = [x.taxon_key for x in taxa_with_descendants]
    print(taxon_keys)
    return list(Occurrence.objects.filter(taxonKey__in=taxon_keys)), searched_taxa, taxa_with_descendants