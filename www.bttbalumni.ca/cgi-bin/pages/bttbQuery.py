"""
URL page that shows SQL query details for committee
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbQuery']

class bttbQuery(bttbPageFile):
	def __init__(self):
		bttbPageFile.__init__(self, '__ROOTPATH__/query.html')
	
	def title(self): return 'BTTB Alumni Committee Queries'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
