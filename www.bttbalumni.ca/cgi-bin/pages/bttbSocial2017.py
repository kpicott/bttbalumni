"""
Page that shows the current list of parade participants and lets the currently
signed in user sign up for a specific instrument.
"""
from bttbAlumni import bttbAlumni
from bttbMember import bttbMember
from pages.bttbPage import bttbPage
from bttbConfig import MapLinks, Error
__all__ = ['bttbSocial2017']

#----------------------------------------------------------------------
def page_css():
    ''':return: A string with the CSS specific to this page'''
    return """<style>

/* The social block contains the table with the current registrations */
.social
{
    clear:      both;
    display:    block;
    margin-top: 20px;
}

.social table
{
    border-collapse:  collapse;
    border:           1px solid #d2d2d2;
    margin-below:     20px;
}

.social th, td
{
    text-align:     left;
    padding:        4px;
    border-right:   2px solid #d2d2d2;
    width:          33%%;
}

.social th
{
    background-color: #AF4C50;
    color:            white;
}

/* Main block is the info to the left */
.main-text
{
    width:  600px;
    margin: 20px;
}
.main-text p
{
    margin-top: 20px;
}

/* social-info is a standalone box in the main area */
.social-info
{
    width:      500px;
    margin:     20px;
    padding:    10px;
}

.social-info p
{
    margin:   5px;
}

/* main-image floats to the right in the main area */
.main-image
{
    float:         right;
    margin-bottom: 20px;
}
</style>"""

#----------------------------------------------------------------------
class bttbSocial2017(bttbPage):
    '''Class that generates the parade information page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find parade information', ex )

        # Read in the current list of people going to the social event
        self.alumni_40_50 = []
        self.alumni_60_70 = []
        self.alumni_80_90 = []
        self.alumni_2000 = []
        alumni_registered,_ = self.alumni.process_query( """
                SELECT alumni.first,alumni.nee,alumni.last,alumni.firstYear,alumni.lastYear
                    FROM 2017_social INNER JOIN alumni
                    WHERE alumni.id=2017_social.alumni_id
                        AND alumni.make_public = '1'
                    ORDER by alumni.last""" )
        # Sort them into their decades
        for (first,nee,last,join_year,quit_year) in alumni_registered:
            if len(nee) > 0:
                name = '%s (%s) %s' % (first,nee,last)
            else:
                name = '%s %s' % (first,last)
            mid = (join_year + quit_year) / 2
            if mid < 1960:
                self.alumni_40_50.append( name )
            elif mid < 1980:
                self.alumni_60_70.append( name )
            elif mid < 2000:
                self.alumni_80_90.append( name )
            else:
                self.alumni_2000.append( name )

        # Get a count of those for whom their decade is unknown (or irrelevant, for guests)
        others_registered,_ = self.alumni.process_query( """
                SELECT name
                    FROM 2017_social
                    WHERE id=NULL
                    ORDER by name""" )
        self.guest_count = 0
        if others_registered:
            self.guest_count = len(others_registered)

    #----------------------------------------------------------------------
    def title(self):
        ''':return: The page title'''
        return '2017 Saturday Night Social Event'

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''

        html = page_css()

        html += MapLinks( """
<div>

<div class="main-image"><img src="/Images70th/Social.jpg"></div>

<div class="main-text">

<h1>Saturday Night Social Event</h1>
<div class='social-info box_shadow'>
<p>
Join your fellow alumni at Central Arena for an evening of sharing memories and making new ones.
</p>
<p>
The social kicks off with an upscale barbecue catered by Leave It To Us. The menu includes an assortment of salads, fresh fruit, desserts and a whole lot of delicious treats from the grill.
</p>
<p>
For those who what to wet their whistles, alcoholic and non-alcoholic refreshments will be served.
</p>
<p>
Although the night is all about reconnecting and socializing there will also be some entertainment including big screen video presentations, a photo booth, a room full of memorabilia and a performance from the Rose Bowl-bound Teen Tour Band.
</p>
<p>
The only thing the night will be missing is a lot of long speeches.
</p>
<p>
DJ Jeff Chalmers (Boom 97.3) will provide a selection of music from the past 70 years through the evening.
</p>
<p>
The night will end with a late evening food service along with lots of hugs and smiles as we say our good nights.
</p>
<p>
This is an event not to be missed.
</p>
</div>

</div>
""" )

        alumni_40_50 = '<br>'.join( self.alumni_40_50 )
        alumni_60_70 = '<br>'.join( self.alumni_60_70 )
        alumni_80_90 = '<br>'.join( self.alumni_80_90 )
        alumni_2000 = '<br>'.join( self.alumni_2000 )

        html += MapLinks( """
        <div class='social'>
        <p>
        See any familiar names to be in attendance from the various decades? If you see any that
        are missing maybe you should
        <a href="mailto:myBandFriend?subject='BTTB Alumni 70th Anniversary'&body='The BTTB Alumni are going strong! I plan on going to the 70th Anniversary reunion, you can too at http://www.bttbalumni.ca'">drop them a line and let them know what a fun time they might be missing!</a>
        </p>
        <table width='100%%'>
        <tr>
            <th>1940's and 1950's</th>
            <th>1960's and 1970's</th>
            <th>1980's and 1990's</th>
            <th>2000 to present</th>
        </tr>
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
        </table>
        <p>
        ...plus %d other guests ...
        </p>
        </div>
        """ % (alumni_40_50, alumni_60_70, alumni_80_90, alumni_2000, self.guest_count) )

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbSocial2017()
    TEST_PAGE.requestor = bttbMember()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
