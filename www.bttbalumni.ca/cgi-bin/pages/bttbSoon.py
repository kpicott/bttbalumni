"""
URL page that says thanks for registering to new alumni
"""

from bttbDB import *
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbSoon']

class bttbSoon(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self): return 'BTTB Alumni : Coming Soon'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		page = ''
		try:
			page = ' '.join(' and '.join(self.params).split('_'))
		except:
			pass
		if len(page) < 1:
			page = 'future developments'
		html = """
		<h1>Watch this space for %s</h1>
		<p>
		Behind the scenes we're working diligently to bring you the
		information you need. This particular function isn't running
		yet but check back soon!
		</p>
		""" % page

		return html

# ==================================================================

import unittest
class testSoon(unittest.TestCase):
	def testDump(self):
		soonPage = bttbSoon()
		print soonPage.content()
	
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
