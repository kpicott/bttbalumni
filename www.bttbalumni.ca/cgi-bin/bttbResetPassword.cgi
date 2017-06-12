#!/usr/bin/env python
"""
Process a request to reset a password.

The specified ID must have the 'reset_requested' field
set to a time no more than a week old. Otherwise it will
be rejected and the user will be told to request a new reset.
"""
print 'Content-type: text/html\n'

from datetime import datetime
from bttbAlumni import bttbAlumni
from bttbConfig import Error, MapLinks, MailChair
from bttbCGI import bttbCGI

class BTTBResetPassword(bttbCGI):
    '''Class to handle parsing of the password reset message POST request'''

    #----------------------------------------------------------------------
    def reject_request(self, why):
        '''Disallow the password reset with an explanatory message'''
        print MapLinks( '''<h1><font color='red'>Password Reset Failed</font></h1>
        <p>
        <i>%s</i>
        </p>
        <p>
        These links may help you resolve your problem:
        <ul>
        <li>link:(/#forgot,Request a new password reset)</li>
        <li>link:(/#home,Visit the home page and try to log in again)</li>
        <li>send:(web@bttbalumni.ca,Contact the webmaster directly)</li>
        </ul>
        </p>''' % why )

    #----------------------------------------------------------------------
    def process_query(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()

        alumni = bttbAlumni()
        alumni_id = self.get_int_param('alumni_id', -1)
        if alumni_id < 0:
            self.reject_request( 'Alumni ID not recognized' )
        else:
            results,_ = alumni.process_query( '''SELECT reset_requested
                                                 FROM alumni
                                                 WHERE id = %d''' % alumni_id )
            if results is None or len(results) == 0:
                self.reject_request( 'No match for the alumni' )
            elif results[0] is None or len(results[0]) == 0:
                self.reject_request( 'No reset was requested' )
            else:
                now = datetime.now()
                then = datetime.strptime(results[0], "%Y-%m-%d %H:%M:%S") 
                if now - timedelta(7) > then:
                    self.reject_request( 'Password reset expired, please request a new one.' )
                else:
                print MapLinks( '''<h1>Request Complete</h1>
                <p>
                Your password has been set to the default "bttb". Please
                log in now and change this to your own password.
                </p><p>
                If you still have trouble logging in send email to
                send:(web@bttbalumni.ca) with a description of your
                problem.
                </p>''' )

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBResetPassword()
    PROCESSOR.process_query()
except Exception, ex:
    Error( 'Could not reset password', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================

