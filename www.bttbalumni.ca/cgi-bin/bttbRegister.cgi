#!env python
"""
Process the BTTB Alumni registration information and add it to the database,
sending a confirmation email if an email address was specified.
"""

print 'Content-type: text/html\n'

import os
import os.path
import re
import cgi
from datetime import datetime
from bttbMember import bttbMember
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

def Cap(name):
	"""
	Returns a capitalized string, but without changing inner characters
	(the "capitalize()" method messes up "McTavish" to "Mctavish"
	"""
	if len(name) < 2: return name.capitalize()
	return name[0].upper() + name[1:]

try:
	params = cgi.parse()
	alumni = bttbAlumni()
	changedAt = datetime.now()
	#
	# If the id was negative then this is an edit:
	#	Look for a previous edit to overwrite
	#	Either insert or update at (negative-id).
	#
	# Otherwise it's a creation, and requires a new id
	#
	uniqueId = getIntParam('id', os.getpid())
	if uniqueId <= 0:
		member = alumni.getMemberFromId(-uniqueId)
	else:
		while alumni.getMemberFromId(uniqueId):
			uniqueId = uniqueId + 1
		member = bttbMember()
		member.setJoinTime( datetime.now() )
		member.setId( uniqueId )
except Exception, e:
	Error( 'Registration processing error', e )

member.setEditTime( changedAt )

#----------------------------------------------------------------------

firstName = Cap( getParam( 'FirstName', '' ) )
lastName = Cap( getParam( 'CurrentLastName', '' ) )
nee = Cap( getParam( 'LastNameInBand', '' ) )
member.setName( firstName, nee, lastName )

#----------------------------------------------------------------------

firstYear = AsYYYY( getParam( 'FirstYear', '' ) )
lastYear = AsYYYY( getParam( 'LastYear', '' ) )
member.setYears( firstYear, lastYear )

#----------------------------------------------------------------------

rank = Cap( getParam( 'HighestRank', '' ) )
member.setRank( rank )

#----------------------------------------------------------------------

password = getParam( 'Password', '' )
member.setPassword( password )

#----------------------------------------------------------------------

memory = getParam( 'SpecialTime', '' ).strip()
memoryId = getIntParam( 'SpecialTimeId', -1 )

#----------------------------------------------------------------------

street1 = Cap( getParam( 'Street1', '' ) )
street2 = Cap( getParam( 'Street2', '' ) )
apt = getParam( 'Apt', '' )
city = Cap( getParam( 'City', '' ) )
province = Cap( getParam( 'Province', '' ) )
country = Cap( getParam( 'Country', '' ) )
postalCode = getParam( 'PostalCode', '' )
phone = getParam( 'Phone', '' )
email = getParam( 'Email', '' )
member.setContact( street1, street2, apt, city, province, country, postalCode, phone, email )

#----------------------------------------------------------------------

member.resetInstruments()
re_instrumentName = re.compile( 'I_(.*)' )
for p in params:
	match = re_instrumentName.match( p )
	if match:
		member.addInstrument( match.group(1) )

otherInstrument = Cap( getParam( 'OtherInstrument', '' ) )
if otherInstrument:
	member.addInstrument( otherInstrument )

#----------------------------------------------------------------------

re_positionName = re.compile( 'P_(.*)' )
for p in params:
	match = re_positionName.match( p )
	if match:
		member.addPosition( match.group(1) )

otherPosition = Cap( getParam( 'OtherPosition', '' ) )
if otherPosition:
	member.addPosition( otherPosition )

#----------------------------------------------------------------------

private = getParam( 'KeepPrivate', '' )
if private: member.setEmailVisible( False )

#----------------------------------------------------------------------

alumni.updateMember( member, memory, memoryId )
#print member.printFullSummary()

#----------------------------------------------------------------------

MailChair( 'New registration: ' + member.fullName(), """
Greetings from the Band Alumni Registration Template System Immediately
Mailing Profile Signups Over Networks
(BART SIMPSON).

There was a new registration requiring your attention dude. Surf on over to
this link to review it:

http://www.bttbalumni.ca/#profiles

---
Robo-Mail
""" )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
