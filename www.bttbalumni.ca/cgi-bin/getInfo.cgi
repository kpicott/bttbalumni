#!/usr/bin/env python
"""
Simple script to dump the registration info in an Excel/Word-friendly
format for Committee members to do what they want with.
"""
from bttbAlumni import bttbAlumni
from bttbConfig import Error

print "Content-Type:application/octet-stream"
print "Content-Disposition:attachment; filename=bttbAlumniInfo.txt\n"

try:
    alumni = bttbAlumni()
except Exception,e:
    Error( 'Could not find alumni data', e)

print alumni.get_committee_text()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
