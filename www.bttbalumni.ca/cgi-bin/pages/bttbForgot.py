# -*- coding: iso-8859-15 -*-
"""
Page that guides the user through the process for resetting their password.
"""

from bttbAlumni import bttbAlumni
from pages.bttbPage import bttbPage
from bttbConfig import MapLinks, Error
__all__ = ['bttbForgot']

# Default dropdown value
DEFAULT_CONTACT="<option id='default-contact' value='-1'>-- Select Your Contact --</option>"

# Maximum number of matches returned by bttbFindMatches.cgi
MATCH_MAX=20

#----------------------------------------------------------------------
def page_js():
    ''':return: A string with the Javascript specific to this page'''
    return r"""<script>
    $(document).ready(function() {
        $("#pattern").bind( "change paste keyup", function() {
            find_matches();
        });
    });

    //
    // Method called when the form to set an instrument is submitted.
    // Use the POST method to avoid exposing any information in the submission.
    // Updates the button and status information based on the returned value.
    //
    var last_match = "";
    function find_matches()
    {
        var form_url = '/cgi-bin/bttbFindMatches.cgi';
        var return_value = 0;

        // Use last_match to prevent multiple executions with the same pattern
        if( last_match === $('#pattern').val() )
        {
            return;
        }
        last_match = $('#pattern').val();

        $.ajax( {
            type    :   "POST",
            url     :   form_url,
            data    :   $('#reset_form').serialize(),
            success :   function(data)
                        {
                            // Look for the previously matched value. If it's still on the
                            // list then select it again, otherwise select the default. (The
                            // ordering is by last name but selection is by ID so there's no
                            // easy way to tell which one is next or previous.)
                            var new_match = -1;
                            var last_id = $('#alumni_id').val();

                            // If an error was returned then don't change anything
                            if( data.substring(0,3) !== "ERR" )
                            {
                                var matches = data.match(/[^\r\n]+/g);
                                var match_count = 0;
                                if( matches !== null )
                                {
                                    match_count = matches.length;
                                }
                                var html = "%s";
                                var i;
                                var actual_matches = 0;
                                for( i=0; i<match_count; i++ )
                                {
                                    var this_match = matches[i];
                                    var fields = this_match.split( '\t' )
                                    if( fields.len < 5 )
                                    {
                                        continue;
                                    }
                                    var first = fields[0];
                                    var nee   = fields[1];
                                    var last  = fields[2];
                                    var id    = fields[3];
                                    var email = fields[4];
                                    if( (email === null) || (email.length === 0) )
                                    {
                                        continue;
                                    }
                                    html += "<option value='" + id + "'>";
                                    if( id === last_id )
                                    {
                                        new_match = last_id;
                                    }
                                    html += first;
                                    if( nee.length > 0 )
                                    {
                                        html += " (" + nee + ")";
                                    }
                                    html += " " + last;
                                    html += " - " + email;
                                    html += "</option>\\n";
                                    actual_matches += 1;
                                }
                                $('#alumni_id').html( html );
                                $('#alumni_id').attr( 'value', new_match );

                                var default_option = "-- Select From " + actual_matches;
                                if( actual_matches === %d )
                                {
                                    default_option += " (or more)";
                                }
                                var plural = "es";
                                if( actual_matches === 1 )
                                {
                                    plural = "";
                                }
                                default_option += " Match" + plural + " --";
                                $('#default-contact').html( default_option );
                            }
                        },
            error   :   function(data)
                        {
                            alert( "Warning, could not check for pattern matches. Try again later." );
                        }
        } );
    }
</script>""" % (DEFAULT_CONTACT, MATCH_MAX)

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

        html = page_js()
        html += MapLinks("""
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
<form method='POST' name='reset_form' id='reset_form'
      action="javascript:submit_form('/cgi-bin/bttbSendReset.cgi', '#reset_form', null);">
<input type='text' placeholder='Name or User ID or Email' id='pattern' name='pattern' size=64/>
<select class='dropdown' name='alumni_id' id='alumni_id'>
%s
<input type='submit' name='submit' value='Request Reset'>
</div>
        """ % DEFAULT_CONTACT )

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
