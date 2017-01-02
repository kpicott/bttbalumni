#!env python
"""
Process the BTTB committee approval request to add new people
to the list of those who are verified after registration.
"""

import os
import os.path
import re
import cgi
from bttbAlumni import *
from bttbConfig import *

print 'Content-type: text/html\n'

try:
	params = cgi.parse()
except Exception, e:
	Error( 'CGI Error', e )

alumni = bttbAlumni()

#----------------------------------------------------------------------

re_approvePattern = re.compile( 'AXXX(.*)' )
for p in params:
	match = re_approvePattern.match( p )
	# Do nothing unless the approval is given. May not match
	# exactly what is expected but avoids the extra work of
	# providing default values for the checkboxes in the form.
	if match:
		id = int(match.group(1))
		isFriend = 'FXXX' + match.group(1) in params
		isCommittee = 'CXXX' + match.group(1) in params
		alumni.approveMember( id, isFriend, isCommittee )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
