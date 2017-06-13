#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
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

        pattern = self.get_param('pattern', '*').replace("'","\\'")
        alumni = bttbAlumni()
        user_query = '''SELECT first,nee,last,id,email
                        FROM alumni
                        WHERE (first like '%%%s%%'
                              OR last like '%%%s%%'
                              OR nee like '%%%s%%'
                              OR user_id like '%%%s%%'
                              OR email like '%%%s%%')
                            AND make_public = 1
                        ORDER BY last
                        LIMIT 20''' % (pattern,pattern,pattern,pattern,pattern)
        results,_ = alumni.process_query( user_query )
        for result in results:
            print '\t'.join([str(field) for field in result])

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBFindMatches()
    PROCESSOR.process_query()
except Exception, ex:
    print 'ERR: %s' % str(ex)

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================

