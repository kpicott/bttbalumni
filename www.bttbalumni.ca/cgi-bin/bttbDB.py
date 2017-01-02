"""
Implementation of bttbData that uses a MySQL database.
May be the only implementation, but it had to be switched once already
so it's only prudent to create this layer just in case.
Although the base class is flexible all uses of this class *must*
follow this pattern:
	db = bttbDB()
	db.Initialize()
	...
	db.Finalize()
"""

import MySQLdb
import os
import re
import datetime
from bttbConfig import *
from bttbData import *
from bttbEvent import *
from bttbMember import *

__all__ = [ 'bttbDB' ]

class bttbDB( bttbData ):
	def __init__(self):
		self.__stage = 'Begin'
		self.__cursor = None
		self.__db = None
		self.__connectDepth = 0
		bttbData.__init__(self)
	
	#----------------------------------------------------------------------
	def cursor(self):		return self.__cursor
	def currentStage(self):	return self.__stage
	def execute(self,sql):
		sql = sql.strip().rstrip()
		self.stage(sql)
		if self.IsDebugOn(): print 'Start "' + self.__stage + '"'
		return self.__cursor.execute(sql)

	#----------------------------------------------------------------------
	def stage(self,name):
		if self.IsDebugOn(): print 'Completed "' + self.__stage + '"'
		self.__stage = name

	#----------------------------------------------------------------------
	def Finalize(self):	self.close()

	#----------------------------------------------------------------------
	def close(self):
		self.stage( 'complete' )
		if self.IsDebugOn(): print 'Close DB connection level %d' % self.__connectDepth
		self.__connectDepth = self.__connectDepth - 1
		if self.IsDebugOn() and self.__connectDepth < 0:
			Error('Too many DB closes', self.__stage)
		if self.__connectDepth <= 0:
			if self.__cursor: self.__cursor.close()
			self.__cursor = None

	#----------------------------------------------------------------------
	def Initialize(self, dbName='bttb'):
		self.__dbName = dbName
		self.connect()

	#----------------------------------------------------------------------
	def connect(self):
		self.__connectDepth = self.__connectDepth + 1
		if self.IsDebugOn(): print 'Open DB connection level %d' % self.__connectDepth
		if self.__cursor:
			return
		try:
			if os.getenv('USER') == 'Dad' or os.getenv('USER') == 'kpicott' or os.getenv('SERVER_NAME') == 'band.local':
				self.__db = MySQLdb.connect( host='localhost', db='%s' % self.__dbName, user='Dad', passwd='mysql300Pins' )
			else:
				self.__db = MySQLdb.connect( host='localhost', db='%s' % self.__dbName.upper(), user='bttb', passwd='bttb999' )

			self.stage( 'Get cursor' )
			self.__cursor = self.__db.cursor()

			return True
		except Exception, e:
			print '*** ERROR: (', self.__stage, ') : ', e
		return False

	#----------------------------------------------------------------------
	def _getTableColumnNames(self, table):
		"""
		Internal function to return a list of the columns used by a table.
		Mostly used to populate the table into an object automatically.
		"""
		columnItems = {}
		try:
			self.connect()
			self.execute( "SHOW COLUMNS FROM " + table )
			columnList = [fieldC for (fieldC, typeC, nullC, keyC, defaultC, extraC) in self.__cursor.fetchall()]
			idx = 0
			for column in columnList:
				columnItems[column] = idx
				idx = idx + 1
			self.close()
		except:
			pass
		return columnItems

	#----------------------------------------------------------------------
	def Archive(self):
		"""
		Dump all of the BTTB Alumni data tables out to files for archival or
		backup purposes.
		"""
		alumDir = DataPath()
		try:
			self.connect()
			self.stage( 'Archive tables' )
			for table in TableList():
				tableFile = alumDir + '/' + self.__dbName + table + 'File.txt'
				Backup( tableFile )
				tableFD = open(tableFile, 'w')
				columnNames = self._getTableColumnNames( table )
				title = ""
				keyNames = columnNames.keys()
				keyNames.sort( lambda x,y: cmp (columnNames[x], columnNames[y]) )
				for col in keyNames:
					title += '%s\t' % col
				title += "\n"
				tableFD.write( title )
				self.stage( 'Archive %s' % table )
				query = "SELECT * from %s" % table
				self.execute( query )
				for row in self.__cursor.fetchall():
					rowString = ""
					for col in row:
						rowString += ArchiveFormat('%s' % col) + '\t'
					rowString += "\n"
					tableFD.write( rowString )
				tableFD.close()
			self.close()
		except Exception, e:
			print Error(self.__stage, e)

	#----------------------------------------------------------------------
	def GetEventAttendees(self, event):
		"""
		Get the tuple list consisting of all attendees of the given event
		"""
		attendList = {}
		try:
			self.connect()
			self.stage( 'Constructing event attendance query' )
			query = """
				SELECT alumni.first,alumni.nee,alumni.last
				FROM alumni INNER JOIN attendance,60thevents
				WHERE alumni.id=attendance.alumni_id
					AND attendance.event_id=60thevents.id
					AND 60thevents.summary='%s'
				ORDER by alumni.last""" % event
			self.execute( query )
			attendList = self.__cursor.fetchall()
			self.close()
		except Exception, e:
			print Error(self.__stage, e)
		return attendList

	#----------------------------------------------------------------------
	def GetMemories(self, id=None):
		"""
		Get the tuple (alumni_id, memory, time, memory_id) with all memories.
		If id is specified then use it to filter the list.
		"""
		memoryList = {}
		try:
			self.connect()
			self.stage( 'Constructing memory query' )
			where = ' WHERE alumni.id=memories.alumni_id AND memories.removed=0'
			if id != None:
				where += ' AND alumni.id=%d' % id
			query = "SELECT alumni.id,memories.memory,memories.memoryTime,memories.submitTime,memories.id FROM alumni INNER JOIN memories%s" % where
			self.execute( query )
			memoryList = self.__cursor.fetchall()
			self.close()
		except Exception, e:
			print Error(self.__stage, e)
		# Convert the tuple to a list, for sorting
		return [memory for memory in memoryList]

	#----------------------------------------------------------------------
	def GetMemoriesAddedAfter(self, earliestTime):
		"""
		Get the tuple (alumni_id, memory, time, memory_id) with all memories
		that were added after the 'earliestTime' date.
		"""
		memoryList = {}
		try:
			self.connect()
			self.stage( 'Constructing memory query' )
			query = "SELECT alumni.id,memories.memory,memories.memoryTime,memories.submitTime,memories.id FROM alumni INNER JOIN memories"
			query += ' WHERE alumni.id=memories.alumni_id AND memories.removed=0'
			query += " AND memories.submitTime > '%s'" % earliestTime.strftime('%Y-%m-%d')
			query += ' ORDER BY memories.submitTime DESC'
			self.execute( query )
			memoryList = self.__cursor.fetchall()
			self.close()
		except Exception, e:
			print Error(self.__stage, e)
		# Convert the tuple to a list, for sorting
		return [memory for memory in memoryList]

	#----------------------------------------------------------------------
	def GetEvents(self):
		"""
		Get the list of all events in the database as bttbEvent objects.
		"""
		eventList = {}
		try:
			self.connect()
			self.stage( 'Constructing events query' )
			query = "SELECT * FROM 60thevents ORDER BY eventDate"
			self.execute( query )
			eventList = self.__cursor.fetchall()
			self.close()
			keys = self._getTableColumnNames( '60thevents' )
		except Exception, e:
			print Error(self.__stage, e)
		return [bttbEvent(keys,event) for event in eventList]

	#----------------------------------------------------------------------
	def GetPublicMemberList(self, sortedBy='firstYear', descending=False, limit=None):
		"""
		Get the list of alumni in the specified order.
		Use the name of the table fields for the sortedBy value.
		Returns a tuple list, the last entry of which contains the field names
		"""
		if descending: sortedBy = sortedBy + ' DESC'
		memberList = []
		try:
			self.connect()
			self.stage( 'Constructing sort query' )
			if limit:
				limit = " LIMIT %d" % limit
			elif self.IsDebugOn():
				limit = " LIMIT 3"
			else:
				limit = ""
			query = " SELECT " + ', '.join(self.GetPublicMemberKeys()) + " FROM alumni ORDER BY " + sortedBy + limit
			self.execute( query )
			memberList = self.__cursor.fetchall()
			self.close()
		except Exception, e:
			print '*** ERROR: (', self.__stage, ') : ', e
		return (memberList, self.GetPublicMemberItems())

	#----------------------------------------------------------------------
	def GetPublicMemberListJoinedAfter(self, earliestTime):
		"""
		Get the list of alumni in join time order who joined after the
		specified date.  Returns a tuple list, the last entry of which
		contains the field names
		"""
		memberList = []
		memberCount = 0
		try:
			self.connect()
			self.stage( 'Constructing joinTime sort query' )
			query = """
			SELECT %s FROM alumni WHERE joinTime > '%s' ORDER BY joinTime DESC
			""" % (', '.join(self.GetPublicMemberKeys()), earliestTime.strftime('%Y-%m-%d'))
			self.execute( query )
			memberList = self.__cursor.fetchall()
			self.execute( 'SELECT COUNT(*) from alumni;' )
			memberCount = int(self.__cursor.fetchone()[0])
			self.close()
		except Exception, e:
			print '*** ERROR: (', self.__stage, ') : ', e
		return (memberList, self.GetPublicMemberItems(), memberCount)

	#----------------------------------------------------------------------
	def GetFullMemberKeys(self):
		"""
		Get the list of all field keys for the alumni member database.
		"""
		return self._getTableColumnNames( 'alumni' )

	#----------------------------------------------------------------------
	def GetFullMemberList(self, sortedBy='firstYear', descending=False, limit=None):
		"""
		Get the list of alumni in the specified order.
		Use the name of the table fields for the sortedBy value.
		Returns a list of tuples containing all alumni table fields.
		The first tuple contains the type names, which could be used to create
		dictionary-like syntax. They should correspond to the bttbMember field
		names.
		"""
		if descending: sortedBy = sortedBy + ' DESC'
		memberList = []
		columnItems = {}
		try:
			columnItems = self.GetFullMemberKeys()
			self.connect()
			if limit:
				limit = " LIMIT %d" % limit
			elif self.IsDebugOn():
				limit = " LIMIT 10"
			else:
				limit = ""
			self.execute( "SELECT * FROM alumni ORDER BY " + sortedBy + limit )
			memberList = self.__cursor.fetchall()
			self.close()
		except Exception, e:
			print Error(self.__stage, e)
			pass
		return (memberList, columnItems)
	
	#----------------------------------------------------------------------
	def GetMember(self, id):
		"""
		Get the full table row for the alumni with the specified id.
		Returns a list of tuples containing all alumni table fields.
		The first tuple contains the type names, which could be used to create
		dictionary-like syntax. They should correspond to the bttbMember field
		names.
		"""
		member = None
		try:
			columnItems = {}
			columnItems = self.GetFullMemberKeys()
			self.connect()
			self.execute( "SELECT * FROM alumni WHERE alumni.id = %d" % id )
			memberInfo = self.__cursor.fetchone()
			self.close()
			if memberInfo:
				member = bttbMember()
				member.loadFromTuple( columnItems, memberInfo )
		except Exception, e:
			Error(self.__stage, e)
			pass
		return member

	#----------------------------------------------------------------------
	def GetFullEventAttendance(self, limit=None):
		"""
		Get the list of all event attendees. Returns a list of tuples:
			(alumni_id, event_id, event_name)
		"""
		query = """
		SELECT DISTINCT alumni.id,60thevents.id,60thevents.summary
		FROM alumni INNER JOIN attendance,60thevents
		WHERE alumni.id = attendance.alumni_id
		AND 60thevents.canAttend = 1
		AND 60thevents.id = attendance.event_id
		ORDER BY alumni.id,60thevents.id
		"""
		attendance = []
		try:
			self.connect()
			if limit:
				limit = " LIMIT %d" % limit
			elif self.IsDebugOn():
				limit = " LIMIT 10"
			else:
				limit = ""
			self.execute( query + limit )
			attendance = self.__cursor.fetchall()
			self.close()
		except:
			pass
		return attendance

	#----------------------------------------------------------------------
	def GetFullEventVolunteers(self, limit=None):
		"""
		Get the list of all event volunteers. Returns a list of tuples:
			(alumni_id, event_id, event_name)
		"""
		query = """
		SELECT DISTINCT alumni.id,60thevents.id,60thevents.summary
		FROM alumni INNER JOIN volunteers,60thevents
		WHERE alumni.id=volunteers.alumni_id
		AND 60thevents.canVolunteer = 1
		AND 60thevents.id = volunteers.event_id
		ORDER BY alumni.id,60thevents.id
		"""
		volunteers = []
		try:
			self.connect()
			if limit:
				limit = " LIMIT %d" % limit
			elif self.IsDebugOn():
				limit = " LIMIT 10"
			else:
				limit = ""
			self.execute( query + limit )
			volunteers = self.__cursor.fetchall()
			self.close()
		except:
			pass
		return volunteers

	#----------------------------------------------------------------------
	def UpdateMember(self, member, replaceIfExists):
		"""
		Add a new member, or replace the existing member's information.
		"""
		try:
			self.connect()
			selectCmd = "SELECT id FROM alumni WHERE alumni.id = %d" % member.id
			self.execute( selectCmd )
			memberInfo = self.__cursor.fetchone()
			if memberInfo:
				if replaceIfExists:
					self.stage( 'TRYING UPDATE' )
					self.__updateMemberData(member)
					self.stage( 'SUCCEEDED AT UPDATE' )
			else:
				self.__addMemberData(member)

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def UpdateMemberVolunteering(self, member, events):
		"""
		Replace a member's volunteer status
		"""
		try:
			self.connect()

			# Remove existing volunteer information
			deleteCmd = """
				DELETE FROM volunteers WHERE alumni_id = %d
				""" % member.id
			self.execute( deleteCmd )
			# Add volunteer information
			allEvents = FullVolunteerList()
			for event in events:
				if event == 'Anything':
					events = VolunteerList()
					break
			for event in events:
				insertCmd = """
					INSERT INTO volunteers (alumni_id, event_id) VALUES (%d, %d);
					""" % (member.id, allEvents[event])
				self.execute( insertCmd )

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def UpdateMemberAttendance(self, member, events):
		"""
		Replace a member's event attendance status
		"""
		try:
			self.connect()

			# Remove existing attendance information
			deleteCmd = """
				DELETE FROM attendance WHERE alumni_id = %d
				""" % member.id
			self.execute( deleteCmd )
			# Add attendance information
			allEvents = AttendList()
			for event in events:
				insertCmd = """
					INSERT INTO attendance (alumni_id, event_id) VALUES (%d, %d);
					""" % (member.id, allEvents[event])
				self.execute( insertCmd )
				if event == 'Concert':
					insertCmd = """
						INSERT INTO attendance (alumni_id, event_id) VALUES (%d, %d);
						""" % (member.id, allEvents['Concert Practice'])
					self.execute( insertCmd )

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def UpdateMemberMemory(self, member, memory, memoryId):
		"""
		Replace a member's memory. Only valid until memory lane addition gives
		a more powerful memory editing capability.
		"""
		try:
			self.connect()

			# Remove existing attendance information
			if memoryId < 0:
				deleteCmd = """
					DELETE FROM memories WHERE alumni_id = %d AND id = %d
					""" % (member.id, -memoryId)
			else:
				deleteCmd = """
					DELETE FROM memories WHERE alumni_id = %d AND id = %d
					""" % (member.id, memoryId)
			self.execute( deleteCmd )
			# Add attendance information
			if memory and len(memory) > 0:
				insertCmd = """
					INSERT INTO memories (alumni_id, memory, memoryTime, submitTime) VALUES (%d, '%s', '%s', '%s');
					""" % (member.id, DbFormat(memory), \
						   member.midpoint().strftime('%Y-%m-%d'), \
						   datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				self.execute( insertCmd )

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def UpdateMemory( self, memberId, memory, memoryTime, memoryId ):
		"""
		Update the memory in the table. If the memory doesn't exist
		then add a new one to the table.
		"""
		try:
			self.connect()

			self.execute( "SELECT id FROM memories WHERE id = %d;" % memoryId )
			memberInfo = self.__cursor.fetchone()
			if memberInfo:
				self.execute( """
				UPDATE memories SET memory='%s', memoryTime='%s'
				WHERE id = %d;
				""" % (DbFormat(memory), memoryTime.strftime('%Y-%m-%d'), memoryId))
			else:
				self.execute( """
					INSERT INTO memories (alumni_id, memory, memoryTime, submitTime)
					VALUES (%d, '%s', '%s', '%s');
					""" % (memberId, DbFormat(memory), \
						   memoryTime.strftime('%Y-%m-%d'), \
						   datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) )

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def RemoveMemory( self, memoryId ):
		"""
		Mark the memory as removed, but don't actually get rid of it.
		"""
		try:
			self.connect()
			self.execute( """
				UPDATE memories SET removed=1 WHERE id = %d;
				""" % memoryId )

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def __addMemberData(self, member):
		"""
		Insert a single alumni into the alumni table, if it isn't already there
		"""
		self.TurnDebugOn()
		try:
			self.stage( 'ADD MEMBER DATA' )
			firstYear = int(member.firstYear) and int(member.firstYear) or 2006
			lastYear = int(member.lastYear) and int(member.lastYear) or 2006
			joinTime = member.joinTime.strftime('%Y-%m-%d %H:%M:%S')
			editTime = member.editTime.strftime('%Y-%m-%d %H:%M:%S')
			instruments = ', '.join(member.instruments)
			positions = ', '.join(member.positions)
			insertCmd = """
			INSERT INTO alumni (first, nee, last, firstYear, lastYear, email, emailVisible,
			isFriend, street1, street2, apt, city, province, country, postalCode, phone, id,
			joinTime, editTime, instruments, positions, approved, onCommittee, rank, password)
			VALUES
			('%s', '%s', '%s', %d, %d, '%s', %d,
			 %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d,
			 '%s', '%s', '%s', '%s', %d, %d, '%s', '%s' );
			""" % (DbFormat(member.first), 				\
				   DbFormat(member.nee), 				\
				   DbFormat(member.last), 				\
				   firstYear, 							\
				   lastYear, 							\
				   DbFormat(member.email), 				\
				   member.emailVisible, 				\
				   member.isFriend, 					\
				   DbFormat(member.street1), 			\
				   DbFormat(member.street2), 			\
				   DbFormat(member.apt), 				\
				   DbFormat(member.city), 				\
				   DbFormat(member.province), 			\
				   DbFormat(member.country), 			\
				   DbFormat(member.postalCode), 		\
				   DbFormat(PhoneFormat(member.phone)),	\
				   member.id, 							\
				   joinTime, 							\
				   editTime,							\
				   DbFormat(instruments), 				\
				   DbFormat(positions), 				\
				   member.approved, 					\
				   member.onCommittee, 					\
				   DbFormat(member.rank),				\
				   DbFormat(member.password) )
			self.execute( insertCmd )
			self.stage( 'ADD COMPLETE' )
		except Exception, e:
			Warning( self.currentStage(), e )
		return True

	#----------------------------------------------------------------------
	def __updateMemberData(self, member):
		"""
		Update alumni data in the alumni table, assuming it's there.
		A bunch of duplication from the above method but since the
		implementation is so small coalescing them would be just as
		large and slightly more complicated.  The only real difference is
		the SQL syntax.
		"""
		try:
			self.stage( 'UPDATE MEMBER DATA' )
			firstYear = member.firstYear and int(member.firstYear) or 2006
			lastYear = member.lastYear and int(member.lastYear) or 2006
			joinTime = member.joinTime.strftime('%Y-%m-%d %H:%M:%S')
			editTime = member.editTime.strftime('%Y-%m-%d %H:%M:%S')
			instruments = ', '.join(member.instruments)
			positions = ', '.join(member.positions)
			self.stage( 'UPDATE COMPLETE' )
			insertCmd = """
			UPDATE alumni SET first='%s', nee='%s', last='%s', firstYear=%d, lastYear=%d,
			email='%s', emailVisible=%d, isFriend=%d,
			street1='%s', street2='%s', apt='%s', city='%s',
			province='%s', country='%s', postalCode='%s', phone='%s', joinTime='%s',
			editTime='%s', instruments='%s', positions='%s',
			approved=%d, onCommittee=%d, rank='%s', password='%s'
			WHERE id = %d;
			""" % (DbFormat(member.first), 				\
				   DbFormat(member.nee), 				\
				   DbFormat(member.last), 				\
				   firstYear, 							\
				   lastYear, 							\
				   DbFormat(member.email), 				\
				   member.emailVisible, 				\
				   member.isFriend, 					\
				   DbFormat(member.street1), 			\
				   DbFormat(member.street2), 			\
				   DbFormat(member.apt), 				\
				   DbFormat(member.city), 				\
				   DbFormat(member.province), 			\
				   DbFormat(member.country), 			\
				   DbFormat(member.postalCode), 		\
				   DbFormat(PhoneFormat(member.phone)), \
				   joinTime, 							\
				   editTime,	 						\
				   DbFormat(instruments), 				\
				   DbFormat(positions), 				\
				   member.approved, 					\
				   member.onCommittee, 					\
				   DbFormat(member.rank),				\
				   DbFormat(member.password),			\
				   member.id )
			self.execute( insertCmd )
			self.stage( 'UPDATE COMPLETE' )
		except Exception, e:
			Warning( self.currentStage(), e )
		return True

	#----------------------------------------------------------------------
	def LogPage(self, pageName, who):
		"""
		Log a hit on a particular sub-page so that we can see what areas
		are of the most interest.
		"""
		try:
			self.connect()
			cmd = "INSERT INTO pages (name, alumni_id, accessTime) VALUES ('%s', %d, '%s');" % (pageName, who, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			self.execute( cmd )
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
			pass
		return True

	#----------------------------------------------------------------------
	def GetMemberInfo(self, name):
		"""
		Get the full table row for the alumn{i,ae} with the specified name.
		Returns a list of bttbMembers whose name matches the given ones.
		"""
		member = None
		try:
			# Put the name in canonical form (no spaces, quotes, lower case
			# only)
			name = re.sub("^'", "", name)
			name = re.sub("'$", "", name)
			name = re.sub('^"', '', name)
			name = re.sub('"$', '', name)
			name = re.sub(' ', '', name)
			name = DbFormat( name.lower() )

			columnItems = {}
			columnItems = self.GetFullMemberKeys()
			self.connect()
			self.execute( "SELECT * FROM alumni WHERE REPLACE(CONCAT(alumni.first,alumni.last),' ','') LIKE '%s';" % (name) )
			memberInfo = self.__cursor.fetchall()
			self.close()
			for memberTuple in memberInfo:
				member = bttbMember()
				member.loadFromTuple( columnItems, memberTuple )
		except Exception, e:
			Error(self.__stage, e)
			pass
		return member

	#----------------------------------------------------------------------
	def GetConcertInstrumentation(self):
		"""
		Get the tuple of concert instrumentation information for all parts
		(instrumentName, instrumentId, signedUpNames)
		"""
		instrumentation = []
		try:
			self.connect()
			alumniColumns = {}
			alumniColumns = self.GetFullMemberKeys()
			self.execute( "SELECT instrument,id FROM instruments WHERE instruments.isInConcert = 1;" )
			parts = self.__cursor.fetchall()
			for instrument,id in parts:
				self.execute( """
					SELECT alumni.*
					FROM alumni INNER JOIN concert
					WHERE alumni.id = concert.alumni_id
						AND concert.instrument_id = %d
					ORDER BY alumni.last
					""" % id )
				players = self.__cursor.fetchall()
				who = []
				for memberTuple in players:
					member = bttbMember()
					member.loadFromTuple( alumniColumns, memberTuple )
					who.append( member.fullName() )
				instrumentation.append( (instrument, id, ', '.join(who)) )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
			pass
		return instrumentation

	#----------------------------------------------------------------------
	def GetMemberConcertPart(self, id):
		"""
		Return the tuple of instrument information relevant to this
		member's participation in the concert.
		(instrumentName)
		"""
		parts = {}
		try:
			self.connect()
			alumniColumns = {}
			alumniColumns = self.GetFullMemberKeys()
			self.execute( """
				SELECT instrument_id
				FROM concert
				WHERE alumni_id = %d
				""" % id )
			hasPart = self.__cursor.fetchone()
			if hasPart and (len(hasPart) > 0):
				self.execute( """
					SELECT instrument,hasConcertMusic
					FROM instruments
					WHERE id = %d
					""" % hasPart[0] )
				parts = self.__cursor.fetchone()
			self.close()
		except Exception, e:
			Error(self.__stage, e)
			pass
		return parts

	#----------------------------------------------------------------------
	def SetConcertPart(self,alumniId,instrumentId):
		"""
		Set the concert part to be played by the given alumnus.
		"""
		try:
			self.connect()
			selectCmd = "SELECT instrument_id FROM concert WHERE concert.alumni_id = %d" % alumniId
			self.execute( selectCmd )
			hasPart = self.__cursor.fetchone()
			if hasPart:
				setCmd = """
				UPDATE concert SET instrument_id=%d
				WHERE alumni_id = %d;
				""" % (instrumentId, alumniId)
			else:
				setCmd = """
				INSERT INTO concert (alumni_id, instrument_id)
				VALUES (%d, %d);
				""" % (alumniId, instrumentId)

			self.execute( setCmd )

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def GetParadeInstrumentation(self, paradeTable):
		"""
		Get the tuple of parade instrumentation information for all parts
		(instrumentName, instrumentId, hasDownload, signedUpNames)

		The parade table is passed in so that this can be shared among
		any and all parade signups. ("parade" for the 60th, "parade65" for
		the 65th, etc.)
		"""
		instrumentation = []
		try:
			self.connect()
			alumniColumns = {}
			alumniColumns = self.GetFullMemberKeys()
			self.execute( "SELECT instrument,id,hasParadeMusic FROM instruments WHERE instruments.isInParade = 1;" )
			parts = self.__cursor.fetchall()
			for instrument,id,download in parts:
				self.execute( """
					SELECT parade.needsInstrument,alumni.*
					FROM alumni INNER JOIN %s
					WHERE alumni.id = parade.alumni_id
						AND parade.instrument_id = %d
					ORDER BY alumni.last
					""" % (paradeTable, id) )
				players = self.__cursor.fetchall()
				who = []
				for memberTuple in players:
					member = bttbMember()
					member.loadFromTuple( alumniColumns, memberTuple[1:] )
					if int(memberTuple[0]):
						who.append( '%s <sup>*</sup>' % member.fullName() )
					else:
						who.append( member.fullName() )
				instrumentation.append( (instrument, id, download, ', '.join(who)) )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
			pass
		return instrumentation

	#----------------------------------------------------------------------
	def GetMemberParadePart(self, id):
		"""
		Return the tuple of instrument information relevant to this
		member's participation in the parade.
		(instrumentName, hasDownload)
		"""
		parts = {}
		try:
			self.connect()
			alumniColumns = {}
			alumniColumns = self.GetFullMemberKeys()
			self.execute( """
				SELECT instrument_id
				FROM parade
				WHERE alumni_id = %d
				""" % id )
			hasPart = self.__cursor.fetchone()
			if hasPart and (len(hasPart) > 0):
				self.execute( """
					SELECT instrument,hasParadeMusic
					FROM instruments
					WHERE id = %d
					""" % hasPart[0] )
				parts = self.__cursor.fetchone()
			self.close()
		except Exception, e:
			Error(self.__stage, e)
			pass
		return parts

	#----------------------------------------------------------------------
	def SetParadePart(self,alumniId,instrumentId,needsInstrument):
		"""
		Set the parade part to be played by the given alumnus.
		"""
		try:
			self.connect()
			selectCmd = "SELECT instrument_id FROM parade WHERE parade.alumni_id = %d" % alumniId
			self.execute( selectCmd )
			hasPart = self.__cursor.fetchone()
			if hasPart:
				setCmd = """
				UPDATE parade SET instrument_id=%d, needsInstrument=%d
				WHERE alumni_id = %d;
				""" % (instrumentId, needsInstrument, alumniId)
			else:
				setCmd = """
				INSERT INTO parade (alumni_id, approved, needsInstrument, instrument_id)
				VALUES (%d, 1, %d, %d);
				""" % (alumniId, needsInstrument, instrumentId)

			self.execute( setCmd )

			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			Error(self.__stage, e)
		return True

	#----------------------------------------------------------------------
	def ProcessQuery(self, query):
		"""
		Process a generic query.
		"""
		results = {}
		description = {}
		try:
			self.connect()
			self.execute( query )
			results = self.__cursor.fetchall()
			description = self.__cursor.description
			# Need a COMMIT since we're using InnoDB
			self.execute( 'COMMIT' )
			self.close()
		except Exception, e:
			print Error(self.__stage, e)
		return results,description

	def GetWallaceList(self):
		"""
		Return the tuple of Wallace B. Wallace winners
		(name, displayName, year, award, submitTime)
		"""
		wallaceList = {}
		try:
			self.connect()
			self.execute( """
				SELECT who, whoDisplay, year, description, submitTime
				FROM wallace
				ORDER BY year
				""" )
			wallaceList = self.__cursor.fetchall()
			self.close()
		except Exception, e:
			Error(self.__stage, e)
			pass
		return wallaceList

#======================================================================

_testWhat = 6
if __name__ == '__main__':
	if _testWhat == 6:
		db = bttbDB()
		db.Initialize()
		db.TurnDebugOn()
		print db.GetWallaceList()
		db.Finalize()
	elif _testWhat == 5:
		db = bttbDB()
		db.Initialize()
		db.TurnDebugOn()
		db.Archive()
		db.Finalize()
	elif _testWhat == 4:
		db = bttbDB()
		db.Initialize()
		db.TurnDebugOn()
		(memberList, columnNames, count) = db.GetPublicMemberListJoinedAfter(datetime.datetime(2006,12,10))
		print "%d members joined after December 10, %d total" % (len(memberList), count)
		db.Finalize()
	elif _testWhat == 3:
		db = bttbDB()
		db.Initialize()
		db.TurnDebugOn()
		db.SetParadePart( 0, 12, 1 )
		print db.GetMemberParadePart( 0 )
		db.SetParadePart( 0, 13, 0 )
		print db.GetMemberParadePart( 0 )
		db.SetParadePart( 754, 12, 1 )
		print db.GetMemberParadePart( 754 )
		db.Finalize()
	elif _testWhat == 2:
		db = bttbDB()
		db.Initialize()
		db.TurnDebugOn()
		print db.GetParadeInstrumentation('parade')
		db.SetParadePart( 0, 12, 1 )
		print db.GetParadeInstrumentation('parade')
		db.SetParadePart( 0, 13, 0 )
		print db.GetParadeInstrumentation('parade')
		db.SetParadePart( 754, 12, 1 )
		db.Finalize()
	elif _testWhat == 1:
		db = bttbDB()
		db.Initialize()
		db.TurnDebugOn()
		db.Archive()
		db.Finalize()
	else:
		print '=========== PUBLIC MEMBERS ============='
		print db.GetPublicMemberList()
		print '=========== EVENT LIST ============='
		print db.GetEvents()
		print '=========== SOCIAL EVENT ============='
		print db.GetEventAttendees('Social')
		print '=========== ATTENDANCE ============='
		print db.GetFullEventAttendance()
		print '=========== VOLUNTEERS ============='
		print db.GetFullEventVolunteers()
		print '=========== ME ============='
		print db.GetMember(0).printFullSummary()
		print '=========== UPDATE ME ============='
		print db.GetMemories(0)
		me = db.GetMember(0)
		me.memory = 'I have no recollection at all'
		db.UpdateMember(me, True)
		db.UpdateMemberMemory(me, me.memory)
		print db.GetMember(0).printFullSummary()
		print '=========== BOB J ============='
		bob = bttbMember()
		bob.approved = True
		bob.onCommittee = True
		bob.editTime = datetime.datetime(2007, 1, 1)
		bob.joinTime = datetime.datetime(2007, 1, 1)
		bob.first = 'Bob'
		bob.last = 'Johnson'
		bob.nee = 'Onthis'
		bob.firstYear = '1980'
		bob.lastYear = '1984'
		bob.email = 'bob@onthis.com'
		bob.emailVisible = True
		bob.isFriend = False
		bob.instruments = ['Tuba', 'Flute', 'Colour Guard']
		bob.positions = ['Drum Major', 'Band Executive']
		bob.rank = 'Odour'
		bob.apt = '456'
		bob.street1 = '123 Fake Street'
		bob.street2 = ''
		bob.city = 'Burlington'
		bob.province = 'Ontario'
		bob.country = 'Canada'
		bob.postalCode = 'B0B 0B0'
		bob.phone = '905-333-3333'
		bob.memory = 'Bob tries hard not to remember those days. Bob also refers to himself in the third person.  Bob Bob Bob.'
		bob.id = 99999
		db.UpdateMember(bob, True)
		db.UpdateMemberVolunteering(bob, ['Anything'])
		db.UpdateMemberAttendance(bob, ['Golf', 'Social', 'Homecoming', 'Brunch', 'Parade', 'Concert'])
		db.UpdateMemberMemory(bob, bob.memory)
		db.stage( 'BOB update complete' )
		db.GetMember(0).printFullSummary()
		db.stage( 'Debug complete' )
		try:
			pageName = 'test'
			db.connect()
			try:
				db.execute( "SELECT * FROM pages WHERE pages.name = '%s'" % pageName )
			except Exception, e:
				Error('SELECT page test', e)
			(name, count) = db.cursor().fetchone()
			print count
			if count:
				count = int(count) + 1
				cmd = "UPDATE pages SET counter=%d WHERE name = '%s';" % (count, pageName)
			else:
				cmd = "INSERT INTO pages (name, counter) VALUES ('%s', 1);" % pageName
			db.execute( cmd )
			db.execute( 'COMMIT' )
			db.close()
		except Exception, e:
			Error('Page test', e)
		db.Finalize()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================

