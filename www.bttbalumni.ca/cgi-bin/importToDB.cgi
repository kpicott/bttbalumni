#!env python

import bttbDB
import re
from bttbConfig import *
from bttbAlumni_XML import bttbAlumni

class ImportAlumniDB:
	def __init__(self):
		"""
		Create all of the initial tables and populate with known data.
		"""
		self.__alumDir = DataPath()
		self.__db = bttbDB.bttbDB()
		self.__db.Initialize()
		self.__db.TurnDebugOn()
		#self.createTables(False)
		#self.updateTables()
		#self.updateTables2()
		#self.updateTables3()
		#self.updateTables4()
		#self.updateTables5()
		#self.updateTables6()
		self.createWallaceBWallaceTable()
		#self.updateTables7()
		#self.createContactTable()
		#self.updateTables8()
		#self.updateTables9()
		#self.createConcertTable()
		#
		# The database has been bootstrapped so there is no use for
		# anything other than the table creation now (to allow new
		# tables to be easily added).
		#
		#self.populateEvents()
		#self.populateAlumni()
		#self.populateMemories()
		#self.populateVolunteers()
		#self.populateAttendance()
		#self.populateInstruments()
		self.__db.Finalize()

	def cursor(self):
		return self.__db.cursor()

	def execute(self,cmd):
		self.stage( cmd )
		self.cursor().execute( cmd )

	def stage(self, what):
		return self.__db.stage( what )

	def createTables(self, dropTables):
		"""
		Create the DB tables.
		"""

		#------------------------------------------------------
		# drop existing table first, in reverse order to avoid
		# foreign key dependency problems.
		#------------------------------------------------------
		if dropTables:
			self.execute( 'DROP TABLE IF EXISTS volunteers' )
			self.execute( 'DROP TABLE IF EXISTS attendance' )
			self.execute( 'DROP TABLE IF EXISTS memories' )
			self.execute( 'DROP TABLE IF EXISTS 60thevents' )
			self.execute( 'DROP TABLE IF EXISTS alumni' )
			self.execute( 'DROP TABLE IF EXISTS pages' )
			self.execute( 'DROP TABLE IF EXISTS instruments' )
			self.execute( 'DROP TABLE IF EXISTS parade' )
			self.execute( 'DROP TABLE IF EXISTS contact' )
			self.execute( 'DROP TABLE IF EXISTS paid' )

		#------------------------------------------------------
		# events TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS 60thevents (
		  id           INT(10) UNSIGNED NOT NULL COMMENT 'Unique id',
		  summary      VARCHAR(30)      NOT NULL COMMENT 'Event title',
		  description  TEXT             NOT NULL COMMENT 'Full event description',
		  canVolunteer TINYINT(1)       NOT NULL DEFAULT '0' COMMENT 'Event needs volunteers',
		  canAttend    TINYINT(1)       NOT NULL DEFAULT '0' COMMENT 'Event can be attended',
		  eventDate    DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00' COMMENT 'Day of event',

		  PRIMARY KEY(id)
		)
		Engine=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='List of event ids and descriptions';
		""" )

		#------------------------------------------------------
		# alumni TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS alumni (
		  first          VARCHAR(40)      NOT NULL DEFAULT '',
		  nee            VARCHAR(40)               DEFAULT '',
		  last           VARCHAR(40)      NOT NULL DEFAULT '',
		  firstYear      INT(10) UNSIGNED NOT NULL DEFAULT '2006',
		  lastYear       INT(10) UNSIGNED NOT NULL DEFAULT '2006',
		  email          VARCHAR(128)              DEFAULT NULL,
		  emailVisible   TINYINT(1)       NOT NULL DEFAULT '1',
		  isFriend       TINYINT(1)       NOT NULL DEFAULT '0',
		  street1        VARCHAR(45)               DEFAULT NULL,
		  street2        VARCHAR(45)               DEFAULT NULL,
		  apt            VARCHAR(20)               DEFAULT NULL,
		  city           VARCHAR(45)               DEFAULT NULL,
		  province       VARCHAR(20)               DEFAULT NULL,
		  country        VARCHAR(25)               DEFAULT NULL,
		  postalCode     VARCHAR(15)               DEFAULT NULL,
		  phone          VARCHAR(19)               DEFAULT NULL,
		  id             INT(10) UNSIGNED NOT NULL DEFAULT '0',
		  joinTime       DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00',
		  editTime       DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00',
		  instruments    TEXT,
		  positions      TEXT,
		  approved       TINYINT(1)       NOT NULL DEFAULT '0',
		  onCommittee    TINYINT(1)       NOT NULL DEFAULT '0',
		  rank           VARCHAR(40)      NOT NULL DEFAULT '',

		  PRIMARY KEY  (id)
		)
		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='People and their profile information';
		""" )

		#------------------------------------------------------
		# memories TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS memories (
		  alumni_id  INT(10) UNSIGNED          DEFAULT '0',
		  memory     TEXT             NOT NULL,
		  memoryTime DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00',
  		  id         INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,

  		  PRIMARY KEY  (id),

		  FOREIGN KEY (alumni_id) REFERENCES alumni(id)
		  	ON DELETE SET NULL
			ON UPDATE CASCADE
		)
		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='List of special memories from band days';
		""" )

		#------------------------------------------------------
		# volunteers TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS volunteers (
		  event_id  INT(10) UNSIGNED NOT NULL DEFAULT '0',
		  alumni_id INT(10) UNSIGNED NOT NULL DEFAULT '0',

		  PRIMARY KEY  (event_id, alumni_id),

		  FOREIGN KEY (alumni_id) REFERENCES alumni(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE,

		  FOREIGN KEY (event_id) REFERENCES 60thevents(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE
		)
		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='Helpers for the 60thevents';
		""" )

		#------------------------------------------------------
		# attendance TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS attendance (
		  event_id  INT(10) UNSIGNED NOT NULL DEFAULT '0',
		  alumni_id INT(10) UNSIGNED NOT NULL DEFAULT '0',

		  PRIMARY KEY  (event_id, alumni_id),

		  FOREIGN KEY (alumni_id) REFERENCES alumni(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE,

		  FOREIGN KEY (event_id) REFERENCES 60thevents(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE
		)
		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='Participants in the 60thevents';
		""" )

		#------------------------------------------------------
		# pages TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS pages (
		  name       VARCHAR(255)     NOT NULL,
  		  alumni_id  INT(10) UNSIGNED NOT NULL,
		  accessTime DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00'
		)

		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='List of page hits';
		""" )

		#------------------------------------------------------
		# instruments TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS instruments (
		  id               INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique id',
		  instrument       VARCHAR(30)      NOT NULL COMMENT 'Instrument name',
		  isInParade       TINYINT(1)       NOT NULL DEFAULT '0' COMMENT 'Is part available for parade?',
		  hasParadeMusic   TINYINT(1)       NOT NULL DEFAULT '0' COMMENT 'Does part have parade music?',
		  isInConcert      TINYINT(1)       NOT NULL DEFAULT '0' COMMENT 'Is part available for concert?',
		  hasConcertMusic  TINYINT(1)       NOT NULL DEFAULT '0' COMMENT 'Does part have concert music?',

		  PRIMARY KEY(id)
		)
		Engine=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='List of parade and concert instrumentation';
		""" )

		#------------------------------------------------------
		# parade TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS parade (
  		  alumni_id        INT(10) UNSIGNED NOT NULL,
		  approved         TINYINT(1)       NOT NULL DEFAULT '0',
		  needs_instrument TINYINT(1)       NOT NULL DEFAULT '0',
  		  instrument_id    INT(10) UNSIGNED NOT NULL,

		  PRIMARY KEY(alumni_id),

		  FOREIGN KEY (alumni_id) REFERENCES alumni(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE,

		  FOREIGN KEY (instrument_id) REFERENCES instruments(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE
		)

		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='Parade participants and their part';
		""" )

	def insertEvent(self, id, summary, description, canAttend, canVolunteer, eventDate ):
		"""
		Insert a single event into the events table, if it isn't already there
		"""
		try:
			self.execute( "SELECT 60thevents.id FROM 60thevents WHERE 60thevents.id = %d;" % (id) )
			if len(self.cursor().fetchall()) == 0:
				insertCmd = "INSERT INTO 60thevents (id, summary, description, canAttend, canVolunteer, eventDate) VALUES (%d, '%s', '%s', %d, %d, '%s');" % (id, summary, description, canAttend, canVolunteer, eventDate)
				self.execute( insertCmd )
			else:
				self.stage( 'SKIP INSERT of Event %d' % (id) )
		except Exception, e:
			Warning( self.__db.currentStage(), e )

	def updateTables(self):
		"""
		Modify the DB tables according to the latest changes
		"""

		#------------------------------------------------------
		# alumni TABLE - Add in the password field
		#------------------------------------------------------
		self.execute( """
		ALTER TABLE alumni ADD
		  password  VARCHAR(10)  COMMENT 'User login password'
		""" )
		self.stage( 'ADD Parade rehearsal event' )
		self.insertEvent( 9, 'Parade Rehearsal', 'Parade music practice at the music centre', 1, 0, '2007-06-15 19:00:00' )
		# Commit is necessary because I'm using InnoDB
		self.execute( 'COMMIT' )

	def updateTables2(self):
		"""
		Modify the DB tables according to second set of changes
		"""

		#------------------------------------------------------
		# memories TABLE - Add in the submitTime field and provide
		#                  default values for all of them.
		#------------------------------------------------------
		self.execute( """
		ALTER TABLE memories ADD
		  submitTime DATETIME NOT NULL DEFAULT '2007-01-01 00:00:00'
		""" )
		self.execute( """
		ALTER TABLE memories ADD
		  removed TINYINT(1) NOT NULL DEFAULT '0' COMMENT 'Memory was deleted'
		""" )
		self.execute( "SELECT alumni_id, id FROM memories" )
		memoryList = self.cursor().fetchall()
		for (alumni_id, id) in memoryList:
			self.execute( """
			SELECT joinTime FROM alumni WHERE id = %d
			""" % alumni_id )
			joinTime = self.cursor().fetchone()[0]
			self.execute( """
			UPDATE memories SET submitTime='%s' WHERE id = %d
			""" % (joinTime.strftime('%Y-%m-%d %H:%M:%S'), id) )
				
		#------------------------------------------------------
		# Add drums to the parade
		#------------------------------------------------------
		self.stage( 'ADD Percussion parade instrument' )
		self.insertInstrument( 'Percussion', 1, 0, 0, 1 )
		self.insertInstrument( 'Triples', 1, 0, 0, 0 )
		self.insertInstrument( 'Snare', 1, 0, 0, 0 )
		self.insertInstrument( 'Bass Drum', 1, 0, 0, 0 )
		self.insertInstrument( 'Bells', 1, 0, 0, 0 )
		# Commit is necessary because I'm using InnoDB
		self.execute( 'COMMIT' )

	def updateTables3(self):
		"""
		Fill out the percussion details in the parade
		"""
		self.stage( 'ADD Percussion parade instrument' )
		self.insertInstrument( 'Triples', 1, 0, 0, 0 )
		self.insertInstrument( 'Snare', 1, 0, 0, 0 )
		self.insertInstrument( 'Bass Drum', 1, 0, 0, 0 )
		self.insertInstrument( 'Bells', 1, 0, 0, 0 )
		# Commit is necessary because I'm using InnoDB
		self.execute( 'COMMIT' )

	def updateTables4(self):
		"""
		Fill out new instruments for which music was found
		"""
		self.stage( 'ADD Euphonium and Baritone sax parade instrument' )
		self.insertInstrument( 'Euphonium', 1, 1, 0, 0 )
		self.insertInstrument( 'Baritone Sax', 1, 1, 0, 0 )
		# Commit is necessary because I'm using InnoDB
		self.stage( 'Commit Update' )
		self.execute( 'COMMIT' )

	def updateTables5(self):
		"""
		Add Drum Major to parade list
		"""
		self.stage( 'ADD Drum Major' )
		self.insertInstrument( 'Drum Major', 1, 0, 0, 0 )
		# Commit is necessary because I'm using InnoDB
		self.stage( 'Commit Update' )
		self.execute( 'COMMIT' )

	def updateTables6(self):
		"""
		Add riders to parade list
		"""
		self.stage( 'ADD riders' )
		self.insertInstrument( 'Can only ride', 1, 0, 0, 0 )
		# Commit is necessary because I'm using InnoDB
		self.stage( 'Commit Update' )
		self.execute( 'COMMIT' )

	def updateTables7(self):
		"""
		Edit the event description
		"""
		self.execute( """
		ALTER TABLE 60thevents ADD
		  location  VARCHAR(30)  COMMENT 'Where the event will take place'
		""" )
		self.execute( """
		UPDATE 60thevents SET description='Friday night social event' WHERE id = 4
		""" )
		self.execute( """
		UPDATE 60thevents SET description='Parade music practice' WHERE id = 9
		""" )
		self.execute( "UPDATE 60thevents SET location='Music Centre/Central Park' WHERE id = 0" )
		self.execute( "UPDATE 60thevents SET location='Music Centre' WHERE id = 1" )
		self.execute( "UPDATE 60thevents SET location='Music Centre' WHERE id = 2" )
		self.execute( "UPDATE 60thevents SET location='Millcroft Golf Course' WHERE id = 3" )
		self.execute( "UPDATE 60thevents SET location='Central Arena' WHERE id = 4" )
		self.execute( "UPDATE 60thevents SET location='Central Arena' WHERE id = 5" )
		self.execute( "UPDATE 60thevents SET location='Music Centre' WHERE id = 6" )
		self.execute( "UPDATE 60thevents SET location='Central Arena' WHERE id = 7" )
		self.execute( "UPDATE 60thevents SET location='Music Centre' WHERE id = 8" )
		self.execute( "UPDATE 60thevents SET location='Music Centre' WHERE id = 9" )
		# Commit is necessary because I'm using InnoDB
		self.stage( 'Commit Update' )
		self.execute( 'COMMIT' )

	def createWallaceBWallaceTable(self):
		"""
		Create the table to hold the Wallace B. Wallace winners
		"""
		self.execute( 'DROP TABLE IF EXISTS wallace' )
		self.execute( """
		CREATE TABLE IF NOT EXISTS wallace (
		  id           INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique id',
		  who          VARCHAR(30)      NOT NULL COMMENT 'Who won it',
		  whoDisplay   VARCHAR(30)      NOT NULL COMMENT 'How their name will be displayed',
		  description  TEXT             NOT NULL COMMENT 'What did they win it for',
		  year         INT(10) UNSIGNED NOT NULL COMMENT 'Year it was won',
		  submitTime   DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00' COMMENT 'When it was submitted',

		  PRIMARY KEY(id)
		)
		Engine=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='List of Wallace B. Wallace winners';
		""" )
		award1972 = DbFormat( """
<p>
Put on his band uniform and hitchiked from Hamilton to the music
centre for a performance in the Rememberance Day Parade.
Unfortunately, it was the parade in Hamilton we were doing that day
and he missed it.
</p>
		""" )
		award1973 = DbFormat( """
<p>
The band was staying in a hotel somewhere for a big parade, (probably
in the states.)  Somehow, his hotel room key ended up in the toilet after
it had been used, but before it had been flushed.  Rather than reach in
and pick it out, this recipient erroneously believed that the weight of
the key would make it too heavy to actually go down the bog so he flushed
the toilet believing that the bad stuff would go away, but the key would
remain.  It didn't.
</p>
		""" )
		award1974 = DbFormat( """
<p>
Dilligently hitchhiked to Kingston for a parade to catch up with the band
after he had to work or just missed the bus or something.  He had a ride all
the way down the 401 when he spotted the equipment truck at the side of the
highway right about at the junction of the 115 that goes up to Peterborough.
He had the driver drop him off so he could catch a ride the rest of the way
with Charlie, or whoever was driving the truck only to discover that the truck
had broken down and was abandoned there.  He started hitching again but
because of the lost time, he didn't make it to Kingston on time.
</p>
		""" )
		award1975 = DbFormat( """
<p>
Packed his passport in his uniform bag which was then loaded into the equipment truck headed for the airport in Europe(1975) . Having realized this, the equipment truck needed to be completely unpacked so he could get on the plane to come home.
</p>
<p>
Receiving "Honourable Mention" that year was Roy Russell. At a Hamilton Tiger Cats game, the band was performing at the half time show. During the idle time, with only 3 or 4 people on the bus, he sat on the driver's seat and decided to push on the pedals. When he pushed on the clutch, the bus started to roll backwards. He saw the two other buses, on either side of them "rolling forward", or so he thought! They stopped after the bus hit the building. The driver, who had a perfect safety record, up to that point in time, was pretty ticked off at him. So was Bob Webb.
</p>
<p>
Even though Roy didn't win the award that year, his legacy lives on. The next year, when the "Band Rules" were revised, there was a rule that said something along the lines of "No band member shall sit in the driver's seat of the bus". He was hoping that they would rename it to the "Russell clause".
</p>
		""" )
		award1988 = DbFormat( """
<p>
Forgot his band shoes and was late (as usual) for the Dixieland gang, so he
went to the uniform room and grabbed the first pair of shoes that looked close
to his size as Phil Austin was yelling at him to get going.
</p>
<p>
When he arrived at the gig he had his shirt on and Phil asked him if the shoes
fit. He wasn't sure and tried them on, putting them on first before his pants.
Then Phil noticed they were on and once again urged Steve to get going.
</p>
<p>
With an instinct born of long years of band experience he grabbed his tunic
and ran. When he got to the door and started to go out in public Phil
fortunately noticed that Steve in his haste had neglected to complete dressing
and was sans pants.
</p>
		""" )
		award2001 = DbFormat( """
<p>
Fell asleep during a concert practice. Bill Hughes took notice and got the
drumline to surround him and wake him up.
</p>
		""" )
		award2002 = DbFormat( """
<p>
Fell through a chair in the rehearsal hall while standing on it, resulting in a leg injury.
</p>
		""" )
		award2003 = DbFormat( """
<p>
When in Miami for the Orange Bowl climbed up a palm tree to get me a coconut. He had a really hard time getting it down and eventually he fell out of the tree. To top it all off, while he was sitting on the ground after his fall, the coconut fell out of the tree and hit him in the head!
</p>
		""" )
		award2004 = DbFormat( """
<p>
Set off fire works and fire crackers inside a Military Safe Zone in Courseulles-Sur-Mer(Juno Beach), France when there for the 60th anniversary of D-Day.
</p>
		""" )
		award1982 = DbFormat( """
<p>
Carolyn was in the position of Drum Major at that time.  While marching in the Calgary Stampede parade, Carolyn majestically, yet inadvertantly positioned her mace right into a sewer grate.  The band continued to march playing "Strike Up the Band" while Carolyn was frantically trying to pull the mace free.  As the clarinets passed by, she gave a final heave, broke the decorative chain and pulled her mace free.  She regained her position and her composure, and continued the rest of the parade, marching the "cane-walk" while constantly being whipped in the right leg with the newly-detached chain.
</p>
<p>
Congratulations on deserving this award.
... and the sad thing was - I was not there to share in this event!
<i>Submitted by Alan Whiskin (past Drum Major with and present husband of Carolyn)</i>
</p>
		""" )
		award1992 = DbFormat( """
<p>
At one of the ever-popular band dances, she decided to wear an ankle length short sleeved dress that buttoned up the front (top to bottom). She was sitting on one of the risers, when one of her favourite songs came on. She jumped up and yes, the dress popped open (top to bottom). It was quite the show.
To this day, we never let her forget it.
</p>
		""" )
		award1996 = DbFormat( """
<p>
For mooning Mr. Garnier and some chaperones by accident on our tour in
Baltimore.
</p>
		""" )
		award1993 = DbFormat( """
<p>
The Band traveled to Toronto to perform our field show at a Toronto Blue Jays
game, as we often did in those days (the Band played during both World Series
and the 1991 All Star Game). We lined up in formation in the bowels of the
Skydome near where our buses parked and marched in twos to down behind the
outfield wall by the visitor's bullpen. As we arrived our Marching Director
Mr. Garnier lined us up in such a way as to prepare us to go out onto the
field. At this moment I should have realized something was wrong as I was
set to lead the group rather then be at the end of it.
</p>
<p>
We didn't think too much of it until we were marching out and the realization
hit us that the two halves of the Band were going to be inverted with the left
on the right and the right on the left. Once set the Drum Major called out
"Band, Are you ready!" to which no one thought to bring to their attention our
current predicament and we reflexively yelled "Yes Sir". The cadence was given
and off we went. In spite of the looks of terror on the faces of some of the
band the whole thing seemed to work, even the scatter which we thought at
the time would have us colliding into one another left and right. Once we got
off the field we all couldn't help but discuss the fact we had just done our
field show backwards in front of 50,000+ fans. For lining us up backwards
Mr. Garnier was awarded that year's Wallace B. Wallace Award.
</p>
		""" )
		award1995 = DbFormat( """
<p>
It was the Band picnic and it was a beautiful, warm summer's day at
Hidden Valley Park. During the game of capture the flag (members against
staff, boosters and parents) Drum Major Simon Matthews started making a break
for it across the open field towards our head Chap Mrs. Webb.  Simon would run
for a moment, then stop and change direction a little, then run some more and
change direction again with Mrs. Webb staring him down all the while.
</p>
<p>
Finally he decided to run right at her hoping to get by. While Simon felt his
moves were good enough to pull it off, Mrs. Webb had other ideas. She held out
her arm which closelined poor Simon and took him down like a tonne of bricks.
It was truly a hilarious sight for all those who saw it and for it Simon was
awarded the 1995 Wallace B. Wallace Award.
</p>
		""")
		self.execute( """
			INSERT INTO wallace
				(who, whoDisplay, description, year, submitTime)
			VALUES
				('Danny Janu',     'Danny Janu',     '%s', 1972, '2007-05-13 12:00:00' ),
				('Barfy',          'Barfy',          '%s', 1973, '2007-05-13 12:00:00' ),
				('Phil McArthur',  'Phil McArthur',  '%s', 1974, '2007-05-13 12:00:00' ),
				('Dave Jacques',   'Dave Jacques',   '%s', 1975, '2007-03-03 12:00:00' ),
				('Carolyn Whiskin','Carolyn Whiskin','%s', 1982, '2007-03-03 12:00:00' ),
				('Steve (Animal) Gaul','Steve (Animal) Gaul','%s', 1988, '2007-04-17 12:00:00' ),
				('Julie Thompson', 'Julie Thompson', '%s', 1992, '2007-03-03 12:00:00' ),
				('Mr. Garnier',    'Mr. Garnier',    '%s', 1993, '2007-03-08 12:00:00' ),
				('Simon Matthews', 'Simon Matthews', '%s', 1995, '2007-03-08 12:00:00' ),
				('Shaun Woods',    'Shaun Woods',    '%s', 1996, '2007-03-03 12:00:00' ),
				('Kevin Winterton','Kevin Winterton','%s', 2001, '2007-03-18 12:00:00' ),
				('Chrissy Taylor', 'Chrissy Taylor', '%s', 2002, '2007-03-03 12:00:00' ),
				('Trevor Davies',  'Trevor Davies',  '%s', 2003, '2007-03-03 12:00:00' ),
				('Myles Tompkins', 'Myles Tompkins', '%s', 2004, '2007-03-03 12:00:00' ),
				('Rob Bennett',    'Rob Bennett',    '<p><i>We know you won it during the 1999 Christmas Parade - and for what... `nuff said</i></p>', 1999, '2007-03-18 12:00:00' );
			""" % (award1972, award1973, award1974, award1975, award1982, award1988, award1992, award1993, award1995, award1996, award2001, award2002, award2003, award2004) )
		self.execute( 'COMMIT' )

	def createContactTable(self):
		"""
		Create the table to hold the 50th anniversary contact information
		"""
		self.execute( 'DROP TABLE IF EXISTS contact' )
		self.execute( """
		CREATE TABLE IF NOT EXISTS contact (
		  id             INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique id',
		  first          VARCHAR(40)      NOT NULL DEFAULT '',
		  nee            VARCHAR(40)               DEFAULT '',
		  last           VARCHAR(40)      NOT NULL DEFAULT '',
		  firstYear      INT(10) UNSIGNED DEFAULT 0,
		  lastYear       INT(10) UNSIGNED DEFAULT 0,
		  email          VARCHAR(128)     DEFAULT NULL,
		  street1        VARCHAR(45)      DEFAULT NULL,
		  street2        VARCHAR(45)      DEFAULT NULL,
		  apt            VARCHAR(20)      DEFAULT NULL,
		  city           VARCHAR(45)      DEFAULT NULL,
		  province       VARCHAR(20)      DEFAULT NULL,
		  country        VARCHAR(25)      DEFAULT NULL,
		  postalCode     VARCHAR(15)      DEFAULT NULL,
		  phone          VARCHAR(19)      DEFAULT NULL,
		  instruments    TEXT,
		  positions      TEXT,

		  PRIMARY KEY  (id)
		)
		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='50th Anniversary contact information';
		""" )
		fd = open( "50thAlumni.txt" )
		re_alumni = re.compile( '([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)' )
		try:
			for line in fd:
				cmd = """
					INSERT INTO contact
						(first, last, firstYear, lastYear, instruments)
					VALUES
				"""
				match = re_alumni.match( line )
				last = DbFormat(match.group(1))
				first = DbFormat(match.group(2))
				if first == 'First':
					continue
				firstYear = match.group(3)
				if len(firstYear) == 0:
					firstYear = '0'
				lastYear = match.group(4)
				if len(lastYear) == 0:
					lastYear = '0'
				section = DbFormat(match.group(5))
				cmd += '\t'
				cmd += "\t('%s', '%s', %s, %s, '%s')" % (DbFormat(first), DbFormat(last), firstYear, lastYear, DbFormat(section))
				print 'DO ' + cmd
				self.execute( cmd )
		finally:
			fd.close()
		self.execute( 'COMMIT' )

	def updateTables8(self):
		"""
		Add a 'registered' field to alumni events
		"""
		#------------------------------------------------------
		# create 'paid' TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS paid (
		  alumni_id INT(10)    UNSIGNED NOT NULL DEFAULT '0' COMMENT 'Alumni who has paid',
		  isPaid    TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT 'Is payment made, only here to make correcting mistakes easier',
		  paidTime  DATETIME            NOT NULL DEFAULT '2007-01-01 00:00:00' COMMENT 'When registration was entered',

		  PRIMARY KEY (alumni_id),

		  FOREIGN KEY (alumni_id) REFERENCES alumni(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE
		)
		Engine=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='List of who has paid their money for events';
		""" )
		# Commit is necessary because I'm using InnoDB
		self.execute( 'COMMIT' )

	def createConcertTable(self):
		"""
		Create the concert signup table
		"""
		#------------------------------------------------------
		# concert TABLE
		#------------------------------------------------------
		self.execute( """
		CREATE TABLE IF NOT EXISTS concert (
  		  alumni_id      INT(10) UNSIGNED NOT NULL COMMENT 'Alumni signing up',
  		  instrument_id  INT(10) UNSIGNED NOT NULL COMMENT 'Part to play',
		  signup_time    DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00' COMMENT 'When the music was downloaded',

		  PRIMARY KEY(alumni_id),

		  FOREIGN KEY (alumni_id) REFERENCES alumni(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE,

		  FOREIGN KEY (instrument_id) REFERENCES instruments(id)
		  	ON DELETE CASCADE
			ON UPDATE CASCADE
		)

		ENGINE=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='Concert participants and their part';
		""" )
		# Commit is necessary because I'm using InnoDB
		self.stage( 'Commit Update' )
		self.execute( 'COMMIT' )

	def updateTables9(self):
		"""
		Fix up instrumentation for concert
		"""
		self.stage( 'Modify concert instrumentation' )
		self.execute("""
		UPDATE instruments set isInConcert = 1
		WHERE instrument IN
		('Alto Sax 1', 'Alto Sax 2', 'Baritone', 'Basses',
		 'Clarinet 1', 'Clarinet 2', 'Clarinet 3',
		 'F Horn 1', 'F Horn 2', 'Flute', 'Piccolo',
		 'Tenor Sax', 'Baritone Sax', 'Euphonium', 'Percussion',
		 'Trombone 1', 'Trombone 2', 'Trombone 3',
		 'Trumpet 1', 'Trumpet 2', 'Trumpet 3')
		""")
		self.insertInstrument( 'Trumpet 4', 0, 0, 1, 1 )
		self.insertInstrument( 'Bass Clarinet', 0, 0, 1, 1 )
		self.insertInstrument( 'Flute 2', 0, 0, 1, 1 )
		self.insertInstrument( 'F Horn 3', 0, 0, 1, 1 )
		self.insertInstrument( 'F Horn 4', 0, 0, 1, 1 )
		self.insertInstrument( 'Bass Trombone', 0, 0, 1, 1 )
		self.insertInstrument( 'Bassoon', 0, 0, 1, 1 )
		self.insertInstrument( 'Oboe', 0, 0, 1, 1 )
		# Commit is necessary because I'm using InnoDB
		self.stage( 'Commit Update' )
		self.execute( 'COMMIT' )

	def populateEvents(self):
		"""
		Initialize all of the event description information.
		"""
		try:
			self.stage( 'Populate Events' )
			self.insertEvent( 0, 'Celebration', 'The 60th anniversary celebration weekend', 0, 0, '2007-06-15 15:00:00' )
			self.insertEvent( 1, 'Parade', 'Marching in Sound of Music Festival Parade Alumni band unit', 1, 0, '2007-06-16 10:00:00' )
			self.insertEvent( 2, 'Concert', 'Sunday afternoon joint BTTB concert', 1, 0, '2007-06-17 15:00:00' )
			self.insertEvent( 3, 'Golf', 'Thursday afternoon Boosters golf tournament', 1, 0, '2007-06-14 13:00:00' )
			self.insertEvent( 4, 'Social', 'Friday night social event', 1, 1, '2007-06-15 19:00:00' )
			self.insertEvent( 5, 'Homecoming', 'Saturday night homecoming', 1, 1, '2007-06-16 19:00:00' )
			self.insertEvent( 6, 'Brunch', 'Sunday family brunch', 1, 1, '2007-06-17 13:00:00' )
			self.insertEvent( 7, 'Registration', 'Friday registration', 0, 1, '2007-06-15 15:00:00' )
			self.insertEvent( 8, 'Concert Practice', 'Sunday morning rehearsal for joint BTTB concert', 1, 0, '2007-06-17 10:00:00' )
			# Commit is necessary because I'm using InnoDB
			self.stage( 'Commit Events' )
			self.execute( 'COMMIT' )
		except Exception, e:
			Error( self.__db.currentStage(), e )

	def populateAlumni(self):
		"""
		Read all of the alumni profile information from the XML files and add
		the appropriate parts to the alumni table.
		"""
		try:
			alumni = bttbAlumni(self.__alumDir)
			self.stage( 'Populate Alumni' )
			for member in alumni.memberList:
				if not member or not member.first: continue
				try:
					member.onCommittee =  member.id in [0, 26965, 5993, 16687, 18964, 16291, 29666, 6799, 25488, 1112, 10141, 4564, 30042]
					self.__db.UpdateMember(member, False)
				except Exception, e:
					Error( 'Failed to insert Member %s:%s' % (member.first, member.editTime), e )
			# Commit is necessary because I'm using InnoDB
			self.execute( 'COMMIT' )
		except Exception, e:
			Error( self.__db.currentStage(), e )

	def insertMemory(self, id, date, memory):
		"""
		Insert a single memory into the memories table, if it isn't already there
		"""
		try:
			self.execute( "SELECT memories.alumni_id FROM memories WHERE memories.alumni_id = %d;" % id )
			if len(self.cursor().fetchall()) == 0:
				insertCmd = "INSERT INTO memories (alumni_id, memory, memoryTime) VALUES (%d, '%s', '%s');" % (id, DbFormat(memory), date)
				self.execute( insertCmd )
			else:
				self.stage( 'SKIP INSERT of Memory from %d' % (id) )
		except Exception, e:
			Warning( self.__db.currentStage(), e )

	def populateMemories(self):
		"""
		Read all of the memories entered into the Alumni XML files and add it
		to the memories table.
		"""
		try:
			alumni = bttbAlumni(self.__alumDir)
			self.stage( 'Populate Memories' )
			for member in alumni.memberList:
				if not member.memory: continue
				approxDate = member.midpoint().strftime('%Y-%m-%d %H:%M:%S')
				self.insertMemory( member.id, approxDate, member.memory )
			# Commit is necessary because I'm using InnoDB
			self.execute( 'COMMIT' )
		except Exception, e:
			Error( self.__db.currentStage(), e )

	def insertVolunteer(self, alumni_id, event_id):
		"""
		Insert a single volunteer record into the volunteers table, if it isn't already there
		"""
		try:
			self.execute( "SELECT volunteers.alumni_id FROM volunteers WHERE (volunteers.alumni_id, event_id) = (%d, %d);" % (alumni_id, event_id) )
			if len(self.cursor().fetchall()) == 0:
				insertCmd = "INSERT INTO volunteers (alumni_id, event_id) VALUES (%d, %d);" % (alumni_id, event_id)
				self.execute( insertCmd )
			else:
				self.stage( 'SKIP INSERT of Volunteer %d for %d' % (alumni_id, event_id) )
		except Exception, e:
			Warning( self.__db.currentStage(), e )

	def populateVolunteers(self):
		"""
		Read all of the event volunteer information from the Alumni XML files
		and populate the volunteer table with that information.
		"""
		try:
			alumni = bttbAlumni(self.__alumDir)
			self.stage( 'Populate Volunteers' )
			for member in alumni.memberList:
				allEvents = FullVolunteerList()
				for event in allEvents:
					if member.isVolunteering( event ) or member.isVolunteering('Anything'):
						self.insertVolunteer( member.id, allEvents[event] )
			# Commit is necessary because I'm using InnoDB
			self.execute( 'COMMIT' )
		except Exception, e:
			Error( self.__db.currentStage(), e )

	def insertAttendance(self, alumni_id, event_id):
		"""
		Insert a single event attendance record into the attendance table, if it isn't already there
		"""
		try:
			qSelect = "SELECT attendance.alumni_id FROM attendance WHERE (attendance.alumni_id, event_id) = (%d, %d);" % (alumni_id, event_id)
			self.execute( "SELECT attendance.alumni_id FROM attendance WHERE (attendance.alumni_id, event_id) = (%d, %d);" % (alumni_id, event_id) )
			if len(self.cursor().fetchall()) == 0:
				insertCmd = "INSERT INTO attendance (alumni_id, event_id) VALUES (%d, %d);" % (alumni_id, event_id)
				self.execute( insertCmd )
			else:
				self.stage( 'SKIP INSERT of Attendance %d at %d' % (alumni_id, event_id) )
		except Exception, e:
			Warning( self.__db.currentStage(), e )

	def populateAttendance(self):
		"""
		Read all of the event attendance information from the Alumni XML files
		and populate the attendance table with that information.
		"""
		try:
			alumni = bttbAlumni(self.__alumDir)
			self.stage( 'Populate Attendance' )
			allEvents = AttendList()
			for member in alumni.memberList:
				self.stage( 'Check attendance for ' + member.fullName() )
				for event in allEvents:
					if member.isAttending( event ):
						self.insertAttendance( member.id, allEvents[event] )
				if member.isAttending( 'Concert' ):
					self.insertAttendance( member.id, allEvents['Concert Practice'] )
			# Commit is necessary because I'm using InnoDB
			self.execute( 'COMMIT' )
		except Exception, e:
			Error( self.__db.currentStage(), e )

	def insertInstrument(self, instrument, isInParade, hasParadeMusic, isInConcert, hasConcertMusic):
		"""
		Insert a single instrument record into the instrument table
		"""
		try:
			qSelect = "SELECT instruments.id FROM instruments WHERE instruments.instrument = '%s';" % (instrument)
			self.execute( qSelect )
			if len(self.cursor().fetchall()) == 0:
				insertCmd = "INSERT INTO instruments (instrument, isInParade, hasParadeMusic, isInConcert, hasConcertMusic) VALUES ('%s', %d, %d, %d, %d);" % (instrument, isInParade, hasParadeMusic, isInConcert, hasConcertMusic)
				self.execute( insertCmd )
			else:
				self.stage( 'SKIP INSERT of instrument "%s"' % (instrument) )
		except Exception, e:
			Warning( self.__db.currentStage(), e )

	def populateInstruments(self):
		"""
		Populate the instrument table with initial static data.
		"""
		try:
			self.stage( 'Populate Instrument' )
			self.insertInstrument( 'Alto Sax 1', 1, 1, 0, 1 )
			self.insertInstrument( 'Alto Sax 2', 1, 1, 0, 1 )
			self.insertInstrument( 'Baritone', 1, 1, 0, 1 )
			self.insertInstrument( 'Basses', 1, 1, 0, 1 )
			self.insertInstrument( 'Clarinet 1', 1, 1, 0, 1 )
			self.insertInstrument( 'Clarinet 2', 1, 1, 0, 1 )
			self.insertInstrument( 'Clarinet 3', 1, 1, 0, 1 )
			self.insertInstrument( 'F Horn 1', 1, 1, 0, 1 )
			self.insertInstrument( 'F Horn 2', 1, 1, 0, 1 )
			self.insertInstrument( 'Flute', 1, 1, 0, 1 )
			self.insertInstrument( 'Piccolo', 1, 1, 0, 1 )
			self.insertInstrument( 'Tenor Sax', 1, 1, 0, 1 )
			self.insertInstrument( 'Trombone 1', 1, 1, 0, 1 )
			self.insertInstrument( 'Trombone 2', 1, 1, 0, 1 )
			self.insertInstrument( 'Trombone 3', 1, 1, 0, 1 )
			self.insertInstrument( 'Trumpet 1', 1, 1, 0, 1 )
			self.insertInstrument( 'Trumpet 2', 1, 1, 0, 1 )
			self.insertInstrument( 'Trumpet 3', 1, 1, 0, 1 )
			self.insertInstrument( 'Colour Guard', 1, 0, 0, 0 )
			self.insertInstrument( 'Majorette', 1, 0, 0, 0 )
			self.insertInstrument( 'Marching Without Instrument', 1, 0, 0, 0 )

			# Commit is necessary because I'm using InnoDB
			self.execute( 'COMMIT' )
		except Exception, e:
			Error( self.__db.currentStage(), e )

if __name__ == '__main__':
	ErrorsInHtml( False )
	db = ImportAlumniDB()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
