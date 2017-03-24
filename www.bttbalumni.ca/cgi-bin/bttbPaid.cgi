#!env python
"""
Process the BTTB Alumni registration payment information and
update the database.
"""

print 'Content-type: text/html\n'
print 'Updating Registration||'
print '<body>'
print '<div class="outlinedTitle">Registration Updated : Paid List</div>'

import os
import os.path
import re
import cgi
import cgitb; cgitb.enable()
from datetime import datetime
from bttbMember import *
from bttbAlumni import bttbAlumni
from bttbConfig import *

re_paid = re.compile("paid([0-9]+)")
try:
    params = cgi.parse()
    alumni = bttbAlumni()
    paidAt = datetime.now()
    (paidList,paidInfo) = alumni.process_query("""
    SELECT alumni.id
    FROM alumni
    WHERE alumni.id IN (SELECT alumni_id FROM paid WHERE isPaid = 1)
    """)
    (unpaidList,unpaidInfo) = alumni.process_query("""
    SELECT alumni.id
    FROM alumni
    WHERE alumni.id IN (SELECT alumni_id FROM paid WHERE isPaid = 0)
    """)
    wasPaid = []
    wasUnpaid = []
    for id in paidList:
        wasPaid.append( id[0] )
    for id in unpaidList:
        wasUnpaid.append( id[0] )
    paid = []
    changed = []
    for param in params:
        match = re_paid.match(param)
        if match:
            id = int(match.group(1))
            paid.append( id )
            if id in wasUnpaid:
                changed.append( id )
                alumni.process_query( """
                UPDATE paid set paidTime='%s',isPaid=1 where alumni_id=%s
                """ % ( paidAt.strftime('%Y-%m-%d %H:%M:%S'), id ) )
            elif not id in wasPaid:
                changed.append( id )
                alumni.process_query( """
                INSERT INTO paid (alumni_id,isPaid,paidTime)
                VALUES (%s, 1, '%s')
                """ % ( id, paidAt.strftime('%Y-%m-%d %H:%M:%S') ) )
    for id in wasPaid:
        if not id in paid:
            alumni.process_query( """
            UPDATE paid set isPaid=0 where alumni_id=%s
            """ % ( id ) )

    (paidList,paidInfo) = alumni.process_query("""
    SELECT alumni.first,alumni.nee,alumni.last,alumni.id
    FROM alumni
    WHERE alumni.id IN (SELECT alumni_id FROM paid WHERE isPaid = 1)
    ORDER BY alumni.last
    """)

    print '<table width="100%"><tr>'
    col = 0
    for (first,nee,last,id) in paidList:
        if col == 4:
            print '</tr><tr>'
            col = 0
        col = col + 1
        fontOn = ""
        fontOff = ""
        if int(id) in changed:
            fontOn = '<div class="emphasis">'
            fontOff = '</div>'
        print '<td>%s%s%s</td>' % (fontOn, SensibleName(first,nee,last), fontOff)
    print '</tr></table>'

except Exception, e:
    Error( 'Registration processing error', e )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
