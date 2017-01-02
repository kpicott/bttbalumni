"""
URL page that says thanks for adding contact information to new alumni
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbThanksContact']

class bttbThanksContact(bttbPageFile):
	def __init__(self):
		bttbPageFile.__init__(self, '__ROOTPATH__/thanksContact.html', '__ROOTPATH__/thanksContact.html')
	
	def title(self): return 'Welcome to the BTTB Alumni Mailing List'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
