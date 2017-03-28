"""
Page that shows the user's browser information.
"""

from bttbPage import bttbPage
__all__ = ['bttbBrowser']

class bttbBrowser(bttbPage):
    '''Class that generates the browser information page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    def title(self):
        ''':return: The page title'''
        return 'Browser Information'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = """
        <script type='text/javascript' src='/js/browser.js'></script>
        <form method='POST' onsubmit='setBrowserInfo(); return true;' action='javascript:setBrowserInfo();'>
        <div id='browserInfo'>
        <input type='submit' value='Click here to load browser info'>
        </div>
        </form>
        """
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbBrowser()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
