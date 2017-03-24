"""
Page that shows the current list of known Wallace B. Wallace winners
"""

from bttbDB import bttbDB
from bttbPage import bttbPage
from bttbConfig import MapLinks
__all__ = ['bttbWallaceb']

class bttbWallaceb(bttbPage):
    '''Class that generates the Wallace B. Wallace page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.__db = bttbDB()
        if __name__ == '__main__':
            self.__db.TurnDebugOn()
        self.__db.Initialize()

    def title(self):
        ''':return: The page title'''
        return 'BTTB Wallace B. Wallace Awards'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks( """
        <h1>Wallace B. Wallace Awards</h1>
        <p>
        <table>
        <tr><th>
        <img src='__IMAGEPATH__/WallaceBWallace.png' width='195' height='257' border='0'>
        </th><td>
        Were you, or do you know someone who was the recipient of one of
        the prestigious Wallace B. Wallace awards? If so, send the information
        to us at send:(wallacebwallace@bttbalumni.ca).
        Include the name of the recipient, the year received (guess if you
        don't know exactly), and the particular reason they won the award.
        We'll post them here as we get them. With any luck we'll be able to
        fill in the entire list and you'll see how some things transcend
        generations. If <b>you</b> won but would rather not have your name
        shown here we can accommodate that too.
        </td></tr>
        </table>
        </p>
        <h2>The Origin Story - by Dave Wallace</h2>
        <p class='quotable'>
        I never WON the WBW award ... I invented it.
         </p>
        <p class='quotable'>
        Bob Webb and I were sitting around in his office at the City Hall one
        day, (so I assume that would have been the summer of '71 or '72
        perhaps,) and I was thumbing through a trophy catalogue.
        I was reading the descriptions of the various figures that go on top
        of these things, i.e. man w/ laurel wreath, golfer, bowler, runner,
        etc. when I read "HALF HORSE".
         </p>
        <p class='quotable'>
        When we actually saw it was the back half ... the lightbulbs went off
        above both our heads.  We actually ordered a trophy with the intent
        that I would pay for it and I thought of it as my legacy to the band.
        At Bob's suggestion it became the "Wallace B Wallace" award.  The
        inscription read "presented annually to the most deserving member,
        Burlington Teen Tour Band".  There actually was a physical trophy but
        because we'd ordered it from some company through the mail, it didn't
        come for weeks.  I put it in a box somewhere at home and forgot about
        it until we decided to actually present it at the gathering we had
        (like the annual meeting,) in the winter.  By then ... I couldn't
        actually find it.  It did turn up among all my junk several years
        later.  By then I figured it was too late to bother about.
        </p>
        """)
        wallace_list = self.__db.GetWallaceList()
        for _,display_name,year,description,_ in wallace_list:
            html += '<div class="outlinedTitle">'
            html += '%d - %s' % (year, display_name.replace(' ', '&nbsp;'))
            html += '</div>'
            html += '<div class="sectionBody">'
            html += description.lstrip().rstrip()
            html += '</div>'
        html += '</p>'
        self.__db.Finalize()
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbWallaceb()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
