import unittest

from taxonomy.taxonomy import sort_by_rank


class TaxonomyModuleTestCase(unittest.TestCase):
    def test_sort_by_rank(self):
        lines = [
            {'rank': 'phylum', 'nr': 2},
            {'rank': 'species', 'nr': 6},
            {'rank': 'genus', 'nr': 5},
            {'rank': 'CLASS', 'nr': 3},
            {'rank': 'kingdom', 'nr': 1},
            {'rank': 'order', 'nr': 4}
        ]

        sorted_lines = sort_by_rank(lines)
        self.assertListEqual([x['nr'] for x in sorted_lines], [1, 2, 3, 4, 5, 6])
