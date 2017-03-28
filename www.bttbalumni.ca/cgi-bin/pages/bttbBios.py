"""
URL page that shows 60th Anniversary Reunion committee member biographical information
"""

from bttbConfig import MapLinks, EmailLink
from bttbPage import bttbPage
__all__ = ['bttbBios']

def position_at(top,left):
    """Utility class to provide string for class positioning"""
    return "style='position:absolute; width: 200px; height: 200px; top: %dpx; left: %dpx;'" % (top,left)

def hide_at(top,left):
    """Utility class to provide string for class positioning"""
    return "style='position:absolute; overflow: auto; display:none; width: 200px; height: 200px; top: %dpx; left: %dpx;'" % (top,left)

class CommitteeMember(object):
    '''Class to manage the committee member information'''
    UNIQUE_ID = 0
    def __init__(self,name,position):
        '''Set up the committee member'''
        CommitteeMember.UNIQUE_ID = CommitteeMember.UNIQUE_ID + 1
        self.idx = CommitteeMember.UNIQUE_ID
        self.title = "<b>" + name + "</b><br><i class='subtext'>" + position + "</i>"
        self.text = []
        self.image = MapLinks("__INSTRUMENTPATH__/Marching.png")

    def set_email(self,email):
        '''Define the committee member's email'''
        self.text.append( EmailLink(email,email) )

    def set_day_job(self,job):
        '''Define the committee member's day job'''
        self.text.append( "<i>" + job + "</i>" )

    def set_instrument(self,instrument):
        '''Define the committee member's instrument'''
        self.image = MapLinks("__INSTRUMENTPATH__/" + instrument + ".png")

    def set_image(self,image):
        '''Define the committee member's picture'''
        self.image = image

    def add_line(self,line):
        '''Add a line to the committee member bio'''
        self.text.append(line)

    def get_html(self):
        '''Get the bio in HTML form'''
        return "<p>" + "<br>".join(self.text) + "</p>"

    def to_string(self,top,left):
        '''Convert the bio to an HTML string'''
        html = "<div class='bio' id='committee%d'>" % self.idx
        # -----------------------------------------------------------------
        # Note that the display:none has to be a separate style element since
        # that's what the scriptaculous library uses to do its effects.
        # -----------------------------------------------------------------
        html += "    <div class='bioPic' %s " % position_at(top, left)
        html += "    id='committee%d_pic'" % self.idx
        html += "     onMouseOver='crossFade(\"committee%d_pic\",\"committee%d_detail\");'" % (self.idx, self.idx)
        html += "     onMouseOut='crossFade(\"committee%d_detail\",\"committee%d_pic\");'>" % (self.idx, self.idx)
        html += "        <img border='0' width='200' height='200' src='" + self.image + "'>"
        html += "    </div>"
        html += "    <div class='bioDetail' %s " % hide_at(top, left)
        html += "    id='committee%d_detail'" % self.idx
        html += "     onMouseOver='crossFade(\"committee%d_pic\",\"committee%d_detail\");'" % (self.idx, self.idx)
        html += "     onMouseOut='crossFade(\"committee%d_detail\",\"committee%d_pic\");'>" % (self.idx, self.idx)
        html += self.get_html()
        html += " </div>"
        html += "    <div class='bioTitle' %s " % position_at(top+200,left)
        html += "    id='committee%d_title'>" % self.idx
        html += self.title
        html += "    </div>"
        html += "</div>\n"
        return html

# Page load is a simple template operation with generic pathnames replaced by
# their configured equivalents.

class bttbBios(bttbPage):
    '''Class that generates the committee database query page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
 
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni 60th Celebration Committee Bios'

#----------------------------------------

    def content(self):
        ''':return: a string with the content for this web page.'''
        ron = CommitteeMember( "Ron Wilk", "Organizing Committee Co-Chair" )
        ron.set_email( "ronwilk@worldchat.com" )
        ron.add_line( "580 Huron Drive" )
        ron.add_line( "Burlington, ON" )
        ron.add_line( "L7T 3V5" )
        ron.add_line( "905 632-4207" )
        ron.set_instrument( "TenorSax" )

        #----------------------------------------

        lana = CommitteeMember( "Lana Schroeder-Wilk", "Organizing Committee Co-Chair" )
        lana.set_email( "ronwilk@worldchat.com" )
        lana.add_line( "580 Huron Drive" )
        lana.add_line( "Burlington, ON" )
        lana.add_line( "L7T 3V5" )
        lana.add_line( "905 632-4207" )
        lana.set_instrument( "Flute" )

        #----------------------------------------

        rob = CommitteeMember( "Rob Bennett", "Steering Committee" )
        rob.set_day_job( "Managing Director, BTTB" )
        rob.set_email( "BennettR@burlington.ca" )
        rob.add_line( "905 335-7807" )
        rob.set_image( MapLinks("__BIOIMAGESPATH__/RobBennett.png") )

        #----------------------------------------

        bill = CommitteeMember( "Bill Hughes", "Steering Committee" )
        bill.set_day_job( "Music Director BTTB" )
        bill.set_email( "daskipper@sympatico.ca" )
        bill.add_line( "R.R.#1" )
        bill.add_line( "Princeton" )
        bill.add_line( "Ontario" )
        bill.add_line( "N0J 1V0" )
        bill.add_line( "Phone: 519-458-4518" )
        bill.set_image( MapLinks("__BIOIMAGESPATH__/BillHughes.png") )

        # -----------------------------------

        don = CommitteeMember( "Don Allan", "Steering Committee" )
        don.set_day_job( "Retired Music Director BTTB" )
        don.set_email( "allnangus@sympatico.ca" )
        don.add_line( "905-639-2230" )
        don.set_instrument( "MusicDirector" )

        # -----------------------------------

        gary = CommitteeMember( "Gary Bourke", "Steering Committee" )
        gary.set_day_job( "Band Boosters President" )
        gary.set_email( "gbourke@cogeco.ca" )
        gary.add_line( "4203 Spruce Ave. " )
        gary.add_line( "Burlington L7L 1L1 " )
        gary.add_line( "Home 905 681 0809 " )
        gary.add_line( "Cell 905 638 1503 " )
        gary.add_line( "Work 905 335 9227" )
        gary.add_line( """<p>
Gary Bourke, President of the Burlington Teen Tour Band Boosters 2006 & 2007, is an active parent and band supporter.  Past Booster Board "Director at Large" in 2004 and 2005, Gary introduced to the non-profit charity Booster organization the sponsorship committee, successfully attracting corporate funding in support of the Burlington Teen Tour Band.  Gary has chaperoned the Band on numerous tours - Holland and France, Iowa, St. Louis and many other performances.  
</p><p>
Gary began his commitment in 2001 when flute-playing daughter Rachelle joined the Burlington Junior Redcoats.  Gary and his wife, Bev, immediately became involved in the Boosters and have not stopped since.  
</p><p>
Gary is owner of the 38-year-old Burlington-based "Professional Painting and Decorating Co." in the commercial/industrial market.   Along with son Jason, who owns his own painting company, Gary provided much of the resources for the painting of the Music Centre during the Enhancement Program in 2006.
</p><p>
In his spare time, Gary is also is a girl's Rep. soccer coach during soccer season.  
</p><p>
Gary's drive and enthusiasm will add much to the Alumni's 60th Anniversary. 
</p>
        """)
        gary.set_image( MapLinks("__BIOIMAGESPATH__/GaryBourke.png") )

        # -----------------------------------

        robg = CommitteeMember( "Rob Garnier", "Steering Committee" )
        robg.set_day_job( "Retired Marching Director" )
        robg.set_email( "robert.garnier@sympatico.ca" )
        robg.set_instrument( "MarchingDirector" )

        # -----------------------------------

        bob = CommitteeMember( "Bob Webb", "Steering Committee" )
        bob.set_day_job( "Retired Marching Director" )
        bob.set_email( "robertwebb@sympatico.ca" )
        bob.add_line( "14 Pirie Drive" )
        bob.add_line( "Dundas Ontario L9H 6X5" )
        bob.add_line( "Phone 905-628-9824 or 905-627-8445" )
        bob.add_line( "Fax 905-628-8709" )
        bob.add_line( "Cell 416-605-3195" )
        bob.set_instrument( "MarchingDirector" )
        bob.set_image( MapLinks("__BIOIMAGESPATH__/BobWebb.png") )

        # -----------------------------------

        gordon = CommitteeMember( "Gordon Cameron", "Media/Publicity" )
        gordon.set_email( "gordon_m_cameron@yahoo.ca" )
        gordon.set_instrument( "Clarinet" )
        gordon.add_line( "770 Hager Avenue, #903" )
        gordon.add_line( "Burlington, Ontario" )
        gordon.add_line( "L7S 1X1" )
        gordon.add_line( "(905) 639-8720" )
        gordon.add_line( """
        <p>
Gordon was in the band from 1989 to 2005 and was the
clarinet section leader for 1994-1995. An
award-winning journalist, Gordon edited a Community
Newspaper in Alberta before returning to Burlington to
work in Communications with the Ontario Community
Newspapers Association (OCNA). He now works in
Government Relations for OCNA, dealing primarily with
Queen's Park. 
</p>
        """)
        gordon.set_image( MapLinks("__BIOIMAGESPATH__/GordonCameron.png") )

        # -----------------------------------

        susie = CommitteeMember( "Susan Dittmer", "Parade" )
        susie.set_email( "susan.dittmer@sympatico.ca" )
        susie.add_line( "2238 Heidi Ave.  " )
        susie.add_line( "Burlington, ON" )
        susie.add_line( "L7M 3W4 " )
        susie.add_line( "905-336-7564" )
        susie.set_instrument( "Clarinet" )

        # -----------------------------------

        randy = CommitteeMember( "Randall Keast", "Membership/Registration" )
        randy.set_email( "rgkeast@hotmail.com" )
        randy.set_instrument( "Trumpet" )

        # -----------------------------------

        sandi = CommitteeMember( "Sandi Remedios", "Treasurer" )
        sandi.set_email( "sremedios@cogeco.ca" )
        sandi.set_instrument( "MarchingDirector" )
        sandi.set_image( MapLinks("__BIOIMAGESPATH__/SandiRemedios.png") )

        # -----------------------------------

        doug = CommitteeMember( "Doug McLean", "History of Band" )
        doug.set_email( "mcleanmedia@sympatico.ca" )
        doug.add_line( "1399 Centre Road," )
        doug.add_line( "Carlisle, ON  L8N 2Z7" )
        doug.add_line( "Telephone:  905-689-8914" )
        doug.add_line( "Cellular:      905-464-0898" )
        doug.add_line( "Office Line:  905-366-1758" )
        doug.add_line( """
<p>
Doug joined the "Burlington Boys & Girls Band" in 1963 and began taking music lessons from Elgin Corlett at the Band's "new" rehearsal facilities amid the automotive fumes on the second floor of Fischer's Garage on John Street. Doug served on the Band Executive as both Auditor 1969 and Treasurer in 1970, the years that the Band first performed at The Rose Bowl, Disney Land, Orange Bowl and Disney World. Although Doug quit the band in 1972 he found it difficult to actually leave and travelled to the Cotton Bowl and the first Philadelphia Parade of Champions as a guest.
 </p><p>
Doug continues to "blow his horn" and is currently a member of the Top Hat Marching Orchestra. He was one of the "Dirty Dozen" original members of that organization which was a spin-off of the Clown Band that Bob Webb, Ken Wright and others had organized for Toronto's professional soccer team - The Blizzard. Although he wasn't an original Clown he has always been comfortable being one.
 </p><p>
Doug has always enjoyed the challenges of fund raising and for the 60th Anniversary Celebrations has coordinated an Artist's Commission with John Newby (another Band Alumni) for both fund raising purposes and as a memorial tribute to the event... and to help us all retain some of the great memories that the ravages of time tend to cause us to forget.
</p>
        """ )
        doug.set_instrument( "Euphonium" )
        doug.set_image( MapLinks("__BIOIMAGESPATH__/DougMcLean.png") )

        # -----------------------------------

        kevin = CommitteeMember( "Kevin Picott", "Webmaster" )
        kevin.set_email( "bttb@picott.ca" )
        kevin.add_line( "2390 Arnold Crescent" )
        kevin.add_line( "Burlington, ON L7P 4G3" )
        kevin.add_line( "(905) 635-4242" )
        kevin.add_line( """
        <p>
        Kevin was in the band from 1978 through 1987, was section leader,
        on the loading crew, in the Soup Group, Dixieland Band, Dance Band,
        You Name It, and continues to play with local Burlington Swing Band
        'No Strings Attached'. A long-time computer geek Kevin spends his
        spare time volunteering for various organizations, including of course
        the BTTBBI now that his son Daniel is a full-fledged band member.
        </p>
        """ )
        kevin.set_instrument( "ValveTrombone" )
        kevin.set_image( MapLinks("__BIOIMAGESPATH__/KevinPicott.png") )

        # -----------------------------------

        ken = CommitteeMember( "Ken Wright", "Events" )
        ken.set_email( "Kenneth.Wright@peelpolice.on.ca" )
        ken.add_line( "2405 Baxter Crescent" )
        ken.add_line( "L7M 4C9" )
        ken.add_line( "905-336-9412" )
        ken.add_line( "Cell 905-464-6183" )
        ken.add_line( """<p>
Ken Wright played clarinet in the band from 1974 to 1980. Assigned the
nickname of "Nipper", Ken was president of the band in 1977. His first
major tour was to England, Holland, and Germany in 1974 and his final
performance was the Tournament of Roses parade on January 1, 1980. Ken's
dad, the late Doug Wright drew his famous Doug Wright's Family cartoon
strip characters in band uniforms in the 70's. The characters are still
being proudly displayed on band insignia. 
</p><p>
After retirement from the band Ken couldn't get parading out of his
blood and got together with Bob Webb and a few friends to form the
Blizzard Clown Band and then the Top Hat Marching Orchestra. Ken has
been a police officer for almost 25 years now. He is married to one of
the original Top Hat banner girls. Ken and Debra's three children have
continued Ken's marching ways and are current band members.
</p>""" )
        ken.set_image( MapLinks("__BIOIMAGESPATH__/KenWright.png") )

        #----------------------------------------

        html = '<link rel="stylesheet" href="/css/bttbBios.css" />'

        html += ron.to_string( 50, 0 )
        html += lana.to_string( 50, 222 )
        html += rob.to_string( 50, 444 )
        #--------------------
        html += bill.to_string( 332, 0 )
        html += don.to_string( 332, 222 )
        html += gary.to_string( 332, 444 )
        #--------------------
        html += robg.to_string( 614, 0 )
        html += bob.to_string( 614, 222 )
        html += gordon.to_string( 614, 444 )
        #--------------------
        html += susie.to_string( 896, 0 )
        html += randy.to_string( 896, 222 )
        html += sandi.to_string( 896, 444 )
        #--------------------
        html += doug.to_string( 1178, 0 )
        html += ken.to_string( 1178, 222 )
        html += kevin.to_string( 1178, 444 )

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbBios()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
