"""
Page that shows the alumni reunion concert information
"""

from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from bttbPage import bttbPage
from bttbConfig import MapLinks, Error
__all__ = ['bttbConcert']

class bttbConcert(bttbPage):
    '''Class that generates the concert information page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find concert information', ex )

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Reunion Concert'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks("""
        <div class='outlinedTitle'>Re-Union Concert 3:00 pm - Sunday June 17<sup>th</sup>, 2007</div>
        <p>
        Below is a list of the instrumentation available for the concert.
        Select the parts you wish to download in PDF format
        (see link:(http://www.adobe.com) for
        a PDF File Reader called Acrobat if you do not already have it).
        </p>
        <p>
        Click on the "SO FAR" text to reveal the names of those who have
        downloaded that particular part.
        </p>
        <form name="concertMusicForm" id="concertMusicForm" action="javascript:submit_form(\'/cgi-bin/bttbConcertMusic.cgi\', \'concertMusicForm\', null);">
        """ )
        parts = self.alumni.getConcertInstrumentation('concert_2017')
        html += "<table><tr>"
        col = 0
        instrument_count = 0
        for instrument_name,instrument_id,who in parts:
            instrument_count = instrument_count + 1
            if who.find(',') < 0:
                if len(who) > 0:
                    who_size = 1
                else:
                    who_size = 0
            else:
                who_size = len(who.split(','))
            checked = ""
            if col == 4:
                html += '</tr><tr>'
                col = 0
            col = col + 1
            html += "<td width='25%%' valign='top'><input type='radio' name='part' align='middle'%s value='%s'>%s" % (checked, instrument_id, instrument_name)
            if who_size > 0:
                html += "&nbsp;<a title='%s' href='#' onClick='Effect.toggle(\"signedUp%d" % (who, instrument_count)
                html += "\", \"slide\"); return false;'>"
                html += " (%d so far) &hellip;</a>" % who_size
            else:
                html += " (None yet)"
            html += "<div id='signedUp%d' style='display:none;'>" % instrument_count
            html += "<div style='background-color:#ffa0a0;"
            html += "border:2px solid red;padding:10px;'>"
            html += who
            html += "</div></div>"
        html += "</tr></table>\n"
        html += MapLinks( """
        <table border='1'><tr><td valign='center'>
        <input type='hidden' name='id' value='%d'>
        We'll have percussion available, and keep in mind only one person can
        play the set. <br>To ensure you have any other instrument you need
        link:(http://www.longandmcquade.com/pdf/lmbandrentbrochure0607-insideON-FINAL.pdf, Long and McQuade in Burlington)
        is offering a rental program the alumni can take advantage of.
        </p>
        </td></tr></table>
        <br>
        <input type='submit' name='submit' value='Reserve My Spot'>
        </form>
        """) % self.requestor.id
        html += MapLinks( """
<p>
Still to come - download of remaining music. Watch for the announcement on
link:(#home, the home page!).
</p>
<p>
Rehearsal opportunities are 7pm-8:30pm Friday May 25<sup>th</sup> and Friday
June 1<sup>st</sup> at the Music Centre. <i>Rehearsals should be followed with
a time of social interaction at a suitable venue.</i>
</p>
<p>
There will be only one combined rehearsal with the current Teen Tour members
at 10:00am on Sunday June 17<sup>th</sup>.
</p>
<h1>Full Concert Lineup</h1>
<div class='indented'>
    <li>Royal Salute</li>
    <li>O Canada</li>
    <li>Strike Up the Band!</li>
    <li>Beatles Medley</li>
    <li>Bugler's Holiday (Trumpet Feature)</li>
    <li>Junior Redcoats</li>
    <li>Cordoba</li>
    <li>Final Countdown</li>
    <li>Czardas</li>
    <li>Queen in Concert</li>
    <li>Yakety Sax (Sax feature)</li>
    <li>Pirates of the Caribbean</li>
    <li>Drum Feature</li>
    <li>Spanish Fever</li>
    <li>2007 Field Show</li>
    <li><b>FINALE</b><ol>
    Never Walk Alone<br>Pride of Burlington</ol></li>
</div>
        """)
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbConcert()
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
