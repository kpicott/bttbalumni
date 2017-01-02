"""
URL page that says thanks for registering to new alumni
"""

from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
import bttbDB
__all__ = ['bttbEvents']

class bttbEvents(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
		self.db = bttbDB.bttbDB()
		try:
			self.alumni = bttbAlumni()
		except Exception, e:
			Error( 'Could not find event information', e )
	
	def title(self): return 'BTTB Alumni 60th Celebration Events'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		self.db.Initialize()

		html = MapLinks( """
		<h1>Schedule of Events</h1>
		<p>
		Here is the current planned schedule of events. More details will be
		posted as they become available.
		</p>
		<p>
		It is our goal to provide opportunities for former members of the 
		Burlington Teen Tour Band and the Burlington Boys and Girls Band to stay
		connected, to provide networking opportunities and to provide support 
		for the current Burlington Teen Tour Band. 
		</p>
		<p>
		In order to run an event of this magnitude, there will necessarily be a
		charge for events. The prices will be set as affordable as possible. Any
		proceeds we make over and above the costs will be used to support the
		BTTB. 
		</p>
		<p>
		When the packages are set, they will be posted here and you will be able
		to purchase advance tickets, including special package discounts.
		</p>

		<img src='__IMAGEPATH__/April1.png' width='155' height='18'>
		<div class='eventInfo'>
			<b class='eventInfo'>&raquo;&nbsp;</b> Official unveiling of commissioned art<br>
			<b class='eventInfo'>&raquo;&nbsp;</b> Hamilton Place Concert
		</div>

		<img src='__IMAGEPATH__/May25.png' width='148' height='24'>
		<div class='eventInfo'>
			<b class='eventInfo'>&raquo;&nbsp;</b> Alumni concert band rehearsal, 7:00 - 8:30 p.m. (<i>Music Centre</i>) <br>
		</div>

		<img src='__IMAGEPATH__/June1.png' width='139' height='18'>
		<div class='eventInfo'>
			<b class='eventInfo'>&raquo;&nbsp;</b> Alumni concert band rehearsal, 7:00 - 8:30 p.m. (<i>Music Centre</i>) <br>
		</div>

		""" )

		eventList = self.db.GetEvents()
		html += MapLinks("<img src='__IMAGEPATH__/June14.png' width='187' height='19'>")
		html += "<div class='eventInfo'>"
		for event in eventList:
			if event.eventDate.day != 14: continue
			html += self.getEvent( event.summary, event.location, event.description, event.eventDate.hour, event.eventDate.minute )
		html += '</div>\n'
		html += MapLinks("<img src='__IMAGEPATH__/June15.png' width='155' height='17'>")
		html += "<div class='eventInfo'>"
		for event in eventList:
			if event.eventDate.day != 15: continue
			html += self.getEvent( event.summary, event.location, event.description, event.eventDate.hour, event.eventDate.minute )
		html += '</div>\n'
		html += MapLinks("<img src='__IMAGEPATH__/June16.png' width='184' height='19'>")
		html += "<div class='eventInfo'>"
		for event in eventList:
			if event.eventDate.day != 16: continue
			html += self.getEvent( event.summary, event.location, event.description, event.eventDate.hour, event.eventDate.minute )
		html += '</div>\n'
		html += MapLinks("<img src='__IMAGEPATH__/June17.png' width='160' height='21'>")
		html += "<div class='eventInfo'>"
		for event in eventList:
			if event.eventDate.day != 17: continue
			html += self.getEvent( event.summary, event.location, event.description, event.eventDate.hour, event.eventDate.minute )
		html += '</div>\n'

		self.db.Finalize()
		return html

	def getEvent(self,name,location,description,hour,minute):
		"""
		Add the event summary with a slideable attendance list to content.
		"""
		html = "<b class='eventInfo'>&raquo;&nbsp;%s</b>" % (hour > 12 and ('%d:%02d pm' % (hour-12,minute)) or ('%d:%02d am' % (hour, minute)))
		html += '&nbsp;&nbsp;' + description + ' (<i>' + location + '</i>)'
		eventList = self.db.GetEventAttendees( name )
		if eventList and len(eventList) > 0:
			html += "&nbsp;-&nbsp;<a href='#' onClick='Effect.toggle(\"attend"
			html += name + "\", \"slide\"); return false;'>"
			html += "%d attending &hellip;</a>" % (len(eventList))
			html += "<div id='attend" + name + "' style='display:none;'>"
			html += "<div style='background-color:#ffa0a0;"
			html += "border:2px solid red;padding:10px;'>"
			html += '<table cellpadding="0" cellspacing="0" width="100%" border="0"><tr>'
			column = 0
			for first,nee,last in eventList:
				if column == 3:
					html += '</tr><tr>'
					column = 0
				column = column + 1
				html += '<td>' + SensibleName(first,nee,last) + '</td>'
			html += '</tr></table></div></div>'
		html += '<br>'
		return html

# ==================================================================

import unittest
class testEvents(unittest.TestCase):
	def testDump(self):
		eventsPage = bttbEvents()
		print eventsPage.content()
	
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
