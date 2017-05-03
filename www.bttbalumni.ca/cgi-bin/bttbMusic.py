# -*- coding: iso-8859-15 -*-
"""
Utilities for handling the available music - find it on disk, populating the database
with any new music, managing the relationship between music and events, and providing
lists of information for pages wanting to make downloads available.
"""
import re
import os.path
import bttbDB
from bttbConfig import MusicPath, Error

__all__ = ['BTTBMusic']

# Recognized audio file extensions
AUDIO_EXTENSIONS = ['.mp3', '.wav']

# Set of expressions to pull part names out of song file names. Each pair consists of
# the expression to match and the instrument part name it matches.
PART_EXPRESSIONS = [
    ( re.compile('Alto.*Sax.*1',        flags=re.IGNORECASE), 'Alto Sax 1' )
,   ( re.compile('Alto.*Sax.*2',        flags=re.IGNORECASE), 'Alto Sax 2' )
,   ( re.compile('Alto.*Sax',           flags=re.IGNORECASE), 'Alto Sax 1' )
,   ( re.compile('Tenor.*Sax.*1',       flags=re.IGNORECASE), 'Tenor Sax 1' )
,   ( re.compile('Tenor.*Sax.*2',       flags=re.IGNORECASE), 'Tenor Sax 2' )
,   ( re.compile('Tenor.*Sax',          flags=re.IGNORECASE), 'Tenor Sax 1' )
,   ( re.compile('Bari.* Sax',          flags=re.IGNORECASE), 'Baritone Sax' )
,   ( re.compile('Flute.*1',            flags=re.IGNORECASE), 'Flute 1' )
,   ( re.compile('Flute.*2',            flags=re.IGNORECASE), 'Flute 2' )
,   ( re.compile('Flute',               flags=re.IGNORECASE), 'Flute 1' )
,   ( re.compile('Piccolo',             flags=re.IGNORECASE), 'Piccolo' )
,   ( re.compile('Tromb.*1',            flags=re.IGNORECASE), 'Trombone 1' )
,   ( re.compile('Tromb.*2',            flags=re.IGNORECASE), 'Trombone 2' )
,   ( re.compile('Tromb.*3',            flags=re.IGNORECASE), 'Trombone 3' )
,   ( re.compile('Tromb.*4',            flags=re.IGNORECASE), 'Trombone 4' )
,   ( re.compile('Bass.*Tromb',         flags=re.IGNORECASE), 'Bass Trombone' )
,   ( re.compile('Tromb',               flags=re.IGNORECASE), 'Trombone' )
,   ( re.compile('Euph.*T',             flags=re.IGNORECASE), 'Baritone/Euphonium Treble Clef' )
,   ( re.compile('Euph.*B',             flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile('Euph',                flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile('Bari.*T.*C',          flags=re.IGNORECASE), 'Baritone/Euphonium Treble Clef' )
,   ( re.compile('Bari.*B.*C',          flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile('Bari',                flags=re.IGNORECASE), 'Baritone/Euphonium Bass Clef' )
,   ( re.compile('Tuba',                flags=re.IGNORECASE), 'Tuba/Sousaphone' )
,   ( re.compile('Sousa',               flags=re.IGNORECASE), 'Tuba/Sousaphone' )
,   ( re.compile('Trump.*1',            flags=re.IGNORECASE), 'Trumpet 1' )
,   ( re.compile('Trump.*2',            flags=re.IGNORECASE), 'Trumpet 2' )
,   ( re.compile('Trump.*3',            flags=re.IGNORECASE), 'Trumpet 3' )
,   ( re.compile('Trump.*4',            flags=re.IGNORECASE), 'Trumpet 4' )
,   ( re.compile('Solo.*Trump',         flags=re.IGNORECASE), 'Solo Trumpet' )
,   ( re.compile('Trump',               flags=re.IGNORECASE), 'Trumpet 1' )
,   ( re.compile(r'F\s*Horn.*1',        flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'F\s*Horn.*2',        flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'F\s*Horn.*3',        flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'F\s*Horn',           flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'French.*Horn.*1',    flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile(r'French.*\s*Horn.*2', flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile(r'French.*\s*Horn.*3', flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile(r'French.*\s*Horn',    flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile('Mellop.*1',           flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile('Mellop.*2',           flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile('Mellop.*3',           flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile('Mellop',              flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile('Horn.*F.*1',          flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile('Horn.*F.*2',          flags=re.IGNORECASE), 'F Horn 2' )
,   ( re.compile('Horn.*F.*3',          flags=re.IGNORECASE), 'F Horn 3' )
,   ( re.compile('Horn.*F.*4',          flags=re.IGNORECASE), 'F Horn 4' )
,   ( re.compile('Horn.*F',             flags=re.IGNORECASE), 'F Horn 1' )
,   ( re.compile('Oboe',                flags=re.IGNORECASE), 'Oboe' )
,   ( re.compile('Bassoon',             flags=re.IGNORECASE), 'Bassoon' )
,   ( re.compile('Clar.*1',             flags=re.IGNORECASE), 'Clarinet 1' )
,   ( re.compile('Clar.*2',             flags=re.IGNORECASE), 'Clarinet 2' )
,   ( re.compile('Clar.*3',             flags=re.IGNORECASE), 'Clarinet 3' )
,   ( re.compile('Clar.*4',             flags=re.IGNORECASE), 'Clarinet 4' )
,   ( re.compile('Bass.*Clar',          flags=re.IGNORECASE), 'Bass Clarinet' )
,   ( re.compile('Clar.*E',             flags=re.IGNORECASE), 'Clarinet in Eb' )
,   ( re.compile('Clar.*',              flags=re.IGNORECASE), 'Clarinet 1' )
,   ( re.compile('Snare.*1',            flags=re.IGNORECASE), 'Snare' )
,   ( re.compile('Snare.*2',            flags=re.IGNORECASE), 'Snare 2' )
,   ( re.compile('Snare',               flags=re.IGNORECASE), 'Snare' )
,   ( re.compile('Cymbals',             flags=re.IGNORECASE), 'Cymbals' )
,   ( re.compile('Bass.*D.*1',          flags=re.IGNORECASE), 'Bass Drum' )
,   ( re.compile('Bass.*D.*2',          flags=re.IGNORECASE), 'Bass Drum 2' )
,   ( re.compile('Bass.*D',             flags=re.IGNORECASE), 'Bass Drum' )
,   ( re.compile('Bells',               flags=re.IGNORECASE), 'Bells' )
,   ( re.compile('Glock',               flags=re.IGNORECASE), 'Bells' )
,   ( re.compile('Drum.*Set',           flags=re.IGNORECASE), 'Percussion' )
,   ( re.compile('Timp',                flags=re.IGNORECASE), 'Timpani' )
,   ( re.compile('Drums',               flags=re.IGNORECASE), 'Percussion' )
,   ( re.compile('Conductor',           flags=re.IGNORECASE), 'Conductor' )
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
        try:
            for (instrument_name,instrument_id) in self.db_instruments:
                self.instrument_lookup[instrument_name] = instrument_id
            #
            for (song_title,song_id) in self.db_songs:
                self.song_lookup[song_title] = song_id
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
                            self.sheet_music[song_name][part_found] = os.path.join( root, music_file )

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
