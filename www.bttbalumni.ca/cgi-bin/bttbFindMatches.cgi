#!/usr/bin/env python
"""
Process the query to find matches for a user.
The form field to match is called "pattern" and it will do a "LIKE"
match on the name fields, the user ID, and the email address.
"""
print 'Content-type: text/plain\n'

from bttbAlumni import bttbAlumni
from bttbConfig import Error, MapLinks
from bttbCGI import bttbCGI

class BTTBFindMatches(bttbCGI):
    '''Class to handle parsing of the match POST request'''

    #----------------------------------------------------------------------
    def process_query(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()

        pattern = self.get_param('pattern', '*'):
        alumni = bttbAlumni()
        results,_ = alumni.process_query( '''SELECT first,nee,last,id,emal
											 FROM alumni
											 WHERE first like '%s'
											    OR last like '%s'
											    OR nee like '%s'
											    OR user_id like '%s'
											    OR email like '%s'
											 ORDER BY last''' )
        print '\n'.join( results )

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBQuery()
    PROCESSOR.process_query()
except Exception, ex:
    Error( 'Could not process query', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================

