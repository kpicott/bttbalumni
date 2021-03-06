"""
URL page that shows all of the globally visible user profile information
"""

from bttbAlumni import bttbAlumni
from bttbPage import bttbPage
from bttbConfig import ErrorMsg
__all__ = ['bttbProfiles']

class bttbProfiles(bttbPage):
    '''Class that generates the user profiles page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Profiles'

    def content(self):
        ''':return: a string with the content for this web page.'''
        try:
            try:
                alumni = bttbAlumni()
                if self.requestor and self.requestor.onCommittee:
                    return alumni.get_alumni_summary_for_committee( self.param('sort') )
                else:
                    return alumni.get_alumni_summary( self.param('sort'), self.requestor )
            except Exception:
                if self.requestor and self.requestor.onCommittee:
                    return alumni.get_alumni_summary_for_committee( 'firstYear' )
                else:
                    return alumni.get_alumni_summary( 'firstYear', self.requestor )
        except Exception, ex:
            return ErrorMsg( 'Could not read member information', ex )

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbProfiles()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
