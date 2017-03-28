"""
URL page that defines content read directly from a page template
with only structural and location modifications.
"""

import os
from bttbPage import bttbPage, NOT_COMMITTEE
from bttbConfig import ErrorMsg, MapLinks

__all__ = ['bttbPageFile']

class bttbPageFile(bttbPage):
    '''Base class for pages that are read from hardcoded files'''
    def __init__(self, fileName, altFileName=None):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.file_name = MapLinks( fileName )
        self.alt_file_name = self.file_name
        if altFileName is not None:
            self.alt_file_name = MapLinks( altFileName )

    def content(self):
        ''':return: a string with the content for this web page.'''
        file_name = self.file_name
        try:
            if self.requestor:
                if self.can_view_page() == NOT_COMMITTEE:
                    file_name = self.alt_file_name
        except Exception:
            pass
        if os.path.isfile( file_name ):
            info = ""
            html_fd = open( file_name )
            try:
                for line in html_fd:
                    info = info + MapLinks(line)
            finally:
                html_fd.close()

            return info
        else:
            return ErrorMsg( 'File contents missing', file_name )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
