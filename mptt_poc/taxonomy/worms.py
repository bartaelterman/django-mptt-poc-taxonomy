import csv
import pandas as pd
from .taxonomy import TAXON_RANKS


def read_csv(filename):
    taxon_csv = pd.read_csv(filename, quotechar='"', quoting=csv.QUOTE_ALL,
                            dtype={
                                'AphiaID': str,
                                'AphiaID_accepted': str,
                                'Class': str,
                                'Family': str,
                                'Genus': str,
                                'Kingdom': str,
                                'Order': str,
                                'Phylum': str,
                                'Species': str,
                                'Subgenus': str,
                                'Subspecies': str
                            })
    taxon_csv = taxon_csv.loc[taxon_csv['taxonRank'].isin(TAXON_RANKS.keys()), :]
    taxon_csv.dropna(subset=['AphiaID', 'AphiaID_accepted'], inplace=True)
    for col in ['Class', 'Family', 'Genus', 'Kingdom', 'Order', 'Phylum', 'Species', 'Subgenus', 'Subspecies']:
        taxon_csv[col].fillna('', inplace=True)
    return taxon_csv


def generate_node_ids(taxa_df):
    ids = taxa_df['Kingdom'].str.cat(
        taxa_df['Phylum'].str.cat(
            taxa_df['Class'].str.cat(
                taxa_df['Order'].str.cat(
                    taxa_df['Family'].str.cat(
                        taxa_df['Genus'].str.cat(
                            taxa_df['Subgenus'].str.cat(
                                taxa_df['Species'].str.cat(
                                    taxa_df['Subspecies'], sep=';'),
                                sep=';'),
                            sep=';'),
                        sep=';'),
                    sep=';'),
                sep=';'),
            sep=';'),
        sep=';'
    )
    taxa_df['node_id'] = ids


class TaxonomyTree:
    def __init__(self, index_attr='key'):
        self.index_value = 0
        self.tree = {'children': {}, 'object': {index_attr: 'root'}, '_id': self.index_value}
        self._index = {0: self.tree}
        self.keymap = {'root': 0}
        self.index_attr = index_attr

    def _get_child(self, subtree, child_key):
        if child_key in subtree['children']:
            node = subtree['children'][child_key]
            return node

    def _add_child(self, subtree, child_key, obj=None):
        self.index_value += 1
        node = {'children': {}, '_id': self.index_value, 'object': obj, 'parent_key': subtree['_id']}
        if obj:
            self._index[self.index_value] = node
            self.keymap[obj[self.index_attr]] = self.index_value
        subtree['children'][child_key] = node
        return node

    def _get_or_add_child(self, subtree, child_key, obj=None):
        if child_key in subtree['children']:
            node = self._get_child(subtree, child_key)
            if obj and not node['object']:
                node['object'] = obj
                self._index[node['_id']] = node
                self.keymap[obj[self.index_attr]] = node['_id']
        else:
            node = self._add_child(subtree, child_key, obj)
        return node

    def get_node_by_key(self, key):
        if key in self.keymap:
            return self._index[self.keymap[key]]

    def add_node(self, obj, name, ancestors):
        parent = self.tree
        for a_name in ancestors:
            parent = self._get_or_add_child(parent, a_name, None)
        self._get_or_add_child(parent, name, obj)


def taxa_to_tree(taxa_df):
    d = TaxonomyTree(index_attr='node_id')
    for i, row in taxa_df.iterrows():
        print(row)
        obj = row.to_dict()
        name = row[row['taxonRank']]
        ancestors = [
            row['Kingdom'],
            row['Phylum'],
            row['Class'],
            row['Order'],
            row['Family'],
            row['Genus'],
            row['Subgenus'],
            row['Species'],
            row['Subspecies']
            ]
        ancestors = [x for x in ancestors if x]
        ancestors = ancestors[0:-1]
        d.add_node(obj, name=name, ancestors=ancestors)
    return d


def get_parent_node_id(row):
    parent_node_id_list = []
    for rank, rank_value in TAXON_RANKS.items():
        if row['taxonRank'] < rank_value:
            parent_node_id_list.append(row[rank])
        else:
            parent_node_id_list.append('')
    return ';'.join(parent_node_id_list)
