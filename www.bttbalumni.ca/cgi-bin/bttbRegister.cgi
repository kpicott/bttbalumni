#!/usr/bin/env python
"""
Process the BTTB Alumni registration information and add it to the database,
sending a confirmation email if an email address was specified.
"""

print 'Content-type: text/html\n'

import re
from datetime import datetime
from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from bttbCGI import bttbCGI
from bttbConfig import Error, AsYYYY, MailChair

class BTTBRegister(bttbCGI):
    '''Class to handle parsing of the registration POST request'''

    #----------------------------------------------------------------------
    def process_registration(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()
        try:
            alumni = bttbAlumni()
            changed_at = datetime.now()
            #
            # If the id was negative then this is an edit:
            #    Look for a previous edit to overwrite
            #    Either insert or update at (negative-id).
            #
            # Otherwise it's a creation, and requires a new id
            #
            unique_id = self.get_int_param('id', alumni.get_unique_id())
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

        member.setEditTime( changed_at )

        #----------------------------------------------------------------------

        first_name = self.capitalize_first( self.get_param( 'FirstName', '' ) )
        last_name = self.capitalize_first( self.get_param( 'CurrentLastName', '' ) )
        nee = self.capitalize_first( self.get_param( 'LastNameInBand', '' ) )
        member.setName( first_name, nee, last_name )

        #----------------------------------------------------------------------

        first_year = AsYYYY( self.get_param( 'FirstYear', '' ) )
        last_year = AsYYYY( self.get_param( 'LastYear', '' ) )
        member.setYears( first_year, last_year )

        #----------------------------------------------------------------------

        rank = self.capitalize_first( self.get_param( 'HighestRank', '' ) )
        member.setRank( rank )

        #----------------------------------------------------------------------

        password = self.get_param( 'Password', '' )
        member.setPassword( password )

        #----------------------------------------------------------------------

        memory = self.get_param( 'SpecialTime', '' ).strip()
        memory_id = self.get_int_param( 'SpecialTimeId', -1 )

        #----------------------------------------------------------------------

        street1 = self.capitalize_first( self.get_param( 'Street1', '' ) )
        street2 = self.capitalize_first( self.get_param( 'Street2', '' ) )
        apt = self.get_param( 'Apt', '' )
        city = self.capitalize_first( self.get_param( 'City', '' ) )
        province = self.capitalize_first( self.get_param( 'Province', '' ) )
        country = self.capitalize_first( self.get_param( 'Country', '' ) )
        postal_code = self.get_param( 'PostalCode', '' )
        phone = self.get_param( 'Phone', '' )
        email = self.get_param( 'Email', '' )
        member.setContact( street1, street2, apt, city, province, country, postal_code, phone, email )

        #----------------------------------------------------------------------

        member.resetInstruments()
        re_instrument_name = re.compile( 'I_(.*)' )
        for param in self.params:
            match = re_instrument_name.match( param )
            if match:
                member.addInstrument( match.group(1) )

        other_instrument = self.capitalize_first( self.get_param( 'OtherInstrument', '' ) )
        if other_instrument:
            member.addInstrument( other_instrument )

        #----------------------------------------------------------------------

        re_position_name = re.compile( 'P_(.*)' )
        for param in self.params:
            match = re_position_name.match( param )
            if match:
                member.addPosition( match.group(1) )

        other_position = self.capitalize_first( self.get_param( 'OtherPosition', '' ) )
        if other_position:
            member.addPosition( other_position )

        #----------------------------------------------------------------------

        private = self.get_param( 'KeepPrivate', '' )
        if private:
            member.setEmailVisible( False )

        #----------------------------------------------------------------------

        alumni.update_member( member, memory, memory_id )
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

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBRegister()
    PROCESSOR.process_registration()
    print "OK"
except Exception, ex:
    Error( 'Could not process registration', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
