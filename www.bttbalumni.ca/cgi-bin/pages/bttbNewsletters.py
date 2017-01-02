"""
Page that shows the previous newsletters
"""

from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbNewsletters']

class bttbNewsletters(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self): return 'BTTB Alumni Newsletters'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		html = MapLinks( """
		<h1>Previous Newsletters</h1>
		<p>
		Click on the newsletter to download the PDF file.
		</p><ol>
		download:(__NEWSLETTERPATH__/Vol1No6.pdf, <div class='date'>June 2007</div>Volume 1 - Number 6)
		download:(__NEWSLETTERPATH__/Vol1No5.pdf, <div class='date'>May 2007</div>Volume 1 - Number 5)
		download:(__NEWSLETTERPATH__/Vol1No4.pdf, <div class='date'>April 2007</div>Volume 1 - Number 4)
		download:(__NEWSLETTERPATH__/Vol1No3.pdf, <div class='date'>March 2007</div>Volume 1 - Number 3)
		download:(__NEWSLETTERPATH__/Vol1No2.pdf, <div class='date'>February 2007</div>Volume 1 - Number 2)
		download:(__NEWSLETTERPATH__/Vol1No1.pdf, <div class='date'>December 2006</div>Volume 1 - Number 1)
		</ol>
		""")
		return html

# ==================================================================

import unittest
class testNewsletters(unittest.TestCase):
	def testDump(self):
		newslettersPage = bttbNewsletters()
		print newslettersPage.content()
	
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
