"""
Keeper of new, old, and obsolete news articles
"""

import os
from bttbAlumni import bttbAlumni
from bttbConfig import *
from datetime import datetime,timedelta
__all__ = ['bttbNews']

class bttbNews:
	def __init__(self):
		try:
			self.alumni = bttbAlumni()
		except Exception, e:
			Error( 'Could not find alumni information', e )

	def createTable(self):
		self.alumni.processQuery( 'DROP TABLE IF EXISTS news' )
		self.alumni.processQuery("""
		CREATE TABLE IF NOT EXISTS news (
		  id           INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
		  title        VARCHAR(64)      NOT NULL COMMENT 'News Article Title',
		  description  TEXT             NOT NULL COMMENT 'News Article Body',
		  appeared     DATETIME         NOT NULL DEFAULT '2007-01-01 00:00:00' COMMENT 'Day the news article first appeared',
		  status        INT(2) UNSIGNED  NOT NULL COMMENT 'News article status',

		  PRIMARY KEY(id)
		)
		Engine=InnoDB
		DEFAULT
		CHARSET=utf8
		COMMENT='List of BTTB Alumni Front Page News Articles';
		""")

	def populateNews(self):
		"""
		Return a string with the content for this web page.
		"""
		# News array format:
		#    DatePosted,Title,Text,Type (0=current, 1=obsolete, 2=broken)
		#
		news = [
			(datetime(2007,9,1), 'Special Offer to BTTB Band Alumni', MapLinks( """
			<p>
			You were once proud to be a BTTB Band Member - Carry on the
			Tradition!
			</p>
			<h4>
			Limited Time Only - Special Offer Good until October 31/2007
			</h4>
			<p>
			'Marching in Time' Limited Edition Unframed Print by John Newby
			Special Offer @ $100 (<i>regular $125</i>) for Band Alumni 
			who participated in the 60th Anniversary <b>ONLY</b>
			</p>
			<h4>
			HELP the Band get to the 2008 Tournament of Roses Parade!  
			Order your print today.  
			</h4>
			<p>
			One of a kind conversation piece.  Great for home or office.  
			</p>
			<h4>
			Regular print price graciously accepted in support of the Rose
			Bowl Tour.
			</h4>
			<p>
			Use the link:(#johnNewby,regular order form) but be sure to 
			mark <b>'ALUMNI'</b> on it in order to take advantage of this
			special offer (and make sure you've registered here with us
			so that we can confirm your alumni status).
			</p>
			"""), 0),
			(datetime(2007,7,15), 'Gearing Down But Still Active', MapLinks( """
			<p>
			The celebration has been over for a while now (watch for news
			soon on the amazing support we were able to give to the BTTB as
			a result), we've all had time to clear our heads, and now it's
			time to think about how to keep the Alumni organization rolling.
			</p>
			<p>
			send:(info@bttbalumni.ca,Email us if you are interested) in
			helping out in deciding the future of the Alumni.
			</p>
			<p>
			This website will shift gears away from the 60th Anniversary
			Celebration and towards an ongoing conversation with Alumni at
			large.  Hope to see you back often!
			</p>
			""" ), 0),
			(datetime(2007,6,20), 'The Post-Celebration Pic That Says It All', MapLinks( """
			<a target='photo' href='__CELEBRATIONHREF__/Cleanup.jpg'>
			<img align='left' src='__CELEBRATIONHREF__/Cleanup_Small.jpg'
			width='150' border='0'></a>
			""" ), 1),
			(datetime(2007,6,15), 'Now the Fun Begins!', MapLinks( """
			<p>
			Finally the day is here and the celebration can begin! Here's a quick summary
			of the weekend's events:
			<ol><table cellpadding='5' cellspacing='5'>
			<tr>
				<th align='left'><i>Parade Music Practice</i></th>
				<td>Friday</td>
				<td>6:30pm</td>
				<td>Music Centre</td>
			</tr>
			<tr>
				<th align='left'><i>Social Event</i></th>
				<td>Friday</td>
				<td>7:30pm</td>
				<td>Central Arena</td>
			</tr>
			<tr>
				<th align='left'><i>SOMF Parade</i></th>
				<td>Saturday</td>
				<td>10:00am</td>
				<td>Beside Central Arena</td>
			</tr>
			<tr>
				<th align='left'><i>Massed Band</i></th>
				<td>Saturday</td>
				<td>1:00pm</td>
				<td>Brant St. at Caroline</td>
			</tr>
			<tr>
				<th align='left'><i>Homecoming</i></th>
				<td>Saturday</td>
				<td>7:00pm</td>
				<td>Central Arena</td>
			</tr>
			<tr>
				<th align='left'><i>Concert Rehearsal</i></th>
				<td>Sunday</td>
				<td>10:30am</td>
				<td>Music Centre</td>
			</tr>
			<tr>
				<th align='left'><i>BBQ Lunch</i></th>
				<td>Sunday</td>
				<td>1:00pm</td>
				<td>Music Centre</td>
			</tr>
			<tr>
				<th align='left'><i>Concert in the Park</i></th>
				<td>Sunday</td>
				<td>3:00pm</td>
				<td>Bandshell</td>
			</tr>
			</table></ol>
			</p>
			"""), 1),
			(datetime(2007,6,15), 'Weekend Tips', MapLinks( """
			<p>
			It's going to be a fantastic Homecoming weekend!  We kicked off
			the weekend on Thursday with the Boosters annual Big Swing Golf
			Tournament which was a rousing success!  A great time was had by
			all who attended.  We saw a large number of alumni on the course,
			and everyone had their picture taken with CL Keedy, 2007 Rose Bowl
			President.
			</p>
			<p>
			The toughest question raised though is... after winning the
			Putting Contest, how is Dave Wallace going to take the Beer
			Fridge (full of beer) back to Dubai with him?
			</p>
			<h4>
			Here are a few reminders and pointers for you to have a fun and
			successful weekend.</h4>
			<ol>
			<li>   If you need any assistance with anything - look for the
			Alumni who have the Green nametags.  Those are members of the
			Organizing Committees.  Ask them for help!  Alumni attending this
			weekend's events will receive nametags on lanyards.  Thanks to
			City Automotive of Burlington for their generous sponsorships of
			these lanyards.
			</li>
			<li>
			Band Boosters hosting BBQ at Central Arena during Friday night
			Social Event The Band Boosters will be hosting a cash BBQ at
			Central Arena during the evening.  Please support the band by
			purchasing a burger, sausage or hot dog at this BBQ.  All proceeds
			will of course be going back to the band.  Remember, there will
			not be chaperones around to give out Meal Money!  If you're
			rushing from work to make the 6:30 practice, you can skip supper
			at home and buy a burger, hot dog or sausage at Central Arena.
			</li>
			<li>
			Here's something you won't remember from band days - a cash bar.
			We will have limited capability for credit card transactions, so
			remember to bring cash for your beverage tickets.  Any tickets
			purchased on Friday can also be used on Satuday.
			</li>
			<li>
			We will be having ticket purchases at the door both Friday
			and Saturday night so that nobody misses out on the great time.
			</li>
			<li>
			The Alumni Band will be forming up by Central Arena to prepare
			for the parade. However, when the current BTTB steps off to start
			the parade at 11 AM, we'd love to see everyone at the New Street
			entrance cheering on the band!  It's going to be a hot parade.
			Remember to wear sunscreen and your uniform ball cap. 
			</li>
			</ol>
			"""), 1),
			(datetime(2007,6,15), 'Last Minute Information', MapLinks( """
			<p>
			There is <b>NO</b> parking available at the Music Centre or
			Central Arena on Saturday morning for the parade.   This is also
			a reminder that on Friday night, you won't be able to leave your
			car there overnight, as it will be towed. The Sound of Music is
			using the arena parking lot as the marshalling area for the parade.
			The Webmaster, Kevin Picott, is also in charge of the parade lineup
			so if you need alternatives find him on Friday night and he'll
			tell you where to go :-).
			</p>
			<p>
			We have arranged parking at Mapleview Mall and Bus Transportation
			to the beginning of the parade.  We have also arranged
			transportation back to Mapleview after the massed band performance
			at Brant St and Caroline St, which is happening immediately after
			the parade.
			</p>
			<h4>Parking Details at Mapleview Centre (Fairview St and Maple Ave)</h4>
			<p>
			Parking is available at the South Parking lot area, below The Bay.
			We will have signs there and look for the Red and Blue Balloons or
			the big Yellow Laidlaw School Bus.  Buses will be departing from
			Mapleview beginning at 9 AM and running until
			approximately 10:45 AM.
			</p>
			<p>
			For those Alumni in the Top Hat Marching Orchestra and Staff of
			the current BTTB, a bus will be waiting at Victoria St waiting to
			take you back to the Music Centre for the start of the parade,
			so you can do it all again!  We would ask those that are changing
			at the end of the parade into their Alumni uniforms to be as quick
			as possible so you don't miss the step off from Teen Tour Way
			onto New Street.
			</p>
			<p>
			Instruments needed for alumni will be returning the same way, so
			Bells players in particular be on the lookout.
			</p>
			<p>
			The Massed Band will then form up at Brant and Caroline for a
			brief performance and presentations.  After this performance,
			the buses will shuttle you back to Mapleview.
			</p>
			<p>
			We will then see you back at Central Arena for 7 PM.
			Thanks for your co-operation, and see you this weekend! 
			</p>
			<p>
			To those alumni who aren't in town, and won't be able to join us,
			we know you're with us in spirit, and we'll see you at the next
			parade!  Check the website through the weekend for updates.
			</p>
			"""), 1),
			(datetime(2007,6,13), 'Bring Your SunScreen!', MapLinks( """
			<p>
			Latest weather reports have Saturday at 29&deg;C for the parade.
			The Alumni hats will help but we're not going to have those nice
			thick tunics and long pants to protect us from the sun!
			</p>
			"""), 1),
			(datetime(2007,6,12), 'Newby Print Reminder', MapLinks( """
			<p>
			When you're at the Music Centre this weekend don't forget to check
			out the John Newby print hanging over the stairway. There are still
			link:(#johnNewby,a limited number available for purchase), which
			will be on display Friday and Saturday night.  John will be
			attending the Homecoming Saturday night if you want to chat.
			</p>
			"""), 1),
			(datetime(2007,6,11), 'Guide to 60th Anniversary Homecoming Reunion Available', MapLinks( """
			<p>
			The special reunion edition of our newsletter is available for
			download.  This edition includes a schedule of events, answers to
			the most frequently asked questions regarding this weekend's
			reunion, greetings from current Managing Director Rob Bennett,
			a map to our events and much, much more.
			</p>
			<p>
			As always, feel free to share the newsletter with any former Band
			members, Boosters or supporters but also encourage them to sign up
			for the reunion and the Alumni Association as well. See you all
			this weekend!
			download:(__NEWSLETTERPATH__/Vol1No6.pdf,Click here to download the PDF file.)
			</p>
			"""), 1),
			(datetime(2007,6,11), 'Picking Up Your Uniform Saturday?', MapLinks( """
			<p>
			If you're coming from out of town, or are just a last minute
			kinda person and are waiting until the morning of the parade to
			pick up your uniform please be at the Music Centre no later than
			9:00am on Saturday morning to pick up your shirt and hat. Our
			uniform volunteers need time to line up too!
			</p>
			"""), 1),
			(datetime(2007,6,9), '6 Most Frequently Asked Questions', MapLinks( """
			<h3>Where can I get the music?</h3>
			<div class='ph3'>
			The Marching Music is online right here. To get the music for your
			instrument, you need to sign in at the bottom of the Red Menu Bar
			seen over to the left of this webpage, you see 2 input fields.
			One for User Name, the other for Password.  Your User Name is your
			current FirstName LastName (e.g. Bob Johnson).  Your Password is
			the password you created on your profile when you first signed up.
			If you didn't have a password, the default password is an empty
			field.  When you've logged on, there are 2 choices:
            <h4>I haven't yet selected my instrument - how do I get my music?</h4>
			<div class='ph4'>
			If you have not yet selected the instrument you're playing, go to
			the section of our web site called "parade", either from the Red
			Menu Bar "60th&gt;Parade" link or link:(#parade,by clicking here).
			Here you will find a list of the instrumentation available for the
			parade (including those who wish to march without an instrument).
			Select a part and you will be pointed to a download of the music
			for that part in PDF format.
			</div>
			<h4>I selected my instrument before, but I need another copy of my music...</h4>
			<div class='ph4'>
			From the Red Menu Bar, click on "Alumni&gt;My Profile" or go
			directly link:(#register,there using this link).  Scroll down
			to the "60th Anniversary Celebrations" section where you will see
			a link to "Click Here to Download your INSTRUMENT parade sheet
			music."
			</div>
			</div>
			<h3>I don't play anymore, can I march?</h3>
			<div class='ph3'>
			ABSOLUTELY!!  We recognize that many of us haven't played for a
			while.  If your horn is a bit "rusty", try and drag it out of the
			closet and do your best.  If you just don't play anymore - that's
			OK, too.  We want to see you on parade!     Our goal is to have
			fun, and represent 60 years of the band.  So come on out and have
			fun marching in the Sound of Music Parade!
			</div>
			<h3>What "Uniform" are we wearing?</h3>
			<div class='ph3'>
			The Uniform of the day is: Alumni Golf Shirt and Ball cap, which
			are available to order in the link:(#tickets,registration package).
			The "bottom" half of the uniform is Blue.  You can wear shorts,
			pants or capris.   Wear appropriate footwear to march a  parade,
			running shoes are fine.
			</div>
			<h3>When can I pick up my Uniform?  or I haven't ordered a Uniform yet, when can I pay for it, and can I pick it up at the same time?</h3>
			<div class='ph3'>
			We are having an "early" registration pickup session at the Music
			Centre this coming Sunday, June 10 between 2 and 4 pm.  We will
			also be accepting payment for those who have not yet paid for
			their registration packages at this same event.  You will also be
			able to pick up your registration package on Friday June 15 at the
			Music Centre after 4 pm.
			</div>
			<h3>Are we practicing?</h3>
			<div class='ph3'>
			We sure are - there is a practice on Friday June 15 at 6:30 at the
			Music Centre.  This practice is immediately followed by the Friday
			Night Social Event at Central Arena.
			</div>
			<h3>Is anything happening after the parade?</h3>
			<div class='ph3'>
			Right after the parade, as a special event, the Junior Redcoats,
			the current Burlington Teen Tour Band, and the Alumni Band, will
			be performing at the intersection of Brant St. and Caroline St.
			It will be a special occassion as the President of the Tournament
			of Roses, Mr. CL Keedy, will be presenting the Tournament of Roses
			Flag to the current band in recognition of their selection to
			perform at the 2008 Rose Bowl Parade.  
			</div>
			<div class='ph3'>
			After that you are free to enjoy the music festival all afternoon.
			Our next official event is the Homecoming 7pm Saturday night.
			</div>
			"""), 1),
			(datetime(2007,6,7), 'Drum Sectional Friday the 15th', MapLinks( """
			<p>
			Attention Parade Drummers! Please show up early, around 4pm, for
			the parade practice next Friday, June 15th. Come/go as you please
			or need to until regular practice time. The time will be used to
			adjust music, harnesses, pass out sticks, and other secret
			percussion rituals.
			</p>
			<p>
			Chris Garnier has arranged some drum music for The Hustle, The
			Thunderer, and the Street Beat.
			download:(__SHEETMUSICPATH__/Percussion.pdf,Click here to download it now.)
			</p>
			"""), 1),
			(datetime(2007,6,5), 'Bonus Concert Practice', MapLinks( """
			<p>
			Bill Hughes has arranged for an additional opportunity to rehearse
			as a concert band, with the current BTTB, this upcoming Sunday,
			June 10<sup>th</sup> at 2 pm.  The two rehearsals that we have
			already had were a great deal of fun, and everyone who attended
			enjoyed themselves immensely.
			</p>
			<p>
			In addition, Bill needs to confirm the number of alumni who are
			intending to play with the concert band on the 17<sup>th</sup>,
			so he can arrange to have enough chairs!
			Please send:(info@bttbalumni.ca,email us if you are intending to perform with the concert band)
			so that  we aren't playing musical chairs on stage on the
			17<sup>th</sup>.
			</p>
			"""), 1),
			(datetime(2007,5,26), 'Get Your Advance Schedule', MapLinks( """
			<p>
			When you register you'll get the full package. As a tease
			sneak-preview we're making available here the
			download:(__IMAGEPATH__/CelebrationSchedule.pdf,schedule of events for the weekend.)
			</p>
			"""), 1),
			(datetime(2007,5,29), 'Want to do a Tribute?', MapLinks( """
			<p>
			Have you ever wanted to thank someone that influenced you while
			you were in the band?  Well, here's the chance you've been waiting
			for!
			</p>
			<p>
			As a part of the Saturday night celebrations, the Reunion Committee
			is looking for Alumni to pay tribute to key people from the band's
			history.  Primarily we are looking for alumni to do a 2 to 4 minute
			speech about a current or former Music or Marching Directors, as
			they have had the greatest impact on the history of the Band, and
			its members.  We are also open to suggestions about speeches
			paying tribute to other individuals or groups which could also be
			recognized.
			</p>
			<p>
			To keep the evening flowing, there will be a limited number of
			presentations.  Please submit a draft of your presentation to us
			by Tuesday June 5 at send:(info@bttbalumni.ca).  Those that are
			selected to present will be informed by Sunday June 10.
			</p>
			<p>
			The excitement is building, and we're now counting the days to
			the 60th Anniversary Weekend!  And, if you haven't yet sent in
			your registration form and payment, get it in soon!   Remember,
			you can bring it to the Concert Band rehearsal this Friday at
			the Music Centre, or email to send:(payments@bttbalumni.ca).
			</p>
			"""), 1),
			(datetime(2007,5,29), 'Burlington Post Special Insert', MapLinks( """
			<p>
			<a target='photo' href='__ARTICLEPATH__/PostInserts.jpg'><img align='left' src='__ARTICLEPATH__/PostInserts_Small.jpg' width='150' height='193' border='0'></a>
			The Burlington Post is proud to be working in conjunction with the
			Burlington Teen Tour Band, its Boosters and Alumni on the occasion
			of the Band's 60th Anniversary.  To celebrate this milestone the
			Burlington Post will be publishing a commemorative 60th
			Anniversary Section in the Sunday June 10th edition.  for more
			information on this supplement please see the attachment below, or
			contact Ted Lindsay at the Burlington Post.  he can be reached at
			905-632-4444 ext 272 or send:(tlindsay@haltonsearch.com).
			</p>
			<br clear='all'>
			"""), 0),
			(datetime(2007,5,26), 'Some parade Information', MapLinks( """
			<p>
			For those of you on Facebook you might be interested in a new
			group that sprung up,
			link:(http://www.facebook.com/event.php?eid=2416331359&ref=nf, those that are attending the Sound of Music Festival.)
			</p>
			<p>
			After the parade hang around Caroline Avenue for some after-parade
			events:
			<li>first is a performance by the popular Baltimore Band "New Edition"</li>
			<li>next up a Massed Band performance featuring us, the present BTTB, and the Junior Redcoats performing together (mothers, cover your children's ears!) </li>
			<li>finally the parade committee is organizing one of the world's
			longest Conga Line. After the post-parade performance listen for
			instructions and join in the fun! It should start around 3:30, so
			even if you need to put your instrument away first there's plenty
			of time to get back.</li>
			</p>
			"""), 1),
			(datetime(2007,5,25), 'Concert Practice A Success!!!', MapLinks( """
			<p>
			Thanks to everyone who came out Friday for the first Concert
			Practice. We were pleasantly surprised to see no less than 60
			people show up to warm up their chops. The Alto Saxes even
			outnumbered the Clarinets!
			</p>
			<p>
			Next week's practice should be even better. Parts are available
			onsite for those unable to print out the music that's here, as
			well as for the extra songs not available here (Queen in Concert,
			Ontario, Irish Washerwoman, Yakety Sax, 2007 FieldShow).
			</p>
			<p>
			We're hoping to beef up the lower brass a bit for next week, as
			well as the tenor saxes, and you can never have too many clarinets.
			Come on out for a fun musical evening, there's plenty of cover for
			those who are shy.
			</p>
			"""), 1),
			(datetime(2007,5,25), 'May Newsletter Available', MapLinks( """
			<p>
			The fifth Alumni newsletter is now available.
			download:(__NEWSLETTERPATH__/Vol1No5.pdf,Click here to download the PDF file.)
			</p>
			"""), 1),
			(datetime(2007,5,16), 'Newby Prints Framed', MapLinks( """
			<p>
			To help accommodate people who may not have time to get out
			themselves we're now offering
			link:(#johnNewby,pre-framed John Newby prints).  Prints 231, 232,
			and 233 are framed and ready to go if you request those numbers,
			or mark "to be framed" on your order form for other numbers.
			</p>
			<p>
			The price of the fully framed prints is $275, a fabulous deal for
			a great piece of art.
			</p>
			"""), 0),
			(datetime(2007,5,14), 'Concert Practice Reminder', MapLinks( """
			<p>
			The first link:(#concert,concert practice) is not far off!
			Anyone local to the Burlington area should be at the Music Centre
			at 7pm on Friday May 25<sup>th</sup>, and then again the following
			Friday, for a concert practice and social event.
			</p>
			<p>
			While you're there the committee members will be on hand to take
			your link:(#tickets,registration and payment) if you haven't
			already signed up.
			</p>
			<p>
			And check out the large size 
			link:(#johnNewby,John Newby print) now hanging proudly
			over the stairs just inside the entrance - got yours yet?
			</p>
			"""), 1),
			(datetime(2007,5,6), 'Concert Music Available for Download', MapLinks( """
			<p>
			At long last the first set of concert music is available for
			downloading. Visit link:(#concert,the concert page) to sign up
			for a part and download the music, just the same as you did for
			the parade.
			</p>
			<p>
			As there is a lot of concert music this is just the first set -
			return for the second set of music later.
			</p>
			"""), 1),
			(datetime(2007,5,4), 'Excitement Building', MapLinks( """
			<p>
			The weather is getting warm, band camp is approaching, and
			excitement is building as the celebration weekend approaches.
			As you can see from the new numbers there are quite a few people
			still waiting to buy their tickets - don't delay, do it today!
			</p>
			<p>
			And remind your brother/sister/spouse/third cousin twice removed
			to get their tickets too. Be there, or be marking time in the gym
			at 2 in the morning!
			</p>
			"""), 1),
			(datetime(2007,4,25), 'First Plateau Reached', MapLinks( """
			<img src='__IMAGEPATH__/500.png' border='0' width='750' height='400'>
			<br>
			We have reached our goal of 500 alumni registered! Thanks to
			everyone who has signed up, and we look forward to the next 500!
			"""), 1),
			(datetime(2007,4,25), 'Special Treat at Parade', MapLinks( """
			<table><tr><td>
			<img align='left' src='__IMAGEPATH__/DovesBG.png' border='0' width='162' height='74'></td><td>
			It's official, and it's going to be public knowledge so we wanted
			you to hear it here first. As the alumni band passes by the viewing
			stands in front of City Hall at the Sound of Music Festival Parade
			a dule of 60 doves will be released in honour of the band's
			60<sup>th</sup> anniversary.
			</tr></tr></table>
			"""), 1),
			(datetime(2007,4,25), 'April Newsletter Available', MapLinks( """
			<p>
			The fourth Alumni newsletter is now available.
			download:(__NEWSLETTERPATH__/Vol1No4.pdf,Click here to download the PDF file.)
			</p>
			"""), 1),
			(datetime(2007,4,20), 'Looking for...', MapLinks( """
			<p>
			Dredge up your memories, dive into your closets, and pull out your
			email and phone contact lists! Add to the fun and excitement of
			the celebration weekend by adding in your own little bit of band
			history.
			</p>
			<p>
			Know any Wallace B. Wallace winners who haven't fessed up?
			send:(wallacebwallace@bttbalumni.ca,Let us hear your version of their story.)
			</p>
			<p>
			Got any old photos, videos, or music clips hanging around?
			send:(info@bttbalumni.ca,Send them to us along with a description.)
			</p>
			<p>
			Know any of your former band friends/cronies/acquaintances that
			haven't signed up yet?  Drop them a line and say hello, and if
			you happen to mention the celebration weekend, so much the better!
			</p>
			<p>
			Got any humourous, serious, or just plain memorable anecdotes from
			your band days? link:(#memories, Add them to the pile for all to share.)
			</p>
			<p>
			Don't forget that this website will live on after the anniversary
			weekend, just like the friendships and relationships we all forged
			in the band. We're all about keeping the rich band history alive.
			</p>
			"""), 0),
			(datetime(2007,4,22), 'Scanathon - Bring Your Photos/Articles/Videos!', MapLinks( """
			<p>
			Got any old band photos, articles, or videos you'd like to share
			but don't want to part with?
			</p>
			<p>
			The Alumni Executive History Committee is producing a DVD for the
			60<sup>th</sup> anniversary weekend. It will include photos, news
			articles, archived video, music and interviews.
			</p>
			<p>
			Come out to the Music Centre on Sunday April 22 between 1pm and
			5pm. The committee will be on hand with
			scanning equipment to preserve your memories for posterity, and
			make them available for everyone to share.
			</p>
			<p>
			If you can't make it out that day you can still have your photos
			included by getting them scanned somewhere else (any office store
			will do it if you don't have a scanner yourself) and mailing them
			to us at the address on the link:(#tickets,order form). If you
			need the disc back you can pick it up at the alumni weekend.
			</p>
			<p>
			A cut-off date to receive photos will be announced shortly so
			please get yours in as soon as possible so that we can include
			them in the weekend.
			</p>
			<p>
			If you have any questions or suggestions for the historical DVD
			please email them to
			send:(jr.peachey@sympatico.ca,John Peachey at jr.peachey@sympatico.ca).
			</p>
			"""), 1),
			(datetime(2007,4,17), 'Streetbeat Made Retro', MapLinks( """
			<p>
			After careful consideration the drumline in the Sound of Music
			Festival parade anniversary band has decided to go back to the
			same streetbeat that was used at the 50<sup>th</sup> reunion.
			</p>
			<p>
			It's the one used in the '80's and '90's with the quad feature
			in the middle and snare drummers do <b>not</b> have to play
			traditional, they may play match.
			</p>
			<p>
			Don't forget to come out to the parade music practice on Friday
			night of the anniversary weekend so that you can refresh your
			memories (or learn it if it's new to you)!
			</p>
			"""), 1),
			(datetime(2007,4,17), 'Big Swing Golf!', MapLinks( """
			<p>
			We're pleased to provide the following information regarding the
			<b>Big Swing Golf Tournament</b> in support of the BTTB. This golf
			tournament is a significant fund raise for the Band Boosters as
			the band prepares for their trip to the Rose Bowl. The Boosters
			have kindly scheduled this event to be in conjunction with the
			60<sup>th</sup> anniversary weekend so to all you golfers, join
			the fun a day early.
			</p>
			<p>
			<b>Thursday June 14th, 2007, Millcroft
			Golf Club, Burlington.</b>
			</p>
			<p>
			Shotgun start is at 1:00pm, play 18 holes of golf including cart,
			dinner, and prizes. There will be longest drive and closest to the
			pin competitions.
			</p>
			<p>
			There will also be a silent auction, loot bags, and an opportunity
			to support a great program for the teenages in the Burlington
			area. All this for only $200.00 per person, or pay for your spot
			before May 15th and save $15.00.
			</p>
			<p>
			This is a charitable event. A tax receipt will be issued for the
			charitable portion of the event. You can even arrange for a
			dinner-only participation if golf is more your spouse's thing than
			yours. Make your cheques payable to: <i>Burlington Teen Tour Band
			Boosters Inc., 3017 St. Clair Avenue, Suite 322, Burlington,
			Ontario, L7N 3P5</i>.
			</p>
			<p>
			Because it is a shotgun start the number of entries are limited
			and is expected to sell out, so book early to avoid
			disappointment. Join the fun with the BTTB Boosters and the Band
			Alumni as we celebrate the 60<sup>th</sup> Anniversary of the
			Burlington Teen Tour Band.
			</p>
			<p>
			For more information please contact
			send:(golf@teentourboosters.com) or visit the Band Boosters web site
			link:(http://teentourboosters.com/Website/FundRaising/tabid/59/Defrault.aspx)
			for further details and registration forms.
			</p>
			"""), 1),
			(datetime(2007,4,17), 'Ordering Updates', MapLinks( """
			<p>
			Well the early bird deadline has passed and we have a bunch of
			happy people already signed up and ready for the weekend.
			There's still plenty of time to order though - head on over to
			link:(#tickets,the ticket page to get the latest order form).
			</p>
			<p>
			New to this form - a new a la carte purchase item that includes
			not just the parade uniform but also the souvenir package being
			prepared specially for this weekend. (The "Scan-a-thon" article
			may give you a hint as to what you might see in the souvenir
			package.)
			</p>
			"""), 1),
			(datetime(2007,4,7), 'Hotels For Celebration Weekend', MapLinks( """
			<p>
			The Holiday Inn Burlington,
			<a target='map' href='http://maps.google.com/maps?f=q&hl=en&q=3063+South+Service+Road,+Burlington,+Ontario&sll=37.0625,-95.677068&sspn=45.736609,69.082031&layer=&ie=UTF8&z=15&ll=43.355016,-79.801383&spn=0.020626,0.033731&om=1&iwloc=addr'>(3063 South Service Rd, 905 639-4443)</a>
			is offering a preferred rate to BTTB Alumni for the 60<sup>th</sup>
			Anniversary Weekend.  The rate for alumni is $118 + taxes.
			</p>
			<p>
			Comfort Inn Burlington
			<a target='map' href='http://maps.google.com/maps?f=q&hl=en&q=3290+South+Service+Road,+Burlington,+Ontario&sll=43.355016,-79.801383&sspn=0.020626,0.033731&layer=&ie=UTF8&z=14&ll=43.357201,-79.797735&spn=0.041251,0.067463&om=1&iwloc=addr'>
			(3290 South Service Rd, 905-639-1700)</a>
			is also offering a preferred rate of $89.99 + taxes.  Mention that
			you are a BTTB Alumnus. 
			</p>
			"""), 1),
			(datetime(2007,4,6), 'StreetBeat Music Online', MapLinks( """
			<p>
			Thanks to Chris Garnier and Kevin Lower there is now sheet music
			to the street beat the Alumni drumline will be doing at the Sound
			of Music Parade. You can download it from your profile if you've
			already signed up for the parade, sign up for the parade now and
			get it, or 
			download:(__SHEETMUSICPATH__/Percussion.pdf,just get it here.)
			</p>
			"""), 2),
			(datetime(2007,4,6), 'Priceless', MapLinks( """
			<p>
			Because some things money <b>can</b> buy...
			</p>
			link:(#tickets, <div style='display:none;' name='priceless' id='priceless'><img id='pricelessImg' name='pricelessImg' border='0' src='__IMAGEPATH__/Priceless/Priceless1.jpg' width='700' height='402' /></div>)
			"""), 1),
			(datetime(2007,4,3), 'John Newby Print Unveiled', MapLinks( """
			<p>
			<a target='photo' href='/JohnNewby/JohnNewbyPrint.jpg'><img align='left' src='/JohnNewby/JohnNewbyPrint_Small.jpg' width='200' height='157' border='0'></a>
			We made a lot of sales of the John Newby print at the unveiling
			after Hamilton Place.  Now that you've seen what a great work of
			art it is! Click on the image to see a closeup, then
			link:(#johnNewby,click here to order yours!)
			And congratulations to the lucky winner of the right to
			purchase limited edition print #1, Lynn Allaster!
			</p>
			<br clear='all'>
			"""), 0),
			(datetime(2007,4,1), 'Early Bird Pricing Extended Two Weeks!', MapLinks( """
			<p>
			To allow everyone time to soak in the magic of Hamilton Place
			we've extended the early bird offer two weeks to April
			15<sup>th</sup>.
			Orders have been coming in and we're filling up fast - don't
			be left outside listening to everyone else have a great time!
			link:(#tickets,Click here to get your order form now!)
			</p>
			"""), 1),
			(datetime(2007,3,27), 'Facebook has Alumni', MapLinks( """
			<p>
			Facebook is a social networking website, in the same genre as
			MySpace, Orkut, Friendster, Yahoo Groups, Google Groups, etc.
			Some band alumni have set up a BTTB group in it where they share
			band experiences, photos, and whatnot.  Check it out, it's a lot
			of fun, and can be highly addictive!
			link:(http://www.facebook.com/group.php?gid=2218469082,Click here to see the group) (you need a free Facebook account to see it of course).
			</p>
			"""), 0),
			(datetime(2007,3,26), 'Newsletter 3 Available', MapLinks( """
			<p>
			The third Alumni newsletter is now available.
			download:(__NEWSLETTERPATH__/Vol1No3.pdf,Click here to download the PDF file.)
			</p>
			"""), 1),
			(datetime(2007,3,25), 'A Tip of the Fuzzy Hat..', MapLinks( """
			<p>
			To link:(#sponsors, all of our sponsors) who are helping us to
			make the anniversary reunion weekend great! Contact us at
			send:(info@bttbalumni.ca) if you or someone you know would like
			to chip in as well - every little bit helps!
			</p>
			"""), 1),
			(datetime(2007,3,23), 'New Marching Music!', MapLinks( """
			<p>
			Due to popular demand the piece "Raindrops" by Burt Bacharach as
			arranged by Eric Ford has been added to the alumni parade order.
			If you've already registered just go to
			link:(#register, your profile page) and download the new music
			(look down in the 60<sup>th</sup> Anniversary Celebration area for
			the link).
			We even have a download:(/SheetMusic/Percussion.pdf, bells part) for
			this one!
			</p>
			"""), 1),
			(datetime(2007,3,23), 'Memorials', MapLinks( """
			<p>
			Sad to say in an organization of our size and history there
			are those who have passed away after leaving their mark with us.
			We remember those with a
			link:(#memorials, special memorial page).
			If you would like to have any of your old friends remembered email
			their name, years of service, and instrument to us at
			send:(info@bttbalumni.ca).
			</p>
			"""), 0),
			(datetime(2007,3,23), 'Meet the Committee', MapLinks( """
			<p>
			Wonder who's behind the scenes for the alumni group and the
			60<sup>th</sup> Anniversary Celebration? Now available is
			some information on
			link:(#bios, the committee members and their responsibilities).
			If you would like to help out on any of the subcommittees
			feel free to contact the person listed in charge of the
			area you're interested in!
			</p>
			"""), 0),
			(datetime(2007,3,23), 'Boosters Website Now Live', MapLinks( """
			<p>
			After a complete revamping the BTTB Boosters Inc. have a brand
			new website. Those interested in the golf tournament might want to
			check it out and register for their spots - there is only a
			limited number since they're using a shotgun start
			link:(http://teentourboosters.com/).
			</p>
			"""), 1),
			(datetime(2007,3,9), 'Newsletter Archive', MapLinks( """
			<p>
			Missed a newsletter? We've added the
			link:(#newsletters, Newsletter Archives) to the alumni menu
			so that you can always go back and look at the old ones.
			</p>
			"""), 1),
			(datetime(2007,3,9), 'Wallace B. Wallace', MapLinks( """
			<p>
			Check out our
			link:(#wallaceb, latest Wallace B. Wallace) winner information.
			Lots of recent ones, but maybe you more experienced alumni can
			dredge up the old memories and help fill in the earlier years.
			</p>
			"""), 0),
			(datetime(2007,2,28), 'Parade Music', MapLinks( """
			<p>
			Courtesy of Sir Bill we now have versions of 
			<br>
			download:(__AUDIOPATH__/StrikeUpTheBand.mp3, Strike Up The Band)
			and
			download:(__AUDIOPATH__/TheThunderer.mp3, The Thunderer)
			as rendered by the 2004 BTTB. (I don't have to tell you to click
			on them to hear the songs do I? &lt;grin&gt;)
			</p>
			"""), 1),
			(datetime(2007,2,28), 'Post Article on John Newby Print', MapLinks( """
			<a target='photo' href='__IMAGEPATH__/PostArticle_20070223.jpg'><img src='__IMAGEPATH__/PostArticle_20070223_Small.jpg' width='100' height='88' border='0'></a>
			"""), 0),
			(datetime(2007,2,28), 'Order Tickets Now!', MapLinks( """
			<p>
			Plan out your weekend now and get your package booked. It's
			vitally important that we get an accurate count of people
			attending for ordering materials, food, and of course
			entertainment of both the liquid and musical variety. We're
			shooting for 1,000 people for the Saturday night Homecoming!
			link:(#tickets,Click here to see all of the details.)
			</p>
			"""), 1),
			(datetime(2007,2,24), 'More Publicity from CHUM/FM', MapLinks( """
			<p>
			CHUM-FM's Roger Ashby and Marilyn Denis gave the band a great plug
			Feb.22 just after 9:00AM -- and Roger immediately received emails
			from two past band members.  He directed them to the web site.
			Roger said that he'll do something similar this Sunday morning,
			Feb.25, on his "Sunday Morning Oldies Show", which airs on 1050
			CHUM from 9 to Noon.
			<br>
			download:(__AUDIOPATH__/ChumFM.mp3, Click here to download the MP3 file of that clip from his show)
			</p>
			"""),1),
			(datetime(2007,2,19), 'Newsletter Now Available', MapLinks( """
			<p>
			The second Alumni newsletter is now available.
			download:(__NEWSLETTERPATH__/Vol1No2.pdf,Click here to download the PDF file.)
			</p>
			"""), 1),
			(datetime(2007,2,18), 'Hamilton Place Tickets Now Available', """
			<p>
			The Burlington Teen Tour Band's annual Hamilton Place concert will
			be on Sunday April 1 at 3pm.  The 60th Anniversary Concert will
			feature the talents of the current band, plus some special events
			relating to the 60<sup>th</sup> Anniversary. 
			</p>
			<p>
			Tickets for the Hamilton Place concert are on sale now.  They can
			be purchased in the lobby of the Music Centre from 1:00 to 3:30.
			Tickets are $15.00 each, $10.00 for youth under 16 and seniors 65+.
			Sales are on a first come first served basis and can be paid for by
			cash or cheques payable to the Burlington Teen Tour Band Boosters
			Inc.  Sales will continue at all BTTB practices until March 28th.
			</p>
			""", 1),
			(datetime(2007,2,18), 'Concert Rehearsal Dates Set', """
			<p>
			Sir Bill Hughes has set two rehearsal dates for those who have
			indicated an interest in playing in the concert, and who live near
			enough to attend in the weeks prior.<ul>
			<li>Friday May 25, 7 p.m. - 8:30 p.m.</li>
			<li>Friday June 1, 7 p.m. - 8:30 p.m.</li>
			</ul>
			To quote Sir Bill, <i>"Rehearsals should be followed with a time
			of social interaction at a suitable venue."</i>
			</p>
			""", 1),
			(datetime(2007,2,12), 'Early Reunion', MapLinks( """
			<table width='95%' style='border: 9px ridge #ff4444;' cellspacing='5' cellpadding='5'>
			<tr><td>
			<a target='photo' href='__IMAGEPATH__/EarlyReunion.jpg'>
			<img src='__IMAGEPATH__/EarlyReunion_small.jpg' align='top' width='272' height='181'></a>
			</td><td>
			Hi There Everyone!
			Sending a picture of a small group from the 67-76 years!!
			We (the group) are excited about the Reunion and decided
			to have a get together prior to the "Big" event, 
			and on Feb 11th met for a brunch in Ingersoll,On at
			The Elmhurst Inn. We had a fantastic time and are looking
			to do again in May, along with finding more of our fellow
			band mates that would like to join us. We are quite
			surprised that more of our Era seem to missing,
			we know you are out there!! So I will leave the names
			of this photo vacant,some of you will know who we
			are. Please sign up on the "BTTB" site and contact
			us, as all the email address's are there for you to contact
			us. It's been great emailing some of you so far and look
			forward to hearing from more of you.
			Cheers, til June!!! -- <i>Lee-Anne Richardson</i>
			</td></tr></table>
			"""), 0 ),
			(datetime(2007,2,4), 'Old information now hidden', MapLinks( """
			<p>
			Now that there is a lot of information to sift through with more
			being added every day the old information is now hidden by
			default. You can still view it though - look for a link at the
			bottom of the lists to view everything.
			</p>
			"""),1 ),
			(datetime(2007,2,4), 'New Pages - Music, Drum Majors, and Wallace B.', MapLinks( """
			<table>
			<tr><th valign='bottom'>
			link:(#tunes, <img src='__IMAGEPATH__/musicClip.png' width='100' height='125' border='0'><br>Hear the Band)
			</th><th valign='bottom'>
			link:(#drumMajors, <img src='__INSTRUMENTPATH__/DrumMajor.png' width='100' height='100' border='0'><br>Drum Majors)
			</th><th valign='bottom'>
			link:(#photos, <img src='__PHOTOPATH__/MarchingThroughTime_Small.jpg' width='100' height='61' border='0'><br>Some Photos)
			</th><th valign='bottom'>
			link:(#wallaceb, <img src='__IMAGEPATH__/WallaceBWallace.png' width='100' height='125' border='0'><br>Wallace B. Wallace Awards)
			</th><th valign='bottom'>
			<a target='photo' href='__IMAGEPATH__/PostArticle_112206.jpg'><img src='__IMAGEPATH__/PostArticle_112206_Small.jpg' width='100' height='112' border='0'><br>Reunion Announcement in<br>Burlington Post
			</th>
			</tr></table>
			"""), 0 ),
			(datetime(2007,2,4), 'Congratulations from Michael Buble', MapLinks( """
			<p>
			Michael Buble recently did an interview for CHUM-FM where he was
			talking about his band's trombone player, Josh Brown, who is a
			former Teen Tour Band member.<br>
			download:(__AUDIOPATH__/MichaelBuble_EQ.mp3, Click here to download the MP3 file of that clip from the interview)
			</p>
			"""), 0 ),
			(datetime(2007,1,22), 'Memories Galore', MapLinks( """
			<p>
			You can now add as many memories as you want, filter out the
			memories you see by year range, and edit the memories
			you've already submitted. Just go to the
			link:(#memories, memory list page).
			</p>
			"""), 0 ),
			(datetime(2007,1,14), 'John Newby Print Preorders', MapLinks( """
			<p>
			You can now download an order form and
			link:(#johnNewby, preorder a John Newby print). If you're ordering
			a limited edition print check to see if your old band uniform or
			hat number is available - you can request it!
			</p>
			"""), 1 ),
			(datetime(2007,1,11), 'Parade Music Available', MapLinks( """
			<p>
			In the menu at the left the link:(#parade, 60<sup>th</sup> Parade)
			is now available for signup. Pick your part, register for the
			parade, and download your music, all in one easy step!
			</p>
			"""), 1 ),
			(datetime(2007,1,8), 'Looking for Alumni!', """
			<p>
			Know anyone else from the band that has not yet registered?
			Help us make this the best celebration ever by spreading the word,
			and don't forget that the fun doesn't end after the celebration.
			The alumni would like to stay in touch for other great events.
			</p>
			<p>
			<a href="mailto:myBandFriend?subject='BTTB Alumni Celebration'&body='The BTTB is having its 60th anniversary celebration. Check out the great events! http://www.bttbalumni.ca'">Click here to send this website to someone else!</a>
			</p>
			""", 0),
			(datetime(2007,1,8), 'Wanted: Volunteers', MapLinks("""
			<p>
			Volunteers will be needed to have a successful Anniversary
			Celebration. Please contact us at
			send:(info@bttbalumni.ca,info@bttbalumni.ca) and let us know how
			you'd like to help.
			</p>
			"""), 1),
			(datetime(2007,1,1), 'Login Added', MapLinks( """
			<p>
			You can now log on to the website to give you access to your
			profile information. Your FIRST LAST name is your login (e.g. <i>Rob
			Bennett</i>) and your default password is blank. Change it by
			editing your profile information.
			</p>
			<p>
			In addition the memories you've been sharing are now available to
			look at. Later on you'll be able to add more, for those who had
			trouble thinking of just one favourite. Other upcoming features of
			the website are in the menus - look for the <b>Coming Soon</b>
			notice on them.
			</p>
			"""), 0),
			(datetime(2006,12,20), 'Music MIA', MapLinks( """
			<p>
			We're looking for some missing marching music parts. If you have any of
			these send:(info@bttbalumni.ca,let us know) and we'll make
			arrangements to get a scanned copy.<br>
			<b>Thunderer</b>: <i>Euphonium (Bass Clef)</i><br>
			<b>Strike Up The Band</b>: <i>Baritone (Treble Clef), Clarinet 3</i><br>
			<b>The Hustle</b>: <i>Trombone 2, Trombone 3, FHorn, Clarinet 3, Baritone
			(Treble Clef)</i><br>
			<b>All of the above</b>: <i>Percussion, Bells</i>
			</p>
			"""), 1),
			(datetime(2006,10,30), 'Tournament of Roses Alumni', MapLinks( """
			<p>
			The Tournament of Roses Parade has a call out for alumni to register in
			with them. If you were in any of the BTTB's appearances there
			link:(http://www.tournamentofroses.com/aboutus/alumni.asp,click here)
			to go to their website to register.
			</p>
			"""), 0),
			(datetime(2006,10,22), 'Concert Music', MapLinks( """
			<p>
			link:(http://www3.sympatico.ca/daskipper/bill.htm,Sir William Hughes), current
			link:(http://teentourband.org/staff.htm,musical director of the BTTB)
			will be directing the concert band at the alumni
			celebrations and in preparation he wants to hear from you.
			link:(#musicSurvey,Click here to take a survey)
			on your favourite music from band days.
			</p>
			"""), 1),
			(datetime(2006,12,10), 'Volunteers', """
			<p>
			Meeting at the music center, 2:00pm, for those who might like to volunteer
			to help with events. Come see the latest memorobilia generously donated
			and displayed throughout the building, meet the Steering and Organizing
			Committees, and find out how you can help!
			</p>
			""", 1),
			(datetime(2006,12,01), 'Tournament of Roses', """
			<p>
			The BTTB has been once again accepted to take part in the 2008 Tournament
			of Roses Parade in Pasadena, California.
			<br>
			<b>Congratulations guys!!!!</b>
			<br>
			Early talk of an alumni contingency
			going down to cheer from the parade route has already started.
			</p>
			""", 0),
			(datetime(2006,11,20), 'Coming soon...', MapLinks( """
			<p>
			Watch this spot for further developments in the areas of:
			<li>Event packages for some or all of the exciting 60<sup>th</sup>
			anniversary celebrations</li>
			<li>Information on a special piece of art commissioned to be
			developed by famous childhood memories artist
			link:(http://john-newby.com/,John Newby)
			(himself an alumnus of the <i>Boys and Girls Band</i>) featuring the band.</li>
			<li>A special 'Memory Lane' section for old pictures, stories,
			audio clips, and memorabilia.</li>
			<li>... and more, no need to be shy in making a request - this website
			and celebration is all for <b>YOU!!!</b></li>
			</p>
			"""), 1)
			]
		news.sort( lambda x,y: cmp(y[0], x[0]) )
		#===================================================================
		self.createTable()
		for when, title, article, status in news:
			self.alumni.processQuery( """
			INSERT INTO news (title, description, appeared, status)
			VALUES ('%s', '%s', '%s', '%d')
			""" % (DbFormat(title).replace("\n","\\n"), DbFormat(article).replace("\n","\\n"), when.strftime('%Y-%m-%d %H:%M:%S'), status) )

# ==================================================================

import unittest
class testNews(unittest.TestCase):
	def testDump(self):
		news = bttbNews()
		news.createTable()
		news.populateNews()
	
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
