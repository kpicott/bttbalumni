"""
Page that shows the current list of memories, in order by approximate date.
"""

import re
from bttbPage import bttbPage
from bttbConfig import *
from datetime import datetime,timedelta
__all__ = ['bttbArticles']

# Helper class to manage article information
class bttbArticle:
	def __init__(self, id):
		self.id = id
		self.scan = ""
		self.thumbnail = ""
		self.date = datetime.now()
		self.publication = ""
		self.headline = ""

def _sortByArticleDate(x,y):	return cmp(x.date, y.date)
class bttbArticles(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)
		fileName = MapLinks( '__ROOTPATH__/Articles/Articles.txt' )
		fd = open( fileName )
		self.articleList = []
		latestArticle = None
		re_date = re.compile('(....)-(..)-(..)')
		try:
			step = 0
			for line in fd:
				# Ignore comment lines
				if line[0] == '#':
					continue
				if step == 0:
					latestArticle = bttbArticle(line)
					step = 1
				elif step == 1:
					latestArticle.scan = line
					step = 2
				elif step == 2:
					latestArticle.thumbnail = line
					step = 3
				elif step == 3:
					matches = re_date.findall( line )
					yy = int(matches[0][0])
					mm = int(matches[0][1])
					dd = int(matches[0][2])
					latestArticle.date = datetime(yy, mm, dd)
					step = 4
				elif step == 4:
					latestArticle.publication = line
					step = 5
				elif step == 5:
					latestArticle.headline = line
					self.articleList.append( latestArticle )
					step = 0
		finally:
			fd.close()
		self.articleList.sort( _sortByArticleDate )

	
	def title(self): return 'BTTB Alumni In The Press'

	def content(self):
		"""
		Return a string with the content for this web page.
		"""

		html = """
		<p>
		Click on any article's thumbnail to see an expanded version of it.
		</p>
		"""
		html += "<table width='90%'><tr>"
		col = 0
		for article in self.articleList:
			if col == 3:
				html += '</tr><tr>'
				col = 0
			html += '<th>'
			img = MapLinks( '__ARTICLEPATH__/' + article.scan )
			thumb = MapLinks( '__ARTICLEPATH__/' + article.thumbnail )
			html += '<a target="Articles" href="%s"><img border="0" src="%s"></a>' % (img, thumb)
			html += '<div class="date">'
			html += article.date.strftime('%Y-%m-%d')
			html += "&nbsp;&nbsp;(&nbsp;"
			html += article.publication
			html += ')</div>'
			html += '<h2>'
			html += article.headline
			html += '</h2>'
			html += '</th>'
			col = col + 1
		html += '</tr></table>'
		return html

# ==================================================================

import unittest
class testArticles(unittest.TestCase):
	def testDump(self):
		articlePage = bttbArticles()
		print articlePage.content()
	
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
