# -*- coding: iso-8859-15 -*-
"""
BTTB member profile information.
"""
import re
import os.path
from datetime import datetime
from xml.dom import minidom
from bttbConfig import *
#
def _sortByNee(x,y):
	xNee = x.nee
	yNee = y.nee
	if xNee: xNee = xNee.lower()
	if yNee: yNee = yNee.lower()
	return cmp(xNee, yNee)
def _sortByFirstName(x,y):	return cmp(x.first.lower(), y.first.lower())
def _sortByLastName(x,y):	return cmp(x.last.lower(), y.last.lower())
def _sortByFirstYear(x,y):	return cmp(x.firstYear, y.firstYear)
def _sortByLastYear(x,y):	return cmp(x.lastYear, y.lastYear)
def _sortByEmail(x,y):
	xemail = x.email
	yemail = y.email
	if( not x.emailVisible ): xemail = '---'
	if( not y.emailVisible ): yemail = '---'
	return cmp(xemail.lower(), yemail.lower())
def _sortByJoinDate(x,y):
	xJoin = x.joinTime
	yJoin = y.joinTime
	if( not x.joinTime ): xJoin = datetime.datetime(2000,1,1)
	if( not y.joinTime ): yJoin = datetime.datetime(2000,1,1)
	return cmp(xJoin, yJoin)
def _sortByInstrument(x,y):	return cmp(','.join(x.instruments).lower(), ','.join(y.instruments).lower())

def _sortMethod(sortColumn):
	"""
	Return a pointer to the 'sortColumn'th sort method
	"""
	if( sortColumn == 1 ):
		return _sortByFirstName
	elif( sortColumn == 2 ):
		return _sortByNee
	elif( sortColumn == 3 ):
		return _sortByLastName
	elif( sortColumn == 4 ):
		return _sortByFirstYear
	elif( sortColumn == 5 ):
		return _sortByLastYear
	elif( sortColumn == 6 ):
		return _sortByEmail
	elif( sortColumn == 7 ):
		return _sortByInstrument
	else:
		# Default to sorting by last name
		return _sortByLastName

re_filePattern = re.compile('[^0-9]*([0-9]+).xml')

class bttbMember:
	def __init__(self,file):
		self.commonInit()
		try:
			if file:
				self.file = os.path.split(file)[1]
				self.xmldoc = minidom.parse( file )
				self.extractDOM()
				try:
					self.id = int(re_filePattern.match(self.file).group(1))
				except:
					pass
			else:
				self.file = 'temp.xml'
				self.xmldoc = minidom.parseString( '<?xml version="1.0"?><member></member>' )
		except:
			self.file = 'temp.xml'
			self.xmldoc = minidom.parseString( '<?xml version="1.0"?><member></member>' )

	def commonInit(self):
		self.approved = False
		self.onCommittee = False
		self.file = None
		self.editTime = None
		self.joinTime = None
		self.first = None
		self.last = None
		self.nee = None
		self.firstYear = None
		self.lastYear = None
		self.email = None
		self.emailVisible = True
		self.friend = False
		self.instruments = []
		self.attend = []
		self.volunteer = []
		self.positions = []
		self.rank = None
		self.apt = None
		self.street1 = ''
		self.street2 = ''
		self.city = ''
		self.province = 'Ontario'
		self.country = 'Canada'
		self.postalCode = ''
		self.phone = ''
		self.memory = None
		self.joiningBand = 0
		self.joiningConcert = 0
		self.id = 9999999

	def toXml(self):
		"""
		Return the current member in XML format
		"""
		return CleanupXML( self.xmldoc.toxml() )

	def midpoint(self):
		"""
		Return a datetime object representing the rough midpoint of the band
		member's tenure (for estimating events they submit without specific
		times)
		"""
		midYear = (int(self.firstYear) + int(self.lastYear)) / 2.0
		if midYear == int(midYear):
			return datetime(int(midYear), 6, 15)
		else:
			return datetime(int(midYear), 12, 31)

	def setEditTime(self,when):
		"""
		Set the member's edit time, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			timeEl = memberEl.getElementsByTagName('edit')[0]
		except Exception, e:
			timeEl = self.xmldoc.createElement('edit')
			memberEl.appendChild( timeEl )

		timeEl.setAttribute('year', ('%d') % when.date().year)
		timeEl.setAttribute('month', ('%d') % when.date().month)
		timeEl.setAttribute('day', ('%d') % when.date().day)
		timeEl.setAttribute('hour', ('%d') % when.time().hour)
		timeEl.setAttribute('minute', ('%d') % when.time().minute)
		timeEl.setAttribute('second', ('%d') % when.time().second)
		self.editTime = when
		if not self.joinTime:
			self.setJoinTime( when )

	def setJoinTime(self,when):
		"""
		Set the member's joining time, creating the XML element if required
		"""
		if not when:
			return
		memberEl = self.xmldoc.firstChild
		try:
			timeEl = memberEl.getElementsByTagName('join')[0]
		except Exception, e:
			timeEl = self.xmldoc.createElement('join')
			memberEl.appendChild( timeEl )

		timeEl.setAttribute('year', ('%d') % when.date().year)
		timeEl.setAttribute('month', ('%d') % when.date().month)
		timeEl.setAttribute('day', ('%d') % when.date().day)
		timeEl.setAttribute('hour', ('%d') % when.time().hour)
		timeEl.setAttribute('minute', ('%d') % when.time().minute)
		timeEl.setAttribute('second', ('%d') % when.time().second)
		self.joinTime = when

	def setId(self,uniqueId):
		"""
		Set the member's unique id - it's in the file name so no XML addition
		is required.
		"""
		self.id = uniqueId

	def setName(self,first,nee,last):
		"""
		Set the member's name, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			nameEl = memberEl.getElementsByTagName('name')[0]
		except Exception, e:
			nameEl = self.xmldoc.createElement('name')
			memberEl.appendChild( nameEl )

		nameEl.setAttribute('first', first)
		nameEl.setAttribute('last', last)
		if nee != last: nameEl.setAttribute('nee', nee)
		self.first = first
		self.last = last
		if nee != last: self.nee = nee

	def setYears(self,first,last):
		"""
		Set the member's years, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			yearEl = memberEl.getElementsByTagName('years')[0]
		except Exception, e:
			yearEl = self.xmldoc.createElement('years')
			memberEl.appendChild( yearEl )

		yearEl.setAttribute('first', first)
		yearEl.setAttribute('last', last)
		self.firstYear = first
		self.lastYear = last

	def addInstrument(self,instrument):
		"""
		Add an instrument, creating the XML parent element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			instrParent = memberEl.getElementsByTagName('instruments')[0]
		except Exception, e:
			instrParent = self.xmldoc.createElement('instruments')
			memberEl.appendChild( instrParent )

		instrEl = self.xmldoc.createElement('instrument')
		instrEl.setAttribute('name', instrument)
		instrParent.appendChild( instrEl )
		self.instruments.append( instrument )

	def addPosition(self,position):
		"""
		Add a position, creating the XML parent element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			posParent = memberEl.getElementsByTagName('positions')[0]
		except Exception, e:
			posParent = self.xmldoc.createElement('positions')
			memberEl.appendChild( posParent )

		posEl = self.xmldoc.createElement('position')
		posEl.setAttribute('name', position)
		posParent.appendChild( posEl )
		self.positions.append( position )

	def setRank(self,rank):
		"""
		Set the member's highest rank, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			rankEl = memberEl.getElementsByTagName('rank')[0]
			rankEl.nodeValue = rank
		except Exception, e:
			rankEl = self.xmldoc.createElement('rank')
			if rank:
				rankText = self.xmldoc.createTextNode(rank)
				rankEl.appendChild( rankText )
			memberEl.appendChild( rankEl )
		self.rank = rank

	def setContact(self,street1,street2,apt,city,province,country,postalCode,phone,email):
		"""
		Set the member's contact information, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			contactEl = memberEl.getElementsByTagName('contact')[0]
		except Exception, e:
			contactEl = self.xmldoc.createElement('contact')
			memberEl.appendChild( contactEl )

		if street1: contactEl.setAttribute('street1', street1)
		if street2: contactEl.setAttribute('street2', street2)
		if apt: contactEl.setAttribute('apt', apt)
		if city: contactEl.setAttribute('city', city)
		if province: contactEl.setAttribute('province', province)
		if country: contactEl.setAttribute('country', country)
		if postalCode: contactEl.setAttribute('postalCode', postalCode)
		if phone: contactEl.setAttribute('phone', phone)
		if email: contactEl.setAttribute('email', email)
		self.street1 = street1
		self.street2 = street2
		self.apt = apt
		self.city = city
		self.province = province
		self.country = country
		self.postalCode = postalCode
		self.phone = phone
		contactEl.setAttribute('email', email)

	def setEmailVisible(self,isVisible):
		"""
		Set the member's email visibility, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			visEl = memberEl.getElementsByTagName('emailVisible')[0]
		except Exception, e:
			visEl = self.xmldoc.createElement('emailVisible')
			memberEl.appendChild( visEl )

		visEl.setAttribute('value', isVisible and "1" or "0")
		self.emailVisible = isVisible

	def setJoiningBand(self,marching):
		"""
		Set the member's marching status, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			bandEl = memberEl.getElementsByTagName('joiningBand')[0]
		except Exception, e:
			bandEl = self.xmldoc.createElement('joiningBand')
			memberEl.appendChild( bandEl )

		if marching == 'Yes':
			self.joiningBand = 1
		elif marching == 'No':
			self.joiningBand = 0
		else:
			self.joiningBand = 2
		bandEl.setAttribute('value', ('%d') % (self.joiningBand))

	def setJoiningConcert(self,playing):
		"""
		Set the member's marching status, creating the XML element if required
		"""
		memberEl = self.xmldoc.firstChild
		try:
			concertEl = memberEl.getElementsByTagName('joiningConcert')[0]
		except Exception, e:
			concertEl = self.xmldoc.createElement('joiningConcert')
			memberEl.appendChild( concertEl )

		if playing == 'Yes':
			self.joiningConcert = 1
		elif playing == 'No':
			self.joiningConcert = 0
		else:
			self.joiningConcert = 2
		concertEl.setAttribute('value', ('%d') % (self.joiningConcert))

	def isAttending(self,event):
		"""
		Returns true if the member wants to attend the given event
		"""
		for attend in self.attend:
			if attend == event:
				return True
		if (event == 'Parade') and self.joiningBand:
			return True
		if (event == 'Concert') and self.joiningConcert:
			return True
		return False

	def addEventAttendance(self,event):
		"""
		Add an event the member will attend, creating the XML parent element if required
		"""
		if not event:
			return
		memberEl = self.xmldoc.firstChild
		try:
			eventParent = memberEl.getElementsByTagName('attending')[0]
		except Exception, e:
			eventParent = self.xmldoc.createElement('attending')
			memberEl.appendChild( eventParent )

		eventEl = self.xmldoc.createElement('event')
		eventEl.setAttribute('name', event)
		eventParent.appendChild( eventEl )
		self.attend.append( event )

	def isVolunteering(self,event):
		"""
		Returns true if the member wants to volunteer for the given event
		"""
		for volunteer in self.volunteer:
			if volunteer == event:
				return True
		return False

	def addEventVolunteer(self,event):
		"""
		Add an event the member will help with, creating the XML parent element if required
		"""
		if not event:
			return
		memberEl = self.xmldoc.firstChild
		try:
			eventParent = memberEl.getElementsByTagName('volunteering')[0]
		except Exception, e:
			eventParent = self.xmldoc.createElement('volunteering')
			memberEl.appendChild( eventParent )

		eventEl = self.xmldoc.createElement('volunteer')
		eventEl.setAttribute('name', event)
		eventParent.appendChild( eventEl )
		self.volunteer.append( event )

	def setMemory(self,memory):
		"""
		Set the member's fond memory, creating the XML element if required
		"""
		if not memory:
			return
		memory = memory.strip()
		memberEl = self.xmldoc.firstChild
		try:
			memoryEl = memberEl.getElementsByTagName('memory')[0]
			self.memory = yearEl.nodeValue
			memoryEl.nodeValue = memory
		except Exception, e:
			memoryEl = self.xmldoc.createElement('memory')
			if memory:
				memoryText = self.xmldoc.createTextNode(memory)
				memoryEl.appendChild( memoryText )
			memberEl.appendChild( memoryEl )

	def extractDOM(self):
		"""
		Read the xml data file, parse it, and populate the object
		"""
		try:
			memberEl = self.xmldoc.firstChild
			#----------------------------------------
			try:
				nameEl = memberEl.getElementsByTagName('name')[0]
				self.first = nameEl.attributes.get('first').value
				self.last = nameEl.attributes.get('last').value
				try:
					self.nee = nameEl.attributes.get('nee').value
				except:
					# Not a required field
					pass
			except Exception, e:
				Warning( '*** Name exception:', e )
			#----------------------------------------
			try:
				timeEl = memberEl.getElementsByTagName('edit')[0]
				self.editTime = datetime(int(timeEl.attributes.get('year').value),	\
									 int(timeEl.attributes.get('month').value),		\
									 int(timeEl.attributes.get('day').value),		\
									 int(timeEl.attributes.get('hour').value),		\
									 int(timeEl.attributes.get('minute').value),	\
									 int(timeEl.attributes.get('second').value))
			except Exception, e:
				self.editTime = datetime.now()
			#----------------------------------------
			try:
				timeEl = memberEl.getElementsByTagName('join')[0]
				self.joinTime = datetime(int(timeEl.attributes.get('year').value),	\
									 int(timeEl.attributes.get('month').value),		\
									 int(timeEl.attributes.get('day').value),		\
									 int(timeEl.attributes.get('hour').value),		\
									 int(timeEl.attributes.get('minute').value),	\
									 int(timeEl.attributes.get('second').value))
			except Exception, e:
				self.joinTime = datetime.now()
			#----------------------------------------
			yearEl = memberEl.getElementsByTagName('years')[0]
			try:
				self.firstYear = yearEl.attributes.get('first').value
				self.lastYear = yearEl.attributes.get('last').value
			except Exception, e:
				Warning( '*** Year exception:', e )
			#----------------------------------------
			try:
				memoryEl = memberEl.getElementsByTagName('memory')[0]
				self.memory = memoryEl.firstChild.nodeValue.strip()
			except:
				pass
			#----------------------------------------
			try:
				rankEl = memberEl.getElementsByTagName('rank')[0]
				self.rank = rankEl.firstChild.nodeValue
			except:
				pass
			#----------------------------------------
			try:
				joinEl = memberEl.getElementsByTagName('joiningBand')[0]
				self.joiningBand = int(joinEl.attributes.get('value').value)
			except:
				pass
			#----------------------------------------
			try:
				joinEl = memberEl.getElementsByTagName('joiningConcert')[0]
				self.joiningConcert = int(joinEl.attributes.get('value').value)
			except:
				pass
			#----------------------------------------
			try:
				eventsEl = memberEl.getElementsByTagName('attending')[0]
				for eventEl in eventsEl.getElementsByTagName('event'):
					try:
						self.attend.append( eventEl.attributes.get('name').value )
					except Exception, e:
						Warning( '*** Events exception:', e )
			except:
				pass
			#----------------------------------------
			try:
				volunteerEl = memberEl.getElementsByTagName('volunteering')[0]
				for eventEl in volunteerEl.getElementsByTagName('volunteer'):
					try:
						self.volunteer.append( eventEl.attributes.get('name').value )
					except Exception, e:
						Warning( '*** Volunteering exception:', e )
			except:
				pass
			#----------------------------------------
			try:
				instrumentsEl = memberEl.getElementsByTagName('instruments')[0]
				for instrumentEl in instrumentsEl.getElementsByTagName('instrument'):
					try:
						self.instruments.append( instrumentEl.attributes.get('name').value )
					except Exception, e:
						Warning( '*** Instrument exception:', e )
			except Exception, e:
				pass
			#----------------------------------------
			try:
				positionsEl = memberEl.getElementsByTagName('positions')[0]
				for positionEl in positionsEl.getElementsByTagName('position'):
					try:
						self.positions.append( positionEl.attributes.get('name').value )
					except Exception, e:
						Warning( '*** Position exception:', e )
			except Exception, e:
				pass
			#----------------------------------------
			try:
				contactEl = memberEl.getElementsByTagName('contact')[0]
				if contactEl.attributes.get('email'):
					self.email = contactEl.attributes.get('email').value
				if contactEl.attributes.get('apt'):
					self.apt = contactEl.attributes.get('apt').value
				if contactEl.attributes.get('street1'):
					self.street1 = contactEl.attributes.get('street1').value
				if contactEl.attributes.get('street2'):
					self.street2 = contactEl.attributes.get('street2').value
				if contactEl.attributes.get('city'):
					self.city = contactEl.attributes.get('city').value
				if contactEl.attributes.get('province'):
					self.province = contactEl.attributes.get('province').value
				if contactEl.attributes.get('country'):
					self.country = contactEl.attributes.get('country').value
				if contactEl.attributes.get('postalCode'):
					self.postalCode = contactEl.attributes.get('postalCode').value
				if contactEl.attributes.get('phone'):
					self.phone = contactEl.attributes.get('phone').value
			except Exception, e:
				Warning( '*** Name exception:', e )
			#----------------------------------------
		except Exception, e:
			Warning( '*** Main level exception:', e )

	def fullName(self):
		"""
		Return a string with the full name, formatted sensibly
		"""
		fullName = ''
		if( self.nee and len(self.nee) > 0 ):
			fullName = ('%s&nbsp;(%s)&nbsp;%s') % (self.first,self.nee,self.last)
		else:
			fullName = ('%s&nbsp;%s') % (self.first,self.last)
		return fullName

	def fullAddress(self):
		"""
		Return a string with the full address, formatted sensibly
		"""
		fullAddress = []
		if self.street1 and len(self.street1) > 0:
			if self.apt and len(self.apt) > 0:
				fullAddress.append( ''.join([self.street1, ', Unit ', self.apt]) )
			else:
				fullAddress.append( self.street1 )
		if self.street2 and len(self.street2) > 0:
			fullAddress.append( self.street2 )
		if self.city and len(self.city) > 0:
			if self.province and len(self.province) > 0:
				fullAddress.append( self.city )
			else:
				fullAddress.append( ''.join([self.city, ', ', self.province]))
		if self.country and len(self.country) > 0:
			fullAddress.append( self.country )
		if self.postalCode and len(self.postalCode) > 0:
			fullAddress.append( self.postalCode )
		if self.phone and len(self.phone) > 0:
			fullAddress.append( self.phone )
		return '<br>'.join( fullAddress )

	def printFullSummary(self):
		"""
		Dump a full summary of the member input information as a block.
		"""
		def pfsRow(title,value):
			print '<tr><th valign="top">', title, '</th>'
			print '<th valign="top">&nbsp;:&nbsp;</th>'
			print '<td valign="top">', value, '</td></tr>'

		print '<table bgcolor="#ffbbbb" cellpadding="0">'
		pfsRow( 'First Year', self.firstYear )
		pfsRow( 'Last Year', self.lastYear )
		pfsRow( 'Email', self.email )
		pfsRow( 'Share Email?', self.emailVisible )
		pfsRow( 'Instrument(s)', ', '.join(self.instruments) )
		pfsRow( 'Position(s)', ', '.join(self.positions) )
		pfsRow( 'Address', self.fullAddress() )
		pfsRow( 'Memory', self.memory )
		pfsRow( 'Joining Parade?', ['No', 'Yes', 'Maybe'][self.joiningBand] )
		pfsRow( 'Joining Concert?', ['No', 'Yes', 'Maybe'][self.joiningConcert] )
		if self.rank:
			pfsRow( 'Boys and Girls Rank', self.rank )
		pfsRow( 'Events Attending', ', '.join(self.attend) )
		pfsRow( 'Events Volunteering', ', '.join(self.volunteer) )
		print '</table>'

	def printSummaryRow(self):
		"""
		Display this member as a row in a table.
		"""
		print '<tr>'
		# Disable the edit link for now, until a login is possible
		# print '<td valign=\'top\'><a'
		# link = CgiHref() + '/register.cgi?id=%d' % (self.id)
		# print 'href="' + link + '">Edit</a></td>'
		print '<td valign=\'top\'>', self.fullName(), '</td>'
		print '<td valign=\'top\' align=\'center\'>', self.firstYear, '</td>'
		print '<td valign=\'top\' align=\'center\'>', self.lastYear, '</td>'
		if( self.email and self.emailVisible ):
			print '<td valign=\'top\'><a class=\'email\' href=\'mailto:' + self.email + '\'>', self.email, '</td>'
		else:
			print '<td valign=\'top\' align=\'center\'>---</td>'
		print '<td valign=\'top\'>', ', '.join(self.instruments), '</td>'
		print '</tr>'

	def printCommitteeSummaryRow(self,checkPrefix):
		"""
		Display full details on this member as a row in a table.
		"""
		print '<tr>'
		if checkPrefix:
			print '<td align=\'center\' valign=\'center\'>'
			print '<input type="checkbox" value="1" name="A' + checkPrefix + self.file + '">'
			print '<td align=\'center\' valign=\'center\'>'
			print '<input type="checkbox" value="1" name="R' + checkPrefix + self.file + '">'
			print '</td>'
			print '<td align=\'center\' valign=\'center\'>'
			print '<input type="checkbox" value="1" name="F' + checkPrefix + self.file + '">'
			print '</td>'
		else:
			print '<td colspan=\'2\' align=\'center\' valign=\'center\'>'
			link = CgiHref() + '/register.cgi?id=%d' % (self.id)
			print '<a href="' + link + '">Edit</a>'
			print '</td>'
			print '<td align=\'center\' valign=\'center\'>'
			if self.friend:
				print '&hearts;'
			else:
				print '&nbsp;'
			print '</td>'
		print '<td valign=\'top\'>', self.fullName(), '</td>'
		print '<td valign=\'top\' align=\'center\'>', self.firstYear, '</td>'
		print '<td valign=\'top\' align=\'center\'>', self.lastYear, '</td>'
		if( self.email and self.emailVisible ):
			print '<td valign=\'top\'><a class=\'email\' href=\'mailto:' + self.email + '\'>', self.email, '</td>'
		else:
			print '<td valign=\'top\' align=\'center\'>---</td>'
		print '<td valign=\'top\'>', ', '.join(self.instruments), '</td>'
		print '<td valign=\'top\'>', self.rank and self.rank or '--', '</th>'
		print '<td width=\'324\' valign=\'top\'>',
		if self.memory:
			print "<a onClick='Effect.toggle(\"memory%d\", \"slide\"); return false;'>Click to Toggle</a>" % (self.id)
			print "<div id='memory%d' style='display:none;'>" % (self.id)
			print "<div style='background-color:#ffa0a0;width:300px;border:2px solid red;padding:10px;'>"
			print self.memory + "</div></div>"
		else:
			print '--',
		print '</th>'
		print '<td width=\'224\' valign=\'top\'>',
		print "<a onClick='Effect.toggle(\"address%d\",\"slide\"); return false;'>Click to Toggle</a>" % (self.id)
		print "<div id='address%d' style='display:none;'>" % (self.id)
		print "<div style='background-color:#a0a0ff;width:200px;border:2px solid blue;padding:10px;'>"
		print self.fullAddress() + "</div></div>"
		print '</td>'
		print '<td valign=\'top\'>', ', '.join(self.positions), '</th>'
		print '<td valign=\'top\'>', self.emailVisible and 'No' or 'Yes', '</th>'
		print '<td valign=\'top\'>', ['No', 'Yes', 'Maybe'][self.joiningBand], '</th>'
		print '<td valign=\'top\'>', ['No', 'Yes', 'Maybe'][self.joiningConcert], '</th>'
		print '<td valign=\'top\'>', ', '.join(self.attend), '</th>'
		print '<td valign=\'top\'>', ', '.join(self.volunteer), '</th>'
		print '</tr>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
