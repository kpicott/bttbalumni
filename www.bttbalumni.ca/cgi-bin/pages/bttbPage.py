"""
Base class for a page that goes in the web content pane.
"""
__all__ = [ 'bttbPage' ]
from datetime import datetime

class bttbPage:
	def __init__(self):
		self.id = None
		self.params = {}
		self.requestor = None
		self.lastLogin = datetime.now()

	def setParams(self, params):	self.params = params
	def setRequestor(self, who):	self.requestor = who
	def setLastLogin(self, when):	self.lastLogin = when
	def title(self):		return 'BTTB Alumni'
	def content(self):		return 'BTTB Alumni'

	def scripts(self):
		"""
		Javascripts and styles are not evaluated by default so they must be
		called out for special treatment after import.
		"""
		return []

	def isCommittee(self):
		"""
		Returns True if the page parameters correspond to an authorized
		committee member, else return False.
		"""
		try:
			return ( int(self.param('committee')) == 1 )
		except:
			return False

	def param(self, name):
		try:
			return self.params[name][0];
		except:
			return None

if __name__ == '__main__':
	page = bttbPage()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
