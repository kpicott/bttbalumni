#!env python
"""
Show pictures in groups with thumbnails.
"""

import os
import os.path
import re
from bttbConfig import *

def displayCelebrationPictures():
	"""
	Scan through the image directories and display pics from the celebration
	"""
	category1 = {}
	category2 = {}
	category2['Homecoming_Andrea'] = 'The Homecoming was amazing - heartfelt speeches and hard-earned camaraderie every where you turned'
	category2['Parade_Photographer'] = 'The Sound of Music parade is always great, topped off with our own alumni band'
	category2['Parade_Kate'] = 'Candid shots of the parade'
	category2['NewbyDonation'] = 'Donation to Music Centre of a John Newby Print accepted by Booster President Gary Bourke, Ron and Lana'
	category1['CLKeedy'] = 'CL Keedy, President of the 2007 Tournament of Roses'
	category1['Displays'] = 'Lots of band memorabilia and displays were set up for perusal'
	category1['Entertainment_Friday'] = 'The Top Hat Marching Orchestra dropped in for a few numbers and a scholarship presentation'
	category1['Groups_Friday'] = 'Alumni from all eras, right from the 40s through to the 2000s were reconnecting'
	category1['Practice_Friday'] = 'The marching and parade music practice was not tooooo bad'

	html = ""
	re_thumb = re.compile("(.*)_Small.jpg")
	try:
		fullDirList = os.listdir(CelebrationPath())
		for dir in fullDirList:
			try:
				if category2[dir]:
					html += '<div class="newsTitle">'
					html += category2[dir]
					html += '<span class="newsDate">2007-06-16</span>'
					html += '</div>'
					html += '<div class="newsArticle">'
					html += '<table cellspacing="10">'
					col = 0
					subDirList = os.listdir(os.path.join(CelebrationPath(), dir))
					for file in subDirList:
						match = re_thumb.match(file)
						if match:
							if col == 4:
								col = 0
								html += '</tr>'
							if col == 0:
								html += '<tr>'
							col = col + 1
							html += MapLinks( """
							<td><a target='photo' href='__CELEBRATIONHREF__/%s/%s.jpg'>
							<img align='left' src='__CELEBRATIONHREF__/%s/%s_Small.jpg'
							width='150' border='0'></a></td>
							""" % (dir, match.group(1), dir, match.group(1)) )
					html += '</tr></table></div>'
			except:
				pass
		html += """<p>Do you remember the time...<i>from Gordon Cameron</i></p><p>
   The first night of the Homecoming Reunion was quite
the time. Not only did the Alumni Band play the four
song marching order (with some members not having
played since they left) but we marched (and
countermarched, although not while playing) around the
parking lot just like old times. We sounded really
good. It's like riding a bike, you never forget how to
march, dress, do roll offs and things like that. The
music comes easy too. It's all still living in your
fingers, you just need to relax and let them do all
the work.
</p><p>
   The social was very well attended with people from
all eras of the Band. Throughout the arena all you
heard were squeals from old friends that hadn't seen
each other in decades, and gales of laughter from
countless stories that all began ...Do you remember the
time...
</p><p>
   Saturday will be just as wonderful with the parade,
downtown performance, and the evening Homecoming
event. If you're not signed up and are still thinking
about whether or not so come out, definitely do it.
You won't regret it!
</p>"""
		for dir in fullDirList:
			try:
				if category1[dir]:
					html += '<div class="newsTitle">'
					html += category1[dir]
					html += '<span class="newsDate">2007-06-15</span>'
					html += '</div>'
					html += '<div class="newsArticle">'
					html += '<table cellspacing="10">'
					col = 0
					subDirList = os.listdir(os.path.join(CelebrationPath(), dir))
					for file in subDirList:
						match = re_thumb.match(file)
						if match:
							if col == 4:
								col = 0
								html += '</tr>'
							if col == 0:
								html += '<tr>'
							col = col + 1
							html += MapLinks( """
							<td><a target='photo' href='__CELEBRATIONHREF__/%s/%s.jpg'>
							<img align='left' src='__CELEBRATIONHREF__/%s/%s_Small.jpg'
							width='150' border='0'></a></td>
							""" % (dir, match.group(1), dir, match.group(1)) )
					html += '</tr></table></div>'
			except:
				pass
	except Exception, e:
		Error( 'Image files error', e )
	return html

if __name__ == '__main__':
	print displayCelebrationPictures()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
