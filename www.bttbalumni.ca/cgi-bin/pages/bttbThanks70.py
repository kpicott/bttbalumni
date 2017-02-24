"""
URL page that says thanks for buying reunion swag
"""

from bttbPageFile import bttbPageFile
__all__ = ['bttbThanks70']

class bttbThanks70(bttbPageFile):
	def __init__(self):
		bttbPageFile.__init__(self, '__ROOTPATH__/thanks2017.html', '__ROOTPATH__/thanks2017.html')
	
	def title(self): return 'See You At the Reunion!'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
