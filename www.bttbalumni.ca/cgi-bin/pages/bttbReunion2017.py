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

	def scripts(self):	return ['__CSSPATH__/bttbSwag.css']

#----------------------------------------

	def content(self):
		html = '''<H1>70<sup>th</sup> Reunion Tickets</H1>
		<a href='#'><div id='allin'></div></a>
		<a href='#'><div id='parade'></div></a>
		<a href='#'><div id='saturday'></div></a>
		<a href='#'><div id='hat'></div></a>
		<a href='#'><div id='shirt'></div></a>
		<a href='#'><div id='golf'></div></a>
'''
		cart_contents = self.param( 'cart' )
		html += '''<a href='#'><div id='cart'>{}</div></a>'''.format(cart_contents)

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
