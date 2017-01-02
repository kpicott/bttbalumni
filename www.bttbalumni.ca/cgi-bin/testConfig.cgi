#!env python

print 'Content-type: text/html\n'

import os
from bttbConfig import *

print '<head><title>BTTB Site Configuration Information</title></head>'

print '<body>'

print '<b>HomeHref</b> = ', HomeHref(), '<br>'
print '<b>DataPath</b> = ', DataPath(), '<br>'
print '<b>CgiHref</b> = ', CgiHref(), '<br>'

print '</body>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
