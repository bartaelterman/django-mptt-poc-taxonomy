import fire
import json
import logging
import requests


BACKBONE_DATASET_KEY = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'
URL = 'https://www.gbif.org/api/species/search?advanced=false&dataset_key={dataset_key}' \
    '&highertaxon_key={species_key}&status=ACCEPTED&status=DOUBTFUL' \
    '&offset={offset}&limit={limit}'


def get_children(species_key):
    offset = 0
    limit = 100
    end_of_records = False
    while not end_of_records:
        logging.warning(f'sending request with offset {offset}')
        r = requests.get(URL.format(dataset_key=BACKBONE_DATASET_KEY, species_key=species_key,
                                    offset=offset,limit=limit))
        logging.warning(f'  status code: {r.status_code}')
        data = r.json()
        logging.warning(f'  {data["count"]} results')
        for taxon in data['results']:
            yield taxon
        if data['endOfRecords']:
            end_of_records = True
        else:
            offset += limit


def download_data(outfile_name, species_key=3):
    with open(outfile_name, 'w+') as out:

        for child in get_children(species_key):
            out.write(json.dumps(child) + '\n')



if __name__ == '__main__':
    fire.Fire(download_data)