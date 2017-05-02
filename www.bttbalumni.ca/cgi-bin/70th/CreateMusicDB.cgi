#!/usr/bin/env python
"""
Create the tables associated with sheet music parts.

This only gets run once, for initializing the database. It was mainly created because there
is no easy way to create foreign keys in the web interface to the BTTB alumni database.
"""
import sys
sys.path.insert(0,'..')

import bttbDB
from bttbConfig import ErrorsInHtml

print 'Content-type: text/html\n'

class CreateMusicDB(object):
    """
    Class to manage creation of the database tables used by sheet music parts.
    """
    def __init__(self):
        """
        Create all of the initial tables and populate with known data.
        """
        self.database = bttbDB.bttbDB()
        self.database.Initialize()
        self.database.turn_debug_on()
        self.table_info = []
        self.type_map = {}
        self.define_tables()

        #------------------------------------------------------
        # drop existing tables first, in reverse order to avoid
        # foreign key dependency problems.
        #------------------------------------------------------
        reversed_list = self.table_info.keys()
        reversed_list.reverse()
        for table in reversed_list:
            self.execute( 'DROP TABLE IF EXISTS %s' % table )
            self.execute('COMMIT')

        #------------------------------------------------------
        # create each table in order, assuming the order
        # correctly addresses foreign key propagation
        #------------------------------------------------------
        for table in self.table_info.keys():
            print 'Creating %s...<br>' % table
            print '<pre>%s</pre>' % self.table_create_sql(table)
            # self.execute( self.table_create_sql(table) )
            # self.execute('COMMIT')

        # self.database.Archive()
        self.database.Finalize()

    #----------------------------------------------------------------------
    def execute(self,cmd):
        """Run a database SQL command"""
        self.database.execute( cmd )

    #----------------------------------------------------------------------
    def table_create_sql(self, table):
        """
        Construct the table creation query from existing information and
        return it for execution.
        """
        sql = 'CREATE TABLE IF NOT EXISTS %s (' % table
        for name, (fields, key_info, description) in self.table_info.iteritems():
            if name != table:
                continue
            for field_name, field_type, field_restrict, field_default, field_comment in fields:
                if field_default:
                    if field_type.find('INT') >= 0 or field_default == 'NULL':
                        sql += "%s %s %s DEFAULT %s COMMENT '%s',\n" % (field_name, field_type, field_restrict, field_default, field_comment)
                    else:
                        sql += "%s %s %s DEFAULT '%s' COMMENT '%s',\n" % (field_name, field_type, field_restrict, field_default, field_comment)
                else:
                    sql += "%s %s %s COMMENT '%s',\n" % (field_name, field_type, field_restrict, field_comment)
                self.type_map['%s-%s' % (table,field_name)] = field_type
            sql += """
                %s
                )
                Engine=InnoDB
                DEFAULT
                CHARSET=utf8
                COMMENT='%s';""" % (key_info, description)
        return sql

    #----------------------------------------------------------------------
    def define_tables(self):
        """
        Create a dictionary of all of the table creation SQL
        """
        #
        # Table information is a layered structure:
        #  {TABLENAME :
        #        ( (FIELD, TYPE, RESTRICTIONS, DEFAULT, COMMENT)+),
        #        KEYINFO,
        #        TABLEDESCRIPTION)

        #------------------------------------------------------
        # music TABLE definition
        #------------------------------------------------------
        self.table_info = {
        'sheet_music' : (
        (
          ('instrument_id', 'INT(10) UNSIGNED', '',         '0',                   'Part for this file'),
          ('song_id',       'INT(10) UNSIGNED', '',         '0',                   'Song for this file'),
          ('file',          'VARCHAR(128)',     '',         'NULL',                'File location, relative to the Music/ root')
        ), """
          PRIMARY KEY  (id),

          FOREIGN KEY (instrument_id) REFERENCES instruments(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE,

          FOREIGN KEY (song_id) REFERENCES songs(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
            """, 'Sheet Music files available for download'),

        #------------------------------------------------------
        # songs TABLE definition
        #------------------------------------------------------
        'songs' : (
        (
          ('title',  'VARCHAR(128)',     '',                      'NULL',  'Song title'),
          ('id',     'INT(10) UNSIGNED', 'NOT NULL AUTO_INCREMENT', None,  'Unique song ID')
          ), """
          PRIMARY KEY  (id),
            """, 'Songs for which sheet music is available'),

        #------------------------------------------------------
        # playlists TABLE definition
        #------------------------------------------------------
        'playlists' : (
        (
          ('song_id',   'INT(10) UNSIGNED', '',         '0',                   'Song on the playlist'),
          ('event_id',  'INT(10) UNSIGNED', '',         '0',                   'Event to which the playlist belongs')
          ), """
          PRIMARY KEY  (id),

          FOREIGN KEY (event_id) REFERENCES events(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE,

          FOREIGN KEY (song_id) REFERENCES songs(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
            """, 'Songs attached to specific events')
        }

#----------------------------------------------------------------------

try:
    if __name__ == '__main__':
        ErrorsInHtml( True )
        NEW_TABLES = CreateMusicDB()
except Exception, ex:
    print 'ERROR: %s' % str(ex)

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
