#!/usr/bin/env python
"""
Page loader file - handles data in the content frame
"""

import os
import Cookie
from bttbDB import *
from bttbConfig import *
import pages
from bttbAlumni import bttbAlumni
from pages.bttbPage import bttbPage
from datetime import datetime,timedelta

__all__ = [ 'bttbContentPanel' ]

class bttbContentPanel:
    """
    Class to handle loading a requested page. Page information provided
    consists solely of the page name and the CGI parameters.
    Since this page should never be linked indirectly by the user, only
    by script-generated references, assumptions are made concerning the
    parameters being passed in (otherwise error page is shown):
        'page' is always present and valid in params
        'user' is valid if present in params, None otherwise
    """
    #----------------------------------------------------------------------
    def __init__(self, params):
        self.params = params
        try:
            self.page = params['page'][0]    # Page to be displayed
            del self.params['page']
        except Exception, e:
            self.page = 'home'
        try:
            self.user = int(params['user'][0])    # Current logged-in user, if any
            del self.params['user']
        except Exception, e:
            self.user = None

        # Convert the page name into a page object, derived from bttbPage
        try:
            if len(self.page) > 1:
                self.page = 'bttb' + self.page[0].upper() + self.page[1:]
            moduleName = 'pages.' + self.page
            module = __import__ (moduleName, globals(), locals(), [self.page])
            classObject = getattr(module, self.page)
            self.page = classObject ()
            self.page.setParams( params )
            alumni = bttbAlumni()
            requestor = alumni.getMemberFromId( self.user )
            reqId = 9999999
            cookie = Cookie.SimpleCookie()
            if not requestor and cookie.has_key('User'):
                requestor = alumni.getMemberFromId( int(cookie['User']) )
            if requestor:
                try:
                    cookie.load(os.environ['HTTP_COOKIE'])
                    if cookie.has_key('WWhenH'):
                        try:
                            lastVisit = datetime.fromtimestamp( int(cookie['WWhenH'].value)/1000 )
                            requestor.setLastVisit( lastVisit )
                        except Exception, e:
                            # Invalid visit timing resets it
                            requestor.setLastVisit( datetime.now() )
                    reqId = requestor.id
                except Exception, e:
                    # If no cookies available guess at the last visit as a
                    # week ago.
                    requestor.setLastVisit( datetime.now() - timedelta(7) )
            self.page.setRequestor( requestor )
            try:
                db = bttbDB()
                db.Initialize()
                db.LogPage('%s?%s' % (moduleName, '&'.join(params)), reqId)
                db.Finalize()
            except:
                pass
        except Exception, e:
            # Backup solution is to go to the error page
            from pages.bttbError import bttbError
            self.page = bttbError( e, self.page )
            try:
                db = bttbDB()
                db.Initialize()
                db.LogPage('error:%s?%s' % (moduleName, '&'.join(params)), reqId)
                db.Finalize()
            except:
                pass

    #----------------------------------------------------------------------
    def pageContent(self):
        """
        Display the desired page in the content frame. This is the
        only part that varies from page to page. Everything else is the same
        in the entire website.
        Returns a type (title, scriptArray, content)
        """
        if isinstance(self.page, bttbPage):
            return (self.page.title(), self.page.scripts(), self.page.content())
        return ('BTTB Alumni : Error loading page', [], MapLinks("""
            <h1>Error loading page %s</h1>
            <p>Try going back and reloading the page. Contact
            send:(web@bttbalumni.ca,the webmaster) if the problem
            persists.</p>
            """) % (self.page) )
    
# ==================================================================

import unittest
class testPage(unittest.TestCase):
    def setUp(self):
        self.nav = bttbContentPanel( {'page':['test'], 'user':['2']} )
        self.badNav = bttbContentPanel( {'page':['hello']} )

    def testBasics(self):
        (navTitle, navScripts, navContent) = self.nav.pageContent()
        (badNavTitle, badNavScripts, badNavContent) = self.badNav.pageContent()
        self.assert_( navContent.find('home') )
        self.assert_( badNavContent.find('Error loading page') )

if 'SCRIPT_FILENAME' in os.environ:
    # Uncomment for debugging
    import cgitb; cgitb.enable()
    import cgi
    params = cgi.parse()
    panel = bttbContentPanel( params )
    (title, scripts, content) = panel.pageContent()
    if not content: content = ErrorMsg('Blank page loaded', params)
    print 'Content-type: text/html\n'
    print title + '|' + '#!#'.join([MapLinks(a) for a in scripts]) + '|' + content
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
