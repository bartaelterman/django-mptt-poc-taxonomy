from django.test import TestCase
from taxonomy.models import AcceptedTaxon, Taxon


class AggregationTest(TestCase):
    def setUp(self):
        taxon1 = Taxon.objects.create(scientific_name='A b', taxon_rank='Species', taxon_key='1', accepted_taxon_key='2')
        taxon2 = Taxon.objects.create(scientific_name='A c', taxon_rank='Species', taxon_key='2', accepted_taxon_key='2')
        taxon3 = Taxon.objects.create(scientific_name='B a', taxon_rank='Species', taxon_key='3', accepted_taxon_key='4')
        taxon4 = Taxon.objects.create(scientific_name='B b', taxon_rank='Species', taxon_key='4', accepted_taxon_key='4')
        taxon1.save()
        taxon2.save()
        taxon3.save()
        taxon4.save()

    def test_aggregate_by_taxon_key(self):
        result = Taxon.t_objects.names_by_taxon_key()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {'accepted_taxon_key': '2', 'names': ['A b', 'A c'], 'taxon_keys': ['1', '2']})
        self.assertEqual(result[1], {'accepted_taxon_key': '4', 'names': ['B a', 'B b'], 'taxon_keys': ['3', '4']})

    def test_index_taxa(self):
        self.assertEqual(len(AcceptedTaxon.objects.all()), 0)
        Taxon.t_objects.index_for_search()
        accepted_taxa = AcceptedTaxon.objects.all().order_by('taxon_key')
        self.assertEqual(len(accepted_taxa), 2)
        self.assertEqual(accepted_taxa[0].taxon_key, '2')
        self.assertEqual(len(accepted_taxa[0].synonyms), 2)
        self.assertListEqual(sorted(accepted_taxa[0].synonyms), sorted(['A b', 'A c']))
        self.assertEqual(len(accepted_taxa[0].synonym_taxon_keys), 2)
        self.assertListEqual(sorted(accepted_taxa[0].synonym_taxon_keys), sorted(['1', '2']))
        self.assertEqual(accepted_taxa[1].taxon_key, '4')
        self.assertEqual(len(accepted_taxa[1].synonyms), 2)
        self.assertListEqual(sorted(accepted_taxa[1].synonyms), sorted(['B a', 'B b']))
        self.assertEqual(len(accepted_taxa[1].synonym_taxon_keys), 2)
        self.assertListEqual(sorted(accepted_taxa[1].synonym_taxon_keys), sorted(['3', '4']))

        # Redo the process, still only 2 AcceptedTaxon objects in the db (the previous ones are removed)
        Taxon.t_objects.index_for_search()
        self.assertEqual(len(AcceptedTaxon.objects.all()), 2)

