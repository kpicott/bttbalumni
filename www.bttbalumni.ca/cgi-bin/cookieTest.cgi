#!env python

import os
import Cookie

print 'Content-Type: text/html'

# Get old count.
count = 0
if os.environ.has_key('HTTP_COOKIE'):
    cookie = Cookie.SimpleCookie()
    cookie.load(os.environ['HTTP_COOKIE'])
    if cookie.has_key('count'):
        count = int(cookie['count'].value)

# Create new count.
count += 1
cookie = Cookie.SimpleCookie()
cookie['count'] = count

# Display.
print cookie
print
print '<html><body>'
print '<p>Visits: %d</p>' % count
print '</body></html>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
