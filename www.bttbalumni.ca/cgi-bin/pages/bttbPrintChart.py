"""
Page that shows the current list of prints ordered.
Hardcoded for now, but I may stick it in a database if desirable.
"""

from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbPrintChart']

class bttbPrintChart(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
		# ---
		self.gicleeNoNumber = 0;
		giclee = [1, 2, 3, 4, 5]
		self.gicleeNumbered = len(giclee);
		self.giclee = {}
		# ---
		artist = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13]
		self.artistNumbered = len(artist);
		self.artistNoNumber = 0;
		self.artist = {}
		# ---
		self.alreadyFramed = [100]
		# ---
		self.limitedNoNumber = 0;
		limited = [
			  1,   2,   3,   4,   5,   6,   7,        9,  10,       12,  13,  14,  15,
			 16,                 20,                 24,                 28,
			           33,                           39,  40,  41,  42,  43,  44,
			 46,  47,  48,           51,                       56,
			 61,       63,  64,            67,            70,  71,  72,  73,       75,
			 76,  77,                                          86,            89,
			      92,            95,       97,  98,  99,      101, 102, 103, 104,
			          108,           111, 112,      114,      116,
			          123, 124,      126,                130, 131, 132,
			     137, 138, 139,                          145,      147,
			                    155, 156,           159, 160,
			               169,                     174,           177,
			     182,                                                   193, 194, 195,
			196, 197, 198, 199, 200, 201, 202, 203,      205, 206, 207, 208, 209, 210,
			211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225,
			226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240,
			241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251
			]
		self.limitedNumbered = len(limited);
		self.limited = {}
		# ---
		for number in limited:
			self.limited[number] = 1
		for number in artist:
			self.artist[number] = 1
		for number in giclee:
			self.giclee[number] = 1
	
	def title(self): return 'BTTB John Newby Print Numbers'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		html = """
		<h1>John Newby Print Numbers Requested</h1>
		<p>
		Prints already requested are crossed out. How about
		ordering your band uniform or hat number?
		</p>
		"""
		#----------------------------------------------------------------------
		html += "<p><table border='1' width='100%'>"
		html += "<tr><td colspan='5'><h2>$350 Giclee Prints - Sold %d</h2></td></tr>" % (self.gicleeNumbered)
		for col in range(1,6):
			html += "<td style='background-repeat: no-repeat; background-position: center center;' align='center' width='16'"
			if col in self.giclee:
				html += " background='/JohnNewby/Negate.png'"
			html += '>%d/%d' % (col, col)
			html += '</td>'
		html += "</tr></table>"
		html += "</p>"
		#----------------------------------------------------------------------
		html += "<p><table border='1' width='100%'>"
		html += "<tr><td colspan='15'><h2>$250 Artist Prints - Sold %d (%d with specified numbers)</h2></td></tr>" % (self.artistNoNumber + self.artistNumbered, self.artistNumbered)
		for col in range(1,16):
			html += "<td style='background-repeat: no-repeat; background-position: center center;' align='center' width='16'"
			if col in self.artist:
				html += " background='/JohnNewby/Negate.png'"
			html += '>%d' % col
			html += '</td>'
		html += "</tr></table>"
		html += "</p>"
		#----------------------------------------------------------------------
		html += "<p>"
		html += "<table border='1'>"
		html += "<tr><td colspan='51'><h2>$125 Limited Edition Prints - Sold %d (%d with specified numbers)</h2></td></tr>" % (self.limitedNumbered + self.limitedNoNumber, self.limitedNumbered)
		for row in range(0,18):
			html += '<tr>'
			html += "<td align='right'>"
			html += "<b>%d&nbsp;-&nbsp;%d</b>" % (row * 25 + 1, row * 25 + 25)
			html += "</td>"
			for col in range(1,26):
				index = row * 25 + col
				html += "<td style='background-repeat: no-repeat; background-position: center center;' align='center'"
				if index in self.limited:
					html += " background='/JohnNewby/Negate.png'"
				html += '>%d' % index
				html += '</td>'
			html += '</tr>'
		html += "</table>"
		html += "</p><p><b>NOTE:</b> Already framed prints available: "
		for col in self.alreadyFramed:
			html += "#" + str(col) + " "
		html += "</p>"
		return html

# ==================================================================

import unittest
class testPrintChart(unittest.TestCase):
	def testDump(self):
		printChartPage = bttbPrintChart()
		print printChartPage.content()
	
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
