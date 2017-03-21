"""
Base class for a page that goes in the web content pane.
"""
__all__ = [ 'bttbPage' ]
from datetime import datetime
from bttbConfig import PhoneParts

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
        self.lastLogin = datetime.now()

    #----------------------------------------------------------------------
    # Default methods
    def setParams(self, params):    self.params = params
    def setRequestor(self, who):    self.requestor = who
    def setLastLogin(self, when):   self.lastLogin = when
    def title(self):                return 'BTTB Alumni'
    def content(self):              return 'BTTB Alumni'

    #----------------------------------------------------------------------
    def scripts(self):
        """
        Javascripts and styles are not evaluated by default so they must be
        called out for special treatment after import.

        __JAVASCRIPTPATH__/SomeJavascript.js
        __CSSPATH__/SomeCSS.css
        JS: Some Javascript code to embed
        CSS: Some CSS code to embed
        """
        return []

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
        js = '''var member_info = { 'first_name' : '%s'
               , 'last_name'     : '%s'
               , 'email'         : '%s'
               , 'night_phone_a' : '%s'
               , 'night_phone_b' : '%s'
               , 'night_phone_c' : '%s'
               };''' % (first_name, last_name, email, phone[0], phone[1], phone[2])
        return js

    #----------------------------------------------------------------------
    def isCommittee(self):
        """
        Returns True if the page parameters correspond to an authorized
        committee member, else return False.
        """
        try:
            return int(self.params('committee')) == 1
        except:
            return False

    #----------------------------------------------------------------------
    def param(self, name):
        """Return the value of a named parameter, or None if not set"""
        try:
            return self.params[name][0]
        except:
            return None

if __name__ == '__main__':
    page = bttbPage()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
