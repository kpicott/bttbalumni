#!env python
"""
Show the committee bios page
"""
from bttbConfig import *

uniqueId = 0

class CommitteeMember:
	def __init__(self,name,position):
		global uniqueId
		uniqueId = uniqueId + 1
		self.idx = uniqueId
		self.title = "<b>" + name + "</b><br><i class='subtext'>" + position + "</i>"
		self.text = []
		self.image = HomeHref() + "/Instruments/Marching.png"

	def setEmail(self,email):
		self.text.append( "<a class='email' href='mailto:" + email + "'>" + email + "</a>" )

	def setDayJob(self,job):
		self.text.append( "<i>" + job + "</i>" )

	def setInstrument(self,instrument):
		self.image = HomeHref() + "/Instruments/" + instrument + ".png"

	def setImage(self,image):
		self.image = image

	def addLine(self,line):
		self.text.append(line)

	def getText(self):
		return "<p>" + "<br>".join(self.text) + "</p>";

	def show(self,top,left):
		print "<div id='committee%d'" % (self.idx)
		print " style='position: absolute; top: %dpx; left: %dpx'>" % (top, left)
		print "	<div class='bioTitle' id='committee%d_title'" % (self.idx)
		print self.title
		print "	</div>"
		# -----------------------------------------------------------------
		# Note that the display:none has to be a separate style element since
		# that's what the scriptaculous library uses to do its effects.
		# -----------------------------------------------------------------
		print "	<div class='bioPic' id='committee%d_pic'" % (self.idx)
		print "	 onMouseOver='crossFade(\"committee%d_pic\",\"committee%d_detail\");'" % (self.idx, self.idx)
		print "	 onMouseOut='crossFade(\"committee%d_detail\",\"committee%d_pic\");'>" % (self.idx, self.idx)
		print "		<img border='0' width='200' height='200' src='" + self.image + "'>"
		print "	</div>"
		print "	<div class='bioDetail' style='display:none;' id='committee%d_detail'" % (self.idx)
		print "	 onMouseOver='crossFade(\"committee%d_pic\",\"committee%d_detail\");'" % (self.idx, self.idx)
		print "	 onMouseOut='crossFade(\"committee%d_detail\",\"committee%d_pic\");'>" % (self.idx, self.idx)
		print self.getText()
		print " </div>"
		print "</div>"

# Page load is a simple template operation with generic pathnames replaced by
# their configured equivalents.

print """
<style type='text/css' media='all'>
.bioTitle
{
	border:				1px solid #888888;
	text-align:			center;
	background-color:	#ccccff;
	position:			absolute;
	top:				0px;
	left:				0px;
	width:				200px;
	height:				50px;
	z-index:			3;
}

.bioPic
{
	display:	block;
	position:	absolute;
	top:		52px;
	left:		0px;
	width:		200px;
	height:		200px;
	z-index:	2;
}

.bioDetail
{
	display:		block;
	position:		absolute;
	top:			52px;
	left:			0px;
	width:			200px;
	height:			200px;
	text-align:		center;
	z-index:		3;
	overflow:		auto;
}
</style>
"""

#----------------------------------------

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
rob.setImage( HomeHref() + "/BioImages/RobBennett.png" )

#----------------------------------------

bill = CommitteeMember( "Bill Hughes", "Steering Committee" )
bill.setDayJob( "Music Director BTTB" )
bill.setEmail( "daskipper@sympatico.ca" )
bill.addLine( "R.R.#1" )
bill.addLine( "Princeton" )
bill.addLine( "Ontario" )
bill.addLine( "N0J 1V0" )
bill.addLine( "Phone: 519-458-4518" )
bill.setImage( HomeHref() + "/BioImages/BillHughes.png" )

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
gary.setImage( HomeHref() + "/BioImages/Boosters.png" )

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

# -----------------------------------

gordon = CommitteeMember( "Gordon Cameron", "Media/Publicity" )
gordon.setEmail( "gordon_m_cameron@yahoo.ca" )
gordon.setInstrument( "ColourGuard" )

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

doug = CommitteeMember( "Doug McLean", "History of Band" )
doug.setEmail( "mcleanmedia@sympatico.ca" )
doug.addLine( "1399 Centre Road," )
doug.addLine( "Carlisle, ON  L8N 2Z7" )
doug.addLine( "Telephone:  905-689-8914" )
doug.addLine( "Cellular:      905-464-0898" )
doug.addLine( "Office Line:  905-366-1758" )
doug.setInstrument( "Euphonium" )

# -----------------------------------

kevin = CommitteeMember( "Kevin Picott", "Webmaster" )
kevin.setEmail( "bttb@picott.ca" )
kevin.addLine( "2390 Arnold Crescent" )
kevin.addLine( "Burlington, ON L7P 4G3" )
kevin.addLine( "(905) 635-4242" )
kevin.setInstrument( "Trombone" )

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
ken.setImage( HomeHref() + "/BioImages/KenWright.png" )

#----------------------------------------

ron.show( 50, 0 )
lana.show( 50, 222 )
rob.show( 50, 444 )
#--------------------
bill.show( 322, 0 )
don.show( 322, 222 )
gary.show( 322, 444 )
#--------------------
robg.show( 594, 0 )
bob.show( 594, 222 )
gordon.show( 594, 444 )
#--------------------
susie.show( 866, 0 )
randy.show( 866, 222 )
doug.show( 866, 444 )
#--------------------
kevin.show( 1138, 0 )
ken.show( 1138, 222 )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
