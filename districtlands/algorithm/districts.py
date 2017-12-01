'''

this module creates a district out of tracts. it contains two main methods:
generic_redistrict - re-district Maryland using a default start
specific_redistrict - given a starting tract, re-district Maryland

and five 'helper' methods:
_take_tract - remove a tract from available_tracts, and return false if that fails
_density - returns the proportion of available adjacent tracts to total adjacent tracts
_create_district - given a starting tract, create a congressional district
_sanitize_districts - changes a district object to json
_test_redistrict - redistricts part of MD using two districts

ISSUES
fragments - after creating most districts, only a few remain. they are
            unsuitable for another district, being possibly non-adjacent
            and/or not having enough population to make another one

run out of tracts - if there are no unused tracts in the adjacency queue,
                    an error will be thrown. shouldn't be hard to fix.

validity - check the resulting districts for population parity. if not
           within a certain margin of error, discard this districting

infinite loop - if no adjacent tracts are available, create_district
                will loop forever

number of districts - Maryland is only assigned 8 congressional districts,
                      but this (as currently implemented) may create more
                      or fewer. should be easy to fix (maybe)

density method - should maybe go in the tract class

sanitize_districts method - should maybe go in the district class


CHANGE LOG
Dorothy Carter - 20171109 - initial creation  
Dorothy Carter - 20171127 - initial work on expanding method
Dorothy Carter - 20171127 - initial work on full redistricting
Dorothy Carter - 20171128 - _density method
                            test redistrict methods  
Dorothy Carter - 20171130 - fixing some bugs     

'''
from . import tracts
from . import geography_objects

import random

# average number of people in an MD congressional district
MAGIC_POPULATION_NUMBER = 723741

# every census tract in md
all_tracts = tracts.get_all_tracts()
available_tracts = [k for k in all_tracts.values()]

def _take_tract(tractid):
    '''
    tries to remove a tract denoted by tractid. returns True
    if success, False if failure
    
    arguments: tractid - a string representing the tract id
                        (or tract object - it will work the same)
    returns: bool denoting successful removal of tract (True)
             or failure (False)
    '''
    try:
        available_tracts.remove(tractid)
        return True
    except ValueError:
        return False
        

def _density(this_tract):
    '''
    this measures how many of the tract's adjacent tracts are
    available to take. this is computationally expensive, but
    does it matter?
    
    argument: this_tract - a tract object
    returns: a float representing the proportion of available
             tracts to total adjacent tracts
    '''
    #total_adjacent = 0
    available_adjacent = 0
    
    # adjacent tracts...
    friends = this_tract.adjacent_to
    
    # ... and tracts adjacent to those
    # avoid duplicates using a set and an if statement
    friends_of_friends = {ff for tract in friends for ff in all_tracts[tract].adjacent_to if ff not in friends}
    
    total_adjacent = len(this_tract.adjacent_to) + len(friends_of_friends)
    
    # find those adjacent
    first_ring_available = [t for t in this_tract.adjacent_to if t in available_tracts]
    second_ring_available = [t for t in friends_of_friends if t in available_tracts]
    available_adjacent = len(first_ring_available) + len(second_ring_available)
    
    return available_adjacent / (total_adjacent * 1.0)


def _create_district(start):
    '''
    this creates one congressional district given a starting tract
    
    it queues all adjacent tracts for the start, then from the first, etc
    and grabs them sequentially until the district is made. It takes the next
    
    
    arguments: start - a tract object from which districting starts
    returns: a tuple consisting of: a district object representing the finished district
                                    the next tract in the queue
    '''
    
    # tries to add the passed-in starting tract to the district
    # will raise an exception if the district is already taken
    created_district = geography_objects.district()
    if _take_tract(start.id):
        created_district.add_tract(start)
    else:
        raise geography_objects.district_error("starting tract is already taken")
    
    # queue up all adjacent tracts to the start
    queue = list()
    queue.extend(start.adjacent_to)
    
    # this loop keeps trying to add tracts until the district hits
    # its population target. see ISSUES above for the potential 
    # infinite loop issue
    while created_district.population <= MAGIC_POPULATION_NUMBER:
        next = all_tracts[queue.pop()] # dequeue the first tract
        #print("in queue: {} ; next score: {}".format(len(queue)+1, _density(next)))
        if _take_tract(next.id):
            # Debug Statement:
            # print(next.id + " success!")
            created_district.add_tract(next)
            
            # queue all tracts adjacent
            # since queue is a set, no dupes
            queue.extend(next.adjacent_to)
    
    
    # this picks a random adjacent tract
    # see issues above for running out of tracts issue
    next = None
    
    # keep best
    max_tract = None
    max_density = 0.0
    
    # .875 adjacent is _goodenough_
    while queue and max_density < .875:
        next = all_tracts[queue.pop()]
        next_density = _density(next)
        if next in available_tracts and next_density > max_density:
            max_density = next_density
            max_tract = next
    
    return (created_district, max_tract)


def _sanitize_districts(district_list):
    '''
    changes a list of district objects into json
    
    arguments: district_list - a list of districts
    returns: a JSON blorb string
    '''
    ls = []
    for district in district_list:
        dist_dict = dict()
        dist_dict["population"] = district.population
        dist_dict["tracts"] = [t.id for t in district.tracts]
        
        ls.append(dist_dict)
    
    return ls
    

def _test_redistrict():
    '''
    only for test purposes. partially re-districts
    Maryland into two normal districts ~700_000 in population
    
    returns: a JSON blorb string
    '''
    districts = []
    next = all_tracts["751200"]
    for _ in range(2):
        new_district, next = _create_district(next)
        districts.append(new_district)
    
    return _sanitize_districts(districts)
    

def generic_redistrict():
    '''
    this redistricts Maryland using a default start tract
    returns: a list of 8 district objects
    '''
    start = all_tracts["751200"]
    return specific_redistrict(start)

def specific_redistrict(start):
    '''
    this redistricts Maryland using a given start tract
    arguments: start - a tract object that districting will start from
    returns: a list of district objects (8 district objects)
    '''
    districts = []
    next = start
    for i in range(8):
        print("loop index: {} len available: {}".format(i, len(available_tracts)))
        new_district, next = _create_district(next)
        districts.append(new_district)
    
    
    # reset the 'global' variables
    all_tracts = tracts.get_all_tracts()
    available_tracts = [k for k in all_tracts.values()]
   
    print("{} tracts remaining after redistricting".format(len(available_tracts)))
    return districts

