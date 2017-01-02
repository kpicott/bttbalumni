"""
Page that lets committee members download the current spreadsheet with
registration information in it.
"""

import os
from bttbMember import *
from bttbAlumni import bttbAlumni
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbRegistration']

class bttbRegistration(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
		self.committeeOnly = True
		try:
			self.alumni = bttbAlumni()
		except Exception, e:
			Error( 'Could not find memory information', e )
	
	def title(self): return 'BTTB Anniversary Celebration Registration'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""
		name = 'committee member'
		if self.requestor:
			name = self.requestor.first
		html = MapLinks( """
		<div class='outlinedTitle'>Registration Spreadsheet</div>
		<p>
		Greetings %s, looking for the registration spreadsheet are you?
		</p>
		""") % name
		greeting = False
		fileName = MapLinks( '__ROOTPATH__/Alumni/Registrations.xls' )
		lockFile = MapLinks( '__ROOTPATH__/Alumni/Registrations.lck' )
		if os.path.isfile( fileName ):
			html += MapLinks( """
			<p>
			You're in luck, the registration information is here!
			</p>
			<table border='0'><tr>
			<td width='200' align='center' valign='top'>
			<form name='changeForm' id='changeForm'
				action="javascript:submitForm(\'changeForm\', \'/cgi-bin/bttbDownloadRegistration.cgi\', null)">
				<input type='hidden' name='id' value='%d'>
				<input type='submit' name='change' value='Change Spreadsheet'>
			</form>
			<br>
			Click here to download the spreadsheet to modify.
			</td>
			<td width='200' align='center' valign='top'>
			<form name='readForm' id='readForm'
				action="javascript:submitForm(\'readForm\', \'/cgi-bin/bttbDownloadRegistration.cgi\', null)">
				<input type='hidden' name='id' value='%d'>
				<input type='submit' name='read' value='Read Only Copy'>
			</form>
			<br>
			Click here to download a copy of the spreadsheet which you can
			look at but won't be allowed to modify.
			</td>
			</tr></table>
			""" % (self.requestor.id, self.requestor.id) )
			greeting = True
		elif os.path.exists( lockFile ):
			lockId = 999999
			fd = open( lockFile )
			try:
				for line in fd:
					try:
						(lockId, lockDate) = line.split('@')
					except:
						# Ignore illegal lines
						continue
					lockId = int(lockId)
			finally:
				fd.close()
			if lockId == self.requestor.id:
				html += MapLinks( """
				<p>
				Since you already have the file I'm assuming you want to
				return your completed version, right?
				</p>
				<p>
				<form method='POST' enctype='multipart/form-data'
				 action="/cgi-bin/bttbDownloadRegistration.cgi">
					<input type='hidden' name='id' value='%d'>
					<input type='file' value='' name='spreadsheet'>
					&nbsp;&nbsp;
					<input type='submit' name='upload' value='Upload'>
				</form>
				</p>
				<p>
				Use the "Browse" button to point to your new version of the
				file and then click the
				"Upload" button to transfer the file back to the website.
				</p>
				""" ) % self.requestor.id
				greeting = True
			elif lockId != 999999:
				locker = self.alumni.getMemberFromId( lockId )
				if locker:
					html += MapLinks( """
					<p>
					Too slow - %s already got the registration file on %s.
					</p>
					<p>
					You can wait for them to return it, or
					send:(%s, send them an email at %s) to bug them to put it back.
					</p>
					""" % (locker.fullName(), lockDate, locker.email, locker.email) )
				else:
					html += """
					<p>
					Too slow - somebody else has the registration file.
					For some reason I can't tell who has it. You'll have
					to wait until they return it before making changes.
					</p>
					"""
				greeting = True
		if not greeting:
			html += MapLinks( """
			<p>
			Uh-oh, something is wrong here. Nobody has the file, including me!
			</p>
			<p>
			Wait a second then reload this page - somebody may be in the middle
			of returning it.
			</p>
			<p>
			If you try a second time and it fails then
			send:(bttb@picott.ca, notify the webmaster immediately)!
			</p>
			""" )
		else:
			html += "</form>"
		history = MapLinks( '__ROOTPATH__/Alumni/Registrations.txt' )
		if os.path.isfile( history ):
			fd = open(history)
			html += '<h2>Spreadsheet History</h2>'
			info = fd.readlines()
			fd.close()
			idx = len(info)
			howMany = 0
			while idx > 0 and howMany < 10:
				idx = idx - 1
				howMany = howMany + 1
				try:
					(what, who, when) = info[idx].split('|')
				except:
					# Ignore illegal lines
					continue
				member = self.alumni.getMemberFromId( int(who) )
				name = 'Unknown Member'
				if member:
					name = member.fullName()
				if what == 'c':
					what = 'File lock'
				elif what == 'e':
					what = 'File read-only download'
				elif what == 'u':
					what = 'File upload'
				elif what == 'm':
					what = 'Missing file transfer error'
				elif what == 'f':
					what = 'File transfer error'
				else:
					what = 'Unknown operation'
				html += '%s by %s on %s<br>\n' % (what, name, when)
			if idx > 0:
				html += '... and %d more...' % idx
		return html

# ==================================================================

import unittest
class testRegistration(unittest.TestCase):
	def testDump(self):
		registrationPage = bttbRegistration()
		registrationPage.requestor = bttbMember()
		registrationPage.requestor.id = 0
		print registrationPage.content()
	
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
