'''

This file is used to test out various modules, functions, and methods
for the algorithm code

'''

import districts

# Test create district function, using the 1st item in the available tracts
# as the arbitrary starting point
def test_create_district():
	print("Creating new district...")
	newdist = districts._create_district(districts.available_tracts[0])
	print("Stats of the new district created:")
	print(newdist)

def main():
	#test_create_district()
	ls = districts._test_redistrict()
	print (ls)

main()
