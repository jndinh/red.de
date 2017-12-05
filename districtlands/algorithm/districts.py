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
Stephen Lin - 20171201 - added stealing methods
Stephen Lin - 20171204 - added stealing based on potential
Stephen Lin - 20171204 - added final sweep evening and cleanup of tracts
                         corrected magic population number

'''
from . import tracts
from . import geography_objects

import random

# average number of people in an MD congressional district
MAGIC_POPULATION_NUMBER = 552573
MAGIC_POPULATION_NUMBER_95PERCENT = 524944

# every census tract in md
# Dictionary of all tracts. Key: tract ID, Value: tract object
all_tracts = tracts.get_all_tracts()
# List of all untaken tracts
available_tracts = [k for k in all_tracts.values()]

# all districts objects made thus far, dictionary form
# keys are district ids and values are district objects
all_districts = {}

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


def get_adjacent_district_ids(reference_district):
    '''
    returns a list of district ids that this district is currently adjacent to

    arguments: reference_district takes in a district object to work with
    '''
    # For every tract in the district, get adjacenies,
    # and for every adjaceny, see if it belongs to another district
    adjacent_districts = list()
    for tract in reference_district.tracts:
        for adjtract in tract.adjacent_to:
            owner_id = all_tracts[adjtract].get_ownership()
            # If tract belongs to another district and we haven't already seen it, mark it down
            if (owner_id != "") and (owner_id != reference_district.district_id) and (owner_id not in adjacent_districts):
                adjacent_districts.append(owner_id)
    return adjacent_districts


def get_my_adjacent_tracts(origin_district, target_district_id):
    '''
    this steals tracts from the victim district to the stealing district

    arguments: origin_district, a district object
    target_district_id, the id of the district we are trying to find
    tracts in the origin district that "touch" it (are adjacent to)

    returns list of tract objects that touch the target district
    '''
    # For every tract in the district, note down the owns who
    # have an adjacent tract that belongs to the target
    # So basically, tracts that are touching the target district
    adjacent_tracts = list()
    for tract in origin_district.tracts:
        for adjtract in tract.adjacent_to:
            owner_id = all_tracts[adjtract].get_ownership()
            if (owner_id == target_district_id):
                adjacent_tracts.append(tract)
                # Confirmed to be touching, no need loop more
                # Saves computation and avoids duplicates in the list
                break
    return adjacent_tracts


def steal_tracts(stealing_district, victim_district):
    '''
    this steals tracts from the victim district to the stealing district

    arguments: stealing_district, a district object
    victim_district, a district object, of which is being stolen from
    '''
    # First, get the tracts in the stealing district that are adjacent to
    # the victim district, so we know where to start stealing from
    my_adjacent_tracts = get_my_adjacent_tracts(stealing_district, victim_district.district_id)

    # Now, using this list as are "queue" of tracts to add,
    # start expanding again with an add tract loop
    # But, all we are doing is stealing the tracts that belong
    # to the victim district
    # Keep doing this until current district is satisfied.
    queue = list()
    for tract in my_adjacent_tracts:
        queue.extend(tract.adjacent_to)

    # this loop keeps trying to steal tracts until the district hits
    # its population target, or has nothing left to steal
    while stealing_district.population < MAGIC_POPULATION_NUMBER and queue:

        next = all_tracts[queue.pop()] # dequeue the next tract

        # Check if tract is part of the victim district, or just free
        if next.owning_district == victim_district.district_id:
            # Steal!
            next = victim_district.remove_tract(next)
            stealing_district.add_tract(next)

            # queue all tracts adjacent
            queue.extend(next.adjacent_to)
        elif _take_tract(next.id):
            # Not stealing, so just take it
            stealing_district.add_tract(next)

            # queue all tracts adjacent
            queue.extend(next.adjacent_to)

    # Try readding some tracts to the victim district
    revalidate_district(victim_district)


def revalidate_district(district):
    '''
    If district is under population (was stolen from), need to add those numbers back up

    arguments: district object that is to be validated
    '''
    queue = list()
    # Just add everything every tract in the district is adjacent to
    # It's not computationally efficient, but currently don't have a method
    # to pick and choose the outer edge tracts only
    for tract in district.tracts:
        queue.extend(tract.adjacent_to)

    # this loop keeps trying to add tracts until the district hits
    # its population target. Or if no more things to add
    # TODO: currently if run out of things to add, just throw hands up and give up
    while district.population < MAGIC_POPULATION_NUMBER and queue:

        # TODO: Check if trapped again? But could end up in vicious recursion cycle...

        next = all_tracts[queue.pop()] # dequeue the next tract

        if _take_tract(next.id):
            district.add_tract(next)

            # queue all tracts adjacent
            queue.extend(next.adjacent_to)


def revalidate_overload(district):
    '''
    this function takes the district, and grabs any free tracts
    adjacent to it until it cant grab anymore

    should be used only as a final passthrough, think of it as
    cleaning up leftover crumbs
    '''
    queue = list()
    # Just add everything every tract in the district is adjacent to
    # It's not computationally efficient, but currently don't have a method
    # to pick and choose the outer edge tracts only
    for tract in district.tracts:
        queue.extend(tract.adjacent_to)

    # this loop keeps trying to add tracts until there's no more things to add
    while queue:
        next = all_tracts[queue.pop()] # dequeue the next tract

        if _take_tract(next.id) and next.owning_district == "":
            district.add_tract(next)

            # queue all tracts adjacent
            queue.extend(next.adjacent_to)


def revalidate_small_districts():
    '''
    this function goes through all the districts made and
    if the population is too small (<95% of the average) then it will
    steal from the neighbor with the biggest potential
    '''
    for id, district in all_districts.items():
        update_potentials()
        if district.population < MAGIC_POPULATION_NUMBER_95PERCENT:
            # Find out who I can steal from
            adjacent_districts = get_adjacent_district_ids(district)

            # Target the adjacent district with most potential
            to_steal_from = adjacent_districts[0]
            for d_id in adjacent_districts:
                if all_districts[d_id].potential >= all_districts[to_steal_from].potential:
                    to_steal_from = d_id

            # Steal!
            steal_tracts(district, all_districts[to_steal_from])


def update_potentials():
    '''
    This updates the "potential" variable for all the districts made thus far
    Potential is number of adjacent tracts available to take
    '''
    for id, district in all_districts.items():
        district.potential = 0 # reset
        tract_set = set() # set, no dupes

        # Grab all adjacent tracts of the districts
        for tractid in district.tracts:
            for tract in all_tracts[tractid].adjacent_to:
                tract_set.add(tract)

        # Sum up number of free tracts to get the potential
        for tractid in tract_set:
            if all_tracts[tractid].owning_district == "":
                district.potential = district.potential + 1


def _create_district(start, district_id):
    '''
    this creates one congressional district given a starting tract

    it queues all adjacent tracts for the start, then from the first, etc
    and grabs them sequentially until the district is made. It takes the next


    arguments: start - a tract object from which districting starts
    district_id: some arbitrary and unqiue int to keep tract of the districts by id
    returns: a tuple consisting of: a district object representing the finished district
                                    the next tract in the queue
    '''

    # tries to add the passed-in starting tract to the district
    # will raise an exception if the district is already taken
    created_district = geography_objects.district(0, district_id)
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
    while created_district.population < MAGIC_POPULATION_NUMBER:
        # Check if trapped
        if not queue:
            # Find out who I can steal from
            adjacent_districts = get_adjacent_district_ids(created_district)

            # Target the adjacent district with most potential
            to_steal_from = adjacent_districts[0]
            update_potentials()
            for district in adjacent_districts:
                if all_districts[district].potential >= all_districts[to_steal_from].potential:
                    to_steal_from = district

            # Steal!
            steal_tracts(created_district, all_districts[to_steal_from])
            break

        next = all_tracts[queue.pop()] # dequeue the next tract

        if _take_tract(next.id):
            # Debug Statement:
            # print(next.id + " success!")
            created_district.add_tract(next)

            # queue all tracts adjacent
            queue.extend(next.adjacent_to)

    # this picks a random adjacent tract
    # see issues above for running out of tracts issue
    next_id = None
    next_id = random.choice(available_tracts)

    return (created_district, all_tracts[next_id])


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


def generic_redistrict():
    '''
    this redistricts Maryland using a default start tract
    returns: a list of 8 district objects
    '''
    start = "24003751200"
    return specific_redistrict(start)


def specific_redistrict(start):
    '''
    this redistricts Maryland using a given start tract
    arguments: start - a tract id representing the tract that districting will start from
    returns: a list of district objects (8 district objects)
    '''
    global all_tracts, all_districts, available_tracts
    start = all_tracts[start]
    districts = []
    next = start

    # Inital setup of districts
    for i in range(8):
        new_district, next = _create_district(next, i)
        districts.append(new_district)
        all_districts[i] = new_district

    # There will be leftover tracts
    # So slowly steal from each other to even things out
    for x in range(0, 15):
        revalidate_small_districts()

    # There may be a few leftover tracts at this point
    # Let whichever district who is able to to just pick them up
    # Their population will be "overloaded", but only by a negligible amount
    update_potentials()
    for id, district in all_districts.items():
        if district.potential > 0:
            revalidate_overload(district)

    # Debug statement:
    # print("{} tracts remaining after redistricting".format(len(available_tracts)))

    # reset the 'global' variables
    all_tracts = tracts.get_all_tracts()
    available_tracts = [k for k in all_tracts.values()]
    all_districts = {}

    return _sanitize_districts(districts)
