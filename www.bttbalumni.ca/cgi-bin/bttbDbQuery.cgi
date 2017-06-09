#!/usr/bin/env python
"""
Process the database query.
Unlike most form replies this one explicitly prints out its responses so there
is no post-load after this script completes.
"""
from bttbAlumni import bttbAlumni
from bttbConfig import Error, MapLinks
from bttbCGI import bttbCGI

class BTTBQuery(bttbCGI):
    '''Class to handle parsing of the registration POST request'''

    #----------------------------------------------------------------------
    def process_query(self):
        '''Read the registration info and add or modify it in the database'''
        self.read_cgi()

        if self.get_int_param('add_user_id', 0) > 0:
            self.populate_user_ids()
            self.process_raw_query( 'SELECT * FROM alumni ORDER BY LAST' )
        else:
            sql_query = self.get_param('queryText', 'SELECT * FROM alumni ORDER BY LAST')
            self.process_raw_query( sql_query )

    #----------------------------------------------------------------------
    @staticmethod
    def populate_user_ids():
        '''Scan the alumni table and populate user IDs with initial values'''
        print 'Content-type: text/html\n'
        alumni = bttbAlumni()
        results,_ = alumni.process_query( 'SELECT first,last,id FROM alumni ORDER BY id' )
        for result in results:
            user_id = result[0] + " " + result[1]
            user_id = user_id.replace( "'", "\\'" )
            alumni_id = result[2]
            alumni.process_query( "UPDATE alumni SET user_id='%s' WHERE id=%d" % (user_id, alumni_id) )

    #----------------------------------------------------------------------
    def process_raw_query(self, sql_query):
        '''Process a raw SQL query and print the results'''
        try:
            output_web = (self.get_int_param( 'outputType', 0 ) == 0)
            if output_web:
                print 'Content-type: text/html\n'
                print '<head><title>' + sql_query + '</title>'
                print MapLinks( """
                    <STYLE type='text/css' media='all'>
                        @import url( '__CSSPATH__/bttbSolo.css' );
                    </STYLE>
                    """ )
                print '</head>'
                print '<body>'
            else:
                print "Content-Type:application/octet-stream"
                print "Content-Disposition:attachment; filename=bttbQueryResult.txt\n"

            alumni = bttbAlumni()
            results,description = alumni.process_query( sql_query )
            if output_web:
                print "<div class='outlinedTitle'>", len(results), " results returned from '%s'</div>" % sql_query
                print "<table border='1'><tr>"
            is_password = []
            try:
                for info in description:
                    if output_web:
                        print "<td>", info[0], "</td>"
                    else:
                        print info[0], '\t',
                    if (type(info[0]) == type('a')) and (info[0] == 'password'):
                        is_password.append( True )
                    else:
                        is_password.append( False )
            except Exception:
                print "<td>", description, "</td>"
            if output_web:
                print "</tr>"
            else:
                print
            try:
                for result in results:
                    if output_web:
                        print "<tr>"
                    idx = 0
                    for item in result:
                        if is_password[idx]:
                            if item == 'bttb':
                                item = '[DEFAULT]'
                            elif item:
                                item = '[SET]'
                        if output_web:
                            print "<td>"
                            if item:
                                print item,
                            else:
                                print '&nbsp;'
                            print "</td>"
                        else:
                            print item, "\t",
                        idx = idx + 1
                    if output_web:
                        print "</tr>"
                    else:
                        print
            except Exception:
                print "<tr><td>", results, "</td></tr>"
            if output_web:
                print "</table>"
        except Exception, ex:
            Error( 'Processing query', ex )

        if output_web:
            print '</body>'

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBQuery()
    PROCESSOR.process_query()
except Exception, ex:
    Error( 'Could not process query', ex )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
