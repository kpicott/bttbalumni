#!env python
"""
Process the BTTB committee approval request to add new people
to the list of those who are verified after registration.
"""

import re
import cgi
from bttbAlumni import bttbAlumni
from bttbConfig import Error

print 'Content-type: text/html\n'

try:
    PARAMS = cgi.parse()
except Exception, ex:
    Error( 'CGI Error', ex )

ALUMNI = bttbAlumni()

#----------------------------------------------------------------------

RE_APPROVE_PATTERN = re.compile( 'AXXX(.*)' )
for p in PARAMS:
    match = RE_APPROVE_PATTERN.match( p )
    # Do nothing unless the approval is given. May not match
    # exactly what is expected but avoids the extra work of
    # providing default values for the checkboxes in the form.
    if match:
        alumni_id = int(match.group(1))
        is_friend = 'FXXX' + match.group(1) in PARAMS
        is_committee = 'CXXX' + match.group(1) in PARAMS
        ALUMNI.approve_member( alumni_id, is_friend, is_committee )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
