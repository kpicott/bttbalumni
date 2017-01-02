"""
URL page to return test data.
"""

from bttbPage import bttbPage

__all__ = ['bttbTest']

class bttbTest(bttbPage):
	def __init__(self):
		pass
	
	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		return 'TEST'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
