#!/usr/bin/env python
"""
Process the BTTB committee approval request to add new people
to the list of those who are verified after registration.
"""

print 'Content-type: text/html\n'

import re
from bttbAlumni import bttbAlumni
from bttbCGI import bttbCGI
from bttbConfig import Error

RE_APPROVE_PATTERN = re.compile( 'AXXX(.*)' )

#----------------------------------------------------------------------
class BTTBApprove(bttbCGI):
    '''Class to handle parsing of the member approval POST request'''

    #----------------------------------------------------------------------
    def process_approval(self):
        '''Read the approval info and add or modify it in the database'''
        self.read_cgi()

        alumni = bttbAlumni()
        try:
            for param in self.params:
                match = RE_APPROVE_PATTERN.match( param )
                # Do nothing unless the approval is given. May not match
                # exactly what is expected but avoids the extra work of
                # providing default values for the checkboxes in the form.
                if match:
                    alumni_id = int(match.group(1))
                    is_friend = 'FXXX' + match.group(1) in self.params
                    is_committee = 'CXXX' + match.group(1) in self.params
                    alumni.approve_member( alumni_id, is_friend, is_committee )

        except Exception, ex:
            Error( 'Approval processing error', ex )

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBApprove()
    PROCESSOR.process_approval()
    print "OK"
except Exception, ex:
    Error( 'Could not process approval', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
