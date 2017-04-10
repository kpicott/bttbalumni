"""
Page that lets a user add new memories
"""

from bttbAlumni import bttbAlumni
from bttbMember import bttbMember
from bttbPage import bttbPage
from bttbConfig import Error, MapLinks
__all__ = ['bttbAddMemory']

class bttbAddMemory(bttbPage):
    '''Class that generates the new memory query page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        try:
            self.alumni = bttbAlumni()
        except Exception, e:
            Error( 'Could not find alumni information', e )
    
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni : Add a Memory'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks( """
        <p>
        Below are all the memories you have submitted so far, and
        a blank space to add a new one (come back again if you have
        more than one to add).
        </p>
        <p>
        You can edit the text as you please, or select the checkbox
        beside the text to delete a memory.
        </p>
        <form method='POST' name='addMemoryForm' id='addMemoryForm'
              action="javascript:submit_form('/cgi-bin/bttbAddMemory.cgi', '#addMemoryForm', null);">
        <input type='hidden' name='id' value='%d'>
        """ % self.requestor.id )
        memoryList = self.alumni.get_memories( self.requestor.id )
        if len(memoryList) > 0:
            html += '<h2>Entered Memories</h2><p>'
        for alumniId, memory, memory_time, _, memory_id in memoryList:
            html += """
            <input type='hidden' name='memory' value='%d'>
            <table border='1'><tr><td>
            <table>
            <tr>
                <td>Date&nbsp;(YYYY-MM-DD):</td>
                <td><input type='text' name='memoryDate%d' value='%s'></td>
            </tr>
            <tr>
                <td align='right'><input type='checkbox' value='1' name='memoryDelete%d'></td>
                <td>Check here to delete this memory</td>
            </tr>
            <tr>
                <td valign='top'>Memory:</td>
                <td><textarea rows='10' cols='70' name='memory%d'>%s</textarea></td>
            </tr>
            </table>
            </td></tr></table>
            """ % (memory_id, memory_id, memory_time.strftime('%Y-%m-%d'), memory_id, memory_id, memory)
        if len(memoryList) > 0:
            html += '</p>'
        html += """
        <h2>Add a New Memory</h2>
        <table border='1'><tr><td>
        <table>
        <tr>
            <td>Date&nbsp;(YYYY-MM-DD):</td>
            <td><input type='text' name='newMemoryDate' value=''></td>
        </tr>
        <tr>
            <td valign='top'>Memory:</td>
            <td><textarea rows='10' cols='70' name='newMemory'></textarea></td>
        </tr>
        </table>
        </td></tr></table>
        """
        html += "<input type='submit' value='Submit Edited Memories'>"
        html += "</form>"
        html += "<p>&nbsp;</p>"
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbAddMemory()
    TEST_PAGE.requestor = bttbMember()
    print TEST_PAGE.content()
    
# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
