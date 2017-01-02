#!env python
"""
Process the BTTB Concert Signup request.
Unlike most form replies this one explicitly prints out its responses so there
is no post-load after this script completes.
"""

print 'Content-type: text/html\n'
print 'Signed Up For Concert||'
print '<body>'
print '<h1>Thanks for Signing Up</h1>'

import cgi
from bttbAlumni import bttbAlumni
from bttbConfig import *

def getParam(name,default):
	"""
	Simple trick to get cgi params using default values
	"""
	try:
		value = params[name][0].strip()
	except:
		value = default
	return value

def getIntParam(name,default):
	"""
	Simple trick to get numeric cgi params using default values
	"""
	try:
		value = int( params[name][0] )
	except:
		value = default
	return value

try:
	params = cgi.parse()
	newPart = getIntParam( 'part', 0 )
	who = getIntParam( 'id', 999999 )
	alumni = bttbAlumni()
	member = alumni.getMemberFromId(who)
	alumni.setConcertPart(who, newPart)
	#
	allParts = alumni.getConcertInstrumentation()
	for iName,iId,whoHas in allParts:
		if iId == newPart:
			print '<p>%s is now signed up in the concert as %s</p>' % (member.fullName(), iName)
			print '<p>Full list of people signed up for this part:<ol>'
			print '<i>%s</i></ol></p>' % whoHas
			print MapLinks( """
			<p>
			download:(/SheetMusic/Concert1/%s.pdf,Click here to download your concert sheet music)
			</p>""" ) % iName.replace(' ', '')
except Exception, e:
	Error( 'Concert signup processing error', e )

print '</body>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
