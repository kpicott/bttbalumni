"""
Page that shows the current list of memories, in order by approximate date.
"""

from bttbAlumni import bttbAlumni
from bttbPage import bttbPage
from bttbConfig import Error, MapLinks
from datetime import datetime,timedelta
__all__ = ['bttbMemories']

def sort_by_memory_date(first_memory,second_memory):
    '''Comparison function for two memories by the date in member 2'''
    return cmp(first_memory[2], second_memory[2])

class bttbMemories(bttbPage):
    '''Class that generates the memories page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find memory information', ex )

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Memories'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = """<script type='text/javascript' src='/js/bttbMemories.js'></script>
                  <style>
                    .recent-memory { display: none; }
                    input[type=text]
                    {
                        width:	100px;
                        padding:	6px 10px;
                    }
                    .date
                    {
                        font-size:   16pt;
                        font-weight: bold;
                        color:       blue;
                        padding:     10px 0px 0px 0px;
                    }
                  </style>"""

        old_news_time = datetime.now() - timedelta(30)
        old_news_time = old_news_time.toordinal()

        memory_list = self.alumni.get_memories()
        memory_list.sort( sort_by_memory_date )
        start_year = 1947
        end_year = datetime.now().year
        if self.param('start_year'):
            start_year = int(self.param('start_year'))
        if self.param('end_year'):
            end_year = int(self.param('end_year'))
        html += MapLinks( """
        <table width='100%%'><tr>
        <td>Showing memories between&nbsp;
        <input type='text' onchange='years_changed()' size='4' id='start_year' value='%d'>
        &nbsp;and&nbsp;
        <input type='text' onchange='years_changed()' size='4' id='end_year' value='%d'></td>
        <td id='recent-link'></td>
        <td align='right'>
        link:(#addMemory,<img border='0' src='/Images/addMemory.png' width='109' height='31'>)
        </form>
        </td></tr></table>
        <div name='yearInfo'>
        """ % (start_year, end_year) )
        # -------------------------
        for alumni_id, memory, memory_time, memory_entry_time, _ in memory_list:

            member = self.alumni.getMemberFromId( alumni_id )

            try:
                memory_entry_time = memory_entry_time.absdate()
            except Exception:
                try:
                    memory_entry_time = memory_entry_time.toordinal()
                except Exception:
                    pass

            is_recent_entry = (memory_entry_time >= old_news_time)

            if not is_recent_entry:
                html += "<div class='old-memory'>\n"

            in_range = "none"
            if memory_time.year <= end_year and memory_time.year >= start_year:
                in_range = "block"

            html += "<div class='yearFilter year:%d' style='display:%s'>" % (memory_time.year,in_range)

            html += "<div class='date'>\n"
            if memory_entry_time > old_news_time:
                html += "<img border='0' width='33' height='15' src='"
                html += MapLinks("__IMAGEPATH__/New.png'>&nbsp;")
            html += "%s %s</div>\n" % (memory_time.strftime('%Y-%m-%d'), member.fullName())
            html += "<p>%s</p>\n" % memory
            html += "</div>\n"

            if not is_recent_entry:
                html += "</div>\n"

        html += "</div>"
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbMemories()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
