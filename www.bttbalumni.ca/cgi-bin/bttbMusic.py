# -*- coding: iso-8859-15 -*-
"""
Utilities for handling the available music - find it on disk, populating the database
with any new music, managing the relationship between music and events, and providing
lists of information for pages wanting to make downloads available.
"""
import re
import os.path
import bttbDB
from bttbConfig import MusicPath, Error, MusicURL

__all__ = ['BTTBMusic']

# Recognized audio file extensions
AUDIO_EXTENSIONS = ['.mp3', '.wav']

# Set of expressions to pull part names out of song file names. Each pair consists of
# the expression to match and the instrument part name it matches.
PART_EXPRESSIONS = [
    ( re.compile(r'-.*Alto.*Sax.*1',        flags=re.IGNORECASE), 'Alto Sax 1' )
,   ( re.compile(r'-.*Alto.*Sax.*2',        flags=re.IGNORECASE), 'Alto Sax 2' )
,   ( re.compile(r'-.*1.*Alto.*Sax',        flags=re.IGNORECASE), 'Alto Sax 1' )
,   ( re.compile(r'-.*2.*Alto.*Sax',        flags=re.IGNORECASE), 'Alto Sax 2' )
,   ( re.compile(r'-.*Alto.*Sax',           flags=re.IGNORECASE), 'Alto Sax 1' )
,   ( re.compile(r'-.*Tenor.*Sax.*1',       flags=re.IGNORECASE), 'Tenor Sax 1' )
,   ( re.compile(r'-.*Tenor.*Sax.*2',       flags=re.IGNORECASE), 'Tenor Sax 2' )
,   ( re.compile(r'-.*Tenor.*Sax',          flags=re.IGNORECASE), 'Tenor Sax 1' )
,   ( re.compile(r'-.*Bari.* Sax',          flags=re.IGNORECASE), 'Baritone Sax' )
,   ( re.compile(r'-.*Flute.*1',            flags=re.IGNORECASE), 'Flute 1' )
,   ( re.compile(r'-.*Flute.*2',            flags=re.IGNORECASE), 'Flute 2' )
,   ( re.compile(r'-.*Flute',               flags=re.IGNORECASE), 'Flute 1' )
,   ( re.compile(r'-.*Piccolo',             flags=re.IGNORECASE), 'Piccolo' )
,   ( re.compile(r'-.*Tromb.*1',            flags=re.IGNORECASE), 'Trombone 1' )
,   ( re.compile(r'-.*Tromb.*2',            flags=re.IGNORECASE), 'Trombone 2' )
,   ( re.compile(r'-.*Tromb.*3',            flags=re.IGNORECASE), 'Trombone 3' )
,   ( re.compile(r'-.*Tromb.*4',            flags=re.IGNORECASE), 'Trombone 4' )
,   ( re.compile(r'-.*1.*Tromb',            flags=re.IGNORECASE), 'Trombone 1' )
,   ( re.compile(r'-.*2.*Tromb',            flags=re.IGNORECASE), 'Trombone 2' )
,   ( re.compile(r'-.*3.*Tromb',            flags=re.IGNORECASE), 'Trombone 3' )
,   ( re.compile(r'-.*4.*Tromb',            flags=re.IGNORECASE), 'Trombone 4' )
,   ( re.compile(r'-.*Bass.*Tromb',         flags=re.IGNORECASE), 'Bass Trombone' )
,   ( re.compile(r'-.*Tromb',               flags=re.IGNORECASE), 'Trombone' )
,   ( re.compile(r'-.*Euph.*T',             flags=re.IGNORECASE), 'Baritone/Euphonium Treble Clef' )
,   ( re.compile(r'-.*Euph.*B',             flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile(r'-.*Euph',                flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile(r'-.*Bari.*T.*C',          flags=re.IGNORECASE), 'Baritone/Euphonium Treble Clef' )
,   ( re.compile(r'-.*Bari.*B.*C',          flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile(r'-.*Bari',                flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile(r'-.*Tuba',                flags=re.IGNORECASE), 'Tuba/Sousaphone' )
,   ( re.compile(r'-.*Sousa',               flags=re.IGNORECASE), 'Tuba/Sousaphone' )
,   ( re.compile(r'-.*Trump.*1',            flags=re.IGNORECASE), 'Trumpet 1' )
,   ( re.compile(r'-.*Trump.*2',            flags=re.IGNORECASE), 'Trumpet 2' )
,   ( re.compile(r'-.*Trump.*3',            flags=re.IGNORECASE), 'Trumpet 3' )
,   ( re.compile(r'-.*Trump.*4',            flags=re.IGNORECASE), 'Trumpet 4' )
,   ( re.compile(r'-.*1.*Trump',            flags=re.IGNORECASE), 'Trumpet 1' )
,   ( re.compile(r'-.*2.*Trump',            flags=re.IGNORECASE), 'Trumpet 2' )
,   ( re.compile(r'-.*3.*Trump',            flags=re.IGNORECASE), 'Trumpet 3' )
,   ( re.compile(r'-.*4.*Trump',            flags=re.IGNORECASE), 'Trumpet 4' )
,   ( re.compile(r'-.*Solo.*Trump',         flags=re.IGNORECASE), 'Solo Trumpet' )
,   ( re.compile(r'-.*Trump',               flags=re.IGNORECASE), 'Trumpet 1' )
,   ( re.compile(r'-.*F\s*Horn.*1',        flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*F\s*Horn.*2',        flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'-.*F\s*Horn.*3',        flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'-.*1.*F.*Horn',         flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*2.*F.*Horn',         flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'-.*3.*F.*Horn',         flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'-.*F\s*Horn',           flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*French.*Horn.*1',    flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*French.*\s*Horn.*2', flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'-.*French.*\s*Horn.*3', flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'-.*French.*\s*Horn',    flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*Horn.*1',            flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*Horn.*2',            flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'-.*Horn.*3',            flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'-.*Horn',               flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*Mellop.*1',           flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*Mellop.*2',           flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'-.*Mellop.*3',           flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'-.*Mellop',              flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*Horn.*F.*1',          flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*Horn.*F.*2',          flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'-.*Horn.*F.*3',          flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'-.*Horn.*F.*4',          flags=re.IGNORECASE), 'F Horn 4' )
,   ( re.compile(r'-.*Horn.*F',             flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'-.*Oboe',                flags=re.IGNORECASE), 'Oboe' )
,   ( re.compile(r'-.*Bassoon',             flags=re.IGNORECASE), 'Bassoon' )
,   ( re.compile(r'-.*Clar.*1',             flags=re.IGNORECASE), 'Clarinet 1' )
,   ( re.compile(r'-.*Clar.*2',             flags=re.IGNORECASE), 'Clarinet 2' )
,   ( re.compile(r'-.*Clar.*3',             flags=re.IGNORECASE), 'Clarinet 3' )
,   ( re.compile(r'-.*Clar.*4',             flags=re.IGNORECASE), 'Clarinet 4' )
,   ( re.compile(r'-.*1.*Clar',             flags=re.IGNORECASE), 'Clarinet 1' )
,   ( re.compile(r'-.*2.*Clar',             flags=re.IGNORECASE), 'Clarinet 2' )
,   ( re.compile(r'-.*3.*Clar',             flags=re.IGNORECASE), 'Clarinet 3' )
,   ( re.compile(r'-.*4.*Clar',             flags=re.IGNORECASE), 'Clarinet 4' )
,   ( re.compile(r'-.*Bass.*Clar',          flags=re.IGNORECASE), 'Bass Clarinet' )
,   ( re.compile(r'-.*Clar.*E',             flags=re.IGNORECASE), 'Clarinet in Eb' )
,   ( re.compile(r'-.*Alto.*Clar',          flags=re.IGNORECASE), 'Clarinet in Eb' )
,   ( re.compile(r'-.*Clar.*',              flags=re.IGNORECASE), 'Clarinet 1' )
,   ( re.compile(r'-.*Snare.*1',            flags=re.IGNORECASE), 'Snare' )
,   ( re.compile(r'-.*Snare.*2',            flags=re.IGNORECASE), 'Snare 2' )
,   ( re.compile(r'-.*Snare',               flags=re.IGNORECASE), 'Snare' )
,   ( re.compile(r'-.*Cymb',                flags=re.IGNORECASE), 'Cymbals' )
,   ( re.compile(r'-.*Bass.*D.*1',          flags=re.IGNORECASE), 'Bass Drum' )
,   ( re.compile(r'-.*Bass.*D.*2',          flags=re.IGNORECASE), 'Bass Drum 2' )
,   ( re.compile(r'-.*Bass.*D',             flags=re.IGNORECASE), 'Bass Drum' )
,   ( re.compile(r'-.*Bells',               flags=re.IGNORECASE), 'Bells' )
,   ( re.compile(r'-.*Glock',               flags=re.IGNORECASE), 'Bells' )
,   ( re.compile(r'-.*Drum.*Set',           flags=re.IGNORECASE), 'Percussion' )
,   ( re.compile(r'-.*Timp',                flags=re.IGNORECASE), 'Timpani' )
,   ( re.compile(r'-.*Quad',                flags=re.IGNORECASE), 'Quads/Quints' )
,   ( re.compile(r'-.*Quint',               flags=re.IGNORECASE), 'Quads/Quints' )
,   ( re.compile(r'-.*Triple',              flags=re.IGNORECASE), 'Quads/Quints' )
,   ( re.compile(r'-.*Drums',               flags=re.IGNORECASE), 'Percussion' )
,   ( re.compile(r'-.*Percussion',          flags=re.IGNORECASE), 'Percussion' )
,   ( re.compile(r'-.*Conductor',           flags=re.IGNORECASE), 'Conductor' )
    ]

class BTTBMusic(object):
    '''Manage the database of available music and sheet music'''
    def __init__(self):
        ''' Initialize the database for music queries '''
        self.database = bttbDB.bttbDB()
        self.database.Initialize()
        self.db_instruments = self.database.get_instruments()
        self.db_songs = self.database.get_songs()
        self.db_sheet_music = self.database.get_sheet_music()

        # Create a reverse lookup for the music information so that they
        # can be easily found by name rather than ID
        self.instrument_lookup = {}
        self.song_lookup = {}
        self.sheet_music_lookup = {}
        self.instruments = {}
        self.songs = {}
        try:
            for (instrument_name,instrument_id) in self.db_instruments:
                self.instrument_lookup[instrument_name] = instrument_id
                self.instruments[instrument_id] = instrument_name
            #
            for (song_title,song_id) in self.db_songs:
                self.song_lookup[song_title] = song_id
                self.songs[song_id] = song_title
            #
            for (song_id, instrument_id, file_path) in self.db_sheet_music:
                self.sheet_music_lookup[song_id] = self.sheet_music_lookup.get(song_id, {})
                self.sheet_music_lookup[song_id][instrument_id] = file_path
        except Exception, ex:
            Error( "Could not initialize music data", ex )

        # Mapping of song names to their audio files
        self.audio_files = {}

        # Song file names that could not be recognized
        self.unknown_song_paths = []

        # Dictionary of sheet music or audio files
        self.sheet_music = {}

    #----------------------------------------------------------------------
    def __del__(self):
        '''Finish interactions with the database'''
        self.database.Finalize()

    #----------------------------------------------------------------------
    def add_song(self, song_name):
        '''
        Add a song name to the database.
        :param song_name: Name of song to be added
        '''
        self.database.process_query( "INSERT INTO songs (title) VALUES ('%s');" % song_name )

    #----------------------------------------------------------------------
    def add_sheet_music(self, song_id, instrument_id, music_path):
        '''
        Add a piece of sheet music to the database.
        If it was already in the database then just return the existing database ID.
        :param song_id: ID of the song for this music
        :param instrument_id: ID of the instrument for this part
        :param music_path: File path of the music (or audio file)
        '''
        self.database.process_query( """INSERT INTO sheet_music (song_id, instrument_id, file)
            VALUES (%d, %d, '%s');""" % (int(song_id), int(instrument_id), music_path) )

    #----------------------------------------------------------------------
    def get_playlist(self, event_id):
        '''
        :param event_id: ID of event in the "events" table of the database
        :return: List of (song ID, song name) attached to the event
        '''
        playlist = []
        all_songs = []
        for song_id in self.database.get_playlist_for_event(event_id):
            all_songs.append( song_id[0] )
        for song_id,song_title in self.songs.iteritems():
            if song_id in all_songs:
                playlist.append( [song_id, song_title] )
        return playlist

    #----------------------------------------------------------------------
    def read_directories(self):
        '''
        Read the music data in from the website directories.
        The following members will be populated:
            audio_files{}        : Key   = Song name
                                   Value = Audio file locations
            unknown_song_paths[] : List of song paths found but not understood
            songs{}              : Key = Song name
                                   Value = Dictionary of part name to file location for that part in this song
        '''
        # Walk the directory structure to find sheet music files. The directory
        # structure must look like this:
        #
        #  Music/
        #       Song/
        #           Part.pdf
        #
        # Song.mp3 can appear in any location and will be associated with Song/
        #
        # Part.pdf can have any recognizable format. If any song files are not
        # recognized they will be added to an error report visible to committee
        # members only.
        #
        try:
            for root, _, files in os.walk( MusicPath() ):
                for music_file in files:
                    (base_name, extension) = os.path.splitext( music_file )
                    if extension in AUDIO_EXTENSIONS:
                        self.audio_files[base_name] = os.path.join( root, music_file )
                    elif extension == '.pdf':
                        song_name = os.path.split( root )[1]
                        part_found = None
                        for (part_regex, part_name) in PART_EXPRESSIONS:
                            if part_regex.search(base_name):
                                part_found = part_name
                                break
                        if part_found is None:
                            self.unknown_song_paths.append( music_file )
                        else:
                            self.sheet_music[song_name] = self.sheet_music.get(song_name, {})
                            music_url = re.sub( MusicPath(), MusicURL(), os.path.join( root, music_file ) )
                            self.sheet_music[song_name][part_found] = music_url

        except Exception, ex:
            Error( 'Failed to read music directories', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
