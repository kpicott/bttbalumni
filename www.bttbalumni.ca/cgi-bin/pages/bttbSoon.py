"""
Web page that hints at things to come
"""

from bttbPage import bttbPage
__all__ = ['bttbSoon']

class bttbSoon(bttbPage):
    '''Class that generates the "coming soon" page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni : Coming Soon'

    def content(self):
        ''':return: a string with the content for this web page.'''

        # If parameters were passed use that to indicate what's coming...
        page = ''
        try:
            page = ' '.join(' and '.join(self.params).split('_'))
        except Exception:
            pass

        # ... otherwise be vague
        if len(page) < 1:
            page = 'future developments'

        html = """
        <h1>Watch this space for %s</h1>
        <p>
        Behind the scenes we're working diligently to bring you the
        information you need. This particular function isn't running
        yet but check back soon!
        </p>
        """ % page

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbSoon()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
