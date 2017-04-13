#!/usr/bin/env python
"""
Process the BTTB Alumni contact request and add it to the database,
marking the contact information as private and sending a confirmation email.
"""
print 'Content-type: text/html\n'

from bttbConfig import Error, MailChair
from bttbCGI import bttbCGI

class BTTBContact(bttbCGI):
    '''Class to handle parsing of the contact POST request'''

    #----------------------------------------------------------------------
    def process_contact(self):
        '''Read the contact info and send email to the info mailing address about it'''
        self.read_cgi()
        first_name = self.capitalize_first( self.get_param( 'first_name', '' ) )
        last_name = self.capitalize_first( self.get_param( 'last_name', '' ) )
        name = first_name + ' ' + last_name
        email = self.get_param( 'email', '' )

        #----------------------------------------------------------------------

        MailChair( subject='New contact request: %s' % name,
                   to='info@bttbalumni.ca',
                   text="""
Greetings from the BTTB Alumni website.

There was a new request to be added to the alumni mailing list. They have not been
added to the band database as they did not register with the website, this is strictly
for the mailing list.

    Name:  %s
    Email: %s

---
Robo-Mail
    """ % ( name, email ) )

        print """
<title>Thanks from the BTTB Alumni</title>
<h1>Thanks for keeping in touch</h1>
<p>
Your information will be verified and you will be then added to our contact
list for updates on alumni activities.
</p>
<p>
Please also check back to the website for news, trivia, memories, fun pictures,
and other cool band stuff.
</p>
<p>
Know anyone else from the band that might want to stay in touch? Help us build
our network by spreading the word!
</p>
<p>
<a href="mailto:myBandFriend?subject='BTTB Alumni'&body='The BTTB Alumni are going strong! I registered with them to stay in touch, you can too at http://www.bttbalumni.ca'">Click here to send the website to someone else!</a>
</p>
<p class='date'>
See you soon!!! - your BTTB Alumni Committee
</p>
        """

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBContact()
    PROCESSOR.process_contact()
except Exception, ex:
    Error( 'Could not process contact request', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
