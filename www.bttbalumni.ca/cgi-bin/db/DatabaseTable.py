'''
Code to manage the basic functions of a database table
'''
import os
import sys
sys.path.insert(0, '..')

from bttbDB import bttbDB
from bttbConfig import DatabasePath

class DatabaseTable(object):
    '''Class to manage the interaction between the database and a single table'''
    def __init__(self, table_name, db):
        '''
        :param table_name: Name of the database table
        :param db: bttbDB object used for SQL queries
        '''
        self.db = db
        self.table_name = table_name
        self.table_create = ''
        self.table_data = []
        self.errors = []

    #----------------------------------------------------------------------
    def __str__(self):
        '''Return this object represented as a string'''
        result = 'TABLE %s\n' % self.table_name
        result += 'SQL %s\n' % self.table_create
        result += 'TABLE DATA\n'
        for table_row in self.table_data:
            result += '   %s' % str(table_row)
        return result

    #----------------------------------------------------------------------
    def add_error(self, msg):
        '''Add an error message to the list'''
        self.errors.append( msg )

    #----------------------------------------------------------------------
    def construct_table(self):
        '''
        Construct the table from the SQL description, if it doesn't already exist
        '''
        sql_table_exists = 'SHOW TABLES LIKE `%s`' % self.table_name
        # TODO: If table doesn't exist
        #       self.database.process_query( self.table_create )

    #----------------------------------------------------------------------
    def read_sql_data(self, sql_file_name):
        '''
        Read the database table creation string from an SQL file. The file is an
        SQL string created from the command
            SHOW CREATE TABLE the_table_name
        '''
        self.table_create = ''
        for line in open(sql_file_name, 'r'):
            self.table_create += line

