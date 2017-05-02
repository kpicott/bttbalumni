#!env python
"""
Populate the entire BTTB alumni database from a backup.
Wipes everything out, rebuilds the tables, and dumps the data.
"""

import bttbDB
from bttbConfig import *
from bttbAlumni_XML import bttbAlumni

class PopulateAlumniDB:
    def __init__(self):
        """
        Create all of the initial tables and populate with known data.
        """
        self.__alumDir = DataPath()
        self.__db = bttbDB.bttbDB()
        self.__db.Initialize()
        self.__db.TurnDebugOn()
        self.__tableInfo = []
        self.__typeMap = {}
        self.defineTables()
        #------------------------------------------------------
        # drop existing tables first, in reverse order to avoid
        # foreign key dependency problems.
        #------------------------------------------------------
        revList = TableList()
        revList.reverse()
        for table in revList:
            self.execute( 'DROP TABLE IF EXISTS %s' % table )
            self.execute('COMMIT')
        #------------------------------------------------------
        # create each table in order, assuming the order
        # correctly addresses foreign key propagation
        #------------------------------------------------------
        for table in TableList():
            self.execute( self.tableCreateSQL(table) )
            self.execute('COMMIT')
        #------------------------------------------------------
        # Populate the tables with the information in the archive
        #------------------------------------------------------
        for table in TableList():
            self.populateTable( table )
            self.execute('COMMIT')
        self.__db.Archive()
        self.__db.Finalize()

    def execute(self,cmd):
        self.__db.execute( cmd )

    def stage(self, what):
        return self.__db.stage( what )

    def tableCreateSQL(self, table):
        """
        Construct the table creation query from existing information and
        return it for execution.
        """
        sql = 'CREATE TABLE IF NOT EXISTS %s (' % table
        for name, fields, keyInfo, description in self.__tableInfo:
            if name != table:
                continue
            for fName, fType, fRestrict, fDefault, fComment in fields:
                if fDefault:
                    if fType.find('INT') >= 0 or fDefault == 'NULL':
                        sql += "%s %s %s DEFAULT %s COMMENT '%s',\n" % (fName, fType, fRestrict, fDefault, fComment)
                    else:
                        sql += "%s %s %s DEFAULT '%s' COMMENT '%s',\n" % (fName, fType, fRestrict, fDefault, fComment)
                else:
                    sql += "%s %s %s COMMENT '%s',\n" % (fName, fType, fRestrict, fComment)
                self.__typeMap['%s-%s' % (table,fName)] = fType
            sql += """
                %s
                )
                Engine=InnoDB
                DEFAULT
                CHARSET=utf8
                COMMENT='%s';""" % (keyInfo, description)
        return sql

    def defineTables(self):
        """
        Create a dictionary of all of the table creation SQL
        """
        #
        # Table information is a layered structure:
        #  (TABLENAME,
        #        ( (FIELD, TYPE, RESTRICTIONS, DEFAULT, COMMENT)+),
        #        KEYINFO,
        #        TABLEDESCRIPTION)
        #

        #------------------------------------------------------
        # events TABLE
        #------------------------------------------------------
        self.__tableInfo = (
        ('60thevents', (
          ('id',           'INT(10) UNSIGNED', 'NOT NULL', None,  'Unique id'),
          ('summary',      'VARCHAR(30)',      'NOT NULL', None,  'Event title'),
          ('description',  'TEXT',             'NOT NULL', None,  'Full event description'),
          ('canVolunteer', 'TINYINT(1)',       'NOT NULL', '0', 'Event needs volunteers'),
          ('canAttend',    'TINYINT(1)',       'NOT NULL', '0', 'Event can be attended'),
          ('eventDate',    'DATETIME',         'NOT NULL', '2007-01-01 00:00:00', 'Day of event'),
          ('location',     'VARCHAR(30)',      'NOT NULL', '', 'Where the event takes place')
          ), 'PRIMARY KEY(id)', 'List of event ids and descriptions' ),

        #------------------------------------------------------
        # alumni TABLE
        #------------------------------------------------------
        ('alumni', (
          ('first',          'VARCHAR(40)',      'NOT NULL', '',     'Given name'),
          ('nee',            'VARCHAR(40)',      '',         '',     'Maiden name'),
          ('last',           'VARCHAR(40)',      'NOT NULL', '',     'Family name'),
          ('firstYear',      'INT(10) UNSIGNED', 'NOT NULL', '2006', 'First year in the band'),
          ('lastYear',       'INT(10) UNSIGNED', 'NOT NULL', '2006', 'Last year in the band'),
          ('email',          'VARCHAR(128)',     '',         'NULL', 'Email address'),
          ('make_public',    'TINYINT(1)',       'NOT NULL', '1',    'Make visible to other alumni?'),
          ('isFriend',       'TINYINT(1)',       'NOT NULL', '0',    'Is this a friend of the band, not an alumni?'),
          ('street1',        'VARCHAR(45)',      '',         'NULL', 'First line of address'),
          ('street2',        'VARCHAR(45)',      '',         'NULL', 'Second line of address'),
          ('apt',            'VARCHAR(20)',      '',         'NULL', 'Apartment number, if any'),
          ('city',           'VARCHAR(45)',      '',         'NULL', 'Home City'),
          ('province',       'VARCHAR(20)',      '',         'NULL', 'Home Province/State'),
          ('country',        'VARCHAR(25)',      '',         'NULL', 'Home Country'),
          ('postalCode',     'VARCHAR(15)',      '',         'NULL', 'Home Postal Code/Zipcode'),
          ('phone',          'VARCHAR(19)',      '',         'NULL', 'Home Phone'),
          ('id',             'INT(10) UNSIGNED', 'NOT NULL', '0',    'Unique Alumni ID'),
          ('joinTime',       'DATETIME',         'NOT NULL', '2007-01-01 00:00:00', 'When this alumni joined'),
          ('editTime',       'DATETIME',         'NOT NULL', '2007-01-01 00:00:00', 'Time of last edit of this information'),
          ('instruments',    'TEXT',             '',         None,   'Instruments this alumni has played'),
          ('positions',      'TEXT',             '',         None,   'Positions this alumni has held'),
          ('approved',       'TINYINT(1)',       'NOT NULL', '0',    'Approved by committee to be added?'),
          ('onCommittee',    'TINYINT(1)',       'NOT NULL', '0',    'Is this a committee member?'),
          ('rank',           'VARCHAR(40)',      'NOT NULL', '',     'Highest rank achieved by alumni'),
          ('password',       'VARCHAR(10)',      '',         'NULL', 'User login password')
          ), 'PRIMARY KEY  (id)', 'People and their profile information'),

        #------------------------------------------------------
        # memories TABLE
        #------------------------------------------------------
        ('memories', 
        (
          ('alumni_id',  'INT(10) UNSIGNED', '',         '0',                   'Alumni submitting the memory'),
          ('memory',     'TEXT',             'NOT NULL', None,                  'Memory text'),
          ('memoryTime', 'DATETIME',         'NOT NULL', '2007-01-01 00:00:00', 'Estimated time memory occurred'),
            ('id',         'INT(10) UNSIGNED', 'NOT NULL AUTO_INCREMENT', None,   'Unique memory ID'),
          ('submitTime', 'DATETIME',         'NOT NULL', '2007-01-01 00:00:00', 'When was memory submitted?'),
          ('removed',    'TINYINT(1)',       'NOT NULL', '0',                   'Was memory deleted?')
          ), """
          PRIMARY KEY  (id),
          FOREIGN KEY (alumni_id) REFERENCES alumni(id)
              ON DELETE SET NULL
            ON UPDATE CASCADE
            """, 'List of special memories from band days'),

        #------------------------------------------------------
        # volunteers TABLE
        #------------------------------------------------------
        ('volunteers', 
        (
          ('event_id',  'INT(10) UNSIGNED', 'NOT NULL', '0', 'Event volunteering for'),
          ('alumni_id', 'INT(10) UNSIGNED', 'NOT NULL', '0', 'Who is volunteering')
          ), """
          PRIMARY KEY  (event_id, alumni_id),

          FOREIGN KEY (alumni_id) REFERENCES alumni(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE,

          FOREIGN KEY (event_id) REFERENCES 60thevents(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
            """, 'Helpers for the 60thevents'),

        #------------------------------------------------------
        # attendance TABLE
        #------------------------------------------------------
        ('attendance',
        (
          ('event_id',  'INT(10) UNSIGNED', 'NOT NULL', '0', 'Event attending'),
          ('alumni_id', 'INT(10) UNSIGNED', 'NOT NULL', '0', 'Who is attending the event')
          ), """
          PRIMARY KEY  (event_id, alumni_id),

          FOREIGN KEY (alumni_id) REFERENCES alumni(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE,

          FOREIGN KEY (event_id) REFERENCES 60thevents(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
        """, 'Participants in the 60thevents'),

        #------------------------------------------------------
        # pages TABLE
        #------------------------------------------------------
        ('pages',
        (
          ('name',       'VARCHAR(255)',     'NOT NULL', None, 'Name of page visited'),
            ('alumni_id',  'INT(10) UNSIGNED', 'NOT NULL', None, 'Alumni who visited'),
          ('accessTime', 'DATETIME',         'NOT NULL', '2007-01-01 00:00:00', 'Time of visit'),
          ('id',         'INT(10) UNSIGNED', 'NOT NULL AUTO_INCREMENT', None, 'Unique id')
        ), 'PRIMARY KEY(id)', 'List of page hits'),

        #------------------------------------------------------
        # instruments TABLE
        #------------------------------------------------------
        ('instruments', 
        (
          ('id',               'INT(10) UNSIGNED', 'NOT NULL AUTO_INCREMENT', None, 'Unique id'),
          ('instrument',       'VARCHAR(30)',      'NOT NULL', None,  'Instrument name'),
          ('isInParade',       'TINYINT(1)',       'NOT NULL', '0',   'Is part available for parade?'),
          ('hasParadeMusic',   'TINYINT(1)',       'NOT NULL', '0',   'Does part have parade music?'),
          ('isInConcert',      'TINYINT(1)',       'NOT NULL', '0',   'Is part available for concert?'),
          ('hasConcertMusic',  'TINYINT(1)',       'NOT NULL', '0',   'Does part have concert music?')
          ), 'PRIMARY KEY(id)', 'List of parade and concert instrumentation'),

        #------------------------------------------------------
        # parade TABLE
        #------------------------------------------------------
        ('parade',
        (
            ('alumni_id',       'INT(10) UNSIGNED', 'NOT NULL', None,  'Alumni in the parade'),
          ('approved',        'TINYINT(1)',       'NOT NULL', '0',   'Is participation approved?'),
          ('needs_instrument','TINYINT(1)',       'NOT NULL', '0',   'Do they need an instrument?'),
            ('instrument_id',   'INT(10) UNSIGNED', 'NOT NULL', None,  'What are they playing?')
          ), """
          PRIMARY KEY(alumni_id),

          FOREIGN KEY (alumni_id) REFERENCES alumni(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE,

          FOREIGN KEY (instrument_id) REFERENCES instruments(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
            """, 'Parade participants and their part'),

        #------------------------------------------------------
        # parade65 TABLE
        #------------------------------------------------------
        ('parade65',
        (
            ('alumni_id',       'INT(10) UNSIGNED', 'NOT NULL', None,  'Alumni in the parade'),
          ('approved',        'TINYINT(1)',       'NOT NULL', '0',   'Is participation approved?'),
          ('needs_instrument','TINYINT(1)',       'NOT NULL', '0',   'Do they need an instrument?'),
            ('instrument_id',   'INT(10) UNSIGNED', 'NOT NULL', None,  'What are they playing?')
          ), """
          PRIMARY KEY(alumni_id),

          FOREIGN KEY (alumni_id) REFERENCES alumni(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE,

          FOREIGN KEY (instrument_id) REFERENCES instruments(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
            """, 'Parade participants for the 65th anniversary and their part'),

        #------------------------------------------------------
        # wallace TABLE
        #------------------------------------------------------
        ('wallace',
        (
          ('id',           'INT(10) UNSIGNED', 'NOT NULL AUTO_INCREMENT', None, 'Unique id'),
          ('who',          'VARCHAR(30)',      'NOT NULL', None, 'Who won it'),
          ('whoDisplay',   'VARCHAR(30)',      'NOT NULL', None, 'How their name will be displayed'),
          ('description',  'TEXT',             'NOT NULL', None, 'What did they win it for'),
          ('year',         'INT(10) UNSIGNED', 'NOT NULL', None, 'Year it was won'),
          ('submitTime',   'DATETIME',         'NOT NULL', '2007-01-01 00:00:00', 'When it was submitted')
          ), 'PRIMARY KEY(id)', 'List of Wallace B. Wallace winners'),

        #------------------------------------------------------
        # concert TABLE
        #------------------------------------------------------
        ('concert',
        (
            ('alumni_id',       'INT(10) UNSIGNED', 'NOT NULL', None,  'Alumni in the concert'),
          ('approved',        'TINYINT(1)',       'NOT NULL', '0',   'Is participation approved?'),
          ('needs_instrument','TINYINT(1)',       'NOT NULL', '0',   'Do they need an instrument?'),
            ('instrument_id',   'INT(10) UNSIGNED', 'NOT NULL', None,  'What are they playing?')
          ), """
          PRIMARY KEY(alumni_id),

          FOREIGN KEY (alumni_id) REFERENCES alumni(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE,

          FOREIGN KEY (instrument_id) REFERENCES instruments(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
            """, 'Concert participants and their part'),

        #------------------------------------------------------
        # paid TABLE
        #------------------------------------------------------
        ('paid',
        (
            ('alumni_id',   'INT(10) UNSIGNED', 'NOT NULL', '0',  'Alumni who paid'),
          ('isPaid',      'TINYINT(1)',       'NOT NULL', '1',  'Is payment made, only here to make correcting mistakes easier.'),
          ('paidTime',    'DATETIME',         'NOT NULL', '2007-01-01 00:00:00',  'When was the payment taken')
          ), """
          PRIMARY KEY(alumni_id),

          FOREIGN KEY (alumni_id) REFERENCES alumni(id)
              ON DELETE CASCADE
            ON UPDATE CASCADE
            """, 'List of who has paid their money for events'),

        #------------------------------------------------------
        # contact TABLE
        #------------------------------------------------------
        ('contact',
        (
          ('id',             'INT(10) UNSIGNED', 'NOT NULL AUTO_INCREMENT', None,    'Unique Alumni ID'),
          ('first',          'VARCHAR(40)',      'NOT NULL', '',     'Given name'),
          ('nee',            'VARCHAR(40)',      '',         '',     'Maiden name'),
          ('last',           'VARCHAR(40)',      'NOT NULL', '',     'Family name'),
          ('firstYear',      'INT(10) UNSIGNED', 'NOT NULL', '2006', 'First year in the band'),
          ('lastYear',       'INT(10) UNSIGNED', 'NOT NULL', '2006', 'Last year in the band'),
          ('email',          'VARCHAR(128)',     '',         'NULL', 'Email address'),
          ('street1',        'VARCHAR(45)',      '',         'NULL', 'First line of address'),
          ('street2',        'VARCHAR(45)',      '',         'NULL', 'Second line of address'),
          ('apt',            'VARCHAR(20)',      '',         'NULL', 'Apartment number, if any'),
          ('city',           'VARCHAR(45)',      '',         'NULL', 'Home City'),
          ('province',       'VARCHAR(20)',      '',         'NULL', 'Home Province/State'),
          ('country',        'VARCHAR(25)',      '',         'NULL', 'Home Country'),
          ('postalCode',     'VARCHAR(15)',      '',         'NULL', 'Home Postal Code/Zipcode'),
          ('phone',          'VARCHAR(19)',      '',         'NULL', 'Home Phone'),
          ('instruments',    'TEXT',             '',         None,   'Instruments this alumni has played'),
          ('positions',      'TEXT',             '',         None,   'Positions this alumni has held')
          ), """
          PRIMARY KEY(id)
            """, 'Parade participants and their part')
        )

    def populateTable(self,table):
        """
        Read in the latest table backup information and populate the
        current tables with it. Assumes your current directory is
        the cgi-bin directory.
        """
        try:
            fd = open('../Alumni/bttb%sFile.txt' % table, 'r')
            try:
                headers = []
                data = []
                for line in fd:
                    if len(headers) == 0:
                        headers = line.rstrip('\n').split('\t')
                        headers.pop() # Ignore the trailing tab
                        cmd = 'INSERT INTO %s (%s) VALUES' % (table, ','.join(headers))
                    else:
                        data = line.rstrip('\n').split('\t')
                        data.pop() # Ignore the trailing tab
                        values = '('
                        idx = 0
                        for field in data:
                            if idx > 0:
                                values += ', '
                            if self.__typeMap['%s-%s' % (table,headers[idx])].find( 'INT' ) >= 0:
                                values += "%s" % DbFormat(field)
                            else:
                                values += "'%s'" % DbFormat(field)
                            idx = idx + 1
                        values += ')'
                        try:
                            self.execute( cmd + values )
                        except Exception,e:
                            print '*** WARNING: Table %s, ' % table, e
            finally:
                fd.close()
        except Exception, e:
            print '*** ERROR: Reading file for %s' % table, e

if __name__ == '__main__':
    ErrorsInHtml( False )
    db = PopulateAlumniDB()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
