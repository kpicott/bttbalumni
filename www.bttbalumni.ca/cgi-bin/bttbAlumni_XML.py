# -*- coding: iso-8859-15 -*-
"""
BTTB Alumni profile information.
"""
#
import re
import os
import os.path
from bttbMember_XML import bttbMember
from bttbConfig import *
from xml.dom import minidom

def fieldString(value):
	"""
	Utility to return the given string or an empty string if it's 'None'
	"""
	return value and value.replace('\n','\\n').replace('\t',' ') or ''

class bttbAlumni:
	def __init__(self,dir):
		self.dir = dir
		self.fileName = dir + '/Profiles.xml'
		self.xmldoc = minidom.parse( self.fileName )
		self.memberFiles = []
		self.editFiles = []
		self.memberList = []
		self.getMemberFileList()
		self.populate()

	def getMemberFileList(self):
		"""
		Read the data directory and find all member files
		"""
		re_memberPattern = re.compile( '[0-9]+.xml$' )
		re_memberEditPattern = re.compile( '[0-9]+.xml_EDIT$' )
		fullDirList = os.listdir(self.dir)
		for file in fullDirList:
			if re_memberPattern.match(file):
				self.memberFiles.append( file )
			elif re_memberEditPattern.match(file):
				self.editFiles.append( file )

	def reject(self,href):
		"""
		Reject the given href (but keep it around, just in case)
		"""
		for memberEl in self.xmldoc.firstChild.getElementsByTagName('member'):
			try:
				if href == memberEl.attributes.get('href').value:
					if memberEl.parentNode is not None:
						memberEl.parentNode.removeChild( memberEl )
						break
			except:
				pass
		path = os.path.join(self.dir, href)
		try:
			Backup( path )
			os.remove( path )
		except:
			pass

	def approve(self,href,isFriend):
		"""
		Add approval for the given href
		"""
		found = False
		for memberEl in self.xmldoc.firstChild.getElementsByTagName('member'):
			try:
				if href == memberEl.attributes.get('href').value:
					memberEl.setAttribute('approved', '1')
					memberEl.setAttribute( 'friend', isFriend and '1' or '0' )
					found = True
			except:
				pass
		if not found:
			memberEl = minidom.createElement('member')
			memberEl.setAttribute( 'href', href )
			memberEl.setAttribute( 'approved', '1' )
			memberEl.setAttribute( 'friend', isFriend and '1' or '0' )
			self.xmldoc.appendChild( memberEl )

	def approveEdit(self,file,isFriend):
		"""
		Add approval of edit for the given file
		"""
		found = False
		path = os.path.join(self.dir, file)
		Backup( path )
		os.rename( path + "_EDIT", path )
		for memberEl in self.xmldoc.firstChild.getElementsByTagName('member'):
			try:
				if file == memberEl.attributes.get('href').value:
					memberEl.setAttribute( 'friend', isFriend and '1' or '0' )
					found = True
			except:
				pass

	def writeFile(self):
		"""
		Write out the updated file in XML format
		"""
		Backup( self.fileName )
		try:
			file = open(self.fileName, 'w')
			self.xmldoc.normalize()
			file.write( CleanupXML( self.xmldoc.toxml() ) )
			file.close()
		except Exception, e:
			Error( 'Writing to file ' + self.fileName, e )

	def populate(self):
		"""
		Walk the DOM and find any files we found in the directory that
		were missing from the tree and add them in
		"""
		existingFiles = {}
		existingFriends = {}
		# Preprocess the file list to make finding the missing ones faster
		for memberEl in self.xmldoc.firstChild.getElementsByTagName('member'):
			try:
				href = memberEl.attributes.get('href').value
				approved = int(memberEl.attributes.get('approved').value)
				existingFiles[href] = approved
				try:
					friend = int(memberEl.attributes.get('friend').value)
					existingFriends[href] = friend
				except:
					pass
			except:
				pass
		# Add in nodes for all of the files not found
		for file in self.memberFiles:
			if( not file in existingFiles ):
				newNode = self.xmldoc.createElement('member')
				newNode.setAttribute('href', file)
				newNode.setAttribute('approved', '0')
				newNode.setAttribute('friend', '0')
				self.xmldoc.firstChild.appendChild( newNode )
		for memberEl in self.xmldoc.firstChild.getElementsByTagName('member'):
			href = memberEl.attributes.get('href').value
			try:
				memberFile = os.path.join(self.dir, href)
				if os.path.exists(memberFile):
					newMember = bttbMember(memberFile)
					if newMember:
						if href in existingFiles:
							newMember.approved = existingFiles[href]
							newMember.friend = href in existingFriends and existingFriends[href] or False
						self.memberList.append( newMember )
			except Exception, e:
				Warning( 'Extracting member information', e )
				pass

	def sortLink(self,columnName,columnIndex,sortIndex):
		"""
		"""
		newColumnLink = columnIndex
		sortedBy = ''
		style = ''
		if sortIndex == columnIndex:
			sortedBy = '&nbsp;&uarr;'
			style = "style='background:#eeee88;'"
			newColumnLink = - newColumnLink
		elif sortIndex == - columnIndex:
			sortedBy = '&nbsp;&darr;'
			style = "style='background:#eeee88;'"
			newColumnLink = - newColumnLink
		return ('<a %s href=\'#' + CgiHref() + '/bttbProfiles.cgi?sort=%d\' onclick=\'loadLink("' + CgiHref() + '/bttbProfiles.cgi?sort=%d"); return true;\'>%s%s</a>') % (style, newColumnLink, newColumnLink, columnName, sortedBy)

	def showSummary(self,sortColumn):
		"""
		Display a summary of the alumni so far in HTML format.
		Only show the fields relevant to other alumni (e.g. omit
		address information)
		"""
		if( len(self.memberList) == 0 ):
			print '<h2>No members have registered yet</h2>'
		else:
			print '<h2>%d Registered Alumni</h2>' % (len(self.memberList)-1)
			print 'If you need to correct something <a href="mailto:info@bttbalumni.ca">email us</a> and we\'ll get it fixed right up!'
			print '<br>'
			print 'Click on a column heading to sort by that column.'
			print "<table cellspacing='0' cellpadding='5' border='1'>"
			print '<tr bgcolor=\'#ffaaaa\'>'
			print '<th valign="center">', self.sortLink('First', 1, sortColumn)
			print self.sortLink('&nbsp;(nee)', 2, sortColumn)
			print self.sortLink('&nbsp;Last', 3, sortColumn)
			print '</th>'
			print '<th valign="center">', self.sortLink('Start&nbsp;Year', 4, sortColumn), '</th>'
			print '<th valign="center">', self.sortLink('End&nbsp;Year', 5, sortColumn), '</th>'
			print '<th valign="center">', self.sortLink('Email', 6, sortColumn), '</th>'
			print '<th valign="center">', self.sortLink('Instrument(s)', 7, sortColumn), '</th>'
			print '</tr>'
			foundUnapproved = 0
			sortedList = []
			try:
				sortedList = self.memberList
				sortedList.sort( bttbMember._sortMethod(abs(sortColumn)) )
				if sortColumn < 0: sortedList.reverse()
				for member in sortedList:
					if member and member.approved:
						member.printSummaryRow()
					elif member:
						foundUnapproved = foundUnapproved + 1
			except Exception, e:
				Error( 'Displaying list', e );
			print "</table>"
			if foundUnapproved > 0:
				print '<p>&nbsp;</p>'
				print '<h2>', foundUnapproved, Pluralize('Member',foundUnapproved), ' Awaiting Confirmation</h2><ol>'
				for member in sortedList:
					if member and not member.approved:
						print '<li>'
						print member.fullName()
						print '</li>'
				print '</ol>'

	def showCommitteeTitle(self,title,sortColumn):
		"""
		Print out the title line of the table showing the profile
		information visible to the committee members.
		"""
		print '<h2>' + title + '</h2>'
		print '<div class="subtext">Click on a column heading to sort by that column.</div>'
		print "<table cellspacing='0' cellpadding='5' border='1'>"
		print '<tr bgcolor=\'#ffaaaa\'>'
		print '<th>Approve</th>'
		print '<th>Reject</th>'
		print '<th>Friend<br>of the<br>Alumni</th>'
		print '<th>', self.sortLink('First', 1, sortColumn)
		print self.sortLink('&nbsp;(nee)', 2, sortColumn)
		print self.sortLink('&nbsp;Last', 3, sortColumn)
		print '</th>'
		print '<th>', self.sortLink('Start&nbsp;Year', 4, sortColumn), '</th>'
		print '<th>', self.sortLink('End&nbsp;Year', 5, sortColumn), '</th>'
		print '<th>', self.sortLink('Email', 6, sortColumn), '</th>'
		print '<th>', self.sortLink('Instrument(s)', 7, sortColumn), '</th>'
		print '<th>Highest Rank</th>'
		print '<th>Memory</th>'
		print '<th>Address</th>'
		print '<th>Positions</th>'
		print '<th>Keep Private?</th>'
		print '<th>Marching?</th>'
		print '<th>Doing Concert?</th>'
		print '<th>Events Attending</th>'
		print '<th>Volunteer for...</th>'
		print '</tr>'

	def showCommitteeSummary(self,sortColumn):
		"""
		Display more details for the committees use
		"""
		if( len(self.memberList) == 0 ):
			print '<h2>No members have registered yet</h2>'
			return
		
		foundUnapproved = 0
		sortedList = []
		try:
			sortedList = self.memberList
			sortedList.sort( bttbMember._sortMethod(abs(sortColumn)) )
			if sortColumn < 0: sortedList.reverse()
			for member in sortedList:
				if member and not member.approved:
					foundUnapproved = foundUnapproved + 1
		except Exception, e:
			Error( 'Displaying list', e );

		hasEdits = False
		if foundUnapproved > 0: hasEdits = True
		if len(self.editFiles) > 0: hasEdits = True

		#----------------------------------------
		# First show the new members pending approval
		if hasEdits:
			print '<form type="POST" action="' + CgiHref() + '/bttbApprove.cgi">'
		if foundUnapproved > 0:
			self.showCommitteeTitle( '%d %s %s' % (foundUnapproved, Pluralize('Member',foundUnapproved), ' Awaiting Confirmation</h2>'), sortColumn )
			for member in sortedList:
				if member and not member.approved:
					member.printCommitteeSummaryRow('XXX')
			print '</table>'
		else:
			print '<h2>No New Members</h2>'

		#----------------------------------------
		# Second show the edits pending approval
		if len(self.editFiles) > 0:
			print '<p>&nbsp;</p>'
			self.showCommitteeTitle( '%d %s %s' % (len(self.editFiles), Pluralize('Edit',len(self.editFiles)), ' Awaiting Confirmation'), sortColumn )
			for file in self.editFiles:
				temp = bttbMember(os.path.join(self.dir,file))
				temp.printCommitteeSummaryRow('EEE')
			print '</table>'
		else:
			print '<h2>No Unapproved Edits</h2>'

		if hasEdits:
			print '<input type="submit" name="submit" value="Approve">'
			print '</form>'

		# ---------------------------------------
		# Last but not least the already-approved list
		if len(sortedList) > 0:
			print '<p>&nbsp;</p>'
			self.showCommitteeTitle( '%d Registered Alumni' % (len(self.memberList)-1), sortColumn )
			for member in sortedList:
				if member and member.approved:
					member.printCommitteeSummaryRow(None)
			print "</table>"

	def showCommitteeText(self):
		"""
		Display full text of all alumni in an Excel/Word-friendly format.
		That is, tab-separated text with a heading line.
		"""
		print '\t'.join(['FirstName','Nee','LastName', 'FirstYear',
						 'LastYear', 'Email', 'Instruments', 'Rank',
						 'Memory', 'Street', 'City', 'Province',
						 'Country', 'PostalCode', 'Phone', 'ShowEmail',
						 'Positions', 'InParade', 'InConcert', 'RegDate',
						 'RegTime', 'EditDate', 'EditTime'
			]) + '\t' + '\t'.join(AttendList()) + '\t' + '\t'.join(VolunteerList()) + '\tApproved\tFriend\tID'
		if( len(self.memberList) == 0 ):
			return
		else:
			for member in self.memberList:
				attend = ''
				for event in AttendList():
					if member.isAttending( event ):
						attend = ('%s%d\t') % (attend, 1)
					else:
						attend = ('%s%d\t') % (attend, 0)
				volunteer = ''
				for event in VolunteerList():
					if member.isVolunteering( event ):
						volunteer = ('%s%d\t') % (volunteer, 1)
					else:
						volunteer = ('%s%d\t') % (volunteer, 0)
				print fieldString(member.first) + '\t',
				print fieldString(member.nee) + '\t',
				print fieldString(member.last) + '\t',
				print fieldString(member.firstYear) + '\t',
				print fieldString(member.lastYear) + '\t',
				print fieldString(member.email) + '\t',
				print fieldString(', '.join(member.instruments)) + '\t',
				print fieldString(member.rank) + '\t',
				print fieldString(member.memory) + '\t',
				print fieldString(', '.join([member.street1, member.street2])) + '\t',
				print fieldString(member.city) + '\t',
				print fieldString(member.province) + '\t',
				print fieldString(member.country) + '\t',
				print fieldString(member.postalCode) + '\t',
				print fieldString(member.phone) + '\t',
				print '%d\t' % (member.emailVisible),
				print fieldString(', '.join(member.positions)) + '\t',
				print '%s\t' % (['No','Yes','Maybe'][member.joiningBand]),
				print '%s\t' % (['No','Yes','Maybe'][member.joiningConcert]),
				(regDate,regTime) = (('%s') % (member.joinTime)).split()
				(editDate,editTime) = (('%s') % (member.editTime)).split()
				print fieldString(regDate) + '\t',
				print fieldString(regTime) + '\t',
				print fieldString(editDate) + '\t',
				print fieldString(editTime) + '\t',
				print attend,
				print volunteer,
				print '%d' % (member.approved) + '\t',
				print '%d' % (member.friend) + '\t',
				print '%d' % (member.id)

	def eventAttendance(self, event):
		"""
		Return an array of the names of people who have indicated
		they will be attending the given event.
		"""
		attendanceList = []
		if( len(self.memberList) == 0 ):
			return
		else:
			sortedList = []
			try:
				sortedList = self.memberList
				sortedList.sort( bttbMember._sortByLastName )
			except Exception, e:
				# If an error in the sort use the unsorted list
				sortedList = self.memberList
			for member in sortedList:
				attend = ''
				if member.isAttending( event ):
					attendanceList.append( member.fullName() )
		return attendanceList

if( __name__ == '__main__' ):
	alum = bttbAlumni('../Alumni')
	alum.showCommitteeSummary(1)

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
