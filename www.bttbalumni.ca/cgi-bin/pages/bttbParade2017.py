"""
Page that shows the current list of parade participants and lets the currently
signed in user sign up for a specific instrument.
"""

import re
from bttbAlumni import bttbAlumni
from bttbMember import bttbMember
from bttbPage import bttbPage
from bttbConfig import MapLinks, Error
__all__ = ['bttbParade']

class bttbParade(bttbPage):
    '''Class that generates the parade information page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find parade information', ex )

    def title(self):
        ''':return: The page title'''
        return '2017 Sound of Music Festival Parade Alumni Band'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks( """
        <h1>Parade Music</h1>
        <p>
        Below is a list of the instrumentation available for the parade
        (including those who wish to march without an instrument).
        Select a part and you will be pointed to a download of the music
        for that part in PDF format (see link:(http://www.adobe.com) for
        a PDF File Reader called Acrobat if you don't already have it).
        </p>
        <p>
        Click on the "SO FAR" text to reveal the names of those who have
        downloaded that particular part.
        </p>
        <form name="paradeMusicForm" id="paradeMusicForm" action="javascript:submit_form(\'/cgi-bin/bttbParadeMusic.cgi\', \'paradeMusicForm\', null);">
        """ )
        parts = self.alumni.getParadeInstrumentation('parade2017')
        html += "<table><tr>"
        col = 0
        instrument_count = 0
        for instrument_name,instrument_id,_,who in parts:
            instrument_count = instrument_count + 1
            if not who.find(','):
                who_size = 0
            else:
                who_size = len(who.split(','))
            who = re.sub('<sup>.</sup>', '', who)
            checked = ""
            if col == 4:
                html += '</tr><tr>'
                col = 0
            col = col + 1
            if instrument_name == 'Marching Without Instrument':
                checked = ' checked'
            if instrument_name == 'Can only ride':
                instrument_name = "Want to participate but am unable to march. Will ride in float with band."
            html += "<td width='25%%' valign='top'><input type='radio' name='part' align='middle'%s value='%s'>%s" % (checked, instrument_id, instrument_name)
            html += "&nbsp;<a title='%s' href='#' onClick='Effect.toggle(\"signedUp%d" % (who, instrument_count)
            html += "\", \"slide\"); return false;'>"
            html += "%d so far &hellip;</a>" % who_size
            html += "<div id='signedUp%d' style='display:none;'>" % instrument_count
            html += "<div style='background-color:#ffa0a0;"
            html += "border:2px solid red;padding:10px;'>"
            html += who
            html += "</div></div>"
        html += "</tr></table>\n"
        html += MapLinks( """
        <table border='1'><tr><td valign='center'>
        <input type='hidden' name='id' value='%d'>
        <input type='checkbox' align='middle' name='needsInstrument' value='1'>&nbsp;Check here if you
        need an instrument. We have some available, but can't guarantee
        anything at this point.<br>To ensure an instrument
        link:(http://www.longandmcquade.com/, Long and McQuade in Burlington)
        has a rental program the alumni can take advantage of.
        </p>
        </td></tr></table>
        <br>
        <input type='submit' name='submit' value='Reserve My Spot'>
        </form>
        """) % self.requestor.id
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbParade()
    TEST_PAGE.requestor = bttbMember()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
