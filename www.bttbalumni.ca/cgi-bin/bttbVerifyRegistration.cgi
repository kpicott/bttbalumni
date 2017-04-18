#!/usr/bin/env python
"""
Check the BTTB Alumni registration information to see if it can be safely
added to the database. This line will be at the end of the returned data.
If it's by itself then all went well.

    OK

Otherwise it will be preceded by one line per error/warning indicating
what the problem was and which fields must be changed in order to fix the problem

    ERROR|WARNING: field1,field2,...fieldN: Message
e.g.
    ERROR: email: That email is already in use
    WARNING: first,nee,last: That name already has a profile associated with it, are you sure this is new?
"""

print 'Content-type: text/plain\n'

import re
from datetime import datetime
from bttbAlumni import bttbAlumni
from bttbCGI import bttbCGI

# Official email parsing, stolen from http://emailregex.com/
RE_EMAIL = re.compile( r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" )

class BTTBVerifyRegistration(bttbCGI):
    '''Class to handle parsing of the registration POST request'''
    ALUMNI = bttbAlumni()

    #----------------------------------------------------------------------
    @staticmethod
    def error(fields, message):
        '''Print out an error line'''
        print 'ERROR: %s: %s' % (','.join(fields), message)

    #----------------------------------------------------------------------
    @staticmethod
    def warning(fields, message):
        '''Print out a warning line'''
        print 'WARNING: %s: %s' % (','.join(fields), message)

    #----------------------------------------------------------------------
    def validate_names(self, first_name, last_name, nee, alumni_id):
        '''Validate the name fields'''
        if len(first_name) == 0:
            self.error( ['FirstName'], "First name must be present" )
        elif len(last_name) == 0:
            self.error( ['CurrentLastName'], "Last name must be present" )
        else:
            results,_ = BTTBVerifyRegistration.ALUMNI.process_query( '''
            SELECT first,nee,last
                FROM alumni
                WHERE first like "%s"
                    AND last like "%s"
                    AND nee like "%s"
                    AND id <> %d
            ''' % (first_name.replace('"', '\\"'), last_name.replace('"', '\\"'), nee.replace('"', '\\"'), alumni_id) )

            if len(results) > 0:
                self.warning( ['FirstName','CurrentLastName','LastNameInBand'], "A similar name is already registered." )

    #----------------------------------------------------------------------
    def validate_email(self, email, alumni_id):
        '''Validate the email field'''
        if len(email) > 0 and not RE_EMAIL.match(email):
            self.error( ['Email'], "Email is not valid" )
        else:
            results,_ = BTTBVerifyRegistration.ALUMNI.process_query( '''
            SELECT email
                FROM alumni
                WHERE email like '%s'
                    AND id <> %d
            ''' % (email, alumni_id) )

            if len(results) > 0:
                self.error( ['Email'], "That email is already in use." )

    #----------------------------------------------------------------------
    def validate_years(self, first_year, last_year):
        '''Validate the years'''
        this_year = datetime.now().year
        if first_year < 1947 or first_year > this_year:
            self.error( ['FirstYear'], "Year joining band must be between 1947 and now (estimate is okay)" )
        if last_year < 1947 or last_year > this_year:
            self.error( ['LastYear'], "Final year in band must be between 1947 and now (estimate is okay)" )

    #----------------------------------------------------------------------
    def verify_registration(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()
        try:
            first_name = self.capitalize_first( self.get_param( 'FirstName', '' ) ).rstrip()
            last_name = self.capitalize_first( self.get_param( 'CurrentLastName', '' ) ).rstrip()
            nee = self.capitalize_first( self.get_param( 'LastNameInBand', '' ) ).rstrip()
            # Negative IDs indicate edits; flip to get the real ID
            alumni_id = - self.get_int_param( 'id', 1 )
            self.validate_names( first_name, last_name, nee, alumni_id )

            email = self.get_param( 'Email', '' ).rstrip()
            self.validate_email( email, alumni_id )

            first_year = self.get_int_param( 'FirstYear', 0 )
            last_year = self.get_int_param( 'LastYear', 0 )
            self.validate_years( first_year, last_year )

        except Exception, ex:
            print 'ERROR: : Could not verify registration - %s' % str(ex)

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBVerifyRegistration()
    PROCESSOR.verify_registration()
    print 'OK'
except Exception, ex:
    print 'ERROR: : Could not verify registration - %s' % str(ex)

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
