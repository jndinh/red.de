'''
this module includes little tests for various modules
this is not to substitute for more formal tests later
'''

import districts
from districts import all_tracts

def test_single_district():
    final = districts._create_district(all_tracts["751200"])
    print(final)
    
def test_total_redistricting():
    redistrict = districts.generic_redistrict()
    print(redistrict)
    

if __name__ == "__main__":
    test_total_redistricting()
