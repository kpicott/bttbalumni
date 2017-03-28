"""
Web page that shows music for the 2017 parade and concert
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbMusic2017']

class bttbMusic2017(bttbPageFile):
    '''Class to manage music information for the 2017 parade and concert'''
    def __init__(self):
        '''Initialize the page'''
        bttbPageFile.__init__(self, '__ROOTPATH__/music2017.html')

    def title(self):
        ''':return: the page title'''
        return 'BTTB Alumni 70th Anniversary Music Downloads'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
