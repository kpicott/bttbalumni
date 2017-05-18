#!/usr/bin/env python
"""
Process the 2017 concert sign-up information. The return value printed is:

    NOT_SIGNED_UP    : The alumni is not signed up for the concert
    SIGNED_UP        : The alumni is signed up for the concert
    PROCESSING_ERROR : There was an error in processing
"""

NOT_SIGNED_UP = 0
SIGNED_UP = 1
PROCESSING_ERROR = -1

print 'Content-type: text/plain\n'

import cgi
from bttbDB import bttbDB

#----------------------------------------------------------------------
def get_int_param(name,default):
    """ Simple trick to get numeric cgi params using default values """
    try:
        value = int( PARAMS[name][0] )
    except Exception:
        value = default
    return value

#----------------------------------------------------------------------
def process_query():
    try:
        DATABASE = bttbDB()
        DATABASE.Initialize()

        ALUMNI_ID = get_int_param( 'id', -1 )
        INSTRUMENT_ID = get_int_param( 'instrument', 0 )

        # Instrument ID of 0 means not participating
        if INSTRUMENT_ID == 0:
            DATABASE.delete_concert_part_2017( ALUMNI_ID )
            print NOT_SIGNED_UP,
        # Any other instrument ID is assumed to be valid
        else:
            DATABASE.set_concert_part_2017( ALUMNI_ID, INSTRUMENT_ID )
            print SIGNED_UP,

        DATABASE.Finalize()

    except Exception, ex:
        # Any exceptions will result in the database not being updated
        print "%d : %s" % (PROCESSING_ERROR, str(ex)),

try:
    PARAMS = cgi.parse()
    process_query()
except Exception, ex:
    print "%d : %s" % (PROCESSING_ERROR, str(ex)),

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
