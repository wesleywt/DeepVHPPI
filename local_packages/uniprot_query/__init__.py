import urllib.parse

import requests
import logging
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
API = 'https://www.uniprot.org/uniprot/?query=reviewed:yes+AND+organism:9606&random=yes&limit=1,length&format=fasta'


class UniprotQueryClient:
    def __init__(self):
        self.base_url = 'https://www.uniprot.org/uniprot/'
        self.fasta = None
        self.map_list = None
        self.uniprotID_map = {}

    def make_request(self, method, endpoint, data, max_retries=10):
        if method == 'GET':
            counter = 0
            for _ in range(max_retries):
                if counter == 10:
                    print('Last retry...........')
                try:
                    response = requests.get(self.base_url + endpoint, params=data)
                    if response.status_code == 200:

                        return response.text
                    else:
                        logger.error(
                            f'Error while making {method} request to {endpoint}: error code"{response.status_code}')

                    if response.status_code == 300:
                        logger.error(
                            f'Redirect error {response.status_code}, get info at {response.headers["Location"]}')
                        response = requests.get('https://www.uniprot.org' + response.headers["Location"])
                        if response.status_code == 200:
                            logger.info(f'Redirect successful')
                            return response.text
                        else:
                            logger.error(
                                f'Error while making {method} request to {endpoint}: error code"{response.status_code}')
                            return None
                    break
                except Exception as e:
                    logger.error(f'Connection error with {method} when making request to {endpoint}: {e}')
                    time.sleep(5)

                    pass

        else:
            raise ValueError('No HTTP method was set, is it GET, POST OR DELETE?')
    def clear(self):
        self.fasta = None

    def make_random_query(self, organism_id: int, limit: int, reviewed='yes') -> str:

        endpoint = f'?query=reviewed:' + reviewed + '+AND+organism:' + str(organism_id) + '&random=yes&limit=' + str(
            limit) + ',length&format=fasta'

        self.fasta = self.make_request("GET", endpoint, dict())
        return self.fasta

    # def make_query(self, organism_id: int, uniprot_id: str, limit:int, reviewed='yes')->str:
    #     endpoint = f'?query=reviewed' + reviewed +

    def uniprot_download(self, uniprotID, format_type='fasta'):
        if '-' in uniprotID:

            query_endpoint = uniprotID.split('-')[0] + "." + format_type
        else:
            query_endpoint = uniprotID + "." + format_type

        if format_type == 'fasta':
            self.fasta = self.make_request('GET', query_endpoint, data=dict())
        return self.fasta

    def convert_to_uniprot(self, organismID, identifiers, convert_from='GENENAME', convert_to='ACC'):

        url = 'https://www.uniprot.org/uploadlists/'
        identifiers = ' '.join(identifiers)  # converts the list object to string for querying
        params = {
            'from': convert_from,
            'to': convert_to,
            'format': 'tab',
            'columns': 'id, entry_name,reviewed',
            'taxon': str(organismID),
            'query': identifiers
        }

        data = urlencode(params)
        data = data.encode('utf-8')
        req = Request(url, data)
        with urlopen(req) as f:
            response = f.read()

        map_list = response.decode('utf-8')
        self.map_list = map_list

        for item in map_list.split('\n'):
            if item.split('\t') != ['']:
                if item.split('\t')[1] == 'reviewed':
                    self.uniprotID_map.update({item.split('\t')[2]: item.split('\t')[0]})

        return self.uniprotID_map

    def get_fasta_seq_only(self):
        """Removes the description line from a fast file, leaving only the sequence"""
        if self.fasta is not None:
            fasta_split = self.fasta.splitlines()  # splits the fasta file into a list at the '\n' where the first item in the
            # list is the description line
            fasta_seq = ''.join(fasta_split[1:])  # joins the rest of the splitline list to construct the sequence
        else:
            fasta_seq = 'No sequence'

        return fasta_seq

    def get_fasta_uniprot_id(self):
        """Extracts the Uniprot ID descriptor from the description line of the fasta file"""
        if self.fasta is not None:
            uniprot_id = self.fasta.split('|')[1]  # the second item in the list will be the uniprot ID
        else:
            uniprot_id = 'No ID'
        return uniprot_id

    def get_fasta_description(self):
        """Use the split methods to splice out information"""
        if self.fasta is not None:

            description = self.fasta.split('|')[2].split("\n")[0]
        else:
            description = 'No description'
        return description


if __name__ == '__main__':
    uniprot_query = UniprotQueryClient()

    converted_to_uniprotID = uniprot_query.convert_to_uniprot(9606, 'CXCL8, VPS33B')
