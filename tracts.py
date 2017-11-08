import json
import csv
import re

from urllib.request import urlopen
from urllib.error import HTTPError
from constants import census_api_key

import geography_objects


def get_all_tracts():
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
            current_tract = geography_objects.tract(t[0], t[3])
            #current_tract = _get_adjacent_tracts(current_tract)
            all_tracts[t[3]] = current_tract
            
        # get the adjacencies
        with open("./tracts/md_adj_tracts.csv", "r") as tracts_csv:
            reader = csv.DictReader(tracts_csv)
            
            # this gets just the tract ids, not county ids or state codes
            # first two chars are 24 (=MD), then 3 chars for county code. then tract id
            tract_regex = re.compile("^24\d{3}(\d{6})$")
            for row in reader:
                row_match = tract_regex.match(row['SOURCE_TRACTID'])
                all_tracts[row_match.group(1)].add_adjacency(tract_regex.match(row['NEIGHBOR_TRACTID']).group(1))

        return [k for k in all_tracts.values()]
