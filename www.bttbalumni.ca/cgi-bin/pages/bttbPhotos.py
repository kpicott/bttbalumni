"""
Page that shows a bunch of submitted photos
"""

from bttbPage import bttbPage
from bttbPictures import displayCelebrationPictures
from bttbConfig import MapLinks
__all__ = ['bttbPhotos']

class bttbPhotos(bttbPage):
    '''Class that generates the photo page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Photos'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = ""

#        html += """
#        <object width="425" height="350">
#           <param name="movie" value="http://www.youtube.com/v/u4x4lAWbYaM"></param>
#           <param name="wmode" value="transparent"></param>
#           <embed src="http://www.youtube.com/v/u4x4lAWbYaM"
#            type="application/x-shockwave-flash" wmode="transparent"
#            width="425" height="350"></embed>
#       </object>
#        """

        html += """
        <div class='newsTitle'>Automated YouTube Search of "Burlington Teen
        Tour Band"<span class='newsDate'>Click an image to start the
        video</span></div>
        <iframe id="videos_list" name="videos_list"
            src="http://www.youtube.com/videos_list?tag=Burlington Teen Tour Band"
            scrolling="auto" width="265" height="400" frameborder="0" marginheight="0"
            marginwidth="0"></iframe> """

        html += displayCelebrationPictures()

        photos = [
             ("Photo1", "1997-06-07", "50th Anniversary Colour Guard")
        ,    ("Photo2", "1997-06-07", "50th Anniversary Flutes and Saxes")
        ,    ("Photo3", "1997-06-07", "50th Anniversary Trombone Rank")
        ,    ("Photo4", "1979-01-01", "Mr. Allan in the old rehearsal hall")
        ,    ("Photo5", "1981-05-05", "Philly '81!")
        ,    ("Photo6", "1982-06-01", "The Music Centre c1982")
        ,    ("Photo7", "1970-11-21", "BTTB on the street, 1970")
        ,    ("Photo8", "1981-05-05", "Philly '81, all bands on deck")
        ,    ("Photo9", "1980-01-01", "Rose Bowl '80 - hurry up and wait")
        ,    ("MarchingThroughTime", "1997-06-07", "The band marches through the ages")
        ]
        html += MapLinks( """
        <p>
        If you have any photos you'd like to share
        send:(info@bttbalumni.ca,send them to us) with a descriptive
        caption and the approximate date it was taken.
        </p>
        """)
        column = 0
        html += "<table cellspacing='5'><tr>"
        for photo_file, _, info in photos:
            if column == 4:
                html += "</tr><tr>"
                column = 0
            column = column + 1
            html += MapLinks( "<th valign='top' width='100'><a target='photos' href='__PHOTOPATH__/%s.jpg'><img width='100' src='__PHOTOPATH__/%s_Small.jpg'></a>" % (photo_file, photo_file))
            html += "<br>%s" % info
            html += "</th>"
        html += "</tr></table>"
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbPhotos()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
