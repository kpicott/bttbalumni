"""
URL page to return test data.
"""

from bttbPage import bttbPage
from bttbDB import bttbDB

__all__ = ['bttbTestDB']

class bttbTestDB(bttbPage):
    '''Class that generates the test page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    def content(self):
        ''':return: a string with the content for this web page.'''
        database = bttbDB()
        database.Initialize()
        database.turn_debug_on()

        results,description = database.process_query( 'SHOW TABLES' )
        info = '<h1>SHOW TABLES Results</h1><p>%s</p>' % str(results)
        info += '<h1>SHOW TABLES Description</h1><p>%s</p>' % str(description)

        for table_info in results:
            table = table_info[0]
            info += '<h1>CREATE %s</h1>' % table
            results,_ = database.process_query( 'SHOW CREATE TABLE %s' % table )
            if len(results) > 0:
                info += '<p>%s</p>' % str(results[0][1])

        results,description = database.process_query( 'DESCRIBE playlists' )
        info += '<h1>Results</h1><p>%s</p>' % str(results)
        info += '<h1>Description</h1><p>%s</p>' % str(description)

        database.Finalize()
        return info

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
