"""
Page that shows the current list of known drum majors
"""
from bttbPage import bttbPage
from bttbConfig import MapLinks
__all__ = ['bttbDrumMajors']

class bttbDrumMajors(bttbPage):
    '''Class that generates the Former Drum Major page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True

    def title(self):
        ''':return: The page title'''
        return 'BTTB Drum Majors'

    def content(self):
        ''':return: a string with the content for this web page.'''
        drum_majors = [
             ("Kerig",       "",            "Ahearn")
        ,    ("Jeff",        "",            "Allen")
        ,    ("George",      "",            "Ashfield")
        ,    ("Phil",        "",            "Austin")
        ,    ("Rob",         "",            "Bennett")
        ,    ("Ashley",      "",            "Benton")
        ,    ("Miles",       "",            "Benton")
        ,    ("Sarah",       "",            "Benton")
        ,    ("Ron",         "",            "Bigelow")
        ,    ("Bob",         "",            "Branch")
        ,    ("Carol",       "Corlett",     "Broadhurst")
        ,    ("Paul",        "",            "Burnip")
        ,    ("Christine",   "Campbell",    "Zsiros")
        ,    ("Cathy",       "Carr",        "Paszt")
        ,    ("Peter",       "",            "Clarke")
        ,    ("Lindsey",     "",            "Crampton")
        ,    ("Gerry",       "",            "Dearing")
        ,    ("Bob",         "",            "Gentile")
        ,    ("Gary",        "",            "Gentile")
        ,    ("Anne",        "Goodyear",    "DeFoa")
        ,    ("Phyllis",     "",            "Gordon")
        ,    ("Brad",        "",            "Hall")
        ,    ("Lea",         "",            "Harrington")
        ,    ("Heather",     "",            "Harris")
        ,    ("Megan",       "",            "Hebert")
        ,    ("John",        "",            "Holman")
        ,    ("Jenny",       "",            "Johnson")
        ,    ("Heather",     "",            "Keenleyside")
        ,    ("MaryAnne",    "Lyons",       "Quaglia")
        ,    ("Sarah",       "",            "MacLeod")
        ,    ("Lorrie-Anne", "",            "Maitland")
        ,    ("Simon",       "",            "Matthews")
        ,    ("Sarah",       "",            "McCleary")
        ,    ("Dave",        "",            "McPetrie")
        ,    ("Bev",         "McCune",      "Norman")
        ,    ("Lisa",        "",            "Nicol")
        ,    ("Nick",        "",            "Quaglia")
        ,    ("Tom",         "",            "Quaglia")
        ,    ("Carol",       "",            "Radford")
        ,    ("Carolyn",     "Ridge",       "Whiskin")
        ,    ("Mike",        "",            "Sharpe")
        ,    ("Scott",       "",            "Shepherd")
        ,    ("Colin",       "",            "Sinclair")
        ,    ("Neal",        "",            "Sinclair")
        ,    ("Kellie",      "",            "Skerett")
        ,    ("Ted",         "",            "Slavin")
        ,    ("Francis",     "",            "Smith")
        ,    ("Alexandra",   "",            "Smyth")
        ,    ("Paul",        "",            "Snyder")
        ,    ("Dustin",      "",            "Steplock")
        ,    ("Gary",        "",            "Stock")
        ,    ("Jeff",        "",            "Thomblison")
        ,    ("Dave",        "",            "Wallace")
        ,    ("Carol",       "",            "Webb")
        ,    ("Allan",       "",            "Whiskin")
        ]
        html = """<h1>Past Drum Majors</h1>
        <p>
        It's a big responsibility, to be in charge of such a large group of
        kids in a performance situation, but these people did it consistently.
        We honour them for the work they did, the leadership they showed, and
        the help they gave to us all.
        </p>
        """
        column = 0
        html += "<table cellspacing='5'><tr>"
        for first, nee, last in drum_majors:
            if column == 4:
                html += "</tr><tr>"
                column = 0
            column = column + 1
            html += MapLinks( "<th width='155' height='60' valign='center' background='__IMAGEPATH__/Plaque.jpg'>" )
            if len(nee) > 0:
                html += "%s (%s) %s" % (first, nee, last)
            else:
                html += "%s %s" % (first, last)
            html += "</th>"
        html += "</tr></table>"
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbDrumMajors()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
