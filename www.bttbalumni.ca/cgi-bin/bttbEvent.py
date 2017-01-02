# -*- coding: iso-8859-15 -*-
"""
BTTB 60th anniversary event information
"""
import re
import os.path
from datetime import datetime
from xml.dom import minidom
from bttbConfig import *

__all__ = ['bttbEvent']

class bttbEvent:
	def __init__(self,fieldNames,dataTuple):
		"""
		Initialize the data fields from the given tuple and it's field names.
		It's semantically equivalent to a dictionary but when calling this
		method there will be many tuples and only one set of common field
		names so this way is more flexible.
		"""
		for field in fieldNames:
			value = dataTuple[fieldNames[field]]
			self.__dict__[field] = value
	
	def __str__(self):
		"""
		Returns a dump of the data dictionary
		"""
		if self.__dict__:
			return 'bttbEvent: %s' % self.__dict__
		else:
			return ''


# ==================================================================

import unittest
class testEvent(unittest.TestCase):
	def testDB(self):
		import bttbDB
		db = bttbDB.bttbDB()
		db.Initialize()
		events = db.GetEvents()
		for eventObj in events:
			print eventObj
		db.Finalize()

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
