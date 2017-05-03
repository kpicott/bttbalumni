"""
Run a test page to show various configurations of music extracted from the database.
"""
from pages.bttbPage import bttbPage
from bttbMusic import BTTBMusic
from bttbConfig import MapLinks, MusicPath

__all__ = ['bttbTestMusic']

class bttbTestMusic(bttbPage):
    '''Class that generates the music test page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        self.music = BTTBMusic()
        self.music.read_directories()

    def title(self):
        ''':return: The page title'''
        return 'BTTB Music Test Page'

    def content(self):
        ''':return: a string with the content for this web page.'''

        html = "<h1>%s</h1>" % MusicPath()
        html += MapLinks( "<table border='1'>" )

        for song_name, song_path in self.music.audio_files.iteritems():
            html += "<tr><th>%s</th><td>%s</td></tr>\n" % (song_name, song_path)

        html += "</table>\n"

        html += '<h2>Found song paths</h2><table border="1">\n'
        for song_name,part_list in self.music.songs.iteritems():
            html += '<tr><th>%s</th><td>%s</td></tr>' % (song_name, ','.join(part_list.keys()))
        html += '</table>\n'

        html += '<h2>Unknown song paths</h2><ul>\n'
        for song_name in self.music.unknown_song_paths:
            html += '<li>%s</li>' % song_name
        html += '</ul>\n'

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbTestMusic()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
