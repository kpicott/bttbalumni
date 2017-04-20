"""
Page that lets a user add new news
"""

from pages.bttbPage import bttbPage
__all__ = ['bttbAddNews']

class bttbAddNews(bttbPage):
    '''Manage the interface to the page through which committe members add news articles'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.committee_only = True
    
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni : Add a News Article'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = """
        <h2>Add a News Article</h2>
        <table border='1'><tr><td>
        <table>
        <tr>
            <td>Date&nbsp;(YYYY-MM-DD):</td>
            <td><input type='text' name='newNewsDate' value=''></td>
        </tr>
        <tr>
            <td valign='top'>Article (HTML allowed):</td>
            <td><textarea rows='10' cols='70' name='newNews'></textarea></td>
        </tr>
        </table>
        </td></tr></table>
        """
        html += "<input type='submit' value='Submit News'>"
        html += "</form>"
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbAddNews()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
