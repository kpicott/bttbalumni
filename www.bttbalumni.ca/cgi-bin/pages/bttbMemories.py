"""
Page that shows the current list of memories, in order by approximate date.
"""

from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
from datetime import datetime,timedelta
__all__ = ['bttbMemories']

def _sortByMemoryDate(x,y):	return cmp(x[2], y[2])
class bttbMemories(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
		try:
			self.alumni = bttbAlumni()
		except Exception, e:
			Error( 'Could not find memory information', e )
	
	def scripts(self): return ['__JAVASCRIPTPATH__/bttbYearFilter.js']

	def title(self): return 'BTTB Alumni Memories'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""

		if self.requestor:
			oldNewsTime = self.requestor.lastVisitTime - timedelta(7)
		else:
			oldNewsTime = datetime(2000,1,1)
		oldNewsTime = oldNewsTime.toordinal()

		memoryList = self.alumni.getMemories()
		html = ""
		memoryList.sort( _sortByMemoryDate )
		startYear = 1947
		endYear = 2007
		if self.param('startYear'):
			startYear = int(self.param('startYear'))
		if self.param('endYear'):
			endYear = int(self.param('endYear'))
		if self.param('all'):
			showAll = True
			allLink = "memories"
			allInfo = "Click here to show only memories that were entered recently"
		else:
			showAll = False
			allLink = "memories?all=1"
			allInfo = "Click here to show all memories in this range"
		html += MapLinks( """
		<table width='100%%'><tr><td>
		<form action="">
		Showing memories between&nbsp;
		<input type='text' onChange='yearsChanged()' size='4' id='startYear'
		value='%d'>
		&nbsp;and&nbsp;
		<input type='text' onChange='yearsChanged()' size='4' id='endYear'
		value='%d'>
		link:(#%s,%s)
		</form>
		</td><td align='right'>
		link:(#addMemory,<img border='0' src='/Buttons/addMemory.png' width='109' height='31'>)
		</form>
		</td></tr></table>
		<div name='yearInfo'>
		""" % (startYear, endYear, allLink, allInfo) )
		# -------------------------
		for alumniId, memory, memoryTime, memoryEntryTime, memoryId in memoryList:
			try:
#				if type(memoryEntryTime) == type(DateTime.DateTime):
				memoryEntryTime = memoryEntryTime.absdate()
			except:
				try:
					memoryEntryTime = memoryEntryTime.toordinal()
				except:
					pass
			if showAll or (memoryEntryTime >= oldNewsTime):
				member = self.alumni.getMemberFromId( alumniId )
				html += "<div id='yearFilter' name='yearFilter' style='display:"
				if memoryTime.year > endYear or memoryTime.year < startYear:
					html += "none"
				else:
					html += "block"
				html += ";' class='year:%d'>" % memoryTime.year
				html += "<div class='date'>"
				if (memoryEntryTime > oldNewsTime) and showAll:
					html += "<img border='0' width='33' height='15' src='"
					html += MapLinks("__IMAGEPATH__/New.png'>&nbsp;")
				html += "%s %s</div>" % (memoryTime.strftime('%Y'), member.fullName())
				html += "<p>%s</p>\n" % memory
				html += "</div>"
		html += "</div>"
		return html

# ==================================================================

import unittest
class testMemories(unittest.TestCase):
	def testDump(self):
		memoryPage = bttbMemories()
		print memoryPage.content()
	
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
