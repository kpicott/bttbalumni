
"""
Page that shows the current list of memories, in order by approximate date.
"""

from bttbPage import bttbPage
__all__ = ['bttbMenuTest']

class bttbMenuTest(bttbPage):
    def __init__(self):
        bttbPage.__init__(self)

    #----------------------------------------------------------------------
    def scripts(self): return ['''CSS:
.container {
    overflow: hidden;
    background-color: #333;
    font-family: Arial;
}

.container a {
    float: left;
    font-size: 16px;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

.dropdown {
    float: left;
    overflow: hidden;
}

.dropdown .dropbtn {
    font-size: 16px;
    border: none;
    outline: none;
    color: white;
    padding: 14px 16px;
    background-color: inherit;
}

.container a:hover, .dropdown:hover .dropbtn {
    background-color: red;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
}

.dropdown-content a {
    float: none;
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    text-align: left;
}

.dropdown-content a:hover {
    background-color: #ddd;
}

.dropdown:hover .dropdown-content {
    display: block;
}
''']

    #----------------------------------------------------------------------
    def title(self): return 'BTTB Alumni Menu Test'

    #----------------------------------------------------------------------
    def content(self):
        """
        Return a string with the content for this web page.
        """
        return '''
<div class="container">
  <a href="#home"><img src="/Images/icon-home.png"></a>
  <div class="dropdown">
    <button class="dropbtn">70th Anniversary</button>
    <div class="dropdown-content">
      <a href="#">Buy Tickets</a>
      <a href="#">Golf Tournament</a>
      <a href="#">News</a>
      <a href="#">Parade</a>
      <a href="#">Concert</a>
    </div>
  </div>
  <div class="dropdown">
    <button class="dropbtn">Alumni</button>
    <div class="dropdown-content">
      <a href="#">Profiles</a>
      <a href="#">My Profile</a>
      <a href="#">News</a>
      <a href="#">Security Information</a>
      <a href="#">Privacy Information</a>
    </div>
  </div>
  <div class="dropdown">
    <button class="dropbtn">Memories</button>
    <div class="dropdown-content">
      <a href="#">Wallace B. Wallace</a>
      <a href="#">Drum Majors</a>
      <a href="#">Memorials</a>
      <a href="#">Pictures</a>
      <a href="#">Memories</a>
      <a href="#">Music Clips</a>
    </div>
  </div>
  <div class="dropdown">
    <button class="dropbtn">Links</button>
    <div class="dropdown-content">
      <a href="#">BTTB</a>
      <a href="#">Band Boosters</a>
      <a href="#">Doug Wright</a>
    </div>
  </div>
  <div class="dropdown">
    <button class="dropbtn">Contact Us</button>
    <div class="dropdown-content">
      <a href="#">General Information</a>
      <a href="#">Golf Tournament</a>
      <a href="#">Website Questions</a>
    </div>
  </div>
  <div class="dropdown">
    <button class="dropbtn">Committee</button>
    <div class="dropdown-content">
      <a href="#">Database Queries</a>
      <a href="#">Approve Members</a>
      <a href="#">Download Alumni Data</a>
      <a href="#"></a>
    </div>
  </div>
</div>

<h3>Dropdown Menu inside a Navigation Bar</h3>
'''

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbMenuTest()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
