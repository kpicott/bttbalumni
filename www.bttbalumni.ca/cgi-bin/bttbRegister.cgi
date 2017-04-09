#!/usr/bin/env python
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
from bttbConfig import Error

def get_param(name,default):
	"""
	Simple trick to get cgi params using default values
	"""
	try:
		value = params[name][0].strip()
	except:
		value = default
	return value

def get_int_param(name,default):
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
	uniqueId = get_int_param('id', os.getpid())
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

firstName = Cap( get_param( 'FirstName', '' ) )
lastName = Cap( get_param( 'CurrentLastName', '' ) )
nee = Cap( get_param( 'LastNameInBand', '' ) )
member.setName( firstName, nee, lastName )

#----------------------------------------------------------------------

firstYear = AsYYYY( get_param( 'FirstYear', '' ) )
lastYear = AsYYYY( get_param( 'LastYear', '' ) )
member.setYears( firstYear, lastYear )

#----------------------------------------------------------------------

rank = Cap( get_param( 'HighestRank', '' ) )
member.setRank( rank )

#----------------------------------------------------------------------

password = get_param( 'Password', '' )
member.setPassword( password )

#----------------------------------------------------------------------

memory = get_param( 'SpecialTime', '' ).strip()
memoryId = get_int_param( 'SpecialTimeId', -1 )

#----------------------------------------------------------------------

street1 = Cap( get_param( 'Street1', '' ) )
street2 = Cap( get_param( 'Street2', '' ) )
apt = get_param( 'Apt', '' )
city = Cap( get_param( 'City', '' ) )
province = Cap( get_param( 'Province', '' ) )
country = Cap( get_param( 'Country', '' ) )
postalCode = get_param( 'PostalCode', '' )
phone = get_param( 'Phone', '' )
email = get_param( 'Email', '' )
member.setContact( street1, street2, apt, city, province, country, postalCode, phone, email )

#----------------------------------------------------------------------

member.resetInstruments()
re_instrumentName = re.compile( 'I_(.*)' )
for p in params:
	match = re_instrumentName.match( p )
	if match:
		member.addInstrument( match.group(1) )

otherInstrument = Cap( get_param( 'OtherInstrument', '' ) )
if otherInstrument:
	member.addInstrument( otherInstrument )

#----------------------------------------------------------------------

re_positionName = re.compile( 'P_(.*)' )
for p in params:
	match = re_positionName.match( p )
	if match:
		member.addPosition( match.group(1) )

otherPosition = Cap( get_param( 'OtherPosition', '' ) )
if otherPosition:
	member.addPosition( otherPosition )

#----------------------------------------------------------------------

private = get_param( 'KeepPrivate', '' )
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
