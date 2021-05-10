import unittest
from taxonomy import worms as w


class WormsModuleTestCase(unittest.TestCase):

    def test_create_tree(self):
        tree = w.TaxonomyTree()
        tree.add_node({'key': 'a', 'name': 'hi'}, name='TestKingdom', ancestors=[])
        tree.add_node({'key': 'b', 'name': 'there'}, name='TestPhylum1', ancestors=['TestKingdom'])
        tree.add_node({'key': 'c', 'name': 'two'}, name='TestPhylum2', ancestors=['TestKingdom'])
        self.assertEqual(tree.get_node_by_key('a')['object']['name'], 'hi')
        self.assertEqual(tree.get_node_by_key('b')['object']['name'], 'there')
        self.assertEqual(tree.get_node_by_key('c')['object']['name'], 'two')

    def test_dont_fail_if_ancestor_doesnt_exist_yet(self):
        tree = w.TaxonomyTree()
        tree.add_node({'key': 'b', 'name': 'there'}, name='TestPhylum1', ancestors=['TestKingdom'])
        tree.add_node({'key': 'a', 'name': 'hi'}, name='TestKingdom', ancestors=[])
        self.assertEqual(tree.get_node_by_key('a')['object']['name'], 'hi')
        self.assertEqual(tree.get_node_by_key('b')['object']['name'], 'there')
        self.assertEqual(len(tree.get_node_by_key('a')['children'].keys()), 1)
        self.assertEqual(tree.get_node_by_key('a')['children']['TestPhylum1']['object']['name'], 'there')
