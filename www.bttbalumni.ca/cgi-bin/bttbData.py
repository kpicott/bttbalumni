"""
Generic interface for data storage. Ensure that all sessions are bracketed:
	data = bttbData()  # or subclass
	data.Initialize()
	... lots of interaction ...
	data.Finalize()
"""

import os
from bttbConfig import *

__all__ = [ 'bttbData' ]

class bttbData:
	def __init__(self):
		self.__debug = False
		self.__publicItems = {}
		self.__publicKeys = ['first', 'nee', 'last', 'firstYear', 'lastYear', 'email', 'instruments', 'emailVisible', 'approved', 'onCommittee', 'id']
		idx = 0
		for key in self.__publicKeys:
			self.__publicItems[key] = idx
			idx = idx + 1
		self.__fullItems = {}
		self.__fullKeys = ['first', 'nee', 'last', 'firstYear', 'lastYear', 'email', 'emailVisible', 'isFriend', 'street1', 'street2', 'apt', 'city', 'province', 'country', 'postalCode', 'phone', 'id', 'joinTime', 'editTime', 'instruments', 'positions', 'approved', 'onCommittee', 'rank', 'password']
		idx = 0
		for key in self.__fullKeys:
			self.__fullItems[key] = idx
			idx = idx + 1

	def Finalize(self):		pass
	def Initialize(self):	pass

	def IsDebugOn(self):	return self.__debug
	def TurnDebugOn(self):	self.__debug = True

	def Archive(self):
		"""
		Dump all of the BTTB Alumni data tables out to files for archival or
		backup purposes.
		"""
		pass

	def GetEventAttendees(self, event):
		"""
		Get the tuple list consisting of all attendees of the given event
		"""
		return []

	def GetMemoriesAddedAfter(self, earliestTime):
		"""
		Get the tuple (alumni_id, memory, time, memory_id) with all memories
		that were added after the 'earliestTime' date.
		"""
		return []

	def GetEvents(self):
		"""
		Get the list of all events in the database as bttbEvent objects.
		"""
		return []

	def GetPublicMemberKeys(self):
		"""
		Get the array corresponding to the keys the public member list
		will use from the database.
		"""
		return self.__publicKeys

	def GetPublicMemberItems(self):
		"""
		Get the dictionary corresponding to the public member list items
		used from the database, value is index ordering.
		"""
		return self.__publicItems

	def GetMember(self, id):
		"""
		Get the full table row for the alumni with the specified id.
		Returns a list of tuples containing all alumni table fields.
		The first tuple contains the type names, which could be used to create
		dictionary-like syntax. They should correspond to the bttbMember field
		names.
		"""
		return None

	def GetFullMemberKeys(self):
		"""
		Get the array corresponding to the keys the full member list
		will use from the database.
		"""
		return []

	def GetFullMemberItems(self):
		"""
		Get the dictionary corresponding to the full member list items
		used from the database, value is index ordering.
		"""
		return []

	def GetMemories(self, id=None):
		"""
		Get the tuple (alumni_id, memory, time, memory_id) with all memories.
		If id is specified then use it to filter the list.
		"""
		return []

	def GetFullEventAttendance(self, limit=None):
		"""
		Get the list of all event attendees. Returns a list of tuples:
			(alumni_id, event_id, event_name)
		"""
		return []

	def GetFullEventVolunteers(self, limit=None):
		"""
		Get the list of all event volunteers. Returns a list of tuples:
			(alumni_id, event_id, event_name)
		"""
		return []

	def UpdateMember(self, member, replaceIfExists):
		"""
		Add a new member, or replace the existing member's information.
		"""
		return False

	def UpdateMemberVolunteering(self, member, events):
		"""
		Replace a member's volunteer status
		"""
		return False

	def UpdateMemberAttendance(self, member, events):
		"""
		Replace a member's event attendance status
		"""
		return False

	def UpdateMemberMemory(self, member, memory, memoryId):
		"""
		Replace a member's memory. Only valid until memory lane addition gives
		a more powerful memory editing capability.
		"""
		return False

	def UpdateMemory( self, member, memory, memoryTime, memoryId ):
		"""
		Update the memory in the table. If the memory doesn't exist
		then add a new one to the table.
		"""
		return False

	#----------------------------------------------------------------------
	def RemoveMemory( memoryId ):
		"""
		Mark the memory as removed, but don't actually get rid of it.
		"""
		return False

	def LogPage(self, pageName, who):
		"""
		Log a hit on a particular sub-page so that we can see what areas
		are of the most interest.
		"""
		return False

	def GetMemberInfo(self, name):
		"""
		Get the full table row for the alumn{i,ae} with the specified name.
		Returns a list of bttbMembers whose name matches the given ones.
		"""
		return []

	def GetConcertInstrumentation(self):
		"""
		Get the tuple of concert instrumentation information for all parts
		(instrumentName, instrumentId, signedUpNames)
		"""
		return []

	def GetMemberConcertPart(self, id):
		"""
		Return the tuple of instrument information relevant to this
		member's participation in the concert.
		(instrumentName)
		"""
		return []

	def SetConcertPart(self,alumniId,instrumentId):
		"""
		Set the concert part to be played by the given alumnus.
		"""
		return []

	def GetParadeInstrumentation(self, paradeTable):
		"""
		Get the tuple of parade instrumentation information for all parts
		(instrumentName, instrumentId, hasDownload, signedUpNames)
		"""
		return []

	def GetMemberParadePart(self, id):
		"""
		Return the tuple of instrument information relevant to this
		member's participation in the parade.
		(instrumentName, hasDownload)
		"""
		return []

	def SetParadePart(self,alumniId,instrumentId,needInstrument):
		"""
		Set the parade part to be played by the given alumnus.
		"""
		return []

	def GetWallaceList(self):
		"""
		Return the tuple of Wallace B. Wallace winners
		(name, displayName, year, award, submitTime)
		"""
		return []

if __name__ == '__main__':
	db = bttbData()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
