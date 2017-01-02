"""
URL page that shows committee member biographical information
"""

from bttbConfig import *
from bttbPage import bttbPage
__all__ = ['bttbBios']

def _posAt(top,left):
	"""Utility class to provide string for class positioning"""
	return "style='position:absolute; width: 200px; height: 200px; top: %dpx; left: %dpx;'" % (top,left)

def _hideAt(top,left):
	"""Utility class to provide string for class positioning"""
	return "style='position:absolute; overflow: auto; display:none; width: 200px; height: 200px; top: %dpx; left: %dpx;'" % (top,left)

uniqueId = 0
class CommitteeMember:
	def __init__(self,name,position):
		global uniqueId
		uniqueId = uniqueId + 1
		self.idx = uniqueId
		self.title = "<b>" + name + "</b><br><i class='subtext'>" + position + "</i>"
		self.text = []
		self.image = MapLinks("__INSTRUMENTPATH__/Marching.png")

	def setEmail(self,email):
		self.text.append( EmailLink(email,email) )

	def setDayJob(self,job):
		self.text.append( "<i>" + job + "</i>" )

	def setInstrument(self,instrument):
		self.image = MapLinks("__INSTRUMENTPATH__/" + instrument + ".png")

	def setImage(self,image):
		self.image = image

	def addLine(self,line):
		self.text.append(line)

	def getText(self):
		return "<p>" + "<br>".join(self.text) + "</p>";

	def toString(self,top,left):
		html = "<div class='bio' id='committee%d'>" % self.idx
		# -----------------------------------------------------------------
		# Note that the display:none has to be a separate style element since
		# that's what the scriptaculous library uses to do its effects.
		# -----------------------------------------------------------------
		html += "	<div class='bioPic' %s " % _posAt(top, left)
		html += "	id='committee%d_pic'" % self.idx
		html += "	 onMouseOver='crossFade(\"committee%d_pic\",\"committee%d_detail\");'" % (self.idx, self.idx)
		html += "	 onMouseOut='crossFade(\"committee%d_detail\",\"committee%d_pic\");'>" % (self.idx, self.idx)
		html += "		<img border='0' width='200' height='200' src='" + self.image + "'>"
		html += "	</div>"
		html += "	<div class='bioDetail' %s " % _hideAt(top, left)
		html += "	id='committee%d_detail'" % self.idx
		html += "	 onMouseOver='crossFade(\"committee%d_pic\",\"committee%d_detail\");'" % (self.idx, self.idx)
		html += "	 onMouseOut='crossFade(\"committee%d_detail\",\"committee%d_pic\");'>" % (self.idx, self.idx)
		html += self.getText()
		html += " </div>"
		html += "	<div class='bioTitle' %s " % _posAt(top+200,left)
		html += "    id='committee%d_title'>" % self.idx
		html += self.title
		html += "	</div>"
		html += "</div>\n"
		return html

# Page load is a simple template operation with generic pathnames replaced by
# their configured equivalents.

class bttbBios(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self): return 'BTTB Alumni 60th Celebration Committee Bios'

	def scripts(self):	return ['__CSSPATH__/bttbBios.css']

#----------------------------------------

	def content(self):
		ron = CommitteeMember( "Ron Wilk", "Organizing Committee Co-Chair" )
		ron.setEmail( "ronwilk@worldchat.com" )
		ron.addLine( "580 Huron Drive" )
		ron.addLine( "Burlington, ON" )
		ron.addLine( "L7T 3V5" )
		ron.addLine( "905 632-4207" )
		ron.setInstrument( "TenorSax" )

		#----------------------------------------

		lana = CommitteeMember( "Lana Schroeder-Wilk", "Organizing Committee Co-Chair" )
		lana.setEmail( "ronwilk@worldchat.com" )
		lana.addLine( "580 Huron Drive" )
		lana.addLine( "Burlington, ON" )
		lana.addLine( "L7T 3V5" )
		lana.addLine( "905 632-4207" )
		lana.setInstrument( "Flute" )

		#----------------------------------------

		rob = CommitteeMember( "Rob Bennett", "Steering Committee" )
		rob.setDayJob( "Managing Director, BTTB" )
		rob.setEmail( "BennettR@burlington.ca" )
		rob.addLine( "905 335-7807" )
		rob.setImage( MapLinks("__BIOIMAGESPATH__/RobBennett.png") )

		#----------------------------------------

		bill = CommitteeMember( "Bill Hughes", "Steering Committee" )
		bill.setDayJob( "Music Director BTTB" )
		bill.setEmail( "daskipper@sympatico.ca" )
		bill.addLine( "R.R.#1" )
		bill.addLine( "Princeton" )
		bill.addLine( "Ontario" )
		bill.addLine( "N0J 1V0" )
		bill.addLine( "Phone: 519-458-4518" )
		bill.setImage( MapLinks("__BIOIMAGESPATH__/BillHughes.png") )

		# -----------------------------------

		don = CommitteeMember( "Don Allan", "Steering Committee" )
		don.setDayJob( "Retired Music Director BTTB" )
		don.setEmail( "allnangus@sympatico.ca" )
		don.addLine( "905-639-2230" )
		don.setInstrument( "MusicDirector" )

		# -----------------------------------

		gary = CommitteeMember( "Gary Bourke", "Steering Committee" )
		gary.setDayJob( "Band Boosters President" )
		gary.setEmail( "gbourke@cogeco.ca" )
		gary.addLine( "4203 Spruce Ave. " )
		gary.addLine( "Burlington L7L 1L1 " )
		gary.addLine( "Home 905 681 0809 " )
		gary.addLine( "Cell 905 638 1503 " )
		gary.addLine( "Work 905 335 9227" )
		gary.addLine( """<p>
Gary Bourke, President of the Burlington Teen Tour Band Boosters 2006 & 2007, is an active parent and band supporter.  Past Booster Board ‘Director at Large’ in 2004 and 2005, Gary introduced to the non-profit charity Booster organization the sponsorship committee, successfully attracting corporate funding in support of the Burlington Teen Tour Band.  Gary has chaperoned the Band on numerous tours - Holland and France, Iowa, St. Louis and many other performances.  
</p><p>
Gary began his commitment in 2001 when flute-playing daughter Rachelle joined the Burlington Junior Redcoats.  Gary and his wife, Bev, immediately became involved in the Boosters and have not stopped since.  
</p><p>
Gary is owner of the 38-year-old Burlington-based ‘Professional Painting and Decorating Co.’ in the commercial/industrial market.   Along with son Jason, who owns his own painting company, Gary provided much of the resources for the painting of the Music Centre during the Enhancement Program in 2006.
</p><p>
In his spare time, Gary is also is a girl’s Rep. soccer coach during soccer season.  
</p><p>
Gary’s drive and enthusiasm will add much to the Alumni’s 60th Anniversary. 
</p>
		""")
		gary.setImage( MapLinks("__BIOIMAGESPATH__/GaryBourke.png") )

		# -----------------------------------

		robg = CommitteeMember( "Rob Garnier", "Steering Committee" )
		robg.setDayJob( "Retired Marching Director" )
		robg.setEmail( "robert.garnier@sympatico.ca" )
		robg.setInstrument( "MarchingDirector" )

		# -----------------------------------

		bob = CommitteeMember( "Bob Webb", "Steering Committee" )
		bob.setDayJob( "Retired Marching Director" )
		bob.setEmail( "robertwebb@sympatico.ca" )
		bob.addLine( "14 Pirie Drive" )
		bob.addLine( "Dundas Ontario L9H 6X5" )
		bob.addLine( "Phone 905-628-9824 or 905-627-8445" )
		bob.addLine( "Fax 905-628-8709" )
		bob.addLine( "Cell 416-605-3195" )
		bob.setInstrument( "MarchingDirector" )
		bob.setImage( MapLinks("__BIOIMAGESPATH__/BobWebb.png") )

		# -----------------------------------

		gordon = CommitteeMember( "Gordon Cameron", "Media/Publicity" )
		gordon.setEmail( "gordon_m_cameron@yahoo.ca" )
		gordon.setInstrument( "Clarinet" )
		gordon.addLine( "770 Hager Avenue, #903" )
		gordon.addLine( "Burlington, Ontario" )
		gordon.addLine( "L7S 1X1" )
		gordon.addLine( "(905) 639-8720" )
		gordon.addLine( """
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
		gordon.setImage( MapLinks("__BIOIMAGESPATH__/GordonCameron.png") )

		# -----------------------------------

		susie = CommitteeMember( "Susan Dittmer", "Parade" )
		susie.setEmail( "susan.dittmer@sympatico.ca" )
		susie.addLine( "2238 Heidi Ave.  " )
		susie.addLine( "Burlington, ON" )
		susie.addLine( "L7M 3W4 " )
		susie.addLine( "905-336-7564" )
		susie.setInstrument( "Clarinet" )

		# -----------------------------------

		randy = CommitteeMember( "Randall Keast", "Membership/Registration" )
		randy.setEmail( "rgkeast@hotmail.com" )
		randy.setInstrument( "Trumpet" )

		# -----------------------------------

		sandi = CommitteeMember( "Sandi Remedios", "Treasurer" )
		sandi.setEmail( "sremedios@cogeco.ca" )
		sandi.setInstrument( "MarchingDirector" )
		sandi.setImage( MapLinks("__BIOIMAGESPATH__/SandiRemedios.png") )

		# -----------------------------------

		doug = CommitteeMember( "Doug McLean", "History of Band" )
		doug.setEmail( "mcleanmedia@sympatico.ca" )
		doug.addLine( "1399 Centre Road," )
		doug.addLine( "Carlisle, ON  L8N 2Z7" )
		doug.addLine( "Telephone:  905-689-8914" )
		doug.addLine( "Cellular:      905-464-0898" )
		doug.addLine( "Office Line:  905-366-1758" )
		doug.addLine( """
<p>
Doug joined the "Burlington Boys & Girls Band" in 1963 and began taking music lessons from Elgin Corlett at the Band's "new" rehearsal facilities amid the automotive fumes on the second floor of Fischer's Garage on John Street. Doug served on the Band Executive as both Auditor 1969 and Treasurer in 1970, the years that the Band first performed at The Rose Bowl, Disney Land, Orange Bowl and Disney World. Although Doug quit the band in 1972 he found it difficult to actually leave and travelled to the Cotton Bowl and the first Philadelphia Parade of Champions as a guest.
 </p><p>
Doug continues to "blow his horn" and is currently a member of the Top Hat Marching Orchestra. He was one of the "Dirty Dozen" original members of that organization which was a spin-off of the Clown Band that Bob Webb, Ken Wright and others had organized for Toronto's professional soccer team - The Blizzard. Although he wasn't an original Clown he has always been comfortable being one.
 </p><p>
Doug has always enjoyed the challenges of fund raising and for the 60th Anniversary Celebrations has coordinated an Artist's Commission with John Newby (another Band Alumni) for both fund raising purposes and as a memorial tribute to the event... and to help us all retain some of the great memories that the ravages of time tend to cause us to forget.
</p>
		""" )
		doug.setInstrument( "Euphonium" )
		doug.setImage( MapLinks("__BIOIMAGESPATH__/DougMcLean.png") )

		# -----------------------------------

		kevin = CommitteeMember( "Kevin Picott", "Webmaster" )
		kevin.setEmail( "bttb@picott.ca" )
		kevin.addLine( "2390 Arnold Crescent" )
		kevin.addLine( "Burlington, ON L7P 4G3" )
		kevin.addLine( "(905) 635-4242" )
		kevin.addLine( """
		<p>
		Kevin was in the band from 1978 through 1987, was section leader,
		on the loading crew, in the Soup Group, Dixieland Band, Dance Band,
		You Name It, and continues to play with local Burlington Swing Band
		'No Strings Attached'. A long-time computer geek Kevin spends his
		spare time volunteering for various organizations, including of course
		the BTTBBI now that his son Daniel is a full-fledged band member.
		</p>
		""" )
		kevin.setInstrument( "ValveTrombone" )
		kevin.setImage( MapLinks("__BIOIMAGESPATH__/KevinPicott.png") )

		# -----------------------------------

		ken = CommitteeMember( "Ken Wright", "Events" )
		ken.setEmail( "Kenneth.Wright@peelpolice.on.ca" )
		ken.addLine( "2405 Baxter Crescent" )
		ken.addLine( "L7M 4C9" )
		ken.addLine( "905-336-9412" )
		ken.addLine( "Cell 905-464-6183" )
		ken.addLine( """<p>
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
		ken.setImage( MapLinks("__BIOIMAGESPATH__/KenWright.png") )

		#----------------------------------------

		html = ron.toString( 50, 0 )
		html += lana.toString( 50, 222 )
		html += rob.toString( 50, 444 )
		#--------------------
		html += bill.toString( 332, 0 )
		html += don.toString( 332, 222 )
		html += gary.toString( 332, 444 )
		#--------------------
		html += robg.toString( 614, 0 )
		html += bob.toString( 614, 222 )
		html += gordon.toString( 614, 444 )
		#--------------------
		html += susie.toString( 896, 0 )
		html += randy.toString( 896, 222 )
		html += sandi.toString( 896, 444 )
		#--------------------
		html += doug.toString( 1178, 0 )
		html += ken.toString( 1178, 222 )
		html += kevin.toString( 1178, 444 )

		return html

# ==================================================================

import unittest
class testBios(unittest.TestCase):
	def testDump(self):
		biosPage = bttbBios()
		print biosPage.content()
	
if __name__ == '__main__':
	unittest.main()


# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
