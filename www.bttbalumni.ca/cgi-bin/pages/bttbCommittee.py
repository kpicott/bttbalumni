"""
URL page that shows committee member links
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbCommittee']

class bttbCommittee(bttbPageFile):
	def __init__(self):
		bttbPageFile.__init__(self, '__ROOTPATH__/accessDenied.html', '__ROOTPATH__/committee.html')
		self.committeeOnly = True
	
	def title(self): return 'BTTB Alumni Committee Links'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
