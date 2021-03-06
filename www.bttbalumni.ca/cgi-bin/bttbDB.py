"""
Implementation of bttbData that uses a MySQL database.
May be the only implementation, but it had to be switched once already
so it's only prudent to create this layer just in case.
Although the base class is flexible all uses of this class *must*
follow this pattern:
    db = bttbDB()
    db.Initialize()
    ...
    db.Finalize()
"""

import MySQLdb
import os
import re
import datetime
from bttbConfig import Error, ErrorMsg, DataPath, ArchiveFormat, Backup, TableList, DbFormat, PhoneFormat, attend_list_2017
from bttbData import bttbData
from bttbEvent import bttbEvent
from bttbMember import bttbMember

__all__ = [ 'bttbDB' ]

class bttbDB( bttbData ):
    '''Manage access to the database'''
    def __init__(self):
        '''Set up the initial connection'''
        self.__stage = 'Begin'
        self.__cursor = None
        self.__db = None
        self.__db_name = None
        self.__connect_depth = 0
        bttbData.__init__(self)

    #----------------------------------------------------------------------
    def cursor(self):
        '''Return the DB cursor location'''
        return self.__cursor

    #----------------------------------------------------------------------
    def current_stage(self):
        '''Return the current DB stage'''
        return self.__stage

    #----------------------------------------------------------------------
    def execute(self,sql):
        '''Run an SQL command'''
        try:
            sql = sql.strip().rstrip()
            self.stage(sql)
            self.debug_print( 'Start "' + self.__stage + '"' )
            results = self.__cursor.execute(sql)
        except Exception, ex:
            self.debug_print( ErrorMsg("Failed to execute %s" % sql, ex) )

        return results

    #----------------------------------------------------------------------
    def stage(self,stage_name):
        '''Set the DB stage'''
        self.debug_print( 'Completed "' + self.__stage + '"' )
        self.__stage = stage_name

    #----------------------------------------------------------------------
    def Finalize(self):
        '''Finalize the database'''
        self.close()

    #----------------------------------------------------------------------
    def close(self):
        '''Close the connection to the database'''
        try:
            self.stage( 'complete' )
            self.debug_print( 'Close DB connection level %d' % self.__connect_depth )
            self.__connect_depth = self.__connect_depth - 1
            if self.is_debug_on() and self.__connect_depth < 0:
                self.debug_print( ErrorMsg('Too many DB closes', self.__stage) )
            if self.__connect_depth <= 0:
                if self.__cursor:
                    self.__cursor.close()
                self.__cursor = None
        except Exception:
            pass

    #----------------------------------------------------------------------
    def Initialize(self, database_name='bttba_bttbalumni'):
        '''Initialize the database'''
        self.__db_name = database_name
        self.connect()

    #----------------------------------------------------------------------
    def connect(self):
        '''Connect to the database'''
        self.__connect_depth = self.__connect_depth + 1
        self.debug_print( 'Open DB connection level %d' % self.__connect_depth )
        if self.__cursor:
            return True

        try:
            if os.getenv('USER') == 'Dad' or os.getenv('USER') == 'kpicott' or os.getenv('SERVER_NAME') == 'band.local':
                self.__db = MySQLdb.connect( host='localhost', db='%s' % self.__db_name, user='Dad', passwd='bttbsql' )
            else:
                self.__db = MySQLdb.connect( host='localhost', db='%s' % self.__db_name, user='bttba', passwd='u2mgAw+tAtHD' )

            self.stage( 'Get cursor' )
            self.__cursor = self.__db.cursor()

            return True
        except Exception, ex:
            self.debug_print( ErrorMsg( 'Failed to connect : %s' % str(ex), self.__stage ) )
        return False

    #----------------------------------------------------------------------
    def get_table_column_names(self, table):
        """
        Internal function to return a list of the columns used by a table.
        Mostly used to populate the table into an object automatically.
        """
        column_items = {}
        try:
            self.connect()
            self.execute( "SHOW COLUMNS FROM " + table )
            column_list = [field_c for (field_c, _, _, _, _, _) in self.__cursor.fetchall()]
            idx = 0
            for column in column_list:
                column_items[column] = idx
                idx = idx + 1
            self.close()
        except Exception:
            pass
        return column_items

    #----------------------------------------------------------------------
    def Archive(self):
        """
        Dump all of the BTTB Alumni data tables out to files for archival or
        backup purposes.
        """
        alum_dir = DataPath()
        try:
            self.connect()
            self.stage( 'Archive tables' )
            for table in TableList():
                table_file = alum_dir + '/' + self.__db_name + table + 'File.txt'
                Backup( table_file )
                table_fd = open(table_file, 'w')
                column_names = self.get_table_column_names( table )
                title = ""
                key_names = column_names.keys()
                key_names.sort( lambda x,y,the_dict=column_names: cmp (the_dict[x], the_dict[y]) )
                for col in key_names:
                    title += '%s\t' % col
                title += "\n"
                table_fd.write( title )
                self.stage( 'Archive %s' % table )
                query = "SELECT * from %s" % table
                self.execute( query )
                for row in self.__cursor.fetchall():
                    row_string = ""
                    for col in row:
                        row_string += ArchiveFormat('%s' % col) + '\t'
                    row_string += "\n"
                    table_fd.write( row_string )
                table_fd.close()
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )

    #----------------------------------------------------------------------
    def GetEventAttendees(self, event):
        """
        Get the tuple list consisting of all attendees of the given event
        """
        attend_list = {}
        query = """
                SELECT alumni.first,alumni.nee,alumni.last
                FROM alumni INNER JOIN attendance,60thevents
                WHERE alumni.id=attendance.alumni_id
                    AND attendance.event_id=60thevents.id
                    AND 60thevents.summary='%s'
                ORDER by alumni.last""" % event
        try:
            self.connect()
            self.stage( 'Constructing event attendance query' )
            self.execute( query )
            attend_list = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return attend_list

    #----------------------------------------------------------------------
    def get_memories(self, alumni_id=None):
        """
        Get the tuple (alumni_id, memory, time, memory_id) with all memories.
        If id is specified then use it to filter the list.
        """
        memory_list = {}
        where = ' WHERE alumni.id=memories.alumni_id AND memories.removed=0'
        if alumni_id != None:
            where += ' AND alumni.id=%d' % alumni_id
        query = "SELECT alumni.id,memories.memory,memories.memoryTime,memories.submitTime,memories.id FROM alumni INNER JOIN memories%s" % where
        try:
            self.connect()
            self.stage( 'Constructing memory query' )
            self.execute( query )
            memory_list = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            return [str(self),str(ex),query,"2017-01-01",99999]
        # Convert the tuple to a list, for sorting
        return [memory for memory in memory_list]

    #----------------------------------------------------------------------
    def get_memories_added_after(self, earliest_time):
        """
        Get the tuple (alumni_id, memory, time, memory_id) with all memories
        that were added after the 'earliest_time' date.
        """
        memory_list = {}
        try:
            self.connect()
            self.stage( 'Constructing memory query' )
            query = "SELECT alumni.id,memories.memory,memories.memoryTime,memories.submitTime,memories.id FROM alumni INNER JOIN memories"
            query += ' WHERE alumni.id=memories.alumni_id AND memories.removed=0'
            query += " AND memories.submitTime > '%s'" % earliest_time.strftime('%Y-%m-%d')
            query += ' ORDER BY memories.submitTime DESC'
            self.execute( query )
            memory_list = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        # Convert the tuple to a list, for sorting
        return [memory for memory in memory_list]

    #----------------------------------------------------------------------
    def GetEvents(self):
        """
        Get the list of all events in the database as bttbEvent objects.
        """
        event_list = {}
        try:
            self.connect()
            self.stage( 'Constructing events query' )
            query = "SELECT * FROM 60thevents ORDER BY eventDate"
            self.execute( query )
            event_list = self.__cursor.fetchall()
            self.close()
            keys = self.get_table_column_names( '60thevents' )
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return [bttbEvent(keys,event) for event in event_list]

    #----------------------------------------------------------------------
    def get_public_member_list(self, sorted_by='firstYear', descending=False, limit=None):
        """
        Get the list of alumni in the specified order.
        Use the name of the table fields for the sorted_by value.
        Returns a tuple list, the last entry of which contains the field names
        """
        if descending:
            sorted_by = sorted_by + ' DESC'
        member_list = []
        column_items = {}
        try:
            column_items = self.get_full_member_keys()
            self.connect()
            if limit:
                limit = " LIMIT %d" % limit
            elif self.is_debug_on():
                limit = " LIMIT 10"
            else:
                limit = ""
            self.execute( "SELECT * FROM alumni WHERE make_public <> 0 ORDER BY " + sorted_by + limit )
            member_list = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return (member_list, column_items)

    #----------------------------------------------------------------------
    def get_public_member_list_since(self, earliest_time):
        """
        Get the list of alumni in join time order who joined after the
        specified date.  Returns a tuple list, the last entry of which
        contains the field names
        """
        member_list = []
        member_count = 0
        try:
            self.connect()
            self.stage( 'Constructing joinTime sort query' )
            query = """
            SELECT %s FROM alumni WHERE joinTime > '%s' AND make_public <> 0 ORDER BY joinTime DESC
            """ % (', '.join(self.GetPublicMemberKeys()), earliest_time.strftime('%Y-%m-%d'))
            self.execute( query )
            member_list = self.__cursor.fetchall()
            self.execute( 'SELECT COUNT(*) from alumni;' )
            member_count = int(self.__cursor.fetchone()[0])
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return (member_list, self.GetPublicMemberItems(), member_count)

    #----------------------------------------------------------------------
    def get_full_member_keys(self):
        """
        Get the list of all field keys for the alumni member database.
        """
        return self.get_table_column_names( 'alumni' )

    #----------------------------------------------------------------------
    def get_full_member_list(self, sorted_by='firstYear', descending=False, limit=None):
        """
        Get the list of alumni in the specified order.
        Use the name of the table fields for the sorted_by value.
        Returns a list of tuples containing all alumni table fields.
        The first tuple contains the type names, which could be used to create
        dictionary-like syntax. They should correspond to the bttbMember field
        names.
        """
        if descending:
            sorted_by = sorted_by + ' DESC'
        member_list = []
        column_items = {}
        try:
            column_items = self.get_full_member_keys()
            self.connect()
            if limit:
                limit = " LIMIT %d" % limit
            elif self.is_debug_on():
                limit = " LIMIT 10"
            else:
                limit = ""
            self.execute( "SELECT * FROM alumni ORDER BY " + sorted_by + limit )
            member_list = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return (member_list, column_items)

    #----------------------------------------------------------------------
    def get_unique_id(self):
        """
        Get an available unique ID from the member database
        """
        unique_id = os.getpid()
        try:
            self.connect()
            self.execute( """
            SELECT u.id + 1 AS FirstAvailableId
                FROM alumni u
                LEFT JOIN alumni u1 ON u1.id = u.id + 1
                WHERE u1.id IS NULL
                ORDER BY u.id
                LIMIT 0, 1 
            """)
            id_record = self.__cursor.fetchone()
            if id_record and (len(id_record) > 0):
                unique_id = id_record[0]
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )

        return unique_id

    #----------------------------------------------------------------------
    def GetMember(self, alumni_id):
        """
        Get the full table row for the alumni with the specified id.
        Returns a list of tuples containing all alumni table fields.
        The first tuple contains the type names, which could be used to create
        dictionary-like syntax. They should correspond to the bttbMember field
        names.
        """
        member = None
        try:
            column_items = {}
            column_items = self.get_full_member_keys()
            self.connect()
            self.execute( "SELECT * FROM alumni WHERE alumni.id = %d" % alumni_id )
            member_info = self.__cursor.fetchone()
            self.close()
            if member_info:
                member = bttbMember()
                member.loadFromTuple( column_items, member_info )
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return member

    #----------------------------------------------------------------------
    def GetFullEventAttendance(self, limit=None):
        """
        Get the list of all event attendees. Returns a list of tuples:
            (alumni_id, event_id, event_name)
        """
        query = """
        SELECT DISTINCT alumni.id,60thevents.id,60thevents.summary
        FROM alumni INNER JOIN attendance,60thevents
        WHERE alumni.id = attendance.alumni_id
        AND 60thevents.canAttend = 1
        AND 60thevents.id = attendance.event_id
        ORDER BY alumni.id,60thevents.id
        """
        attendance = []
        try:
            self.connect()
            if limit:
                limit = " LIMIT %d" % limit
            elif self.is_debug_on():
                limit = " LIMIT 10"
            else:
                limit = ""
            self.execute( query + limit )
            attendance = self.__cursor.fetchall()
            self.close()
        except Exception:
            pass
        return attendance

    #----------------------------------------------------------------------
    def update_member(self, member, replaceIfExists):
        """
        Add a new member, or replace the existing member's information.
        """
        try:
            self.connect()
            select_cmd = "SELECT id FROM alumni WHERE alumni.id = %d" % member.id
            self.execute( select_cmd )
            member_info = self.__cursor.fetchone()
            if member_info:
                if replaceIfExists:
                    self.stage( 'TRYING UPDATE' )
                    self.update_member_data(member)
                    self.stage( 'SUCCEEDED AT UPDATE' )
            else:
                self.add_member_data(member)

            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return True

    #----------------------------------------------------------------------
    def update_attendance_2017(self, member, events):
        """
        Replace a member's event attendance status
        """
        try:
            self.connect()

            # Remove existing attendance information
            delete_cmd = """
                DELETE FROM attendance WHERE alumni_id = %d
                """ % member.id
            self.execute( delete_cmd )
            # Add attendance information
            all_events = attend_list_2017()
            for event in events:
                insert_cmd = """
                    INSERT INTO attendance (alumni_id, event_id) VALUES (%d, %d);
                    """ % (member.id, all_events[event])
                self.execute( insert_cmd )
                if event == 'Concert':
                    insert_cmd = """
                        INSERT INTO attendance (alumni_id, event_id) VALUES (%d, %d);
                        """ % (member.id, all_events['Concert Practice'])
                    self.execute( insert_cmd )

            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return True

    #----------------------------------------------------------------------
    def update_member_memory(self, member, memory, memory_id):
        """
        Replace a member's memory. Only valid until memory lane addition gives
        a more powerful memory editing capability.
        """
        try:
            self.connect()

            # Remove existing attendance information
            if memory_id < 0:
                delete_cmd = """
                    DELETE FROM memories WHERE alumni_id = %d AND id = %d
                    """ % (member.id, -memory_id)
            else:
                delete_cmd = """
                    DELETE FROM memories WHERE alumni_id = %d AND id = %d
                    """ % (member.id, memory_id)
            self.execute( delete_cmd )
            # Add attendance information
            if memory and len(memory) > 0:
                insert_cmd = """
                    INSERT INTO memories (alumni_id, memory, memoryTime, submitTime) VALUES (%d, '%s', '%s', '%s');
                    """ % (member.id, DbFormat(memory), \
                           member.midpoint().strftime('%Y-%m-%d'), \
                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.execute( insert_cmd )

            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return True

    #----------------------------------------------------------------------
    def update_memory( self, memberId, memory, memory_time, memory_id ):
        """
        Update the memory in the table. If the memory doesn't exist
        then add a new one to the table.
        """
        try:
            self.connect()

            self.execute( "SELECT id FROM memories WHERE id = %d;" % memory_id )
            member_info = self.__cursor.fetchone()
            if member_info:
                self.execute( """
                UPDATE memories SET memory='%s', memoryTime='%s'
                WHERE id = %d;
                """ % (DbFormat(memory), memory_time.strftime('%Y-%m-%d'), memory_id))
            else:
                self.execute( """
                    INSERT INTO memories (alumni_id, memory, memoryTime, submitTime)
                    VALUES (%d, '%s', '%s', '%s');
                    """ % (memberId, DbFormat(memory), \
                           memory_time.strftime('%Y-%m-%d'), \
                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) )

            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return True

    #----------------------------------------------------------------------
    def remove_memory( self, memory_id ):
        """
        Mark the memory as removed, but don't actually get rid of it.
        """
        try:
            self.connect()
            self.execute( """
                UPDATE memories SET removed=1 WHERE id = %d;
                """ % memory_id )

            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return True

    #----------------------------------------------------------------------
    def add_member_data(self, member):
        """
        Insert a single alumni into the alumni table, if it isn't already there
        """
        try:
            self.stage( 'ADD MEMBER DATA' )
            first_year = int(member.firstYear) and int(member.firstYear) or 2006
            last_year = int(member.lastYear) and int(member.lastYear) or 2006
            join_time = member.joinTime.strftime('%Y-%m-%d %H:%M:%S')
            edit_time = member.editTime.strftime('%Y-%m-%d %H:%M:%S')

            # Default email to NULL if it has no content, so that it can be
            # allowed as a unique value.
            email = member.email.strip()
            if email is not None and len(email) == 0:
                email = 'NULL'
            else:
                email = "'%s'" % email

            instruments = ', '.join(member.instruments)
            positions = ', '.join(member.positions)
            insert_cmd = """
            INSERT INTO alumni (first, nee, last, user_id, firstYear, lastYear, email, make_public,
            isFriend, street1, street2, apt, city, province, country, postalCode, phone, id,
            joinTime, editTime, instruments, positions, approved, onCommittee, rank, password)
            VALUES
            ('%s', '%s', '%s', '%s', %d, %d, %s, %d,
             %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d,
             '%s', '%s', '%s', '%s', %d, %d, '%s', '%s' );
            """ % (DbFormat(member.first),              \
                   DbFormat(member.nee),                \
                   DbFormat(member.last),               \
                   DbFormat(member.user_id),            \
                   first_year,                          \
                   last_year,                           \
                   email,                               \
                   member.make_public,                  \
                   member.isFriend,                     \
                   DbFormat(member.street1),            \
                   DbFormat(member.street2),            \
                   DbFormat(member.apt),                \
                   DbFormat(member.city),               \
                   DbFormat(member.province),           \
                   DbFormat(member.country),            \
                   DbFormat(member.postalCode),         \
                   DbFormat(PhoneFormat(member.phone)), \
                   member.id,                           \
                   join_time,                           \
                   edit_time,                           \
                   DbFormat(instruments),               \
                   DbFormat(positions),                 \
                   member.approved,                     \
                   member.onCommittee,                  \
                   DbFormat(member.rank),               \
                   DbFormat(member.password) )
            self.execute( insert_cmd )
            self.stage( 'ADD COMPLETE' )
        except Exception, ex:
            Warning( self.current_stage(), ex )
        return True

    #----------------------------------------------------------------------
    def update_member_data(self, member):
        """
        Update alumni data in the alumni table, assuming it's there.
        A bunch of duplication from the above method but since the
        implementation is so small coalescing them would be just as
        large and slightly more complicated.  The only real difference is
        the SQL syntax.
        """
        try:
            self.stage( 'UPDATE MEMBER DATA' )
            first_year = member.firstYear and int(member.firstYear) or 2006
            last_year = member.lastYear and int(member.lastYear) or 2006
            join_time = member.joinTime.strftime('%Y-%m-%d %H:%M:%S')
            edit_time = member.editTime.strftime('%Y-%m-%d %H:%M:%S')
            instruments = ', '.join(member.instruments)
            positions = ', '.join(member.positions)
            self.stage( 'UPDATE COMPLETE' )
            insert_cmd = """
            UPDATE alumni SET first='%s', nee='%s', last='%s', user_id='%s', firstYear=%d, lastYear=%d,
            email='%s', make_public=%d, isFriend=%d,
            street1='%s', street2='%s', apt='%s', city='%s',
            province='%s', country='%s', postalCode='%s', phone='%s', joinTime='%s',
            editTime='%s', instruments='%s', positions='%s',
            approved=%d, onCommittee=%d, rank='%s', password='%s'
            WHERE id = %d;
            """ % (DbFormat(member.first),              \
                   DbFormat(member.nee),                \
                   DbFormat(member.last),               \
                   DbFormat(member.user_id),            \
                   first_year,                          \
                   last_year,                           \
                   DbFormat(member.email),              \
                   member.make_public,                  \
                   member.isFriend,                     \
                   DbFormat(member.street1),            \
                   DbFormat(member.street2),            \
                   DbFormat(member.apt),                \
                   DbFormat(member.city),               \
                   DbFormat(member.province),           \
                   DbFormat(member.country),            \
                   DbFormat(member.postalCode),         \
                   DbFormat(PhoneFormat(member.phone)), \
                   join_time,                           \
                   edit_time,                           \
                   DbFormat(instruments),               \
                   DbFormat(positions),                 \
                   member.approved,                     \
                   member.onCommittee,                  \
                   DbFormat(member.rank),               \
                   DbFormat(member.password),           \
                   member.id )
            self.execute( insert_cmd )
            self.stage( 'UPDATE COMPLETE' )
        except Exception, ex:
            Warning( self.current_stage(), ex )
        return True

    #----------------------------------------------------------------------
    def LogPage(self, pageName, who):
        """
        Log a hit on a particular sub-page so that we can see what areas
        are of the most interest.
        """
        try:
            self.connect()
            cmd = "INSERT INTO pages (name, alumni_id, accessTime) VALUES ('%s', %d, '%s');" % (pageName, who, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.execute( cmd )
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return True

    #----------------------------------------------------------------------
    def GetMemberInfo(self, name):
        """
        Get the full table row for the alumn{i,ae} with the specified name.
        Returns a list of bttbMembers whose name matches the given ones.
        """
        member = None
        try:
            # Put the name in canonical form (no spaces, quotes, lower case only)
            raw_name = name
            name = re.sub("^'", "", name)
            name = re.sub("'$", "", name)
            name = re.sub('^"', '', name)
            name = re.sub('"$', '', name)
            name = re.sub(' ', '', name)
            name = DbFormat( name.lower() )

            column_items = {}
            column_items = self.get_full_member_keys()
            self.connect()
            self.execute( """
                SELECT *
                FROM alumni
                WHERE REPLACE(CONCAT(alumni.first,alumni.last),' ','') LIKE '%s'
                        OR email LIKE '%s'
                        OR user_id LIKE '%s'
            """ % (name, raw_name, name) )
            member_info = self.__cursor.fetchone()
            self.close()
            if member_info and len(member_info) > 0:
                member = bttbMember()
                member.loadFromTuple( column_items, member_info )
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return member

    #----------------------------------------------------------------------
    def get_parade_registration_2017(self):
        """
        Return a list of tuples comprising the people who have signed up
        for the parade so far the parts they have signed up for
            [(alumni_name,instrument_name)]
        """
        playing = None
        try:
            self.connect()
            self.execute( """
                SELECT
                alumni.first,alumni.nee,alumni.last,instruments.id,2017_parade.registered
                FROM alumni INNER JOIN instruments,2017_parade
                WHERE alumni.id=2017_parade.alumni_id
                    AND instruments.id=2017_parade.instrument_id
                ORDER by alumni.last""" )
            playing = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )

        return playing

    #----------------------------------------------------------------------
    def get_parade_part_2017(self, alumni_id):
        """
        Return the tuple of instrument information relevant to this
        member's participation in the parade.
        (instrument_id, needs_instrument)
        """
        try:
            self.connect()
            self.execute( """
                SELECT instrument_id,registered
                FROM 2017_parade
                WHERE alumni_id = %d
                """ % alumni_id )
            parts = self.__cursor.fetchone()
            if parts and (len(parts) > 0):
                return parts
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )

        return None

    #----------------------------------------------------------------------
    def set_parade_part_2017(self,alumni_id,instrument_id,registered):
        """
        Set the parade part to be played by the given alumnus.
        """
        try:
            self.connect()
            select_cmd = "SELECT instrument_id FROM 2017_parade WHERE 2017_parade.alumni_id = %d" % alumni_id
            self.execute( select_cmd )
            has_part = self.__cursor.fetchone()
            if has_part:
                set_cmd = """
                UPDATE 2017_parade SET instrument_id=%d, registered=%d
                WHERE alumni_id = %d;
                """ % (instrument_id, registered, alumni_id)
            else:
                set_cmd = """
                INSERT INTO 2017_parade (alumni_id, registered, instrument_id)
                VALUES (%d, %d, %d);
                """ % (alumni_id, registered, instrument_id)

            self.execute( set_cmd )

            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return True

    #----------------------------------------------------------------------
    def delete_parade_part_2017(self,alumni_id):
        """
        Remove the alumnus from the parade database.
        """
        return self.process_query( "DELETE FROM 2017_parade WHERE alumni_id = %d" % alumni_id )

    #----------------------------------------------------------------------
    def get_concert_registration_2017(self):
        """
        Return a list of tuples comprising the people who have signed up
        for the concert so far the parts they have signed up for
            [(alumni_name,instrument_name)]
        """
        try:
            self.connect()
            self.execute( """
                SELECT
                alumni.first,alumni.nee,alumni.last,instruments.id
                FROM alumni INNER JOIN instruments,2017_concert
                WHERE alumni.id=2017_concert.alumni_id
                    AND instruments.id=2017_concert.instrument_id
                ORDER by alumni.last""" )
            playing = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            Error(self.__stage, ex)

        return playing

    #----------------------------------------------------------------------
    def get_concert_part_2017(self, alumni_id):
        """
        Return the instrument ID relevant to this member's participation in the concert.
        """
        try:
            self.connect()
            self.execute( """
                SELECT instrument_id
                FROM 2017_concert
                WHERE alumni_id = %d
                """ % alumni_id )
            parts = self.__cursor.fetchone()
            if parts and (len(parts) > 0):
                return parts[0]
            self.close()
        except Exception, ex:
            Error(self.__stage, ex)

        return None

    #----------------------------------------------------------------------
    def set_concert_part_2017(self,alumni_id,instrument_id):
        """
        Set the concert part to be played by the given alumnus.
        """
        try:
            self.connect()
            select_cmd = "SELECT instrument_id FROM 2017_concert WHERE 2017_concert.alumni_id = %d" % alumni_id
            self.execute( select_cmd )
            has_part = self.__cursor.fetchone()
            if has_part:
                set_cmd = """
                UPDATE 2017_concert SET instrument_id=%d
                WHERE alumni_id = %d;
                """ % (instrument_id, alumni_id)
            else:
                set_cmd = """
                INSERT INTO 2017_concert (alumni_id, instrument_id)
                VALUES (%d, %d);
                """ % (alumni_id, instrument_id)

            self.execute( set_cmd )

            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
            self.close()
        except Exception, ex:
            Error(self.__stage, ex)
        return True

    #----------------------------------------------------------------------
    def delete_concert_part_2017(self,alumni_id):
        """
        Remove the alumnus from the concert database.
        """
        return self.process_query( "DELETE FROM 2017_concert WHERE alumni_id = %d" % alumni_id )

    #----------------------------------------------------------------------
    def get_instruments(self):
        """
        Return the list of tuples of (instrument name, instrument id)
        currently present in the database.
        """
        return self.process_query( "SELECT instrument,id FROM instruments" )[0]

    #----------------------------------------------------------------------
    def get_songs(self):
        """
        Return the list of tuples of (song name, song id)
        currently present in the database.
        """
        return self.process_query( "SELECT title,id FROM songs" )[0]

    #----------------------------------------------------------------------
    def get_sheet_music(self):
        """
        Return the list of tuples of (song id, instrument id, file)
        currently present in the database.
        """
        return self.process_query( "SELECT song_id,instrument_id,file FROM sheet_music" )[0]

    #----------------------------------------------------------------------
    def get_playlist_for_event(self, event_id):
        """
        Return the list of song ids on the playlist for a given event
        """
        return self.process_query( "SELECT song_id FROM playlists WHERE event_id=%d" % event_id )[0]

    #----------------------------------------------------------------------
    def process_query(self, query):
        """
        Process a generic query.
        """
        results = {}
        description = {}
        try:
            self.connect()
            self.execute( query )
            results = self.__cursor.fetchall()
            description = self.__cursor.description
            # Need a COMMIT since we're using InnoDB
            self.execute( 'COMMIT' )
        except Exception, ex:
            results = {}
            description = {}
        self.close()
        return results,description

    #----------------------------------------------------------------------
    def GetWallaceList(self):
        """
        Return the tuple of Wallace B. Wallace winners
        (name, displayName, year, award, submitTime)
        """
        wallace_list = {}
        try:
            self.connect()
            self.execute( """
                SELECT who, whoDisplay, year, description, submitTime
                FROM wallace
                ORDER BY year
                """ )
            wallace_list = self.__cursor.fetchall()
            self.close()
        except Exception, ex:
            self.debug_print( ErrorMsg(self.__stage, ex) )
        return wallace_list

#======================================================================

TEST_WHAT = 6
def test_db():
    '''Test the database'''
    if TEST_WHAT == 6:
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()
        print database.GetWallaceList()
        database.Finalize()
    elif TEST_WHAT == 5:
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()
        database.Archive()
        database.Finalize()
    elif TEST_WHAT == 4:
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()
        (member_list, _, count) = database.get_public_member_list_since(datetime.datetime(2006,12,10))
        print "%d members joined after December 10, %d total" % (len(member_list), count)
        database.Finalize()
    elif TEST_WHAT == 3:
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()
        database.SetParadePart( 0, 12, 1 )
        print database.GetMemberParadePart( 0 )
        database.SetParadePart( 0, 13, 0 )
        print database.GetMemberParadePart( 0 )
        database.SetParadePart( 754, 12, 1 )
        print database.GetMemberParadePart( 754 )
        database.Finalize()
    elif TEST_WHAT == 2:
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()
        print database.GetParadeInstrumentation('parade')
        database.SetParadePart( 0, 12, 1 )
        print database.GetParadeInstrumentation('parade')
        database.SetParadePart( 0, 13, 0 )
        print database.GetParadeInstrumentation('parade')
        database.SetParadePart( 754, 12, 1 )
        database.Finalize()
    elif TEST_WHAT == 1:
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()
        database.Archive()
        database.Finalize()
    else:
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()
        print '=========== PUBLIC MEMBERS ============='
        print database.get_public_member_list()
        print '=========== EVENT LIST ============='
        print database.GetEvents()
        print '=========== SOCIAL EVENT ============='
        print database.GetEventAttendees('Social')
        print '=========== ATTENDANCE ============='
        print database.GetFullEventAttendance()
        print '=========== ME ============='
        print database.GetMember(0).printFullSummary()
        print '=========== UPDATE ME ============='
        print database.get_memories(0)
        my_membership = database.GetMember(0)
        my_membership.memory = 'I have no recollection at all'
        database.update_member(my_membership, True)
        database.update_member_memory(my_membership, my_membership.memory)
        print database.GetMember(0).printFullSummary()
        print '=========== BOB J ============='
        bob = bttbMember()
        bob.approved = True
        bob.onCommittee = True
        bob.editTime = datetime.datetime(2007, 1, 1)
        bob.joinTime = datetime.datetime(2007, 1, 1)
        bob.first = 'Bob'
        bob.last = 'Johnson'
        bob.nee = 'Onthis'
        bob.firstYear = '1980'
        bob.lastYear = '1984'
        bob.email = 'bob@onthis.com'
        bob.make_public = True
        bob.isFriend = False
        bob.instruments = ['Tuba', 'Flute', 'Colour Guard']
        bob.positions = ['Drum Major', 'Band Executive']
        bob.rank = 'Odour'
        bob.apt = '456'
        bob.street1 = '123 Fake Street'
        bob.street2 = ''
        bob.city = 'Burlington'
        bob.province = 'Ontario'
        bob.country = 'Canada'
        bob.postalCode = 'B0B 0B0'
        bob.phone = '905-333-3333'
        bob.memory = 'Bob tries hard not to remember those days. Bob also refers to himself in the third person.  Bob Bob Bob.'
        bob.id = 99999
        database.update_member(bob, True)
        database.update_attendance_2017(bob, ['Golf', 'Social', 'Homecoming', 'Brunch', 'Parade', 'Concert'])
        database.update_member_memory(bob, bob.memory)
        database.stage( 'BOB update complete' )
        database.GetMember(0).printFullSummary()
        database.stage( 'Debug complete' )
        try:
            page_name = 'test'
            database.connect()
            try:
                database.execute( "SELECT * FROM pages WHERE pages.name = '%s'" % page_name )
            except Exception, ex:
                self.debug_print( ErrorMsg('SELECT page test', ex) )
            (_, count) = database.cursor().fetchone()
            print count
            if count:
                count = int(count) + 1
                cmd = "UPDATE pages SET counter=%d WHERE name = '%s';" % (count, page_name)
            else:
                cmd = "INSERT INTO pages (name, counter) VALUES ('%s', 1);" % page_name
            database.execute( cmd )
            database.execute( 'COMMIT' )
            database.close()
        except Exception, ex:
            self.debug_print( ErrorMsg('Page test', ex) )
        database.Finalize()

if __name__ == '__main__':
    test_db()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================

