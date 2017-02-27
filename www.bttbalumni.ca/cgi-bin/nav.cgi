#!/usr/bin/python
"""
Master file which loads the correct page based on URL parameters
"""

#
# Possible forms of page URLs:
#        http://www.bttbalumni.ca
#        http://www.bttbalumni.ca/
#        http://www.bttbalumni.ca#page
#        http://www.bttbalumni.ca/#page
#        http://www.bttbalumni.ca/#page&u=1&v=2&...
#        http://www.bttbalumni.ca/cgi-bin/nav.cgi#page
#        http://www.bttbalumni.ca/cgi-bin/nav.cgi#page&u=1&v=2&...
#
# Only the last two will ever be seen in the browser address bar by the user.
#
# The page is divided into four zones, similar to frames:
#
#      +-----+--------------------------+
#      |  1  |            2             |
#      +-----+--------------------------+
#      |     |                          |
#      |     |                          |
#      |  3  |            4             |
#      |     |                          |
#      |     |                          |
#      +-----+--------------------------+
#
# 1 = Navigation
# 2 = Title, including semi-transparent fade-out background
# 3 = Title logo
# 4 = Content, controlled by bttbPage contents
#

import os
from bttbConfig import *
import pages

class bttbNavigation:
    """
    Class to handle all of the page navigation within the website. Keeps
    everything consistent and manages persistent information such as user name
    and state.
    """
    #----------------------------------------------------------------------
    def __init__(self):
        self.buttonState = None        # Which buttons are opened
        self.cookie = None            # Cookie values being used
        # Need this early so that error messages can show up
        self.showHeader()

    #----------------------------------------------------------------------
    def showNavigation(self):
        """
        Display the navigation buttons with Javascript embedded
        """
        try:
            print "<div id='mainMenu'>"
            print "<ul id='verticalMenu' class='menu'>"
            print "<li>"
            print MapLinks( "button:(#music, Music, Download music for 70th anniversary parade)" )
            print "</li>"
            print "<li>"
            print MapLinks( "button:(#profiles, Alumni, Keep in touch with other alumni)" )
            print "<ul class='subMenu'>"
            print MapLinks( "buttonSub:(#register, Register, Register yourself to keep in touch)" )
            print MapLinks( "buttonSub:(#profiles, Profiles, See all of the registered alumni)" )
            print MapLinks( "buttonSub:(#register, MyProfile, Edit yur profile information)" )
            print MapLinks( "buttonSub:(http://www.facebook.com/groups/2218469082, Forum, Chat with other alumni in our interactive Facebook forum)" )
            print MapLinks( "buttonSub:(#newsletters, Newsletters, See old Alumni newsletters)" )
            print MapLinks( "buttonSub:(#security, Security, Website security information)" )
            print "</ul>"
            print "</li>"
            print "<li>"
            print MapLinks( "button:(#memories, Memories, Take a stroll down memory lane)" )
            print "<ul class='subMenu'>"
            print MapLinks( "buttonSub:(#photos, Pictures, See images from the past 70 years)" )
            print MapLinks( "buttonSub:(#memories, Memories, Read exciting band stories or add your own)" )
            print MapLinks( "buttonSub:(#drumMajors, DrumMajors, Past Drum Majors)" )
            print MapLinks( "buttonSub:(#wallaceb, WallaceB, Wallace B. Wallace awards)" )
            print MapLinks( "buttonSub:(#tunes, Music, Listen to bands past and present)" )
            print MapLinks( "buttonSub:(#memorials, Memorials, Remember those who have gone before)" )
            print "</ul>"
            print "</li>"
            print "<li>"
            print MapLinks( "button:(#soon_links, Links, See other related websites)" )
            print "<ul class='subMenu'>"
            print MapLinks( "buttonSub:(http://teentourband.org, BTTB, The band that started it all - still going strong)" )
            print MapLinks( "buttonSub:(http://teentourboosters.com, Boosters, Support organization for the band)" )
            print MapLinks( "buttonSub:(https://www.facebook.com/groups/2218469082, Parade, Facebook signup for the 70th Anniversary Band)" )
            print MapLinks( "buttonSub:(#committee, Committee, For Committee use only)" )
            print MapLinks( "buttonSub:(#johnNewby, JohnNewby, Artist commissioned to create a special band painting)" )
            print MapLinks( "buttonSub:(http://archives.cbc.ca/IDC-1-68-2352-13715/arts_entertainment/canadian_comics/clip7, DougWright, Canadian cartoonist responsible for the characters in the band logo)" )
            print "</ul>"
            print "</li>"
            print "<li>"
            print MapLinks( "button:(#home, Home, Return to the home page)" )
            print "</li>"
            print "</div>"
            print "<div id='login' class='login'>"
            print "</div>"
            print "<div style='display:none;' class='mainMenuHighlight' id='mainMenuHighlight'>"
            print MapLinks( "    <img width='39' height='412' src='__MENUPATH__/IconHighlight.png'>" )
            print "</div>"
            print "</div>"

        except Exception, e:
            Error( 'Showing navigation', e )

    #----------------------------------------------------------------------
    def showTitle(self):
        """
        Display the title bar, assumed to be ignored by most
        """
        print MapLinks( """
        <div id='divTop'>
               <img src='__IMAGEPATH__/top_fade140.png' border='0' width='1194' height='140'>
        </div>
        <div id='mainTitle'>
            <img src='__IMAGEPATH__/BTTBAlumni.png' border='0' width='300' height='126'>
        </div>
        <div id='subTitle'>
            <img src='__IMAGEPATH__/Reconnect.png' border='0' width='300' height='57'>
        </div>
        <div id='clustrmap'>
        <a href="http://www2.clustrmaps.com/counter/maps.php?url=http://www.bttbalumni.ca" id="clustrMapsLink"><img width="108" src="http://www2.clustrmaps.com/counter/index2.php?url=http://www.bttbalumni.ca" style="border:1px solid red;" alt="Locations of BTTB visitors" title="Locations of BTTB visitors" id="clustrMapsImg" onError="return clustrMapError();" />
        </a>
        </div>
        """ )


    #----------------------------------------------------------------------
    def showTitleLogo(self):
        """
        Display the title bar logo in the upper left corner.
        This will be a "picture of the week" along with an attached
        animation to blow it up and display a description of it.
        """
        print MapLinks( """
        <div id='logo'>
            link:(#profiles, <img border='0' src='__IMAGEPATH__/SiteLogo.png' width='123' height='110'>)
        </div>
        """ )

    #----------------------------------------------------------------------
    def showContent(self):
        """
        Display the desired page in the content frame. This is the
        only part that varies from page to page. Everything else is the same
        in the entire website.
        """
        print "<div id='contentBox'>"
        print "    <div id='content'>"
        print """
        <NOSCRIPT>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <p><b>
        <font color='red'>Warning: This site relies heavily on JavaScript,
        which you currently have disabled. Please enable it or use another
        browser in order to enjoy the full experience.</font></b></p>
        <p>
        <a href='/javascript.html'>See this page</a> for information on how
        to turn it back on.
        </p>
        </NOSCRIPT>
        """
        print "       </div>"
        print "</div>"
    
    #----------------------------------------------------------------------
    def showHead(self):
        """
        Print out the standard <head> section for the page
        """
        print '<head>'
        print "<link rel='alternate' type='application/rss+xml' title='BTTB Alumni News' href='http://www.bttbalumni.ca/cgi-bin/bttbRSS.cgi' />"
        print '<title>BTTB Alumni</title>'
        print MapLinks( """
        <link rel="shortcut icon" href="/Favicon.ico" type="image/x-icon" />
        <script type='text/javascript' src='__JAVASCRIPTPATH__/bttb.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/bttbLogin.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/bttbUrlParser.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/prototype.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/images.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/dhtmlHistory.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/scriptaculous.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/bttbMenu.js'></script>
        """ )
        if 'HTTP_USER_AGENT' not in os.environ:
            os.environ['HTTP_USER_AGENT'] = 'Firefox'
        if os.environ['HTTP_USER_AGENT'].find('MSIE') >= 0:
            if os.environ['HTTP_USER_AGENT'].find('MSIE 7') >= 0:
                print MapLinks( """
                <STYLE type='text/css' media='all'>
                    @import url( '__CSSPATH__/bttbMenu_IE7.css' );
                    @import url( '__CSSPATH__/bttbAlumni.css' );
                </STYLE>
                """ )
            else:
                print MapLinks( """
                <STYLE type='text/css' media='all'>
                    @import url( '__CSSPATH__/bttbMenu.css' );
                    @import url( '__CSSPATH__/bttbAlumni.css' );
                    @import url( '__CSSPATH__/bttbMenu_IE.css' );
                    @import url( '__CSSPATH__/bttbAlumni_IE.css' );
                </STYLE>
                """ )
        else:
            print MapLinks( """
            <STYLE type='text/css' media='all'>
                @import url( '__CSSPATH__/bttbMenu.css' );
                @import url( '__CSSPATH__/bttbAlumni.css' );
            </STYLE>
            """ )
        print '</head>'
    
    #----------------------------------------------------------------------
    def showHeader(self):
        """
        Print out the standard header for our pages.
        """
        print 'Content-type: text/html; charset=ISO-8859-1'
        print 'Cache-Control: no-cache, must-revalidate, no-store'
        print 'Expires: Mon, 26 Jul 1997 05:00:00 GMT'
        #if self.user:          print 'Set-Cookie: user=' + self.user
        #if self.onCommittee: print 'Set-Cookie: committee=1'
        print 'Pragma: no-cache'
        print
        # Go into IE 6 compatibility mode
        print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'
    
    #----------------------------------------------------------------------
    def showPage(self):
        """
        Master function to display the entire web page
        """
        self.showHead()
        print '<body onresize="onSizeChange()" onload="initialize()">'
        self.showTitle()
        self.showTitleLogo()
        self.showNavigation()
        self.showContent()
        print '</body>'

# ==================================================================

import unittest
class testNav(unittest.TestCase):
    def setUp(self):
        self.nav = bttbNavigation()

    def testBasics(self):
        self.nav.showPage()

if 'SCRIPT_FILENAME' in os.environ:
    # Uncomment for debugging
    # import cgitb; cgitb.enable()
    nav = bttbNavigation()
    nav.showPage()
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

