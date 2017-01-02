#!env python

print 'Content-type: text/html\n'

import os
import cgi

print '<body>'
print '<h1>CGI</h1>'
params = cgi.parse()
for param in params:
	print '<b>',param,'</b>=',params[param],'<br>'
print '<h1>Environment</h1>'
for env in os.environ:
	print '<b>',env,'</b>=',os.environ[env],'<br>'
print '</body>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
