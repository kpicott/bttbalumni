#!/usr/bin/python
"""
Master file which loads the correct page based on URL parameters

 Possible forms of page URLs:
        http://www.bttbalumni.ca
        http://www.bttbalumni.ca/
        http://www.bttbalumni.ca#page
        http://www.bttbalumni.ca/#page
        http://www.bttbalumni.ca/#page&u=1&v=2&...
        http://www.bttbalumni.ca/cgi-bin/nav.cgi#page
        http://www.bttbalumni.ca/cgi-bin/nav.cgi#page&u=1&v=2&...

 Only the last two will ever be seen in the browser address bar by the user.

 See bttbAlumni.css for the page layout description.

"""
import os
from bttbConfig import MapLinks, Error
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
        self.show_header()

    #----------------------------------------------------------------------
    def show_navigation(self):
        """
        Display the navigation buttons with Javascript embedded
        """
        # The menus list has two types of entry:
        #   [link, text] for main level links
        #   [text, [children]] for dropdowns, where [children] = [[link,text],...]
        # Prepend a "?" to the link for a disabled coming-soon style
        menus = [ ['/#home', '<img src="/Images/icon-home.png">']
                , ['70th Anniversary', [ ['/#store2017', 'Buy Tickets']
                                       , ['/#golf2017', 'Golf Tournament']
                                       , ['?/#calendar2017', 'Calendar of Events']
                                       , ['?/#parade2017', 'Parade']
                                       , ['?/#concert2017', 'Concert']
                                       , ['?/#news2017', 'Reunion News']
                                       ]
                  ]
                , ['Alumni',    [ ['/#profiles', 'Profiles']
                                , ['/#register', 'My Profile']
                                , ['/#newsletters', 'News']
                                , ['/#security', 'Privacy Information']
                                ]
                  ]
                , ['Memories',  [ ['/#wallaceb', 'Wallace B. Wallace']
                                , ['/#drumMajors', 'Drum Majors']
                                , ['/#memorials', 'Memorials']
                                , ['/#photos', 'Pictures']
                                , ['/#memories', 'Memories']
                                , ['/#tunes', 'Music Clips']
                                , ['?/#headChaperones', 'Former Head Chaperones']
                                , ['?/#bandExecutive', 'Former Band Executive']
                                , ['?/#boosterExecutive', 'Former Band Booster Executive']
                                ]
                  ]
                , ['Links',     [ ['http://teentourband.org', 'BTTB']
                                , ['http://teentourboosters.com', 'Band Boosters']
                                , ['http://www.cbc.ca/archives/entry/doug-wrights-family', 'Doug Wright']
                                , ['?bandPhotoAlbums', 'Band Photo Albums']
                                , ['?YouTube', 'BTTB on YouTube']
                                ]
                  ]
                , ['Committee', [ ['/#committee', 'Old Committee Page']
                                , ['?/#approve', 'Pending Approvals']
                                , ['?/#countdowns', 'Edit Countdowns']
                                , ['?/#newsAdd', 'Edit News Items']
                                , ['?/#database', 'Database Queries']
                                , ['?/#reunionData2017', 'Reunion Data']
                                , ['?/#webwork', 'Website Development Plan']
                                , ['?/#download', 'Download Alumni Data']
                                ]
                  ]
                ]
        try:
            print """
<div class="site-top">
  <div class="header" id="header">
    <div class="header-container">
      <div class="header">
        <div class="header-title">
          <a href="#home"><img align="middle" src="/Images/SiteLogoSmall.png"></a>
  	      <div class="title tooltip">BTTB Alumni
		    <span class="tooltiptext">Reconnect with old friends and help keep the history of the Burlington Teen Tour Band alive</span>
          </div>
        </div>
        <div class="header-menu">
          <div class="contact"><a href="/#contact"><i class="fa fa-envelope-o">&nbsp;</i>Contact Us</a></div>
          <div id="login"><i class="fa fa-key">&nbsp;</i>Login</div>
          <div id="welcome"><i class="fa fa-user">&nbsp;</i>Register</div>
        </div>
      </div>
    </div>
    <div class="nav-container">
      <div class="nav">"""

            for menu_entry in menus:
                committee_class = ''
                if 'Committee' in menu_entry:
                    committee_class = ' class="committee-only"'
                if isinstance(menu_entry[1], list):
                    menu_name = menu_entry[0]
                    submenu = menu_entry[1]
                    print '<div class="dropdown"%s>' % committee_class
                    print '  <button class="dropbtn">%s</button>' % menu_name
                    print '  <div class="content">'
                    for (link, text) in submenu:
                        if link[0] == '?':
                            print '    <a href="#" class="coming-soon"><span>%s</span></a>' % text
                        else:
                            print '    <a href="%s">%s</a>' % (link, text)
                    print '  </div>'
                    print '</div>'
                else:
                    print '<a %s href="%s">%s</a>' % (committee_class, menu_entry[0], menu_entry[1])
            print """
      </div>
    </div>
  </div>
</div>
"""

        except Exception, e:
            Error( 'Showing navigation', e )

    #----------------------------------------------------------------------
    def show_login_dialog(self):
        """
        Display the modal login dialog at a fixed point on the page
        """
        print """
<div id="login-dialog" style="display:none;" class="modal shadow">
  <form id="login-form" name="login-form" class="modal-content animate" action="/cgi-bin/login.cgi" onclick="javascript:check_login()">
    <div class="imgcontainer">
      <span onclick="javascript:close_login()" class="close" title="Close Modal">&times;</span>
      <img src="/Images/img_avatar2.png" alt="Avatar" class="avatar">
    </div>
    <div class="login-container">
      <label><b>Username</b></label>
      <input type="text" placeholder="Enter Username" id="user" name="user" required>
      <label><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="password" required>
      <button class="loginbtn" type="submit">Login</button>
    </div>
    <div class="login-container">
      <button type="button" onclick="javascript:close_login()" class="cancelbtn">Cancel</button>
      <span title='Default user name is FIRST LAST, no password' class="psw">
      <div style="display:none;" id='login-error'>Login not recognized</div>
      <a href='mailto:bttb@picott.ca?subject=Forgot My Login&body=I forgot my login information, please reset my password and mail back my id.'href="">Forgot Login?</a></span>
    </div>
  </form>
</div>
"""

    #----------------------------------------------------------------------
    def show_content(self):
        """
        Display the desired page in the content frame. This is the
        only part that varies from page to page. Everything else is the same
        in the entire website.
        """
        print """<div id='content'>
        <NOSCRIPT>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <p><b>
        <font color='red'>Warning: This site relies heavily on JavaScript,
        which you currently have disabled. Please enable it or use another
        browser in order to enjoy the full experience.</font></b></p>
        <p>
        <a href='/pages/javascript.html'>See this page</a> for information on how
        to turn it back on.
        </p>
        </NOSCRIPT>
        </div>"""
    
    #----------------------------------------------------------------------
    def show_head(self):
        """
        Print out the standard <head> section for the page
        """
        print '<head>'
        print "<link rel='alternate' type='application/rss+xml' title='BTTB Alumni News' href='http://www.bttbalumni.ca/cgi-bin/bttbRSS.cgi' />"
        print '<title>BTTB Alumni</title>'
        print MapLinks( """
        <link href="https://fonts.googleapis.com/css?family=Raleway|Source+Sans+Pro:700" rel="stylesheet">
        <link rel="shortcut icon" href="/Favicon.ico" type="image/x-icon" />
        <script type='text/javascript' src='__JAVASCRIPTPATH__/bttb2.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/bttbLogin.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/bttbUrlParser.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/prototype.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/images.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/dhtmlHistory.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/scriptaculous.js'></script>
        <script type='text/javascript' src='__JAVASCRIPTPATH__/jquery-3.1.1.min.js'></script>
        """ )
        print MapLinks( """
            <STYLE type='text/css' media='all'>
                @import url( '__CSSPATH__/bttbNav.css' );
                @import url( '__CSSPATH__/bttbPage.css' );
                @import url( '__CSSPATH__/bttbEffects.css' );
                @import url( '__CSSPATH__/font-awesome.min.css' );
            </STYLE>
            """ )
        print '</head>'
    
    #----------------------------------------------------------------------
    def show_header(self):
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
    def show_page(self):
        """
        Master function to display the entire web page
        """
        self.show_head()
        print '<body onresize="onSizeChange()" onload="initialize()">'

        # Fixed position dialog
        self.show_login_dialog()

        print '<div class="page">'

        # Lower left
        self.show_navigation()

        # Lower right
        self.show_content()

        print '</div>'

        print '</body>'

# ==================================================================

import unittest
class testNav(unittest.TestCase):
    def setUp(self):
        self.nav = bttbNavigation()

    def testBasics(self):
        self.nav.show_page()

if 'SCRIPT_FILENAME' in os.environ:
    # Uncomment for debugging
    # import cgitb; cgitb.enable()
    nav = bttbNavigation()
    nav.show_page()
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

