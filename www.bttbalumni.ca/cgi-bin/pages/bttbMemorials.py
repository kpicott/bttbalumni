"""
Manage the Memorials web page
"""

from bttbPageFile import bttbPageFile
from bttbConfig import MapLinks
__all__ = ['bttbMemorials']

class bttbMemorials(bttbPageFile):
    '''Class that generates the committee database query page'''
    def __init__(self):
        '''Set up the page'''
        bttbPageFile.__init__(self, '__ROOTPATH__/memorials.html')
        self.members_only = True

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Memorials'

    def content(self):
        ''':return: a string with the content for this web page.'''
        memorials = [
            ("Elgin", "Corlett", 1947, 1967, "Founder, Director"),
            ("Larry", "Duke", 1947, 1953, "Flute"),
            ("Keith", "Hall", 1947, 1950, "Trombone"),
            ("Roy", "Hall", 1947, 1950, "Percussion"),
            ("Larry", "Oake", 1947, 1953, "Flute"),
            ("Roger", "Hammill", 1954, 1961, "Trombone"),
            ("Rob", "Herdman", 1961, 1965, "Tuba"),
            ("Bob", "Champ", 1962, 1970, "Trumpet"),
            ("Charlie", "Parsons", 1962, 1997, "Equipment Manager, Truck Driver, Chaperone"),
            ("Cathy", "Blezard", 1963, 1968, "Trumpet"),
            ("Cathy", "Corlett", 1963, 1967, "Clarinet "),
            ("Anne", "(Gordon)&nbsp;Hall", 1964, 1970, "Colour Guard"),
            ("Louise", "Dagenais", 1965, 1971, "Majorette"),
            ("Pat", "(Millward)&nbsp;Plummer", 1965, 1975, "Majorette/Flute"),
            ("Pete", "Conway", 1968, 1972, "Percussion"),
            ("Tim", "Watt", 1968, 1973, "Percussion"),
            ("Mary", "Ford", 1968, 1973, "Colour Guard"),
            ("Eric", "Ford", 1968, 1976, "Director"),
            ("Helen 'Lois'", "Hanley", 1968, 1974, "Band Booster"),
            ("Dani", "Jainu", 1969, 1972, "Sousaphone"),
            ("Audrey", "Cook", 1969, 1969, "Clarinet"),
            ("Cindy", "Schmidt", 1972, 1976, "Colour Guard"),
            ("George", "Newell", 1972, 1978, "Booster/Chaperone"),
            ("Nancy", "(Neil)&nbsp;Kerr", 1976, 1981, "Saxophone"),
            ("Don", "Bennett", 1977, 1982, "French Horn"),
            ("Antony", "Roberts", 1981, 1985, "Percussion"),
            ("Paul", "Hill", 1980, 1985, "Flute"),
            ("Willem", "Murray", 1987, 1989, "Percussion")
        ]
        html = MapLinks( """
        <style>
        *
        {
            color:  white;
        }
        </style>
        <p>
        <table width='100%' border='0' cellspacing='5' cellpadding='10' bgcolor='black'>
        <tr valign='top' height='118'><th colspan='3'><img width='600' height='118' border='0' src='__IMAGEPATH__/WeRemember.jpg'></th></tr>
        """ )
        for first,last,first_year,last_year,instrument in memorials:
            html += '<tr valign="center" height="30">'
            html += '<td class="memorial">%s&nbsp;%s</td>' % (first,last)
            html += '<td class="memorial">%d&nbsp;-&nbsp;%d</td>' % (first_year,last_year)
            html += '<td class="memorial">%s</td>' % (instrument)
            html += '</tr>'
        html += '<tr><th>&nbsp;</th></tr>'
        html += '</table></p>'
        html += MapLinks( """
        <p>
        Would you like to remember anyone else from the band? Send the
        information to send:(info@bttbalumni.ca) to honour those who
        have gone before us.
        </p>
        """ )
        return html


# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbMemorials()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
