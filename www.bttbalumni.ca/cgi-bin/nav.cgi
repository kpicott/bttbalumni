#!/usr/bin/python
"""
Old master file, just redirects to the new one

Historical links like this:

        http://www.bttbalumni.ca/cgi-bin/nav.cgi#page&u=1&v=2&...

are redirected here:

        http://www.bttbalumni.ca/&u=1&v=2&...#page
"""
#----------------------------------------------------------------------
import os
import cgi
import cgitb
cgitb.enable()
from urlparse import urlparse

print '''Content-type: text/html

<head>
<script type='text/javascript' src='/js/jquery-3.1.1.min.js'></script>
<script>
    // Split the hash value and the search fields
    var pieces = location.hash.split( '?' );
    var hash = pieces[0];
    var search = ''
    if( pieces.length > 1 )
    {
        search = '?' + pieces[1];
    }

    // Remove any existing user ID tag
    hash = hash.replace( /:[0-9]+/, '' );

    // Load the new location
    var new_location = 'http://bttbalumni.ca/' + search + hash;
    location.href = new_location;
</script>
</head>
<body></body>
'''
    
# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================

