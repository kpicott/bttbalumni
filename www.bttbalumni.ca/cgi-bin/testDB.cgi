#!/usr/bin/env python

import MySQLdb

class AlumniDB:
	def __init__(self):
		self.__stage = 'Begin'
		self.__cursor = None
		self.__db = None
		print '<head><title>My SQL Test page</title></head>'
		print '<body>'

	def stage(self,name):
		print 'Completed "' + self.__stage + '"<br>'
		self.__stage = name

	def close(self):
		self.stage( 'complete' )
		print '</body>'
		if self.__cursor: self.__cursor.close()

	def connect(self):
		try:
			self.__db = MySQLdb.connect( host='localhost', user='bttb', passwd='bttb999' )

			self.stage( 'Get cursor' )
			self.__cursor = self.__db.cursor()

			self.stage( 'cursor USE DB' )
			self.__cursor.execute( 'USE `BTTB`;' )

			self.stage( 'Fetch all' )
			tableList = self.__cursor.fetchall()

			self.stage( 'API select DB' )
			self.__db.select_db( 'BTTB' )

			self.stage( 'Complete' )
			return True
		except Exception, e:
			print '*** ERROR: (', self.__stage, ') : ', e
		return False

print 'Content-type: text/html'
db = AlumniDB()
if db.connect():
	db.close()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
