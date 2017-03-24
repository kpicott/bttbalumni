"""
URL page to return error data.
"""

from bttbPage import bttbPage
from bttbConfig import ErrorMsg

__all__ = ['bttbError']

class bttbError(bttbPage):
    '''Class that generates the error page'''
    def __init__(self, error, page):
        '''Set up the page'''
        self.error = '%s' % error
        self.page = ' Error loading page %s' % page
    
    def content(self):
        ''':return: a string with the content for this web page.'''
        return ErrorMsg( self.page, self.error )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
