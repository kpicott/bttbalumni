"""
URL page that shows cookie information
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbCookies']

class bttbCookies(bttbPageFile):
	def __init__(self):
		bttbPageFile.__init__(self, '__ROOTPATH__/cookies.html')
	
	def title(self): return 'BTTB Alumni Website Cookie Information'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
