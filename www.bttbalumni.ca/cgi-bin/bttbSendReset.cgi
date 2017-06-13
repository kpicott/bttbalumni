#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Process a request to send a password reset link.
The specified ID will have the 'reset_requested' field
set to the current timestamp in the database and get a
password reset link emailed (linking to a script that
will take the ID and reset the password if there is a
reset_requested value that is less than a week old).
"""
print 'Content-type: text/html\n'

from datetime import datetime
from bttbAlumni import bttbAlumni
from bttbConfig import Error, MapLinks, MailChair
from bttbCGI import bttbCGI

class BTTBSendReset(bttbCGI):
    '''Class to handle parsing of the password reset message POST request'''

    #----------------------------------------------------------------------
    def process_query(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()

        alumni = bttbAlumni()
        alumni_id = self.get_int_param('alumni_id', -1)
        if alumni_id < 0:
            Error( 'Reset request not recognized', '' )
        else:
            results,_ = alumni.process_query( '''SELECT email
                                                 FROM alumni
                                                 WHERE id = %d''' % alumni_id )
            if results is None or len(results) == 0:
                Error( 'Reset request not recognized', '' )
            elif results[0] is None or len(results[0]) == 0:
                Error( 'No email associated with your ID', '' )
            else:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                alumni.process_query( '''UPDATE alumni
                                         SET reset_requested='%s'
                                         WHERE id = %d''' % (now, alumni_id) )
                MailChair( subject='BTTB Alumni Password Reset Request',
                           to='%s' % results[0],
                           text='''
Your password reset request has been received. If you did not request
a password reset please ignore this email.

Click on this link to reset your password to the default password "bttb".
Once you have reset your password, log in immediately to set a new password.

http://bttbalumni.ca/?id=%d#resetPassword
                           ''' % alumni_id )
                print MapLinks( '''<h1>Request Sent</h1>
                <p>
                Please check your email for a link that will reset your
                password. Be sure to also check your spam folder, just in
                case. The link is only valid for one week.
                </p><p>
                If you do not receive a link send email to
                send:(web@bttbalumni.ca) to reset manually.
                </p>''' )

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBSendReset()
    PROCESSOR.process_query()
except Exception, ex:
    Error( 'Could not send reset request', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================

