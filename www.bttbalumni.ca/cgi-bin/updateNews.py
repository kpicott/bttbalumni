"""
Keeper of new, old, and obsolete news articles
"""

import os
from bttbAlumni import bttbAlumni
from bttbConfig import *
from datetime import datetime,timedelta
__all__ = ['bttbNews']

class bttbUpdateNews:
	def __init__(self):
		try:
			self.alumni = bttbAlumni()
		except Exception, e:
			Error( 'Could not find alumni information', e )

	def update20080120(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2008,1,16), 'Celebration of the Life of Roy Hall', MapLinks( """
			<p>
			For those who weren't aware, Roy Hall passed away on December 26, 2007
			after a brief battle with cancer.   Roy was a Founding member of the
			Burlington Boys & Girls Band, and a life long supporter of the
			Burlington Teen Tour Band.

			On behalf of the Hall family, please accept this invitation to a service
			of celebration of the life of Roy Hall which will be held on Saturday
			January 19 at 11 am at Compass Point Church (formerly Park Bible
			Church).  Compass Point is located on Kerns Rd in Burlington (off the
			North Service Rd, west of Brant St).

			The Hall family has indicated that if anyone is interested in making a
			donation in Roy's memory, they can do so to either the Carpenter Hospice
			in Burlington, or to the Burlington Teen Tour Band.

			On behalf of the alumni of the BTTB, we extend our condolences to the
			Hall family.

			On a personal note, it was an honor to march in front of Mr. Hall during
			the Sound of Music parade this past summer. 
			<br>
			<i>--- Ron Wilk</i>
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20080120_2(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2008,1,16), 'Bill Snowdon', MapLinks( """
			<p>
			It is with great sadness that I announce that last night Bill
			Snowdon passed away. As most of you are aware Bill was suffering
			from Lou Gerrigs disease, which came on very fast over the last
			few months.
			</p>
			<p>
			Bill was the Drum Line instructor and assistant director of the
			Burlington Junior Redcoats and had to resign this past September
			due to his health.  He was also an active Band Booster and
			chaperoned the band on several occasions and tours.
			</p>
			<p>
			Our thought and prayers are with Mary and Ben during this
			sad and difficult time.
			<br>
			<i>--- Rob Bennett</i>
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20080120_3(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2008,1,16), 'Bill Snowdon Obituary', MapLinks( """
			<p>
			SNOWDON, William Bill passed away peacefully on Sunday,
			January 20, 2008, at the age of 54. Treasured husband of Mary
			Taylor. Dearly loved and devoted father of Benjamin. Beloved son
			of Freda and Ray and brother of Michael and Brian. Bill was an
			active man, dedicated to his passions. Through his interests and
			caring, he touched the lives of many people, both young and old.
			Fond memories will be cherished by his family and friends here at
			home and in England. Visitation will be held at SMITH'S FUNERAL
			HOME, 1167 Guelph Line (one stoplight north of QEW), BURLINGTON
			(905-632-3333), on Wednesday from 3-5 and 7-9 p.m. A celebration
			of Bill's life will be held at the same location on Thursday,
			January 24, 2008 at 1:00 p.m. Many thanks to Marizel Magsino,
			nurses and support workers, JNE staff and the McMaster ALS Clinic,
			all of whom provided Bill with wonderful care and support. In
			lieu of flowers, donations to the Hamilton Health Sciences
			Foundation - ALS Clinic or the ALS Society of Ontario would be
			appreciated by the family. <a href='www.smithsfh.com'>Smith
			Funeral Home Website</a>.
			</p>
			<p>
			See the article on Bill in the Flamborough newspaper:
			<a href="http://www.flamboroughreview.com/printarticle/151478">
			http://www.flamboroughreview.com/printarticle/151478</a>
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20080520(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2008,5,20), 'Big Swing Golf Tournament', MapLinks( """
			<p>
			Some of you remember this tournament from last year - it's
			sponsored by the Band Boosters and runs the Thursday before the
			Sound of Music Festival. It's cheaper than last year, at $175 a
			person including golf, cart, and food, with a silent auction and
			raffle to help raise money for the band. We lost flower day this
			year for reasons beyond our control so we're really counting on
			this one to help fund the summer tour (Rhode Island,
			Massachusetts, and Quebec).
			</p>
			<p>
			You can see the full details at
			link:(http://teentourboosters.com/Website/UpcomingEvents/tabid/58/Default.aspx, the Band Boosters website)
			or email directly to send:(golf@teentourboosters.com).
			</p>
			"""), 0)
			,
			(datetime(2008,5,20), 'Alumni Weekend DVD Update', MapLinks( """
			<p>
			We would like to apologize for the delay in getting the DVD's from
			the 60<sup>th</sup> anniversary out to those who have paid for
			them.  I had jumped the gun in the last email announcing their
			status.  At that time there was a bit more final checking and
			review prior to going into production.  I am pleased to announce
			that the DVD's have been sent to print, and we expect to have them
			available this week!  An email will be sent to those alumni who
			had ordered the DVD letting them know when they're available.	
			<br>
			Ron Wilk, 60<sup>th</sup> Anniversary Celebration Co-Chair
			</p>
			"""), 0)
			,(datetime(2008,5,20), 'Annual Fundraising Dinner', MapLinks( """
			<p>
			It's not until Saturday September 27th but you'll want to mark
			your calendars now as the Band Boosters host their annual
			fundraising Dinner/Dance (last year called the "Gala"). This event
			will be held at the RBG. It's a great evening and a great way to
			show your support for the BTTB. Further details will be coming out
			over the summer.
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20080606(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2008,6,6), '60th Anniversary DVD Now Available', MapLinks( """
			<p>
			We're pleased to announce that the 60<sup>th</sup> anniversary DVD is now available for distribution.  For those alumni living in the Burlington area, if you're able to stop by at the Music Centre over the next 2 weeks on Wednesday and Sunday practice, either Lana or I will be there with the DVD.  If you're not able to pick up during those times, we'll be mailing them out after that.
			</p>
			<p>
			We'd like to thank John Peachey for his time and efforts in putting the DVD together.  There's just under 2 hours of band history in the form of still photos, video clips and music.  The DVD also features many pictures and video from the 60<sup>th</sup> Anniversary weekend.
			</p>
			<p>
			Thanks again for your patience in waiting for the final product.  We're sure the wait was worth it!!! 
			<br>
			Ron Wilk, 60<sup>th</sup> Anniversary Celebration Co-Chair
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20080913(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2008,9,13), 'Reserve Your Date for Golf Now!', MapLinks( """
			<p>
			It's too late for this year's tournament, and it was a great one.
			Why not start planning early for next year and get that foursome
			together? If you put away a mere $4 each week starting now the
			golf will be paid for by the time it rolls around.
			</p>
			<p>
			As usual see
			link:(http://teentourboosters.com/Website/UpcomingEvents/tabid/58/Default.aspx, the Band Boosters website)
			for details and how to keep up to date. You can even make a
			smaller cash donation through PayPal right on the website if golf
			is not your thing!
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20080914(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2008,9,14), 'Dance to the Music Tickets', MapLinks( """
			<p>
			Looking for a great night out that will also help support the band
			and their upcoming big tour? On September 27th the Band Boosters
			are supporting the "Dance to the Music" event (formerly known as
			the Mayor's Gala) as a fundraiser.
			</p>
			<p>
			Latest information is always available on the
			link:(http://teentourboosters.com/Default.aspx?tabid=58, the Band Boosters website)
			Grab a ticket, or a whole table and combine a great time with
			supporting a great cause. Tickets are $125 and available at any
			band practice, the September 15th Booster meeting (Senior's Centre
			at 7pm), or via the Booster website contact information.
			</p>
			<p>
			Oh yes - entertainment features bands that include former band members.
			Hope to see you there!
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20090413(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2009,4,13), 'Sound of Music Festival Request for Information', MapLinks( """
			<p>
			The Sound of Music Festival is looking for Festival Programs for
			1984, 1985, 1992, 1995.   In addition to that, they are looking for
			anyone that was on the board for those years (they are inviting
			them back for a special recognition celebration).  If anyone has
			kept the programs from those years, please respond to
			send:(info@bttbalumni.ca) and we will pass it along to the
			appropriate people at the Sound of Music Festival group.
			</p>
			"""), 0),
			(datetime(2009,4,13), 'Alumni Band Performance - Sound of Music Festival: Saturday June 20th', MapLinks( """
			<p>
			Can you believe it's already 2 years since the 60th anniversary!
			That was a great weekend celebrating 60 years of the Burlington
			Teen Tour Band!  We've had many discussions with alumni asking
			when we'd be playing again, and have found the perfect opportunity.
			</p>
			<p>
			2009 marks the 30th edition of the Sound of Music Festival.
			The Grande Festival Parade will be taking place on Saturday
			June 20th.  The Sound of Music Festival parade committee, chaired
			by BTTB Alumni Kevin Picott send:(parade@soundofmusic.on.ca), has
			penciled in the BTTB Alumni Band to perform in this parade.  
			</p>
			<p>
			We would appreciate feedback from the alumni whether we can get a
			suitable band together.  We have close to 700 alumni registered
			through the website and we should be able to put together a good
			size band.  There's also a lot of work to be done in putting this
			together.  Please let us know if you are interested in helping out
			in putting this event together. 
			</p>
			<p>
			Send a message to us at send:(info@bttbalumni.ca) if you would
			like to march in the 2009 parade.  We need to know fairly soon so
			we can confirm our attendance in the parade.
			</p>
			"""), 0),
			(datetime(2009,4,12), 'Joel Haynes Jazz Nomination', MapLinks( """
			<p>
			Some exciting news. BTTB Alumni Joel Haynes is fortunate to have
			been nominated for 2 categories in Canada's "National Jazz Awards"
			for 2009:  "Best Jazz Drummer of the Year" and "Best Jazz Recording
			of the Year".   If you are interested in casting a vote, you can
			check out some of his most recent work on his website,
			link:(http://www.joelhaynes.com) and/or
			link:(http://www.myspace.com/joelhaynes).
			</p>
			<p>
			Only 1 vote per computer will count.  It doesn't matter if you
			have more than 1 e-mail address on your computer.  The vote will
			only count if you vote once on your computer.  Here is how you
			can do this:
			<li>go into the website
			link:(http://www.nationaljazzawards.com)</li>
			<li>click on the 2009 voting button</li>
			<li>make a selection for EVERY category (or your vote won't count).
			If you do not know who to choose for in the other categories, you
			can choose "None of the Above". </li>
			</p>
			<p>
			Thank-you for your support --- Joel Haynes.
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20120430(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2012,4,30), 'Alumni Band Performance - Sound of Music Festival: Saturday June 16th', MapLinks( """
			<p>
			The Sound of Music parade is coming up quickly.  I hope you have
			all been dusting off your band instruments and getting ready for
			the parade.  June 16th is the day of the parade.  It will be the
			65th anniversary of the band. So come on down to represent the
			many generations of the Teen Tour Band!  
			</p>
			<p>
			We need to know numbers so we can make sure we have enough flags
			for the colourguard, enough drums for the drummers, and tubas etc.
			You can register on the facebook under the event
			link:(https://www.facebook.com/events/346445498740886,BTTB 65th Anniversary Parade @ The Sound Of Music)
			There will be updates on this site continuously the closer to the
			event.
			</p>
			<p>
			The band music that we will perform on parade day is available for
			download
			link:(http://www.bttbalumni.ca/SheetMusic/, here on this website in PDF format)
			. Lyres are welcome though some of our
			eyes are having a hard time reading those tiny little dots these
			days so memorizing is good too.
			</p>
			<p>
			We are planning to have a short practise on June 10th and then
			some beverages after so please mark your calenders.  We will let
			you know the place and time the closer to the date and once it is
			all finalized. But it will help if we know the numbers so we can
			warn drinking establishments that we are coming.  
			</p>
			<p>
			Looking forward to seeing you all there.  The more the merrier!
			<br>
			--- Cindy Bond send:(cbond6@cogeco.ca)
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20120602(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2012,6,2), 'Sound of Music Festival Update', MapLinks( """
			<p>
			<b>REHEARSAL:</b> Friday June 15, 6:30 - 8:00 PM, Music Centre.
			Drum line separate or earlier? After rehearsal is "free time". 
			</p>
			<p>
			<b>MUSIC:</b> Click on the Music Tab on the left. Remember, we're
			playing the Eric Ford version of Strike up the Band.
			</p>
			<p>
			<b>UNIFORM:</b> Red Shirt, Blue pants.  A limited amount of
			XL Alumni shirts will be available for $10.  TopHat members are
			OK to wear either THMO uniforms or THMO T-shirts.
			</p>
			<p>
			<b>Sound of Music Parade:</b> Arrive at Music Centre by 10 AM.
			Parking is <b>EXTREMELY LIMITED</b>. Parade moves off at 11. We
			are the last unit in the parade. Transportation for those
			participating first with either BTTB or Top Hats is being worked on.
			</p>
			<p>
			Hope to see you all out!!!  It should be a great time had by all.
			<br>
			--- Cindy Bond send:(cbond6@cogeco.ca)
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20121028(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2012,10,28), 'BTTB Needs Your Help With Aviva Community Fund', MapLinks( """
			<p>
			Aviva Insurance is running a promotion where they are donating
			$1,000,000 in a community fund to organizations through an online
			competition.
			</p>
			<p>
			The Burlington Teen Tour Band Boosters have entered on behalf of
			the band in order to help fund the trip to Ireland in March 2013
			to celebrate St Patrick's Day.  Their goal is to ensure that all
			members of the band are able to attend this cultural and
			educational event.   
			</p>
			<p>
			You can help by visiting
			link:(https://www.avivacommunityfund.org/ideas/acf14790, the Aviva Community Fund Voting Page)
			and adding your vote to support the band. You can vote once per
			day so check in every morning and vote! Registration is required
			but can be done directly with your Facebook account so it just
			takes a second. (15 seconds if you want to register separately.)
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def update20130123(self):
		#
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		news = [
			(datetime(2013,01,23), 'A Band Member\'s Story', MapLinks( """
			<p><i>
			I grew up in Burlington and attended a grade school where I was
			lucky enough to have been given the chance to learn to play an
			instrument. My home life wasn't the greatest and money was usually
			at the centre of the unrest. My father and mother fought a lot and
			I was always looking for a reason to get out of the house. When I
			was 13, a neighborhood kid took me to the Music Centre and I spent
			my first afternoon with the band. Soon I was a member. For the rest
			of my teenage years I made music and especially dear to me, great
			life long friends. Although I know my parents could not afford to
			send me on tour I was always able to go. To those that made it
			possible all those years ago I say thank you.
			</i></p>
			<p>
			This story is as true today as it was when you were a band member.
			</p>
			<p>
			We all have a Baltimore tour, a Myrtle Beach, a Warren Ohio, a
			Parade of Champions, a Rose, Cotton or Orange Bowl tour story to
			remember or tell.
			</p>
			<p>
			Please help "pay it forward"
			</p>
			<p>
			Like the Bryan Adams hit "Summer of 69" "those were the best days
			of my life"
			</p>
			<p>
			Please consider making a donation to the Boosters to help make
			memories for a band member today.  <b>Alumni donations will go
			directly to help a Band Member in need get to Ireland</b>.
			</p>
			<p>
			Ways to donate:
			<ol>
			<li> Drop into the Music Centre for a visit! We are in the lobby
			at the beginning and end of every practice</li>
			<li> Visit link:(http://teentourboosters.com, the Boosters website)
			to make an online donation</li>
			<li> Mail a cheque to:<br><i>
			Burlington Teen Tour Band Boosters<br>
			3017 St.Clair Ave. Suite 322<br>
			Burlington, ON<br>
			L7N 3P5
			</i></li>
			</p>
			<p>
			Together we can make memories happen!
			</p>
			"""), 0)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		self.insertNews( news )

	def insertNews(self, news):
		#===================================================================
		for when, title, article, status in news:
			newNews = """
			DELETE FROM news WHERE title='%s';
			INSERT INTO news (title, description, appeared, status)
			VALUES ('%s', '%s', '%s', '%d')
			""" % (DbFormat(title).replace("\n","\\n"), DbFormat(title).replace("\n","\\n"), DbFormat(article).replace("\n","\\n"), when.strftime('%Y-%m-%d %H:%M:%S'), status)
			print newNews
			self.alumni.processQuery( newNews )

if __name__ == '__main__':
	updater = bttbUpdateNews()
	# updater.update20080120()
	# updater.update20080120_2()
	# updater.update20080120_3()
	# updater.update20080520()
	#updater.update20080606()
	#updater.update20080913()
	#updater.update20080914()
	#updater.update20090413()
	#updater.update20120430()
	#updater.update20120602()
	#updater.update20121028()
	updater.update20130123()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
