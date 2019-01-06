"""
Page that shows the current list of known drum majors
"""
from pages.bttbPage import bttbPage
from bttbAlumni import bttbAlumni
from bttbConfig import Error
__all__ = ['bttbDrumMajors']

#----------------------------------------------------------------------
def page_css():
    ''':return: A string with the CSS specific to this page'''
    return """<style>
.approved
{
    background-image:   url("__IMAGEPATH__/Plaque.jpg");
    background-color:   #888822;
    height:             60px;
    width:              155px;
    text-align:         center;
    padding-top:        10px;
    font-weight:        bold;
    float:              left;
    margin:             5px;
}
.pending
{
    background-image:   url("__IMAGEPATH__/PlaquePending.jpg");
    background-color:   #888888;
    height:             60px;
    width:              155px;
    text-align:         center;
    padding-top:        10px;
    font-weight:        bold;
    float:              left;
    margin:             5px;
}
</style>"""

#----------------------------------------------------------------------
class bttbDrumMajors(bttbPage):
    '''Class that generates the Former Drum Major page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find alumni information', ex )

        # Get all of the drum major information from the database
        self.drum_majors,_ = self.alumni.process_query( """
                SELECT first_name,nee,last_name,alumni_id,first_year,last_year,approved
                FROM drum_majors""" )

        # Get any alumni information referenced by the drum major database
        known_alumni,_ = self.alumni.process_query( """
                SELECT alumni.first_name,alumni.nee,alumni.last_name,alumni.id
                FROM alumni
                INNER JOIN drum_majors
                WHERE alumni.id=drum_majors.alumni_id""" )
        self.alumni_info = {}
        for (first_name,nee,last_name,alumni_id) in known_alumni:
            self.alumni_info[id] = (first_name,nee,last_name,alumni_id)

    def title(self):
        ''':return: The page title'''
        return 'BTTB Drum Majors'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = page_css()
        html += """<h1>Past Drum Majors</h1>
        <p>
        It's a big responsibility, to be in charge of such a large group of
        kids in a performance situation, but these people did it consistently.
        We honour them for the work they did, the leadership they showed, and
        the help they gave to us all.
        </p>
        """
        for (first_name, nee, last_name, alumni_id, first_year, last_year, approved) in self.drum_majors:
            html += "<div class='%s'>" % ['pending','approved'][approved]
            if len(nee) > 0:
                name = "%s (%s) %s" % (first_name, nee, last_name)
            else:
                name = "%s %s" % (first_name, last_name)

            # At a certain length the names overflow
            if len(name) > 18:
                html += "<span style='font-size: 8pt'>%s</span>" % name
            else:
                html += name

            # If either year is defined then add that information
            if first_year == 0:
                first_year = last_year
            if last_year == 0:
                last_year = first_year
            if first_year > 0:
                if first_year == last_year:
                    html += "<br>%d" % first_year
                else:
                    html += "<br>%d %d" % (first_year, last_year)

            html += "</div>"
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
