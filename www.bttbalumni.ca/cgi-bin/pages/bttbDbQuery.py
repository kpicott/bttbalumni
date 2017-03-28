"""
Page that allows entry of database queries (random and hardcoded)
"""

from bttbPage import bttbPage
#from bttbConfig import InTestMode
__all__ = ['bttbDbQuery']

class bttbDbQuery(bttbPage):
    '''Class that generates the committee database query page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.committee_only = True

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Committee database queries'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = "<script type='text/javascript' src='/js/bttbDbForm.js'></script>"

        queries = (
             ("All Profiles", "all", "Profile information for all of the alumni currently")
        ,    ("Committee Profiles", "committee", "Profile information for committee members")
        #,    ("Missing Parade", "parade", "Contact info for everyone who signed up to be in the parade but has not downloaded their music and/or confirmed yet.")
        #,    ("Missing Friday", "friday", "Contact info for everyone who signed up to be at the social event but has not paid yet.")
        #,    ("Missing Saturday", "saturday", "Contact info for everyone who signed up to be at the homecoming but has not paid yet.")
        #,    ("Parade Drumline", "drumline", "The drumline for the parade.")
        ,    ("Contact Missing", "contactMissing", "People on our 50th anniversary contact sheet who have not signed up.")
        ,    ("Duplicate Names", "duplicate", "People who appear to be signed up more than once, based on similar names.")
        ,    ("Remove", "remove", "Remove a set of IDs that were duplicates (use with caution!).")
        ,    ("Query name", "qname", "Find information for an alumni by name.")
        ,    ("Reset Password", "reset", "Reset a password for an alumni by id.")
        )
        html += """
        <h1>Database Queries</h1>
        <p>
        <table><tr><td>
        <input onchange='output_type_changed()' type='checkbox' value='1' name='outputType' id='outputType'>
        </td><td>
        <div id='outputTypeInfo'>
        Output will be shown on screen. Check this box to download output
        to a text file.</div></input>
        </td></tr></table>
        </p>
        <p>
        <table border='1'><tr><td>
        <h2>Hardcoded Queries (press button then "Run Query")</h2>
        <table>
        """
        for value,tag,info in queries:
            html += "<tr>"
            html += "    <td align='right'><button class='shadow_button'"
            html += r"        onclick='query_select(\"%s\")' \>%s</button>" % (tag, value)
            html += "    </td>"
            html += "    <td>" + info + "</td>"
            html += "</tr>"
        html += """
        </table>
        </p>
        </td></tr></table>
        </p>
        <form target='data' id='dbQueryForm' action="/cgi-bin/bttbDbQuery.cgi">
        <textarea name='queryText' id='queryText' rows='10' cols='80'></textarea><br>
        <button type='submit' class='shadow_button'>Run Query</button>
        </form>
        """
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbDbQuery()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
