#!env python
"""
Process the database query.
Unlike most form replies this one explicitly prints out its responses so there
is no post-load after this script completes.
"""

import os
import cgi
from bttbAlumni import bttbAlumni
from bttbConfig import *

def getParam(name,default):
    """
    Simple trick to get cgi params using default values
    """
    try:
        value = params[name][0].strip()
    except:
        value = default
    return value

def getIntParam(name,default):
    """
    Simple trick to get numeric cgi params using default values
    """
    try:
        value = int( params[name][0] )
    except:
        value = default
    return value

try:
    params = cgi.parse()
    outputWeb = (getIntParam( 'outputType', 0 ) == 0)
    query = getParam('queryText', 'SELECT * FROM alumni ORDER BY LAST')
    if outputWeb:
        print 'Content-type: text/html\n'
        #print 'Query Results||'
        print '<head><title>' + query + '</title>'
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
    results,description = alumni.process_query( query )
    if outputWeb:
        print "<div class='outlinedTitle'>", len(results), " results returned from '%s'</div>" % query
        print "<table border='1'><tr>"
    isPassword = []
    try:
        for info in description:
            if outputWeb:
                print "<td>", info[0], "</td>"
            else:
                print info[0], '\t',
            if (type(info[0]) == type('a')) and (info[0] == 'password'):
                isPassword.append( True )
            else:
                isPassword.append( False )
    except:
        print "<td>", description, "</td>"
    if outputWeb:
        print "</tr>"
    else:
        print
    try:
        for result in results:
            if outputWeb:
                print "<tr>"
            idx = 0
            for item in result:
                if isPassword[idx]:
                    if item:
                        item = '[SET]'
                if outputWeb:
                    print "<td>"
                    if item:
                        print item,
                    else:
                        print '&nbsp;'
                    print "</td>"
                else:
                    print item, "\t",
                idx = idx + 1
            if outputWeb:
                print "</tr>"
            else:
                print
    except:
        print "<tr><td>", results, "</td></tr>"
    if outputWeb:
        print "</table>"
except Exception, e:
    Error( 'Processing query', e )

if outputWeb:
    print '</body>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
