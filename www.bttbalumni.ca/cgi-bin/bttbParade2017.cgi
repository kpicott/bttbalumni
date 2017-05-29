#!/usr/bin/env python
"""
Process the 2017 parade sign-up information. The return value printed is:

    NOT_SIGNED_UP    : The alumni is not signed up for the parade and not registered on the store
    NOT_REGISTERED   : The alumni is signed up for the parade and not registered on the store
    NO_INSTRUMENT    : The alumni is not signed up for the parade but registered on the store
    SIGNED_UP        : The alumni is signed up for the parade and registered on the store
    PROCESSING_ERROR : There was an error in processing
"""

NOT_SIGNED_UP = 0
NOT_REGISTERED = 1
NO_INSTRUMENT = 2
SIGNED_UP = 3
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
        database = bttbDB()
        database.Initialize()

        alumni_id = get_int_param( 'id', -1 )
        instrument_id = get_int_param( 'instrument', 0 )
        registered_id = get_int_param( 'registered', 0 )

        # Instrument ID of 0 means not participating
        if instrument_id == 0:
            database.delete_parade_part_2017( alumni_id )
            if registered_id == 0:
                print NOT_SIGNED_UP,
            else:
                print NO_INSTRUMENT,
        # Any other instrument ID is assumed to be valid
        else:
            database.set_parade_part_2017( alumni_id, instrument_id, registered )
            if registered_id == 0:
                print NOT_REGISTERED,
            else:
                print SIGNED_UP,

        database.Finalize()

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
