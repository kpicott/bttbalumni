#!/usr/bin/env python
"""
Utility script to automatically populate the databases with information that
was previously hardcoded in the page generation scripts.

Moving the data to the databases allows a web-facing interface to modify them.
"""

print 'Content-type: text/html\n'

import sys
sys.path.insert(0,'..')

from bttbAlumni import bttbAlumni
from bttbCGI import bttbCGI
from bttbConfig import Error

class PopulateOldData(bttbCGI):
    '''Class to handle population of the database with the registration spreadsheet information'''
    def __init__(self):
        '''Set up the database handler'''
        bttbCGI.__init__(self)
        self.alumni = bttbAlumni()

    #----------------------------------------------------------------------
    def populate_memorials(self):
        '''
        Add all of the memorial information to the database
        '''
        memorials = [
            ("Elgin", "", "Corlett", 1947, 1967, "Founder, Director"),
            ("Larry", "", "Duke", 1947, 1953, "Flute"),
            ("Keith", "", "Hall", 1947, 1950, "Trombone"),
            ("Roy", "", "Hall", 1947, 1950, "Percussion"),
            ("Larry", "", "Oake", 1947, 1953, "Flute"),
            ("Roger", "", "Hammill", 1954, 1961, "Trombone"),
            ("Dave", "", "Allaster", 1959, 1972, "Trumpet"),
            ("Rob", "", "Herdman", 1961, 1965, "Tuba"),
            ("Bob", "", "Champ", 1962, 1970, "Trumpet"),
            ("Charlie", "", "Parsons", 1962, 1997, "Equipment Manager, Truck Driver, Chaperone"),
            ("Cathy", "", "Blezard", 1963, 1968, "Trumpet"),
            ("Cathy", "", "Corlett", 1963, 1967, "Clarinet "),
            ("Anne", "Gordon", "Hall", 1964, 1970, "Colour Guard"),
            ("Louise", "", "Dagenais", 1965, 1971, "Majorette"),
            ("Pat", "Millward", "Plummer", 1965, 1975, "Majorette/Flute"),
            ("Neal", "", "Sinclair", 1967, 1973, "Drum Major"),
            ("Pete", "", "Conway", 1968, 1972, "Percussion"),
            ("Tim", "", "Watt", 1968, 1973, "Percussion"),
            ("Mary", "", "Ford", 1968, 1973, "Colour Guard"),
            ("Eric", "", "Ford", 1968, 1976, "Director"),
            ("Helen \"Lois\"", "", "Hanley", 1968, 1974, "Band Booster"),
            ("Dani", "", "Jainu", 1969, 1972, "Sousaphone"),
            ("Audrey", "", "Cook", 1969, 1969, "Clarinet"),
            ("Cindy", "", "Schmidt", 1972, 1976, "Colour Guard"),
            ("George", "", "Newell", 1972, 1978, "Booster/Chaperone"),
            ("Nancy", "Neil", "Kerr", 1976, 1981, "Saxophone"),
            ("Glen", "", "De Foa", 1976, 1979, ""),
            ("Don", "", "Bennett", 1977, 1982, "French Horn"),
            ("Paul", "", "Hill", 1980, 1985, "Flute"),
            ("Toni", "Gaul", "Clement", 1980, 1987, "Flute/Piccolo"),
            ("Antony", "", "Roberts", 1981, 1985, "Percussion"),
            ("Cathy", "Carr", "Paszt", 1982, 1987, "Saxophone/Drum Major"),
            ("Dr. Michael", "", "Sharpe", 1982, 1987, "Trumpet/Drum Major"),
            ("Willem", "", "Murray", 1987, 1989, "Percussion"),
            ("Mac", "", "Elliot", 2012, 2013, "Percussion")
        ]

        for (first,nee,last,year_joined,year_left,positions) in memorials:
            insert = '''INSERT INTO memorials
                            (first_name, nee, last_name, first_year, last_year, positions)
                        VALUES ('%s', '%s', '%s', %d, %d, '%s')''' % (first,nee,last,year_joined,year_left,positions)

            # Add to the memorials
            results, _ = self.alumni.process_query( insert )
            print '<p><pre>%s</pre><b>%s</b></p>' % (insert, str(results))

    #----------------------------------------------------------------------
    def populate_drum_majors(self):
        '''
        Add all of the Drum Major information to the database
        '''
        drum_majors = [
             ("Kerig",       "",            "Ahearn")
        ,    ("Jeff",        "",            "Allen")
        ,    ("George",      "",            "Ashfield")
        ,    ("Phil",        "",            "Austin")
        ,    ("Rob",         "",            "Bennett")
        ,    ("Ashley",      "",            "Benton")
        ,    ("Miles",       "",            "Benton")
        ,    ("Sarah",       "",            "Benton")
        ,    ("Ron",         "",            "Bigelow")
        ,    ("Bob",         "",            "Branch")
        ,    ("Carol",       "Corlett",     "Broadhurst")
        ,    ("Paul",        "",            "Burnip")
        ,    ("Christine",   "Campbell",    "Zsiros")
        ,    ("Cathy",       "Carr",        "Paszt")
        ,    ("Peter",       "",            "Clarke")
        ,    ("Lindsey",     "",            "Crampton")
        ,    ("Gerry",       "",            "Dearing")
        ,    ("Bob",         "",            "Gentile")
        ,    ("Gary",        "",            "Gentile")
        ,    ("Anne",        "Goodyear",    "DeFoa")
        ,    ("Phyllis",     "",            "Gordon")
        ,    ("Brad",        "",            "Hall")
        ,    ("Lea",         "",            "Harrington")
        ,    ("Heather",     "",            "Harris")
        ,    ("Megan",       "",            "Hebert")
        ,    ("John",        "",            "Holman")
        ,    ("Jenny",       "",            "Johnson")
        ,    ("Heather",     "",            "Keenleyside")
        ,    ("MaryAnne",    "Lyons",       "Quaglia")
        ,    ("Sarah",       "",            "MacLeod")
        ,    ("Lorrie-Anne", "",            "Maitland")
        ,    ("Simon",       "",            "Matthews")
        ,    ("Sarah",       "",            "McCleary")
        ,    ("Dave",        "",            "McPetrie")
        ,    ("Bev",         "McCune",      "Norman")
        ,    ("Lisa",        "",            "Nicol")
        ,    ("Nick",        "",            "Quaglia")
        ,    ("Tom",         "",            "Quaglia")
        ,    ("Carol",       "",            "Radford")
        ,    ("Carolyn",     "Ridge",       "Whiskin")
        ,    ("Mike",        "",            "Sharpe")
        ,    ("Scott",       "",            "Shepherd")
        ,    ("Colin",       "",            "Sinclair")
        ,    ("Neal",        "",            "Sinclair")
        ,    ("Kellie",      "",            "Skerett")
        ,    ("Ted",         "",            "Slavin")
        ,    ("Francis",     "",            "Smith")
        ,    ("Alexandra",   "",            "Smyth")
        ,    ("Paul",        "",            "Snyder")
        ,    ("Dustin",      "",            "Steplock")
        ,    ("Gary",        "",            "Stock")
        ,    ("Jeff",        "",            "Thomblison")
        ,    ("Dave",        "",            "Wallace")
        ,    ("Carol",       "",            "Webb")
        ,    ("Allan",       "",            "Whiskin")
        ]

        for (first,nee,last) in drum_majors:
            insert = '''INSERT INTO drum_majors
                            (first_name, nee, last_name)
                        VALUES ('%s', '%s', '%s')''' % (first,nee,last)

            # Add to the memorials
            results, _ = self.alumni.process_query( insert )
            print '<p><pre>%s</pre><b>%s</b></p>' % (insert, str(results))

    #----------------------------------------------------------------------
    def populate_database(self):
        '''Walk all of the database tables to be populated'''
        self.read_cgi()

        self.populate_memorials()
        self.populate_drum_majors()

#----------------------------------------------------------------------

try:
    PROCESSOR = PopulateOldData()
    PROCESSOR.populate_database()
except Exception, ex:
    Error( 'Could not populate the old data', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
