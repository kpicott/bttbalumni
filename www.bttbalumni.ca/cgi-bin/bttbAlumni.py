# -*- coding: iso-8859-15 -*-
"""
BTTB Alumni profile information.
"""
#
import re
import os
import os.path
from datetime import datetime
from bttbMember import *
from bttbConfig import *
from bttbDB import *

__all__ = ['bttbAlumni']

def fieldString(value):
	"""
	Utility to return the given string or an empty string if it's 'None'
	"""
	return value and value.replace('\n','\\n').replace('\t',' ') or ''

class bttbAlumni:
	def __init__(self):
		self.memberList = []
		self.__db = bttbDB()
		if __name__ == '__main__': self.__db.TurnDebugOn()
		self.__db.Initialize()

	def __del__(self):
		self.__db.Finalize()

	def sortInverse(self,sortIndex):
		"""
		Return the string representing the opposite sorting method (e.g.
		ascending instead of descending)
		"""
		forwards = sortIndex.replace('_desc','')
		if sortIndex == forwards:
			return sortIndex + '_desc'
		else:
			return forwards

	def sortLink(self,columnName,columnIndex,sortIndex):
		"""
		Construct a link to the table sorted by the columnIndex, given that
		the current sort is by sortIndex
		"""
		newColumnLink = columnIndex
		sortedBy = ''
		colour = ''
		if sortIndex == columnIndex:
			sortedBy = '&nbsp;&uarr;'
			colour = '#eeee88'
			newColumnLink = self.sortInverse( newColumnLink )
		elif sortIndex == self.sortInverse( columnIndex ):
			sortedBy = '&nbsp;&darr;'
			colour = '#eeee88'
			newColumnLink = self.sortInverse( newColumnLink )
		page = '#profiles?sort=%s' % newColumnLink
		link = '%s%s' % (columnName, sortedBy)
		return PageLink( page, link, 'Sort by ' + columnName, colour )

	def sortLinkC(self,columnName,columnIndex,sortIndex):
		"""
		Construct a link to the table sorted by the columnIndex, given that
		the current sort is by sortIndex
		"""
		newColumnLink = columnIndex
		sortedBy = ''
		colour = ''
		if sortIndex == columnIndex:
			sortedBy = '&nbsp;&uarr;'
			colour = '#eeee88'
			newColumnLink = self.sortInverse( newColumnLink )
		elif sortIndex == self.sortInverse( columnIndex ):
			sortedBy = '&nbsp;&darr;'
			colour = '#eeee88'
			newColumnLink = self.sortInverse( newColumnLink )
		return PageLink( '#profiles?sort=%s&committee=1' % newColumnLink, '%s%s' % (columnName, sortedBy), 'Sort by ' + columnName, colour )

	def getSummary(self,sortColumn,whoWantsIt):
		"""
		Display a summary of the alumni so far in HTML format.
		Only show the fields relevant to other alumni (e.g. omit
		address information)
		"""
		keys = self.__db.GetPublicMemberKeys()
		descending = False
		sortKey = None
		if sortColumn.replace('_desc','') == sortColumn:
			sortKey = sortColumn
		else:
			descending = True
			sortKey = self.sortInverse(sortColumn)
		(memberList, items) = self.__db.GetPublicMemberList(sortKey, descending)
		html = ''
		if( len(memberList) < 2 ):
			html += '<h2>No members have registered yet</h2>'
		else:
			html += '<h2>%d Registered Alumni</h2>' % (len(memberList)-1)
			html += 'If you need to correct something '
			html += EmailLink('info@bttbalumni.ca', 'email us')
			html += ' and we will get it fixed right up!'
			html += '<br>'
			html += 'Click on a column heading to sort by that column.'
			html += "<table cellspacing='0' cellpadding='5' border='1'>"
			html += '<tr bgcolor=\'#ffaaaa\'>'
			html += '<th valign="center">%s' % self.sortLink('First', 'first', sortColumn)
			html += self.sortLink('&nbsp;(nee)', 'nee', sortColumn)
			html += self.sortLink('&nbsp;Last', 'last', sortColumn)
			html += '</th>'
			html += '<th valign="center">%s</th>' % self.sortLink('Start&nbsp;Year', 'firstYear', sortColumn)
			html += '<th valign="center">%s</th>' % self.sortLink('End&nbsp;Year', 'lastYear', sortColumn)
			html += '<th valign="center">%s</th>' % self.sortLink('Email', 'email', sortColumn)
			html += '<th valign="center">%s</th>' % self.sortLink('Instrument(s)', 'instruments', sortColumn)
			html += '</tr>'
			foundUnapproved = 0
			try:
				for member in memberList:
					if member and member[items['approved']]:
						html += '<tr>'
						html += '<td valign=\'top\'>'
						if member[items['onCommittee']]:
							html += CommitteeMark()
						sensibleName = SensibleName( member[items['first']], member[items['nee']], member[items['last']] )
						html += sensibleName
						if whoWantsIt and whoWantsIt.id == member[items['id']]:
							link = '#register?id=%d' % member[items['id']]
							html += '<br>' + PageLink(link, 'Click to Edit', 'Edit your profile')
						html += '</td>'
						html += '<td valign=\'top\' align=\'center\'>%s</td>' % member[items['firstYear']]
						html += '<td valign=\'top\' align=\'center\'>%s</td>' % member[items['lastYear']]
						if( member[items['email']] and member[items['emailVisible']] ):
							html += '<td valign=\'top\'>'
							html += EmailLink( member[items['email']] )
							html += '</td>'
						else:
							html += '<td valign=\'top\' align=\'center\'>---</td>'
						html += '<td valign=\'top\'>%s</td>' % member[items['instruments']]
						html += '</tr>'
					elif member:
						foundUnapproved = foundUnapproved + 1
			except Exception, e:
				Error( 'Displaying list', e );
			html += "</table>\n"
			if foundUnapproved > 0:
				html += '<p>&nbsp;</p>'
				html += '<h2>%d %s Awaiting Confirmation</h2><ol>' % (foundUnapproved, Pluralize('Member',foundUnapproved))
				for member in memberList:
					if member and not member[items['approved']]:
						html += '<li>'
						html += SensibleName( member[items['first']], member[items['nee']], member[items['last']] )
						html += '</li>'
				html += '</ol>\n'
			return html

	def processQuery(self, query):
		"""
		Process a generic query with unknown result type.
		"""
		return self.__db.ProcessQuery(query)

	def getCommitteeSummary(self,sortColumn):
		"""
		Display a summary of the alumni so far in HTML format.
		Only show the fields relevant to other alumni (e.g. omit
		address information)
		"""
		keys = self.__db.GetPublicMemberKeys()
		descending = False
		sortKey = None
		if sortColumn.replace('_desc','') == sortColumn:
			sortKey = sortColumn
		else:
			descending = True
			sortKey = self.sortInverse(sortColumn)
		(memberList, items) = self.__db.GetFullMemberList(sortKey, descending)
		html = ''
		if( len(memberList) < 2 ):
			html += '<h2>No members have registered yet</h2>'
		else:
			foundUnapproved = 0
			try:
				for member in memberList:
					if member and not member[items['approved']]:
						foundUnapproved = foundUnapproved + 1
			except Exception, e:
				Error( 'Searching for unapproved members', e );

			if( foundUnapproved > 0 ):
				html += '<form name="approveForm" id="approveForm" '
				html += ' action="javascript:submitForm(\'approveForm\', \'/cgi-bin/bttbApprove.cgi\', \'/#profiles?committee=1\');">'
				html += self.getCommitteeTitle( '%d %s %s' % (foundUnapproved, Pluralize('Member',foundUnapproved), 'Awaiting Confirmation'), sortColumn )
				for member in memberList:
					if member and not member[items['approved']]:
						memberObj = bttbMember()
						memberObj.loadFromTuple( items, member )
						html += memberObj.getCommitteeSummaryRow('XXX')
				html += '</table>'
				html += '<input type="submit" name="submit" value="Approve">'
				html += '</form>'
			else:
				html += '<h2>No New Members</h2>'

			html += '<h2>%d Registered Alumni (click to edit)</h2>' % (len(memberList)-1)
			try:
				column = 0
				html += '<table><tr>'
				for member in memberList:
					if not member or not member[items['approved']]: continue
					if column == 4:
						html += '</tr>\n<tr>'
						column = 0
					column = column + 1
					html += '<td>'
					link = '#register?id=%d' % member[items['id']]
					html += PageLink(link, SensibleName( member[items['first']], member[items['nee']], member[items['last']] ))
					html += '</td>'
			except Exception, e:
				Error( 'Displaying registered alumni list', e );
			html += "</tr></table>\n"
			return html

	def getCommitteeTitle(self,title,sortColumn):
		"""
		Print out the title line of the table showing the profile
		information visible to the committee members.
		"""
		html = '<h2>' + title + '</h2>'
		html += '<div class="subtext">Click on a column heading to sort by that column.</div>'
		html += "<table cellspacing='0' cellpadding='5' border='1'>"
		html += '<tr bgcolor=\'#ffaaaa\'>'
		html += '<th>Approve</th>'
		html += '<th>Committee</th>'
		html += '<th>Friend<br>of the<br>Alumni</th>'
		html += '<th>%s %s %s</th>' % (self.sortLinkC('First', 'first', sortColumn), self.sortLinkC('&nbsp;(nee)', 'nee', sortColumn), self.sortLinkC('&nbsp;Last', 'last', sortColumn))
		html += '<th>%s</th>' % self.sortLinkC('Start&nbsp;Year', 'firstYear', sortColumn)
		html += '<th>%s</th>' % self.sortLinkC('End&nbsp;Year', 'lastYear', sortColumn)
		html += '<th>%s</th>' % self.sortLinkC('Email', 'email', sortColumn)
		html += '<th>%s</th>' % self.sortLinkC('Instrument(s)', 'instruments', sortColumn)
		html += '<th>%s</th>' % self.sortLinkC('Highest Rank', 'rank', sortColumn)
		html += '<th>Address</th>'
		html += '<th>%s</th>' % self.sortLinkC('Positions', 'positions', sortColumn)
		html += '<th>%s</th>' % self.sortLinkC('Keep Private?', 'emailVisible', sortColumn)
		html += '</tr>'
		return html

	def ArchiveData(self):
		"""
		Archive all of the database table information, just in case
		"""
		return self.__db.Archive()

	def getMemberFromId(self, id):
		"""
		Get back a bttbMember whose id matches the given one.
		"""
		if id == None:
			return None
		return self.__db.GetMember(id)

	def getMemberFromLogin(self, name, password):
		"""
		Get back a bttbMember whose login information matches the given one,
		or None if nobody matches.
		"""
		member = self.__db.GetMemberInfo(name)
		if member:
			if member.password and member.password != password:
				member = None
		return member

	def getMostRecent(self, howMany):
		"""
		Return a tuple consisting of the list of the most recent 'howMany'
		members to join and the size of the entire membership list.
		"""
		(memberList, items) = self.__db.GetPublicMemberList('joinTime', True)
		return (memberList[0:howMany], len(memberList))

	def getJoinedAfter(self, earliestTime):
		"""
		Return a tuple consisting of the list of the members who joined
		after the 'earliestTime' and the size of the entire membership list.
		"""
		(memberList, items, totalRegistration) = self.__db.GetPublicMemberListJoinedAfter(earliestTime)
		return (memberList, totalRegistration)

	def getCommitteeText(self):
		"""
		Display full text of all alumni in an Excel/Word-friendly format.
		That is, tab-separated text with a heading line.
		"""
		(memberList, items) = self.__db.GetFullMemberList('last', False)
		html = '\t'.join([a[0].upper()+a[1:] for a in SortDictByValue(items)])
		eventList = self.__db.GetEvents()
		for event in eventList:
			if event.canAttend:
				html += '\tAttend' + event.summary
			if event.canVolunteer:
				html += '\tVolunteer' + event.summary
		html += '\n'

		attendance = self.__db.GetFullEventAttendance()
		volunteers = self.__db.GetFullEventVolunteers()
		if( len(memberList) == 0 ):
			return
		for member in memberList:
			alumniId = member[items['id']]
			html += '\t'.join([fieldString(str(a)) for a in member])
			for event in eventList:
				if event.canAttend:
					attend = '0'
					for (aid, eid, ename) in attendance:
						if aid == alumniId and eid == event.id:
							attend = '1'
							break
					html += '\t' + attend
				if event.canVolunteer:
					volunteer = '0'
					for (aid, eid, ename) in volunteers:
						if aid == alumniId and eid == event.id:
							volunteer = '1'
							break
					html += '\t' + volunteer
			html += '\n'
		return html

	def getMemories(self, id=None):
		"""
		Return the list of memories from the alumni (or all if id=None).
		"""
		return self.__db.GetMemories(id)

	def getMemoriesAfter(self, earliestTime):
		"""
		Return the list of memories from the alumni submitted after the given
		date.
		"""
		return self.__db.GetMemoriesAddedAfter(earliestTime)

	def getParadeInstrumentation(self, paradeTable):
		"""
		Return the list of current parade participants
		"""
		return self.__db.GetParadeInstrumentation(paradeTable)

	def updateMember(self, member, memory, memoryId):
		"""
		Add a new member into the database if it isn't there already,
		or replace it's data if it is already there.
		"""
		self.__db.UpdateMember( member, True )
		self.__db.UpdateMemberMemory( member, memory, memoryId )
		self.ArchiveData()

	def updateMemory(self, member, memory, memoryTime, memoryId):
		"""
		Update the memory in the table. If the memory doesn't exist
		then add a new one to the table.
		"""
		self.__db.UpdateMemory( member.id, memory, memoryTime, memoryId )

	def removeMemory(self, memoryId):
		"""
		Remove the memory from the table.
		"""
		self.__db.RemoveMemory( memoryId )

	def approveMember(self, id, isFriend, onCommittee):
		"""
		Officially approve a new member. The "isFriend" and "onCommittee"
		flags are only accessible to committee members so access them
		from here.
		"""
		member = self.getMemberFromId( id )
		if member:
			member.approved = True
			member.isFriend = isFriend
			member.onCommittee = onCommittee
			member.editTime = datetime.now()
			self.__db.UpdateMember( member, True )
		else:
			Error( 'Tried to approve non-existing member', '%d' % id )

if( __name__ == '__main__' ):
	alum = bttbAlumni()
	print alum.getCommitteeSummary('last')
	print alum.approveMember(3, True, True)

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
