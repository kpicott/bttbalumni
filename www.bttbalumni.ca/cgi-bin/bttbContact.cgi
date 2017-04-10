#!/usr/bin/env python
"""
Process the BTTB Alumni contact request and add it to the database,
marking the contact information as private and sending a confirmation email.
"""
print 'Content-type: text/html\n'

import cgi
from datetime import datetime
from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from bttbConfig import Error, AsYYYY, MailChair

#----------------------------------------------------------------------
def get_param(name,default):
    """
    Simple trick to get cgi params using default values
    """
    try:
        value = PARAMS[name][0].strip()
    except Exception:
        value = default
    return value

#----------------------------------------------------------------------
def get_int_param(name,default):
    """
    Simple trick to get numeric cgi params using default values
    """
    try:
        value = int( PARAMS[name][0] )
    except Exception:
        value = default
    return value

#----------------------------------------------------------------------
def capitalize_first(name):
    """
    Returns a capitalized string, but without changing inner characters
    (the "capitalize()" method messes up "McTavish" to "Mctavish"
    """
    if len(name) < 2:
        return name.capitalize()
    return name[0].upper() + name[1:]

#----------------------------------------------------------------------
def process_contact():
    '''Read the contact info and add or modify it in the database'''
    try:
        alumni = bttbAlumni()
        changed_dat = datetime.now()
        #
        # If the id was negative then this is an edit:
        #    Look for a previous edit to overwrite
        #    Either insert or update at (negative-id).
        #
        # Otherwise it's a creation, and requires a new id
        #
        unique_id = get_int_param('id', alumni.get_unique_id())
        if unique_id <= 0:
            member = alumni.getMemberFromId(-unique_id)
        else:
            while alumni.getMemberFromId(unique_id):
                unique_id = unique_id + 1
            member = bttbMember()
            member.setJoinTime( datetime.now() )
            member.setId( unique_id )
    except Exception, ex:
        Error( 'Registration processing error', ex )

    member.setEditTime( changed_dat )

    #----------------------------------------------------------------------

    first_name = capitalize_first( get_param( 'FirstName', '' ) )
    last_name = capitalize_first( get_param( 'CurrentLastName', '' ) )
    nee = capitalize_first( get_param( 'LastNameInBand', '' ) )
    member.setName( first_name, nee, last_name )

    #----------------------------------------------------------------------

    first_year = AsYYYY( get_param( 'FirstYear', '' ) )
    last_year = AsYYYY( get_param( 'LastYear', '' ) )
    member.setYears( first_year, last_year )

    #----------------------------------------------------------------------

    email = get_param( 'Email', '' )
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

The data has also been entered into the database but is kept private.

---
Robo-Mail
    """ )

try:
    PARAMS = cgi.parse()
    process_contact()
    print "OK"
except Exception, ex:
    Error( 'Could not process contact', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
