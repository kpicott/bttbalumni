"""
Page that shows the ordering information for 60th anniversary tickets
"""

from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbTickets']

class bttbTickets(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self): return 'BTTB 60th Anniversary Celebration Tickets'

	def scripts(self):	return ['__JAVASCRIPTPATH__/bttbTickets.js']

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		packages = (
			("The Pride of Burlington", "PrideOfBurlington", 131, 7, 173, 57 ),
			("Strike Up The Band", "StrikeUpTheBand", 179, 7, 221, 57 ),
			("We Are Family", "WeAreFamily", 227, 7, 269, 57 ),
			("The Sound of Music", "TheSoundOfMusic", 275, 7, 317, 57 )
		)
		items = (
			("Friday Social and Barbecue", "FridaySocial", 131, 7, 173, 57),
			("Saturday Parade Participant", "Parade", 179, 7, 221, 57),
			("Saturday Homecoming", "SaturdayHomecoming", 227, 7, 269, 57),
			("Sunday Lunch", "SundayLunch", 275, 7, 317, 57),
			("BTTB Alumni Shirt", "Shirt", 323, 7, 365, 57),
			("60<sup>th</sup> Anniversary Hat", "Hat", 371, 7, 413, 57)
		)
		html = MapLinks("""
		<h1>Tickets Available Now!!!</h1>
		<p>Roll over an image to see details.
		download:(__IMAGEPATH__/PackageOrderForm.doc, Click here to download the order form in Word format) with the detailed information
		download:(__IMAGEPATH__/PackageInformation.doc, in this second Word file)
		or
		download:(__IMAGEPATH__/PackageOrderForm.pdf, Click here to download the order form in PDF format)
		Instructions on where to send the form and payment are
		printed on the form itself. If you have any questions regarding
		the ordering or any of the events
		send:(info@bttbalumni.ca,drop us a line and we'll do our best to answer)
		</p>
		""" )
		html += MapLinks("""
		<table cellpadding='0' cellspacing='0' border='0'>
		<tr>
		<td valign='top'>
			<table cellpadding='0' cellspacing='0' border='0'>
			<tr height='64'><td><img border='0' width='342' height='64'
			 src='__PACKAGEIMAGEPATH__/TicketsPackages.png'
			 alt='Package Deals'
			 usemap='#packageMap'>
			</td>
			</tr><tr>
			<td height='64'><img border='0' width='434' height='64'
			 src='__TICKETITEMPATH__/TicketsALaCarte.png'
			 alt='A La Carte Items'
			 usemap='#itemMap'>
			</td>
			</tr><tr>
			<td valign='center'>
			<p>&nbsp;</p>
			<div style='display:none;' name='ticketText' id='ticketText'>
			</div>
			</td>
			</tr></table>
		</td>
		<td valign='top'>
			<img style='display:none;' name='ticketImage' id='ticketImage' width='442' src='__PACKAGEIMAGEPATH__/TicketsPackages.png'>
		</td>
		</tr></table>
		""" )

		html += "<map id='packageMap' name='packageMap'>"
		for title,image,x1,y1,x2,y2 in packages:
			html += "<area shape='rect' coords='%d,%d,%d,%d'" % (x1,y1,x2,y2)
  			html += " onmouseover='javascript:showTicket(\"Packages\", \"%s\")'" % image
			html += " alt='%s' />" % title
		html += "</map>"
		html += "<map id='itemMap' name='itemMap'>"
		for title,image,x1,y1,x2,y2 in items:
			html += "<area shape='rect' coords='%d,%d,%d,%d'" % (x1,y1,x2,y2)
  			html += " onmouseover='javascript:showTicket(\"IndividualItems\",\"%s\")'" % image
			html += " alt='%s' />" % title
		html += "</map>"
		return html

# ==================================================================

import unittest
class testTickets(unittest.TestCase):
	def testDump(self):
		ticketsPage = bttbTickets()
		print ticketsPage.content()
	
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
