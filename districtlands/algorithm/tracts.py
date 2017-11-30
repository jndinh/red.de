'''

this file includes methods to fetch census tracts and deal with them

currently, there is just one method: get_all_tracts(), which fetches
all the census tracts, adds their adjacencies, and returns them as a dictionary

CHANGELOG
Dorothy Carter - 20171107 - initial creation of script
Dorothy Carter - 20171110 - cast population to int

'''

import json
import csv
import re
import os

from urllib.request import urlopen
from urllib.error import HTTPError
from .constants import census_api_key
from . import geography_objects

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

def get_all_tracts():
    '''
    this method grabs all MD census tracts and populates their adjacency lists
    returns: a dictionary of all tracts where the keys are the tract ids and
             the values are the tract objects
    '''
    
    # this gets the population 18 years & older (P010000) for all census tracts in MD    
    url = "https://api.census.gov/data/2010/sf1?get=P0100001&for=tract:*&in=state:24&key=" + census_api_key

    response = urlopen(url)
    if response.getcode() != 200:
        raise HTTPError("HTTP status code is not 200: " + str(response.getcode()))
    else:
        all_tracts = {}
        data = json.load(response)
        for t in data[1:]: # the first object is titles of variables
            # population is [0], tract_id is [3]
            current_tract = geography_objects.tract(int(t[0]), t[3])
            #current_tract = _get_adjacent_tracts(current_tract)
            all_tracts[t[3]] = current_tract
            
        # get the adjacencies
        with open(BASE_DIR + "\\algorithm\\tracts_folder\\md_adj_tracts.csv", "r") as tracts_csv:
            reader = csv.DictReader(tracts_csv)
            
            # this gets just the tract ids, not county ids or state codes
            # first two chars are 24 (=MD), then 3 chars for county code. then tract id
            tract_regex = re.compile("^24\d{3}(\d{6})$")
            for row in reader:
                row_match = tract_regex.match(row['SOURCE_TRACTID'])
                all_tracts[row_match.group(1)].add_adjacency(tract_regex.match(row['NEIGHBOR_TRACTID']).group(1))

        return all_tracts
