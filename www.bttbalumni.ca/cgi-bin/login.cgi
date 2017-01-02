#!env python
#
# Confirm login information for a user and return a response:
#  Input:	user=USERNAME
#			password=PASSWORD
#  Output:  "0"										(if user not valid)
#			"id|onCommittee?|first|fullName"	(if user valid)
#

print 'Content-type: text/html\n'

import cgi
from bttbAlumni import *
params = cgi.parse()
first = ''
last = ''
password = ''
member = None
try:
	for p in params:
		if p == 'user':
			name = params[p][0].strip().rstrip()
		elif p == 'password':
			password = params[p][0]
	alumni = bttbAlumni()
	member = alumni.getMemberFromLogin(name, password)
except:
	pass
if member:
	print '%d|%d|%s|%s' %(member.id, member.onCommittee, member.first, member.fullName() )
else:
	print 'fail'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
