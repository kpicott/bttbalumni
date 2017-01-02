#!env python
"""
Add in a new memory for the current user.
"""

print 'Content-type: text/html\n'
print 'Memories Edited||'
print '<body>'

import os
import os.path
import re
import cgi
from datetime import datetime
from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from bttbConfig import *

def getParam(name,default):
	"""
	Simple trick to get cgi params using default values
	"""
	try:
		value = params[name][0].strip()
	except:
		value = default
	return value

def getIntParam(name,default):
	"""
	Simple trick to get numeric cgi params using default values
	"""
	try:
		value = int( params[name][0] )
	except:
		value = default
	return value

re_dateFmt = re.compile('([12][09][0-9][0-9])[_/-]*([0-9]+)[_/-]*([0-9]+)')

def dateFromString(dateStr):
	"""
	Get back a datetime object from a user string. 
	"""
	try:
		match = re_dateFmt.match( dateStr )
		if match:
			(yy, mm, dd) = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
			if yy < 1900: yy = 1900 + yy
			if yy > 2100: yy = 2007
			return datetime( yy, mm, dd )
	except Exception, e:
		pass
	return datetime.now()

try:
	params = cgi.parse()
	alumni = bttbAlumni()
	#
	# If the id was negative then this is an edit:
	#	Look for a previous edit to overwrite
	#	Either insert or update at (negative-id).
	#
	# Otherwise it's a creation, and requires a new id
	#
	id = getIntParam('id', 0)
	member = alumni.getMemberFromId(id)
	print '<h1>Memory Changes Performed</h1>'
	print '<table border="1">'
	if 'memory' in params:
		for memoryId in params['memory']:
			try:
				date = dateFromString(params['memoryDate%s' % memoryId][0])
			except:
				date = member.midpoint()
			delete = getIntParam( 'memoryDelete%s' % memoryId, 0 )
			try:
				memory = params['memory%s' % memoryId][0]
				if delete:
					alumni.removeMemory( int(memoryId) )
					print '<tr>'
					print '<td valign="top"><h2>DELETE</h2></td>'
					print '<td valign="top"><div class="date">%s</div></td>' % date.strftime('%Y-%m-%d')
					print '<td valign="top">%s</td>' % memory
					print '</tr>'
				else:
					alumni.updateMemory( member, memory, date, int(memoryId) )
					print '<tr>'
					print '<td valign="top"><h2>EDIT</h2></td>'
					print '<td valign="top"><div class="date">%s</div></td>' % date.strftime('%Y-%m-%d')
					print '<td valign="top">%s</td>' % memory
					print '</tr>'
			except:
				pass

	try:
		date = dateFromString(params['newMemoryDate'][0])
		memory = params['newMemory'][0].strip().rstrip()
		if len(memory) > 0:
			alumni.updateMemory( member, memory, date, 999999 )
			print '<tr>'
			print '<td valign="top"><h2>ADD</h2></td>'
			print '<td valign="top"><div class="date">%s</div></td>' % date.strftime('%Y-%m-%d')
			print '<td valign="top">%s</td>' % memory
			print '</tr>'
	except:
		pass

	print '</table>'

	alumni.ArchiveData()
except Exception, e:
	Error( 'Memory processing error', e )

print '</body>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
