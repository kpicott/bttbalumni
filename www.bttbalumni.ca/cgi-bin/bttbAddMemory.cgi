#!/usr/bin/env python
"""
Add in a new memory for the current user.
"""

print 'Content-type: text/html\n'

import re
from datetime import datetime
from bttbAlumni import bttbAlumni
from bttbConfig import Error
from bttbCGI import bttbCGI

RE_DATE_FMT = re.compile('([12][09][0-9][0-9])[_/-]*([0-9]+)[_/-]*([0-9]+)')

class BTTBAddMemory(bttbCGI):
    '''Class to handle parsing of the registration POST request'''

    #----------------------------------------------------------------------
    @staticmethod
    def date_from_string(date_str):
        """
        Get back a datetime object from a user string.
        """
        try:
            match = RE_DATE_FMT.match( date_str )
            if match:
                (year, month, day) = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
                if year < 1900:
                    year = 1900 + year
                if year > 2100:
                    year = 2007
                return datetime( year, month, day )
        except Exception:
            pass
        return datetime.now()

    #----------------------------------------------------------------------
    def process_memory(self):
        '''Process all of the form parameters and print the resulting details'''
        self.read_cgi()
        try:
            alumni = bttbAlumni()
            #
            # If the id was negative then this is an edit:
            #    Look for a previous edit to overwrite
            #    Either insert or update at (negative-id).
            #
            # Otherwise it's a creation, and requires a new id
            #
            member_id = self.get_int_param('id', 0)
            member = alumni.getMemberFromId(member_id)
            print '<h1>Memory Changes Performed</h1>'
            print '<table border="1" cellpadding="5">'
            if 'memory' in self.params:
                for memory_id in self.params['memory']:
                    try:
                        date = self.date_from_string(self.params['memoryDate%s' % memory_id][0])
                    except Exception:
                        date = member.midpoint()
                    delete = self.get_int_param( 'memoryDelete%s' % memory_id, 0 )
                    try:
                        memory = self.params['memory%s' % memory_id][0]
                        if delete:
                            alumni.remove_memory( int(memory_id) )
                            print '<tr>'
                            print '<td valign="top"><h2>DELETE</h2></td>'
                            print '<td valign="top"><div class="date">%s</div></td>' % date.strftime('%Y-%m-%d')
                            print '<td valign="top">%s</td>' % memory
                            print '</tr>'
                        else:
                            alumni.update_memory( member, memory, date, int(memory_id) )
                            print '<tr>'
                            print '<td valign="top"><h2>EDIT</h2></td>'
                            print '<td valign="top"><div class="date">%s</div></td>' % date.strftime('%Y-%m-%d')
                            print '<td valign="top">%s</td>' % memory
                            print '</tr>'
                    except Exception:
                        pass

            try:
                date = self.date_from_string(self.params['newMemoryDate'][0])
                memory = self.params['newMemory'][0].strip().rstrip()
                if len(memory) > 0:
                    alumni.update_memory( member, memory, date, 999999 )
                    print '<tr>'
                    print '<td valign="top"><h2>ADD</h2></td>'
                    print '<td valign="top"><div class="date">%s</div></td>' % date.strftime('%Y-%m-%d')
                    print '<td valign="top">%s</td>' % memory
                    print '</tr>'
            except Exception:
                pass

            print '</table>'

        except Exception, ex:
            Error( 'Memory processing error', ex )

#----------------------------------------------------------------------

try:
    PROCESSOR = BTTBAddMemory()
    PROCESSOR.process_memory()
except Exception, ex:
    Error( 'Could not process new memory', ex )


# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
