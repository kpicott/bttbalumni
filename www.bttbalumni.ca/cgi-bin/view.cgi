#!/usr/bin/env python
'''
Page loader file - handles data in the content frame
'''

import re
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

# Recognize a title line in a hardcoded HTML file
RE_HTML_TITLE = re.compile( r'<title>(.*)</title>', re.IGNORECASE )

__all__ = [ 'bttbContentPanel' ]

class bttbContentPanel(object):
    '''
    Class to handle loading a requested page. Page information provided
    consists solely of the page name and the CGI parameters.
    Since this page should never be linked indirectly by the user, only
    by script-generated references, assumptions are made concerning the
    parameters being passed in (otherwise error page is shown):
        'page' is always present and valid in init_params

    The 'content' and 'title' members are used to identify the raw HTML
    content and the new page title respectively.
    '''
    #----------------------------------------------------------------------
    def __init__(self, init_params):
        self.params = init_params

        # Who requested the page, defaults to unknown
        self.requestor_id = UNKNOWN_ID
        self.requestor = None

        # Content of the page to load
        self.content = ''

        # Default title of the page - bttbPage classes will override the
        # title() method to give a new title. Hardcoded pages can use
        # <title</title> on a single line to have it extracted.
        self.title = 'BTTB Alumni'

        # URL to the page
        try:
            page = init_params['page'][0]    # Page to be displayed
            del self.params['page']
        except Exception:
            page = 'home'

        self.find_requestor()

        try:
            # First check to see if the page exists as hardcoded HTML
            page_name = os.path.join( PagePath(), page + '.html' )
            if os.path.isfile( page_name ):
                try:
                    page_fd = open( page_name, 'r' )
                    self.content = page_fd.read()
                    page_fd.close()
                    title_match = RE_HTML_TITLE.search( self.content )
                    if title_match:
                        self.content = RE_HTML_TITLE.sub( '', self.content )
                        self.title = title_match.group(1)
                    self.log_history( '', page_name )
                    return
                except IOError:
                    pass

            # Convert the page name into a page object, derived from bttbPage
            if len(page) > 1:
                page = 'bttb' + page[0].upper() + page[1:]
            module_name = 'pages.' + page
            module = __import__ (module_name, globals(), locals(), [page])
            class_object = getattr(module, page)
            page = class_object ()
            page.setParams( init_params )
            page.setRequestor( self.requestor )
            self.content = page.content()
            self.title = page.title()

            self.log_history( '', module_name )
        except Exception, ex:
            # Backup solution is to go to the error page
            from pages.bttbError import bttbError
            page = bttbError( ex, page )
            self.title = 'BTTB Alumni : Error'
            self.content = '''<h1>Error loading page %s</h1>
            <p>Try going back and reloading the page. Contact
            send:(web@bttbalumni.ca,the webmaster) if the problem persists.</p>
            <p><font color='white'>%s</font></p>
            ''' % (page, str(ex))
            self.log_history( 'error:', module_name )

    #----------------------------------------------------------------------
    def find_requestor(self):
        '''
        Examine the web page data to see if the requestor can be found.
        Set self.requestor to the result, None if no requestor was found.
        '''
        alumni = bttbAlumni()
        self.requestor = None

        cookie = Cookie.SimpleCookie()

        # If the requester wasn't already present then look in the cookies
        if cookie.has_key('User'):
            self.requestor = alumni.getMemberFromId( int(cookie['User']) )

        if self.requestor is not None:
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
    def add_preamble(self):
        '''
        Look at the current configuration and set any scripts or styles needed
        for the page.
        '''
        self.content += '<script>$(document).ready(function() {\n'
        self.content += '$("title").html( \'%s\' );\n' % self.title
        self.content += '});</script>\n'

    #----------------------------------------------------------------------
    def page_content(self):
        '''
        Display the desired page in the content frame. This is the
        only part that varies from page to page. Everything else is the same
        in the entire website.
        '''
        self.add_preamble()
        return self.content

# ==================================================================

import unittest
class TestPage(unittest.TestCase):
    '''Unit test for a simple page'''
    def setUp(self):
        '''Initialize some sample page content'''
        self.nav = bttbContentPanel( {'page':['test'] } )
        self.bad_nav = bttbContentPanel( {'page':['hello']} )

    def test_basics(self):
        '''Test basic loading of a page and error content'''
        nav_content = self.nav.page_content()
        bad_nav_content = self.bad_nav.page_content()
        self.assert_( nav_content.find('home') )
        self.assert_( bad_nav_content.find('Error loading page') )

if 'SCRIPT_FILENAME' in os.environ:
    # Uncomment for debugging
    import cgitb
    cgitb.enable()
    import cgi
    PARAMS = cgi.parse()
    PANEL = bttbContentPanel( PARAMS )
    CONTENT = PANEL.page_content()
    if not CONTENT:
        CONTENT = ErrorMsg('Blank page loaded', PARAMS)
    print 'Content-type: text/html\n'
    print MapLinks(CONTENT)
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
