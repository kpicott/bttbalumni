"""
URL page that says thanks for registering to new alumni
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbThanks']

class bttbThanks(bttbPageFile):
    '''Class that generates the registration thanks page'''
    def __init__(self):
        '''Set up the page'''
        bttbPageFile.__init__(self, '__ROOTPATH__/thanks.html', '__ROOTPATH__/thanksAgain.html')

    def title(self):
        ''':return: The page title'''
        return 'Welcome to the BTTB Alumni'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
