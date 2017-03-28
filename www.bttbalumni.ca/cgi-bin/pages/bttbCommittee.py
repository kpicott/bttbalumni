"""
Web page that shows committee member links.

It's really a hardcoded page, it's just access through here to allow
putting the restriction on that only committee members can see it
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbCommittee']

class bttbCommittee(bttbPageFile):
    '''Class that generates the committee database query page'''
    def __init__(self):
        '''Set up the page'''
        bttbPageFile.__init__(self, '__ROOTPATH__/accessDenied.html', '__ROOTPATH__/committee.html')
        self.commitee_only = True

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Committee Links'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
