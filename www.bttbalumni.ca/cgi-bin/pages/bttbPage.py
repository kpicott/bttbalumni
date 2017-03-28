"""
Base class for a page that goes in the web content pane.
"""
__all__ = [ 'bttbPage', 'VIEW_OKAY', 'NOT_MEMBER', 'NOT_COMMITTEE' ]
from datetime import datetime
from bttbConfig import PhoneParts

# Status values returned from can_view_page
VIEW_OKAY     = 0  # Legal to view page
NOT_MEMBER    = 1  # Not a member, tried to view members-only page
NOT_COMMITTEE = 2  # Not on committee, tried to view committee-only page

class bttbPage(object):
    '''
    Base class for generated pages.
    Derive from this and override the title() and content() methods to
    provide the information needed to generate a sub-page.
    '''
    def __init__(self):
        self.id = None
        self.params = {}
        self.requestor = None
        self.last_login = datetime.now()

        # Special flags to set if the page is only allowed to be viewed
        # by committee members or logged-in members respectively
        self.committee_only = False
        self.members_only = False

    #----------------------------------------------------------------------
    # Default methods
    def set_params(self, params):
        '''Set the CGI parameters passed to the page'''
        self.params = params

    def set_requestor(self, who):
        '''Set the page requestor (bttbMember)'''
        self.requestor = who

    def set_last_login(self, when):
        '''Set the last login time of the page requestor'''
        self.last_login = when

    def title(self):
        ''':return: Default page title'''
        return 'BTTB Alumni'

    def content(self):
        ''':return: Default web page content.'''
        return 'BTTB Alumni'

    #----------------------------------------------------------------------
    def requestor_as_member_info(self):
        """
        Return Javascript that maps the requestor information onto a
        member_info variable that can be used by other Javascript.

        Only the fields needed are put in - new ones can be added as needed
        """
        first_name = ''
        last_name = ''
        email = ''
        phone = ['','','']
        if self.requestor is not None:
            first_name = self.requestor.first
            last_name = self.requestor.last
            email = self.requestor.email
            phone = PhoneParts( self.requestor.phone )
        return '''var member_info = { 'first_name' : '%s'
               , 'last_name'     : '%s'
               , 'email'         : '%s'
               , 'night_phone_a' : '%s'
               , 'night_phone_b' : '%s'
               , 'night_phone_c' : '%s'
               };''' % (first_name, last_name, email, phone[0], phone[1], phone[2])

    #----------------------------------------------------------------------
    def can_view_page(self):
        """
        Returns True if this page is allowed to be viewed by the current
        web viewer.
        """
        if self.committee_only and not self.is_on_committee():
            return NOT_COMMITTEE
        if self.members_only and not self.is_member():
            return NOT_MEMBER
        return VIEW_OKAY

    #----------------------------------------------------------------------
    def is_on_committee(self):
        """
        Returns True if the current web page viewer is a recognized committee member
        """
        return (self.requestor is not None) and self.requestor.onCommittee

    #----------------------------------------------------------------------
    def is_member(self):
        """
        Returns True if the current web page viewer is logged in as a member.
        """
        return self.requestor is not None

    #----------------------------------------------------------------------
    def param(self, name):
        """Return the value of a named parameter, or None if not set"""
        try:
            return self.params[name][0]
        except KeyError:
            return None

#----------------------------------------------------------------------
if __name__ == '__main__':
    TEST_PAGE = bttbPage()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
