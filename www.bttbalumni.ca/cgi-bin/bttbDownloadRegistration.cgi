#!env python
"""
Process the BTTB Alumni registration download request. The request could be
one of:
	- upload new version
		Loads new file in Registrations.xls
		Remove the lock file Registrations.lck
	- download version to modify
		Downloads current version
		Renames last 5 versions to Registrations.xls.{1-5}
		Creates Registrations.lck to indicate who has the file
	- download version to read
		Downloads current version
"""

import os
import os.path
import cgi
import cgitb; cgitb.enable()
import sys
from datetime import datetime
from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from bttbConfig import *
try:
	import msvcrt,os
	msvcrt.setmode( 0, os.O_BINARY ) # stdin  = 0
	msvcrt.setmode( 1, os.O_BINARY ) # stdout = 1
except ImportError:
	pass


regFile = MapLinks( '__ROOTPATH__/Alumni/Registrations.xls' )

def downloadFile(where):
	"""
	Show an instant download link.
	"""
	print MapLinks( """
	<a target="download" href="%s">Click here to download the file</a>
	""" % where )

def addStat(who, what):
	try:
		statFile = MapLinks( '__ROOTPATH__/Alumni/Registrations.txt' )
		sfd = open(statFile, 'a')
		sfd.write( '\n%s|%d|%s' % (what, who, datetime.now().strftime('%Y-%m-%d %H:%M:%S')) )
		sfd.close()
		lockFile = MapLinks( '__ROOTPATH__/Alumni/Registrations.lck' )
		if what == 'c':
			lfd = open(lockFile, 'w')
			lfd.write( '%d@%s\n' % (who, datetime.now().strftime('%Y-%m-%d %H:%M:%S')) )
			lfd.close()
		elif what == 'u':
			Backup( lockFile )
	except Exception, e:
		print 'EXCEPT:', e
		# can't do anything about failed stats
		pass

try:
	print 'Content-type: text/html\n'
	alumni = bttbAlumni()
	data = cgi.FieldStorage()
	id = int(data['id'].value)
	if data.has_key('change'):
		print 'Registration Data||'
		print '<body>'
		print '<div class="outlinedTitle">Change Spreadsheet</div>'
		print '<p>You now have the spreadsheet locked.</p>'
		addStat( id, 'c' )
		copiedFile = Backup( regFile )
		(bkdir,baseFile) = os.path.split(copiedFile)
		downloadFile('__BACKUPHREF__/%s' % baseFile)
		print '</body>'
	elif data.has_key('read'):
		print 'Registration Data||'
		print '<body>'
		print '<div class="outlinedTitle">Read Spreadsheet</div>'
		print '<p>The spreadsheet is still available for others.</p>'
		addStat( id, 'e' )
		downloadFile('__DATAHREF__/Registrations.xls')
		print '</body>'
	elif data.has_key('upload'):
		print '<body>'
		if data.has_key('spreadsheet'):
			fsrc = data['spreadsheet'].file
			if fsrc:
				try:
					msvcrt.setmode( fsrc, os.O_BINARY )
				except:
					pass
				addStat( id, 'u' )
				Backup( regFile )
				fdst = open(regFile, 'wb')
				while True:
					chunk = fsrc.read(1024)
					if not chunk:
						break
					fdst.write( chunk )
				fdst.close()
				print '<H1>Spreadsheet Upload Succeeded</H1>'
				print '<p>Your version of the spreadsheet is now uploaded.</p>'
			else:
				addStat( id, 'm' )
				print '<H1>Spreadsheet Upload Missing</H1>'
				print '<p>Transmission probably failed, try again.</p>'
		else:
			addStat( id, 'f' )
			print '<H1>Spreadsheet Upload Failed</H1>'
			print '<p>Could not upload your spreadsheet. Try again, it might be a slow connection.</p>'
		print '<p>Returning to the home page in 10 seconds...</p>'
		print '<META HTTP-EQUIV=\'REFRESH\' CONTENT="10; URL=\'/#home\'" />'
		print '</body>'
	else:
		print 'ERROR: Invalid function. Reload page and try again'
except Exception, e:
	Error( 'Registration file error', e )

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
