#!/usr/bin/env python
"""
Utility page to show various configurations of music extracted from the
database and add the music into the database if it wasn't already there.
"""
print 'Content-type: text/html\n'

import sys
sys.path.insert(0,'..')

from bttbCGI import bttbCGI
from bttbMusic import BTTBMusic
from bttbConfig import MapLinks, MusicPath, Error

class PopulateMusic(bttbCGI):
    '''Class that generates the music test page'''
    def __init__(self):
        '''Set up the page'''
        bttbCGI.__init__(self)
        self.members_only = True
        self.music = BTTBMusic()
        self.music.read_directories()

    def populate_database(self):
        '''
        Use the scanned music directory information to figure out what needs to be
        added to the various music-related database tables, then do it.

        Print out a report of the contents of the music directories and the contents
        of the database music tables.
        '''

        print MapLinks( "<link rel='stylesheet' href='__CSSPATH__/bttbEffects.css'>\n" )
        print MapLinks( "<link rel='stylesheet' href='__CSSPATH__/bttbPage.css'>\n" )

        print "<h1>Music Root - %s</h1>" % MusicPath()

        list_of_songs = {}

        print "<h2>Audio Files</h2><div class='box_shadow' style='padding: 10px;'><p><table border='1'>"
        for song_name, song_path in self.music.audio_files.iteritems():
            list_of_songs[song_name] = True
            print "<tr><th>%s</th><td>%s</td></tr>\n" % (song_name, song_path)
        print "</table></p></div>\n"

        print '<h2>Found song paths</h2><div class="box_shadow" style="padding: 10px;"><p><table border="1">\n'
        for song_name,part_list in self.music.sheet_music.iteritems():
            list_of_songs[song_name] = True
            title = '<th rowspan="%d" valign="top">%s</th>' % (len(part_list.keys()), song_name.replace(' ', '&nbsp;'))
            for part_name,music_path in part_list.iteritems():
                print '<tr>%s<td>%s</td><td>%s</td></tr>' % (title, part_name, music_path.replace(' ', '&nbsp;'))
                title = ''
        print '</table></p></div>\n'

        print '<h2>Unknown song paths</h2><div class="box_shadow" style="padding: 10px;"><p><ul>\n'
        for song_name in self.music.unknown_song_paths:
            print '<li>%s</li>' % song_name
        print '</ul></p></div>\n'

        print '<h2>Instruments In Database</h2><div class="box_shadow" style="padding: 10px;"><p><ul>\n'
        for instrument_name,instrument_id in self.music.instrument_lookup.iteritems():
            print '<li>%s : %s</li>' % (str(instrument_id), str(instrument_name))
        print '</ul></p></div>\n'

        print '<h2>Songs In Database</h2><div class="box_shadow" style="padding: 10px;"><p><ul>\n'
        for song_title,song_id in self.music.song_lookup.iteritems():
            print '<li>%s : %s</li>' % (str(song_id), str(song_title))
        print '</ul></p></div>\n'

        print '<h2>Sheet Music In Database</h2><div class="box_shadow" style="padding: 10px;"><p><table border="1">\n'
        for song_id,part_info in self.music.sheet_music_lookup.iteritems():
            print '<tr><th>%s</th><td>' % str(song_id)
            for instrument_id,file_path in part_info.iteritems():
                print '%s : %s<br>' % (str(instrument_id), str(file_path))
            print '</td></tr>'
        print '</table></p></div>\n'

        #----------------------------------------------------------------------
        # Now that we've reported on the current state of things, figure out what needs to
        # be added and report on that.

        #----------------------------------------------------------------------
        # Check the song list to see if any new songs should be added to the songs table
        print '<h2>Songs Added To Database</h2><div class="box_shadow" style="padding: 10px;"<p><ul>\n'
        for song_name in list_of_songs:
            if song_name not in self.music.song_lookup:
                self.music.add_song( song_name )
                print '<li>%s</li>' % song_name
        print '</ul></p></div>\n'

        #----------------------------------------------------------------------
        # Check the sheet music list to see if the pairs of songs/parts exist there yet
        print '<h2>Sheet Music Added To Database</h2><div class="box_shadow" style="padding: 10px;"<p><table border="1">\n'
        print '<tr><th>Song</th><th>Song ID</th><th>Instrument ID</th><th>Instrument</th><th>File</th></tr>'
        for song_name,part_list in self.music.sheet_music.iteritems():
            if song_name not in self.music.song_lookup:
                print '<tr><th colspan="5">'
                Error( 'Sheet music song not found in database', song_name )
                print '</th></tr>\n'
                continue
            song_id = self.music.song_lookup[song_name]
            for part_name,music_path in part_list.iteritems():
                print '<tr><td>%s</td>' % str(song_id)
                print '<th>%s</th>' % song_name
                if part_name not in self.music.instrument_lookup:
                    print '<th colspan="3">'
                    Error( 'Sheet music instrument not found in database', part_name )
                    print '</th>\n'
                    continue
                instrument_id = self.music.instrument_lookup[part_name]
                print '<td>%s</td><td>%s</td>' % (instrument_id, part_name)
                if song_id in self.music.db_sheet_music:
                    if instrument_id in self.music.db_sheet_music[song_id]:
                        # Already in the database
                        continue
                self.music.add_sheet_music( song_id, instrument_id, music_path )
                print '<td>%s</td>' % music_path
                print '</tr>'
        print '</table></p></div>\n'

# ==================================================================

try:
    PROCESSOR = PopulateMusic()
    PROCESSOR.populate_database()
except Exception, ex:
    Error( 'Could not process registration', ex )


# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
