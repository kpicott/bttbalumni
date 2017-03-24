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

def _sortByMemoryDate(x,y):    return cmp(x[2], y[2])
class bttbParade(bttbPage):
    def __init__(self):
        bttbPage.__init__(self)
        try:
            self.alumni = bttbAlumni()
        except Exception, e:
            Error( 'Could not find parade information', e )
    
    def title(self): return 'Sound of Music Festival Parade Alumni Band'

    def content(self):
        """
        Return a string with the content for this web page.
        """
        try:
            if not self.requestor:
                return LoginRequired( 'Parade Signup' )
        except:
            pass
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
        <form name="paradeMusicForm" id="paradeMusicForm" action="javascript:submitForm(\'paradeMusicForm\', \'/cgi-bin/bttbParadeMusic.cgi\', null);">
        """ )
        parts = self.alumni.getParadeInstrumentation('parade65')
        html += "<table><tr>"
        col = 0
        instCount = 0
        for iName,iId,iDownload,who in parts:
            instCount = instCount + 1
            if not who.find(','):
                whoSize = 0
            else:
                whoSize = len(who.split(','))
            who = re.sub('<sup>.</sup>', '', who)
            checked = ""
            if col == 4:
                html += '</tr><tr>'
                col = 0
            col = col + 1
            if iName == 'Marching Without Instrument':
                checked = ' checked'
            if iName == 'Can only ride':
                iName = "Want to participate but am unable to march. Will ride in float with band."
            html += "<td width='25%%' valign='top'><input type='radio' name='part' align='middle'%s value='%s'>%s" % (checked, iId, iName)
            html += "&nbsp;<a title='%s' href='#' onClick='Effect.toggle(\"signedUp%d" % (who, instCount)
            html += "\", \"slide\"); return false;'>"
            html += "%d so far &hellip;</a>" % whoSize
            html += "<div id='signedUp%d' style='display:none;'>" % instCount
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
