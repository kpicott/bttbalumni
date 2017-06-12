"""
Page that guides the user through the process for resetting their password.
"""

from bttbAlumni import bttbAlumni
from pages.bttbPage import bttbPage
from bttbConfig import MapLinks, Error
__all__ = ['bttbForgot']

#----------------------------------------------------------------------
def page_js():
    ''':return: A string with the Javascript specific to this page'''
    return """<script>
    $(document).ready(function() {
        $("#pattern").bind( "change paste keyup", function() {
            alert( $(this).val() );
        });
    });

    //
    // Method called when the form to set an instrument is submitted.
    // Use the POST method to avoid exposing any information in the submission.
    // Updates the button and status information based on the returned value.
    //
    function find_matches()
    {
        var form_url = '/cgi-bin/bttbFindMatches.cgi';
        var return_value = 0;
        $.ajax( {
            type    :   "POST",
            url     :   form_url,
            data    :   $('#parade_form').serialize(),
            success :   function(data)
                        {
                            // 0 = Not signed up, not registered
                            if( data[0] === "0" )
                            {
                                $('#parade-status').attr( 'class', 'status-not' );
                                $('#parade-status').html( 'No Part Chosen' );
                                $('#parade-action').attr( 'value', 'Choose Part' );
                                $('#position-query').html( '-- Select Parade Part --' );
                            }
                            // 1 = Signed up, not registered
                            else if( data[0] === "1" )
                            {
                                $('#parade-status').attr( "class", "status-unpaid" );
                                $('#parade-status').html( "%s" );
                                $('#parade-action').attr( "value", "Change Instrument" );
                                $('#position-query').html( '-- Not Going To Play --' );
                            }
                            // 2 = Not signed up, registered
                            else if( data[0] === "2" )
                            {
                                $('#parade-status').attr( 'class', 'status-unpaid' );
                                $('#parade-status').html( 'Registered, Choose Part' );
                                $('#parade-action').attr( 'value', 'Choose Part' );
                                $('#position-query').html( '-- Select Parade Part --' );
                            }
                            // 3 = Signed up, registered
                            else if( data[0] === "3" )
                            {
                                $('#parade-status').attr( "class", "status-in" );
                                $('#parade-status').html( "Fully Signed Up" );
                                $('#parade-action').attr( "value", "Change Instrument" );
                                $('#position-query').html( '-- Not Going To Play --' );
                            }
                            else
                            {
                                $('#parade-status').attr( "class", "status-err" );
                                $('#parade-status').html( "ERR " + data + ": Try Again" );
                            }
                            if( $('#instrument option:selected').text() === 'Will Ride The Float' )
                            {
                                alert( "Please email info@bttbalumni.ca for more information regarding riding the float.");
                            }
                        },
            error   :   function(data)
                        {
                            $('#parade-status').attr( "class", "status-err" );
                            $('#parade-status').html( "ERR " + data + ": Try Again" );
                        }
        } );
    }
</script>""" % PAY_MESSAGE

#----------------------------------------------------------------------
class bttbForgot(bttbPage):
    '''Class that generates the password reset page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find alumni information', ex )

    #----------------------------------------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Password Reset'

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''

        html = MapLinks("""
<h1>Forgot your login?</h1>
<p>
Enter some or all of your name, user ID, or email address to
get a list of matches. The dropdown list will be populated with
any matches. When you find yours then select it and hit the
"Request Reset" button. It will send an email to the matching
address with a link to reset your password.
</p>
<p>
If you are unable to find your name but you are sure that you have
registered then send mail to send:(web@bttbalumni) with your name
(including your name while in band, if different). (If you specified
to hide your information in your profile your name will not appear here.)
</p>
<div class='box-shadow'>
<form method='POST' name='reset_form' id='reset_form' action='javascript:find_matches();'>
<input type='text' placeholder='Name or User ID or Email' id='pattern' name='pattern' size=64/>
<select class='dropdown' name='matches' id='matches'>
<div id='match-list'>
<option value='-1'>-- Select Your Contact --</option>
</div>
<input type='submit' name='submit' value='Request Reset'>
</div>
        """ )

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbForgot()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
