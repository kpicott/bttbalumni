#!/usr/bin/env python
"""
Process the BTTB Alumni contact request and add it to the database,
marking the contact information as private and sending a confirmation email.
"""
print 'Content-type: text/html\n'

import os
import os.path
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
    #    Look for a previous edit to overwrite
    #    Either insert or update at (negative-id).
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

email = getParam( 'Email', '' )
member.setContact( '', '', '', '', '', '', '', '', email )
member.setEmailVisible( False )

#----------------------------------------------------------------------

alumni.updateMember( member, '', -1 )

#----------------------------------------------------------------------

MailChair( 'New contact request: ' + member.fullName(), """
Greetings from the Band Alumni Registration Template System Immediately
Mailing Profile Signups Over Networks
(BART SIMPSON).

There was a new request to be added to the contact list for the alumni,
but not register with the website.

Name: """ + member.fullName() + """
Years in Band: """ + member.firstYear + " - " + member.lastYear + """
Email: """ + member.email + """

The data has also been entered into the database but the email is kept private.

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
