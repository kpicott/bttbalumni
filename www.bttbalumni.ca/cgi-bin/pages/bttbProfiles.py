"""
URL page that shows all of the globally visible user profile information
"""

from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbProfiles']

class bttbProfiles(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
	
	def title(self): return 'BTTB Alumni Profiles'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		try:
			try:
				alumni = bttbAlumni()
				if( self.isCommittee() and self.requestor and self.requestor.onCommittee ):
					return alumni.getCommitteeSummary( self.param('sort') )
				else:
					return alumni.getSummary( self.param('sort'), self.requestor )
			except:
				if( self.isCommittee() and self.requestor and self.requestor.onCommittee ):
					return alumni.getCommitteeSummary( 'firstYear' )
				else:
					return alumni.getSummary( 'firstYear', self.requestor )
		except Exception, e:
			return ErrorMsg( 'Could not read member information', e )


# ==================================================================

import unittest
class testProfiles(unittest.TestCase):
	def testDump(self):
		page = bttbProfiles()
		print page.content()
	
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
