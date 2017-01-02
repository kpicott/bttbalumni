"""
URL page that defines content read directly from a page template
with only structural and location modifications.
"""

import os
from bttbPage import bttbPage
from bttbConfig import *

__all__ = ['bttbPageFile']

class bttbPageFile(bttbPage):
	def __init__(self, fileName, altFileName=None):
		bttbPage.__init__(self)
		self.fileName = MapLinks( fileName )
		self.altFileName = self.fileName
		if altFileName: self.altFileName = MapLinks( altFileName )
		self.committeeOnly = False
	
	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		fileName = self.fileName
		try:
			if self.requestor:
				if (not self.committeeOnly) or self.requestor.onCommittee:
					fileName = self.altFileName
		except:
			pass
		if os.path.isfile( fileName ):
			info = ""
			fd = open( fileName )
			try:
				for line in fd:
					info = info + MapLinks(line)
			finally:
				fd.close()

			return info
		else:
			return ErrorMsg( 'File contents missing', fileName )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
