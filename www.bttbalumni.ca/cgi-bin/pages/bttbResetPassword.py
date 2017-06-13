# -*- coding: iso-8859-15 -*-
"""
Page that guides the user through the process for resetting their password.
"""

from datetime import datetime,timedelta
from bttbAlumni import bttbAlumni
from pages.bttbPage import bttbPage
from bttbConfig import MapLinks, Error, ErrorMsg, MailChair
__all__ = ['bttbResetPassword']

#----------------------------------------------------------------------
class bttbResetPassword(bttbPage):
    '''Class that generates the password reset confirmation page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find alumni information', ex )

    #----------------------------------------------------------------------
    @staticmethod
    def reject_request(why):
        '''Disallow the password reset with an explanatory message'''
        return MapLinks( '''<h1><font color='red'>Password Reset Failed</font></h1>
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
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Password Reset Confirmation'

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''

        if 'id' not in self.params:
            return ErrorMsg( 'No alumni ID for the reset confirmation', '' )

        alumni_id = int(self.param('id'))
        if alumni_id < 0:
            return self.reject_request( 'Alumni ID not recognized' )

        results,_ = self.alumni.process_query( '''SELECT reset_requested,user_id
                                                  FROM alumni
                                                  WHERE id = %d''' % alumni_id )

        if results is None or len(results) == 0:
            return self.reject_request( 'No match for the alumni' )

        if results[0] is None or len(results[0]) == 0 or results[0][0] is None:
            return self.reject_request( 'No reset was requested' )

        user_id = results[0][1]
        reset_request_date = results[0][0]

        now = datetime.now()

        if now - timedelta(7) > reset_request_date:
            return self.reject_request( 'Password reset expired, please request a new one.' )

        MailChair( subject='BTTB Alumni Password Reset Request',
                   to='web@bttbalumni.ca',
                   text='''
A password reset request has been processed for ID=%d, USER=%s.
                           ''' % (alumni_id, user_id) )

        self.alumni.process_query( '''UPDATE alumni
                                      SET password='bttb'
                                      WHERE id = %d''' % alumni_id )
        return MapLinks( '''<h1>Request Complete</h1>
<p>
Your password has been set to the default "bttb".
</p>
<p>
Your user ID is "%s".
</p>
<p>
Please log in now and set your own passwword.
</p><p>
If you still have trouble logging in send email to
send:(web@bttbalumni.ca) with a description of your
problem.
</p>''' % user_id )

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbResetPassword()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
