"""
Page that shows a bunch of music clips for download.
"""

from bttbPage import bttbPage
from bttbConfig import MapLinks
__all__ = ['bttbTunes']

class bttbTunes(bttbPage):
    '''Class that generates the music clip page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Music Clips'

    def content(self):
        ''':return: a string with the content for this web page.'''
        audio = [
              ('ConcertVariations.mp3', 'Concert Variations')
            , ('FieldShow1982.mp3', 'Field show music - 1982 version')
            , ('FieldShowExit1982.mp3', 'Field show drum beat exit')
            , ('ManciniSpectacular.mp3', 'Mancini Spectacular')
            , ('MarchSpiritoso.mp3', 'March Spiritoso')
            , ('StarsAndStripes.mp3', 'The Stars and Stripes Forever')
            , ('WashingtonPost.mp3', 'Washington Post')
            , ('TheHustle.mp3', 'The Hustle')
            , ('StrikeUpTheBand.mp3', 'Strike Up The Band')
            , ('TheThunderer.mp3', 'The Thunderer')
            , ('Superman.mp3', 'Theme from "Superman"')
            , ('ExitStreetBeat.mp3', 'Triple Beat')
            ]
        html = MapLinks( """
        <h1>Music Clips</h1>
        <p>
        We have a bunch of music clips of the band you might enjoy.
        If you have any you'd like to share send them to us at
        send:(info@bttbalumni.ca).
        </p>
        <table cellspacing='10'><tr>
        """ )
        column = 0
        for audio_file, description in audio:
            if column == 4:
                html += '</tr><tr>'
                column = 0
            column = column + 1
            html += MapLinks( """
            <th>
            <a href="__AUDIOPATH__/%s"><img src='__IMAGEPATH__/musicClip.png' width='100' height='125' border='0'><br>%s</a>
            </th>
            """ % (audio_file, description))
        html += "</tr></table>"
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbTunes()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
