#!/usr/bin/env python
"""
Utility script to automatically populate the databases with information found
in the registration spreadsheet.

The spreadsheet is presumed to reside in the same directory as the script, and
the information is in a tab-separated-value format.

The population is non-destructive. Items in the spreadsheet that are not in
the database are added to it, but items not in the spreadsheet are not removed
from the database.
"""

print 'Content-type: text/html\n'

import sys
sys.path.insert(0,'..')

from bttbAlumni import bttbAlumni
from bttbCGI import bttbCGI
from bttbConfig import Error

# Name of file being uploaded
SPREADSHEET_FILE_NAME = 'BTTB 70th Reunion Attendance - Reunion.tsv'

# Magic 'instruments' database ID meaning "no instrument selected"
UNSPECIFIED_INSTRUMENT = 46

class SpreadsheetToDB(bttbCGI):
    '''Class to handle population of the database with the registration spreadsheet information'''
    def __init__(self):
        '''Set up the database handler'''
        bttbCGI.__init__(self)
        self.alumni = bttbAlumni()

    #----------------------------------------------------------------------
    def set_in_parade(self, alumni_id):
        '''
        Set the alumni member as being a parade participant. No instrument
        is defined in the spreadsheet so use "Unspecified" if they aren't
        already signed up.
        '''
        if alumni_id is None:
            return

        query = 'SELECT * from 2017_parade WHERE alumni_id = %d' % alumni_id

        # If already in the parade then just set the registration status
        results,_ = self.alumni.process_query( query )
        if len(results) > 0:
            update = 'UPDATE 2017_parade SET registered=1 WHERE alumni_id=%d' % alumni_id
            self.alumni.process_query( update )
            return

        # Add to the parade
        insert = 'INSERT INTO 2017_parade (alumni_id, instrument_id, registered) VALUES (%d, %d, 1)' % (alumni_id, UNSPECIFIED_INSTRUMENT)
        results, _ = self.alumni.process_query( insert )
        print '<p>%s<br><i>%s</i></p>' % (insert, str(results))

    #----------------------------------------------------------------------
    def set_in_social(self, alumni_id, name):
        '''
        Set the alumni member as being a social participant.
        '''
        if alumni_id is not None:
            query = 'SELECT * from 2017_social WHERE alumni_id = %d' % alumni_id
            insert = 'INSERT INTO 2017_social (alumni_id) VALUES (%d)' % alumni_id
        else:
            query = "SELECT * from 2017_social WHERE name = '%s'" % name
            insert = "INSERT INTO 2017_social (alumni_id, name) VALUES (-1, '%s')" % name

        # If already registered return
        results,_ = self.alumni.process_query( query )
        if len(results) > 0:
            return

        # Add to the social event
        results,_ = self.alumni.process_query( insert )
        print '<p>%s<br><i>%s</i></p>' % (insert, str(results))

    #----------------------------------------------------------------------
    def populate_database(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()

        # Index values that will be used from the spreadsheet
        name_idx = -1
        id_idx = -1
        all_inclusive_early_idx = -1
        all_inclusive_idx = -1
        social_idx = -1
        parade_idx = -1

        tsv_fd = open(SPREADSHEET_FILE_NAME, 'r')
        for line in tsv_fd:
            fields = line.rstrip().split( '\t' )
            if name_idx < 0:
                for i in range(0,len(fields)):
                    if fields[i] == 'Name':
                        name_idx = i
                    elif fields[i] == 'ID':
                        id_idx = i
                    elif fields[i] == 'All-Inclusive (Early)':
                        all_inclusive_early_idx = i
                    elif fields[i] == 'All-Inclusive':
                        all_inclusive_idx = i
                    elif fields[i] == 'Social':
                        social_idx = i
                    elif fields[i] == 'Parade':
                        parade_idx = i
            # Process the information line
            else:
                # First establish the identification available; id or name
                alumni_id = None
                try:
                    name = fields[name_idx]
                    alumni_id = int(fields[id_idx])
                except ValueError:
                    pass

                # Check 1 - signed up for parade
                try:
                    if int(fields[parade_idx]) > 0:
                        self.set_in_parade( alumni_id )
                except ValueError:
                    pass

                # Check 2 - signed up for social event
                try:
                    if int(fields[social_idx]) > 0:
                        self.set_in_social( alumni_id, name )
                except ValueError:
                    pass

                # Check 3 - signed up for both, early or not
                try:
                    if int(fields[all_inclusive_early_idx]) > 0:
                        self.set_in_parade( alumni_id )
                        self.set_in_social( alumni_id, name )
                except ValueError:
                    pass
                try:
                    if int(fields[all_inclusive_idx]) > 0:
                        self.set_in_parade( alumni_id )
                        self.set_in_social( alumni_id, name )
                except ValueError:
                    pass

        tsv_fd.close()

#----------------------------------------------------------------------

try:
    PROCESSOR = SpreadsheetToDB()
    PROCESSOR.populate_database()
except Exception, ex:
    Error( 'Could not process registration', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
