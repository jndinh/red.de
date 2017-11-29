'''

This module defines classes for geographic areas. The classes defined are: tract and district.

A tract object represents a census tract. Specifically, it stores its
* population (int)
* ID (str)
* adjacent tracts (list of tracts)

A district object represents a congressional district. It stores
* population (int)
* component tracts (list of tracts)

CHANGE LOG
Dorothy Carter - 20171028 - initial creation of classes & script
Dorothy Carter - 20171107 - removal of sample scripts
Dorothy Carter - 20171109 - __eq__() method in tract
                            population updating in district
                            creation of district_error

'''


class tract:
    def __init__(self, pop=0, tract_id=""):
        '''
        this initializes a tract object.
        arguments: pop (=population of tract). Int. Default 0
                   tract_id. Str. Default 0
        sets the adjacent_to attribute to an empty list
        '''
        self.population = pop
        self.id = tract_id
        self.adjacent_to = []

    def add_adjacency(self, tract):
        '''
        this appends a tract to the list of adjacent tracts

        arguments: tract. A str (the tract id). No default
        '''

        self.adjacent_to.append(tract)

    def set_adjacencies_to(self, areas):
        '''
        this is a convenience to set the adjacent_to attribute to a new list
        provided in case extra processing has to go here

        arguments: areas. A list of tract ids (strs) it is adjacent to. No default
        '''

        self.adjacent_to = areas

    def bulk_add_adjacencies(self, tracts):
        '''
        this appends a list of tracts to the list of adjacent tracts

        arguments: tracts. A list of tract ids (strs) it is adjacent to. No default
        '''

        self.adjacent_to.extend(tracts)

    def get_adjacencies(self):
        '''
        this returns the adjacent_to list. not strictly necessary (could use self.adjacent_to),
        but provided as a convenience

        can use as:
        for tract in this_tract.get_adjacencies():
            pass
        '''
        return self.adjacent_to

    def __str__(self):
        '''
        this prints the tract object nicely.
        '''
        return "Census tract " + self.id + ". Population: " + str(self.population)
    
    def __eq__(self, other):
        '''
        this compares tract ids to determine equality
        '''
        
        if hasattr(other, "id"):
            return self.id == other.id
        else:
            return self.id == other.__str__()


    def __eq__(self, other):
        '''
        this compares tract ids to determine equality
        '''

        if hasattr(other, "id"):
            return self.id == other.id
        else:
            return self.id == other.__str__()


class district:
    def __init__(self, pop=0):
        '''
        this initializes a tract object.
        arguments: pop (=population of tract). Int. Default 0
        sets the tracts attribute to an empty list
        '''
        self.population = pop
        self.tracts = []

    def add_tract(self, tract_id, tract_pop):
        '''
        this initializes a new tract object and adds it to the tracts list
        arguments: tract_id. Str. No default
                   tract_pop (=population of tract). Int. No default
        '''
        self.tracts.append( tract(tract_pop, tract_id) )
        self.population += tract_pop
        
    def add_tract(self, tract):
        '''
        this adds a previously created tract object to the tracts list
        arguments: tract. A tract object. No default
        '''
        self.tracts.append(tract)
        self.population += tract.population
        
    def bulk_add_tract(self, many_tracts):
        '''
        this adds a list of tracts to the component tracts
        arguments: many_tracts. A list of tracts. No default
        '''
        self.tracts.extend(many_tracts)
        
        for tract in many_tracts:
            self.population += tract.population
            
    def set_tracts_to(self, new_tracts):
        '''
        this sets the list of component tracts to the list passed in
        also updates population
        arguments: new_tracts. A list of tracts. No default
        '''
        self.tracts = new_tracts

        for tract in new_tracts:
            self.population += tract.population


    def get_tracts(self):
        '''
        this returns the list of component tracts. not strictly necessary (use self.tracts),
        but provided as a convenience
        '''
        return self.tracts

    def __str__(self):
        '''
        this prints the district object nicely
        '''
        return "District population: " + str(self.population) + ". " + str(len(self.tracts)) + " tracts included"


class district_error(Exception):
    def __init__(self, msg=""):
        '''
        this defines an error originating in these modules,
        to distinguish from runtime, etc
        arguments: msg - str - an explanation of the exception
        '''
        super.__init__(msg)
