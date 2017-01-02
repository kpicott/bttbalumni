"""
Page that shows the current list of alumni who have paid for registration.
"""

import re
from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbPaid']

class bttbPaid(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
		self.committeeOnly = True
		try:
			self.alumni = bttbAlumni()
		except Exception, e:
			Error( 'Could not find alumni information', e )
	
	def title(self): return 'BTTB Alumni Paid Up For Anniversary Celebration'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		html = MapLinks( """
		<div class='outlinedTitle'>Alumni Paid Up</div>
		<p>
		Below is a list of all alumni we have registered. If they are
		checked in the list that means they have paid for registration.
		</p>
		<p>
		Check the names of newly paid alumni to add them as well,
		and then hit the "Update Registration" button to confirm your new list.
		</p>
		<form name="paidForm" id="paidForm" action="javascript:submitForm(\'paidForm\', \'/cgi-bin/bttbPaid.cgi\', null);">
		<input type='submit' name='submit' value='Update the Registration'>
		<br>
		""" )
		(paidList,paidInfo) = self.alumni.processQuery("""
		SELECT alumni.first,alumni.nee,alumni.last,alumni.id
		FROM alumni
		WHERE alumni.id IN (SELECT alumni_id FROM paid WHERE isPaid = 1)
		ORDER by alumni.last
		""")
		(unpaidList,unpaidInfo) = self.alumni.processQuery("""
		SELECT alumni.first,alumni.nee,alumni.last,alumni.id
		FROM alumni
		WHERE alumni.id NOT IN (SELECT alumni_id FROM paid WHERE isPaid = 1)
		OR alumni.id IN (SELECT alumni_id FROM paid WHERE isPaid = 0)
		ORDER by alumni.last
		""")
		html += '<fieldset><legend>%d Paid So Far</legend><table width="95%%" border="0" cellpadding="0" cellspacing="0">' % len(paidList)
		col = 0
		for (first,nee,last,id) in paidList:
			if col == 4:
				html += '</tr><tr>'
				col = 0
			col = col + 1
			name = SensibleName(first,nee,last)
			html += '<td><input checked type="checkbox" value="1" name="paid%s">%s</td>' % (id,name)
		html += """</tr></table>
		</fieldset>
		<input type='submit' name='submit' value='Update the Registration'>
		<br>
		<fieldset><legend>%d Not Paid (yet)</legend><table width="95%%" border="0" cellpadding="0" cellspacing="0"><tr>
		""" % len(unpaidList)
		col = 0
		for (first,nee,last,id) in unpaidList:
			if col == 4:
				html += '</tr><tr>'
				col = 0
			col = col + 1
			name = SensibleName(first,nee,last)
			html += '<td><input type="checkbox" value="1" name="paid%s">%s</td>' % (id,name)
		html += '</fieldset>'
		html += '</tr></table>'
		html += """
		<br>
		<input type='submit' name='submit' value='Update the Registration'>
		</form>
		"""
		return html

# ==================================================================

import unittest
class testMemories(unittest.TestCase):
	def testDump(self):
		paradePage = bttbParade()
		paradePage.requestor = bttbMember()
		print paradePage.content()
	
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
