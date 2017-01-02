"""
Page that shows the alumni reunion concert information
"""

from bttbDB import bttbDB
from bttbMember import *
from bttbAlumni import *
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbConcert']

class bttbConcert(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
		try:
			self.alumni = bttbAlumni()
		except Exception, e:
			Error( 'Could not find concert information', e )
	
	def title(self): return 'BTTB Alumni Reunion Concert'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		try:
			if not self.requestor:
				return LoginRequired( 'Concert Signup' )
		except:
			pass
		html = MapLinks("""
		<div class='outlinedTitle'>Re-Union Concert 3:00 pm - Sunday June 17<sup>th</sup>, 2007</div>
		<p>
		Below is a list of the instrumentation available for the concert.
		Select the parts you wish to download in PDF format
		(see link:(http://www.adobe.com) for
		a PDF File Reader called Acrobat if you do not already have it).
		</p>
		<p>
		Click on the "SO FAR" text to reveal the names of those who have
		downloaded that particular part.
		</p>
		<form name="concertMusicForm" id="concertMusicForm" action="javascript:submitForm(\'concertMusicForm\', \'/cgi-bin/bttbConcertMusic.cgi\', null);">
		""" )
		parts = self.alumni.getConcertInstrumentation()
		html += "<table><tr>"
		col = 0
		instCount = 0
		for iName,iId,who in parts:
			instCount = instCount + 1
			if who.find(',') < 0:
				if len(who) > 0:
					whoSize = 1
				else:
					whoSize = 0
			else:
				whoSize = len(who.split(','))
			checked = ""
			if col == 4:
				html += '</tr><tr>'
				col = 0
			col = col + 1
			html += "<td width='25%%' valign='top'><input type='radio' name='part' align='middle'%s value='%s'>%s" % (checked, iId, iName)
			if whoSize > 0:
				html += "&nbsp;<a title='%s' href='#' onClick='Effect.toggle(\"signedUp%d" % (who, instCount)
				html += "\", \"slide\"); return false;'>"
				html += " (%d so far) &hellip;</a>" % whoSize
			else:
				html += " (None yet)"
			html += "<div id='signedUp%d' style='display:none;'>" % instCount
			html += "<div style='background-color:#ffa0a0;"
			html += "border:2px solid red;padding:10px;'>"
			html += who
			html += "</div></div>"
		html += "</tr></table>\n"
		html += MapLinks( """
		<table border='1'><tr><td valign='center'>
		<input type='hidden' name='id' value='%d'>
		We'll have percussion available, and keep in mind only one person can
		play the set. <br>To ensure you have any other instrument you need
		link:(http://www.longandmcquade.com/pdf/lmbandrentbrochure0607-insideON-FINAL.pdf, Long and McQuade in Burlington)
		is offering a rental program the alumni can take advantage of.
		</p>
		</td></tr></table>
		<br>
		<input type='submit' name='submit' value='Reserve My Spot'>
		</form>
		""") % self.requestor.id
		html += MapLinks( """
<p>
Still to come - download of remaining music. Watch for the announcement on
link:(#home, the home page!).
</p>
<p>
Rehearsal opportunities are 7pm-8:30pm Friday May 25<sup>th</sup> and Friday
June 1<sup>st</sup> at the Music Centre. <i>Rehearsals should be followed with
a time of social interaction at a suitable venue.</i>
</p>
<p>
There will be only one combined rehearsal with the current Teen Tour members
at 10:00am on Sunday June 17<sup>th</sup>.
</p>
<h1>Full Concert Lineup</h1>
<div class='indented'>
	<li>Royal Salute</li>
	<li>O Canada</li>
	<li>Strike Up the Band!</li>
	<li>Beatles Medley</li>
	<li>Bugler's Holiday (Trumpet Feature)</li>
	<li>Junior Redcoats</li>
	<li>Cordoba</li>
	<li>Final Countdown</li>
	<li>Czardas</li>
	<li>Queen in Concert</li>
	<li>Yakety Sax (Sax feature)</li>
	<li>Pirates of the Caribbean</li>
	<li>Drum Feature</li>
	<li>Spanish Fever</li>
	<li>2007 Field Show</li>
	<li><b>FINALE</b><ol>
	Never Walk Alone<br>Pride of Burlington</ol></li>
</div>
		""")
		return html

# ==================================================================

import unittest
class testConcert(unittest.TestCase):
	def testDump(self):
		concertPage = bttbConcert()
		concertPage.requestor = bttbMember()
		print concertPage.content()
	
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
