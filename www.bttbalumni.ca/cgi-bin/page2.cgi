#!/usr/bin/env python
'''
Page loader file - handles data in the content frame
'''

import os
import Cookie
from bttbDB import bttbDB
from bttbConfig import MapLinks, ErrorMsg, PagePath
import pages
from bttbAlumni import bttbAlumni
from pages.bttbPage import bttbPage
from datetime import datetime,timedelta

# Token used by error logging when requestor is not known
UNKNOWN_ID = 9999999

__all__ = [ 'bttbContentPanel' ]

class bttbContentPanel(object):
    '''
    Class to handle loading a requested page. Page information provided
    consists solely of the page name and the CGI parameters.
    Since this page should never be linked indirectly by the user, only
    by script-generated references, assumptions are made concerning the
    parameters being passed in (otherwise error page is shown):
        'page' is always present and valid in init_params
        'user' is valid if present in init_params, None otherwise
    '''
    #----------------------------------------------------------------------
    def __init__(self, init_params):
        self.params = init_params

        # Who requested the page, defaults to unknown
        self.requestor_id = UNKNOWN_ID
        self.requestor = None

        # List of CSS: and JS: scripts needed for finishing the page load
        self.scripts = []

        # URL to the page
        try:
            self.page = init_params['page'][0]    # Page to be displayed
            del self.params['page']
        except Exception:
            self.page = 'home'

        # ID of the user requesting the page
        try:
            self.user = int(init_params['user'][0])    # Current logged-in user, if any
            del self.params['user']
        except Exception:
            self.user = None

        self.find_requestor( self.user )
        self.define_scripts()

        try:
            # First check to see if the page exists as hardcoded HTML
            self.page_name = os.path.join( PagePath(), self.page + '.html' )
            if os.path.isfile( self.page_name ):
                try:
                    page_fd = open( self.page_name, 'r' )
                    self.page = page_fd.read()
                    page_fd.close()
                    self.log_history( '', self.page_name )
                    return
                except IOError:
                    pass

            # Convert the page name into a page object, derived from bttbPage
            if len(self.page) > 1:
                self.page = 'bttb' + self.page[0].upper() + self.page[1:]
            module_name = 'pages.' + self.page
            module = __import__ (module_name, globals(), locals(), [self.page])
            class_object = getattr(module, self.page)
            self.page = class_object ()
            self.page.setParams( init_params )

            self.page.setRequestor( self.requestor )

            self.log_history( '', module_name )
        except Exception, ex:
            # Backup solution is to go to the error page
            from pages.bttbError import bttbError
            self.page = bttbError( ex, self.page )
            self.log_history( 'error:', module_name )

    #----------------------------------------------------------------------
    def find_requestor(self, user):
        '''
        Examine the web page data to see if the requestor can be found.
        Set self.requestor to the result, None if no requestor was found.
        :param user: User ID passed to the script, None if none passed
        '''
        alumni = bttbAlumni()
        self.requestor = alumni.getMemberFromId( user )

        cookie = Cookie.SimpleCookie()

        # If the requester wasn't already present then look in the cookies
        if not self.requestor and cookie.has_key('User'):
            self.requestor = alumni.getMemberFromId( int(cookie['User']) )

        if self.requestor:
            self.requestor_id = self.requestor.id
            try:
                # Look for the last visited time, so that only new stuff will be shown
                cookie.load(os.environ['HTTP_COOKIE'])
                if cookie.has_key('WWhenH'):
                    try:
                        last_visit = datetime.fromtimestamp( int(cookie['WWhenH'].value)/1000 )
                        self.requestor.setLastVisit( last_visit )
                    except Exception:
                        # Invalid visit timing resets it
                        self.requestor.setLastVisit( datetime.now() )
            except Exception:
                # If no cookies available guess at the last visit as a week ago.
                self.requestor.setLastVisit( datetime.now() - timedelta(7) )

    #----------------------------------------------------------------------
    def log_history(self, prefix, page_ref):
        '''
        Log a visit in the database.
        :param prefix: Type of history log, e.g. "error:"
        :param page_ref: Name of page or module being loaded
        '''
        try:
            database = bttbDB()
            database.Initialize()
            database.LogPage('%s%s?%s' % (prefix, page_ref, '&'.join(self.params)), self.requestor_id)
            database.Finalize()
        except Exception:
            pass

    #----------------------------------------------------------------------
    def set_login_or_logout(self):
        '''
        Define the content of the login area, based on whether someone is
        already logged in or not.
        '''
        if self.requestor is None:
            self.scripts.append( '''JS: $(document).ready(function() {
                $("#login").html( '<i class="fa fa-key"></i><a href="#" onclick="javascript:doLogin();">Login</a>' );
            });''')
        else:
            self.scripts.append( '''JS: $(document).ready(function() {
                $("#login").html( '<i class="fa fa-key"></i><a href="#" onclick="javascript:doLogout();">Logout</a>' );
            });''')

    #----------------------------------------------------------------------
    def set_register_or_welcome(self):
        '''
        Define the content of the welcome area, based on whether someone is
        already logged in or not.
        '''
        if self.requestor is None:
            self.scripts.append( '''JS: $(document).ready(function() {
                $("#welcome").html( '<i class="fa fa-user"></i><a href="/#register">Register Now</a>' );
            });''' )
        else:
            self.scripts.append( '''JS: $(document).ready(function() {
                $("#welcome").html( '<i class="fa fa-user"></i>Welcome %s' );
            });''' % self.requestor.fullName() )

    #----------------------------------------------------------------------
    def define_scripts(self):
        '''
        Look at the current configuration and set any scripts or styles needed
        for the page.
        '''
        self.set_register_or_welcome()
        self.set_login_or_logout()
        if self.requestor is not None and self.requestor.onCommittee:
            self.scripts.append( 'CSS: .committee-only { display: inherit; }' )
        else:
            self.scripts.append( 'CSS: .committee-only { display: none; }' )

    #----------------------------------------------------------------------
    def page_content(self):
        '''
        Display the desired page in the content frame. This is the
        only part that varies from page to page. Everything else is the same
        in the entire website.
        Returns a type (title, scriptArray, content)
        '''
        if isinstance(self.page, bttbPage):
            return (self.page.title(), self.page.scripts() + self.scripts, self.page.content())
        elif isinstance(self.page, str):
            return ('BTTB Alumni', self.scripts, MapLinks(self.page))
        return ('BTTB Alumni : Error loading page', [], MapLinks('''
            <h1>Error loading page %s</h1>
            <p>Try going back and reloading the page. Contact
            send:(web@bttbalumni.ca,the webmaster) if the problem
            persists.</p>
            ''') % (self.page) )

# ==================================================================

import unittest
class TestPage(unittest.TestCase):
    '''Unit test for a simple page'''
    def setUp(self):
        '''Initialize some sample page content'''
        self.nav = bttbContentPanel( {'page':['test'], 'user':['2']} )
        self.bad_nav = bttbContentPanel( {'page':['hello']} )

    def test_basics(self):
        '''Test basic loading of a page and error content'''
        (_, _, nav_content) = self.nav.page_content()
        (_, _, bad_nav_content) = self.bad_nav.page_content()
        self.assert_( nav_content.find('home') )
        self.assert_( bad_nav_content.find('Error loading page') )

if 'SCRIPT_FILENAME' in os.environ:
    # Uncomment for debugging
    import cgitb
    cgitb.enable()
    import cgi
    PARAMS = cgi.parse()
    PANEL = bttbContentPanel( PARAMS )
    (TITLE, SCRIPTS, CONTENT) = PANEL.page_content()
    if not CONTENT:
        CONTENT = ErrorMsg('Blank page loaded', PARAMS)
    print 'Content-type: text/html\n'
    print TITLE + '|' + '#!#'.join([MapLinks(a) for a in SCRIPTS]) + '|' + CONTENT
else:
    unittest.main()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
