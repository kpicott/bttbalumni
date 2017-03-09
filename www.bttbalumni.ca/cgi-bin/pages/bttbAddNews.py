"""
Page that lets a user add new memories
"""

from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbAddMemory']

def _sortByMemoryDate(x,y):	return cmp(x[2], y[2])
class bttbAddMemory(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self):
        return 'BTTB Alumni : Add a News Article'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
        if not self.isCommittee():
            return CommitteAccessRequired()

		html = """
		<h2>Add a News Article</h2>
		<table border='1'><tr><td>
		<table>
		<tr>
			<td>Date&nbsp;(YYYY-MM-DD):</td>
			<td><input type='text' name='newNewsDate' value=''></td>
		</tr>
		<tr>
			<td valign='top'>Article (HTML allowed):</td>
			<td><textarea rows='10' cols='70' name='newNews'></textarea></td>
		</tr>
		</table>
		</td></tr></table>
		"""
		html += "<input type='submit' value='Submit News'>"
		html += "</form>"
		return html

# ==================================================================

import unittest
class testAddNews(unittest.TestCase):
	def testDump(self):
		testPage = bttbAddNews()
        bttbAddNews.params['committee'] = [True]
		print testPage.content()
	
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
