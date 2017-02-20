"""
Web page showing the reunion purchasing information
"""

from bttbConfig import *
from bttbPage import bttbPage
__all__ = ['bttbReunion2017']

# Page load is a simple template operation with generic pathnames replaced by
# their configured equivalents.

class bttbReunion2017(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self): return 'BTTB Alumni 70th Anniversary Reunion'

	def scripts(self):
		return [ '__CSSPATH__/bttbReunion2017.css'
			   , '__JAVASCRIPTPATH__/bttbReunion2017.js'
			   ]

#----------------------------------------
	def announcement(self):
		'''Copy of the Facebook announcement, in HTML format'''
		return MapLinks('''<p>The 70<sup>th</sup> Anniversary organizing committee is pleased
to finally announce our plans for this year's big reunion taking place over Sound of Music Weekend (June 16-18).</p>
<p>
On Friday we'll be holding a golf tournament at Indian Wells. Ticket price will include golf,
lunch, dinner and a goody bag. For those who don't want to golf, but do want to come for supper
their will be an option to do that as well.
</p>
<p>
We all know what the Saturday of Sound of Music means -- it's parade time. Our goal is to have
as many former members lined up and marching through downtown Burlington as possible. I mean,
there are thousands of us out there, so there's no reason why we can't make this the biggest
Teen Tour Band ever to step off. We're in the midst of finalizing the music selections, but we
are working to ensure that the marching order will include meaningful pieces from all eras of
the Band's history. For those who'd like to participate but no longer play, there will be an
opportunity to march along with the Band. For those who are unable to walk the route a float
will be provided.
</p>
<p>
Following the parade will be a barbecue lunch and then free time to spend with your old Band
friends before the evening's main event -- a reunion to be held at Central Arena. This will be
your opportunity to mix and mingle with Band members, staff, boosters and supporters from the
last 70 years. The night will feature music, food, drinks and lots of memories. (We also plan
to go light on the speeches.)
</p>
<p>
On Sunday, there will be a very special performance as the Alumni join with the current Burlington
Teen Tour Band to play the closing concert of the Sound of Music Festival at the Central Park
Bandshell. Music will be provided in advance so you can get cracking before we rehearse all together.
</p>
<p>
The cost for the entire weekend (with the exception of the golf tournament) is $130 + HST if you pay
before April 15 and $150 + HST thereafter. For that price you not only get admission to all reunion
events, but a hat and golf shirt (which will also be the parade uniform), a lanyard and a few other
special surprises. Tickets to specific events and clothing can also be purchased separately. See below
for details.
</p>
<p>
If you have any questions about the event, feel free to ask them either via our link:(https://www.facebook.com/groups/2218469082,Facebook page)
or via e-mail at send:(info@bttbalumni.ca).
</p>
<p>
And don't forget to tell all your Band friends about the 70th reunion. After all, it the people who truly make an event like this a success.
</p>
''')

#----------------------------------------

	def content(self):
		html = '''<div id='info'>%s</div>
		<h2>Click on the images to purchase tickets and merchandise</h2>
		<a onclick='go_to_store()'><div id='allin'></div></a>
		<a onclick='go_to_store()'><div id='parade'></div></a>
		<a onclick='go_to_store()'><div id='saturday'></div></a>
		<a onclick='go_to_store()'><div id='hat'></div></a>
		<a onclick='go_to_store()'><div id='shirt'></div></a>
		<a onclick='go_to_store()'><div id='golf'></div></a>
''' % self.announcement()

		return html

# ==================================================================

import unittest
class testReunion2017(unittest.TestCase):
	def testDump(self):
		reunion2017Page = bttbReunion2017()
		print reunion2017Page.content()
	
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
