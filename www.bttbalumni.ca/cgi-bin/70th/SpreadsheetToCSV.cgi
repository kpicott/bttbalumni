#!/usr/bin/env python
"""
Utility script to automatically create a CSV file for name tag info with data
found in the registration spreadsheet.

The spreadsheet is presumed to reside in the same directory as the script, and
the information is in a tab-separated-value format.

The fields in the CSV file will be
    First
    Nee
    Last
    FirstYear
    LastYear
    Instrument(s)
    OnCommittee
    InSocial
    InParade

If only the name is given (no alumni ID) then only the First/Last will be
populated, presumed to be a space-separated pair.
"""

print 'Content-type: text/csv'
print 'Content-Disposition: attachment; filename="BTTBReunionAttendance.csv"\n'

import sys
sys.path.insert(0,'..')

from bttbAlumni import bttbAlumni
from bttbCGI import bttbCGI
from bttbConfig import Error

# Name of file being uploaded
SPREADSHEET_FILE_NAME = 'BTTB 70th Reunion Attendance - Reunion.tsv'

# Magic 'instruments' database ID meaning "no instrument selected"
UNSPECIFIED_INSTRUMENT = 46

class SpreadsheetToCSV(bttbCGI):
    '''Class to handle population of the database with the registration spreadsheet information'''
    def __init__(self):
        '''Set up the database handler'''
        bttbCGI.__init__(self)
        self.alumni = bttbAlumni()

    #----------------------------------------------------------------------
    def print_csv(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()

        # Index values that will be used from the spreadsheet
        name_idx = -1
        id_idx = -1
        all_inclusive_early_idx = -1
        all_inclusive_idx = -1
        social_idx = -1
        parade_idx = -1

        # First print the header line
        print 'First,Nee,Last,FirstYear,LastYear,Instrument(s),OnCommittee,InSocial,InParade'

        tsv_fd = open(SPREADSHEET_FILE_NAME, 'r')
        for line in tsv_fd:
            fields = line.rstrip().split( '\t' )
            if len(fields) == 0:
                continue
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
                member = None
                try:
                    name = fields[name_idx]
                    alumni_id = int(fields[id_idx])
                    member = self.alumni.getMemberFromId( alumni_id )
                except ValueError:
                    alumni_id = -1

                in_parade = False
                in_social = False
                # Check 1 - signed up for parade
                try:
                    if fields[parade_idx] != "":
                        in_parade = True
                except ValueError:
                    pass

                # Check 2 - signed up for social event
                try:
                    if fields[social_idx] != "":
                        in_social = True
                except ValueError:
                    pass

                # Check 3 - signed up for both, early or not
                try:
                    if fields[all_inclusive_early_idx] != "":
                        in_parade = True
                        in_social = True
                except ValueError:
                    pass
                try:
                    if fields[all_inclusive_idx] != "":
                        in_parade = True
                        in_social = True
                except ValueError:
                    pass

                csv_fields = []
                if member == None:
                    try:
                        first,last = name.split(' ',1)
                    except Exception:
                        continue
                    csv_fields.append( '"%s"' % first )
                    csv_fields.append( '' )
                    csv_fields.append( '"%s"' % last )
                    csv_fields.append( '' )
                    csv_fields.append( '' )
                    csv_fields.append( '' )
                    csv_fields.append( '0' )
                else:
                    csv_fields += ['"%s"' % member.first, '"%s"' % member.nee, '"%s"' % member.last]
                    csv_fields.append( str(member.firstYear) )
                    csv_fields.append( str(member.lastYear) )
                    csv_fields.append( '"%s"' % ' '.join(member.instruments) )
                    csv_fields.append( ['0','1'][member.onCommittee] )

                csv_fields.append( ['0','1'][in_social] )
                csv_fields.append( ['0','1'][in_parade] )
                print ','.join( csv_fields )

        tsv_fd.close()

#----------------------------------------------------------------------

try:
    PROCESSOR = SpreadsheetToCSV()
    PROCESSOR.print_csv()
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
