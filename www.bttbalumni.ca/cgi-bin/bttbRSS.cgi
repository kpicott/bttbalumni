#!env python
#
# Dump out the BTTB Alumni news feed in RSS format
#
import cgi
from bttbAlumni import *
params = cgi.parse()
try:
	for p in params:
		if p == 'article':
			article = params[p][0]
	alumni = bttbAlumni()
	print """
<?xml version="1.0"?>
<rss version="2.0">
<channel>

<title>BTTB Alumni News</title>
<description>The ongoing news articles relating to the Burlington Teen Tour
Band Alumni group, hosted on the main website.</description>
<lastBuildDate>Jun 27 2007 18:07:00 EDT</lastBuildDate>
<webmaster>bttb@picott.ca</webmaster>
<managingEditor>info@bttbalumni.ca</managingEditor>
<copyright>Copyright 2007, BTTB Alumni</copyright>
<link>http://www.bttbalumni.ca</link>

<item>
<title>The Title Goes Here</title>
<description>The description goes here</description>
<pubDate>Jun 27 2007 18:07:00 EDT</pubDate>
<link>http://www.bttbalumni.ca/#article?id=1</link>
</item>

<item>
<title>Another Title Goes Here</title>
<description>Another description goes here</description>
<pubDate>Jun 27 2007 18:07:00 EDT</pubDate>
<link>http://www.bttbalumni.ca/#article?id=2</link>
</item>

</channel>
</rss>"""
except:
	pass

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
