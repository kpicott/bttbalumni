"""
Page that shows the alumni reunion weekend sponsors
"""

from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbSponsors']

class bttbSponsors(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self): return 'BTTB Alumni Reunion Weekend Sponsors'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		html = MapLinks( """
			<div class="outlinedTitle">
			A Big Thank You! to all of the Anniversary Reunion Weekend Sponsors
			</div>
			<table cellspacing='20'>
			<tr>
				<th colspan='2'><img src='__SPONSORIMAGEPATH__/Boosters.png'
					width='229' height='126'
					title='Burlington Teen Tour Band Boosters Inc. - Funding and BBQ'
					alt='BTTBB Inc.'></th>
				<th><img src='__SPONSORIMAGEPATH__/BetterBitters.png'
					 width='214' height='86'
					 title='Better Bitters Microbrewery - Homecoming beer and wine'
					 alt='Better Bitters Microbrewery'></th>
			</tr>
			<tr>
				<th><img src='__SPONSORIMAGEPATH__/CityAutomotive.png'
					 width='100' height='100'
					 title='City Automotive - Alumni weekend lanyards'
					 alt='City Automotive'></th>
				<th><img src='__SPONSORIMAGEPATH__/Terra.png'
					 width='173' height='71'
					 title='Terra Greenhouses - Centrepieces'
					 alt='Terra Greenhouses'></th>
				<th><img src='__SPONSORIMAGEPATH__/Yamaha.png'
					 width='174' height='50'
					 title='Yamaha - Parade Drums'
					 alt='Yamaha'></th>
			</tr>
			<tr>
				<th><img src='__SPONSORIMAGEPATH__/PearlStreetCafe.png'
					 title='Pearl Street Cafe - Homecoming catering'
					 width='159' height='81'
					 alt='Pearl Street Cafe'></th>
				<th><img src='__SPONSORIMAGEPATH__/WSI.jpg'
					 width='116' height='61'
					 title='Waste Services - Alumni weekend totes'
					 alt='Waste Services'></th>
				<th><img src='__SPONSORIMAGEPATH__/CoachCanada.png'
					 width='150' height='61'
					 title='Coach Canada - Eddie Graf Band'
					 alt='Coach Canada'></th>
			</tr>
			<tr>
				<th><img src='__SPONSORIMAGEPATH__/McLeanMedia.png'
					 title='McLean Media - Staff, handout, and golf balls'
					 width='150' height='109'
					 alt='McLean Media'></th>
				<th>&nbsp;</th>
				<th><img src='__SPONSORIMAGEPATH__/SmartFlyer.png'
					 width='192' height='90'
					 title='Smart Flyer - Advertising and handout'
					 alt='Smart Flyer'></th>
			</tr>
			</table>
			<p>
			Contact us at send:(info@bttbalumni.ca) if you or someone you know
			would like to help out as well. Every little bit helps!
			</p>
		""" )
		return html

# ==================================================================

import unittest
class testSponsors(unittest.TestCase):
	def testDump(self):
		sponsorsPage = bttbSponsors()
		print sponsorsPage.content()
	
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
