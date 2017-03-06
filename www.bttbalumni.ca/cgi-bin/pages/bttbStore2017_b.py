"""
Page that shows the store for items up for sale at the 2017 reunion
"""

from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbStore2017_b']

class bttbStore2017_b(bttbPage):
    def __init__(self):
        bttbPage.__init__(self)
    
    def title(self): return 'BTTB Alumni 70th Anniversary Reunion Store'

    def scripts(self): return ['__CSSPATH__/bttbStore2017_b.css'
                              ,'__CSSPATH__/bttbEffects.css'
                              ]

    def content(self):
        """
        Return a string with the content for this web page.
        """
        html = MapLinks( """
<div id="store">
    <div id="dates" class="box_shadow"><img src="/Images70th/Store/Dates.jpg"</div>
    <div id="golf" class="box_shadow"><img src="/Images70th/Store/GolfLink.jpg"</div>
    <div id="title" class="box_shadow"><img src="/Images70th/Store/Title.jpg"</div>
    <div id="allin" class="item box_shadow">
        <div class="image"><img src="/Images70th/Store/merch_inclusive.jpg"</div>
        <div class="info">info</div>
        <div class="cost">cost</div>
        <div class="buttons">
            <div class="name">name</div>
            <div class="shirt_size">shirt</div>
            <div class="add">add</div>
        </div>
    </div>
    <div id="saturday" class="item box_shadow">
        <div class="image"><img src="/Images70th/Store/merch_saturday.jpg"</div>
        <div class="info">info</div>
        <div class="cost">cost</div>
        <div class="buttons">
            <div class="name">name</div>
            <div class="shirt_size">shirt</div>
            <div class="add">add</div>
        </div>
    </div>
    <div id="parade" class="item box_shadow">
        <div class="image"><img src="/Images70th/Store/merch_parade.jpg"</div>
        <div class="info">info</div>
        <div class="cost">cost</div>
        <div class="buttons">
            <div class="name">name</div>
            <div class="shirt_size">shirt</div>
            <div class="add">add</div>
        </div>
    </div>
    <div id="shirt_size" class="item box_shadow">
        <div class="image"><img src="/Images70th/Store/merch_shirt.jpg"</div>
        <div class="info">info</div>
        <div class="cost">cost</div>
        <div class="buttons">
            <div class="name">name</div>
            <div class="shirt_size">shirt</div>
            <div class="add">add</div>
        </div>
    </div>
    <div id="hat" class="item box_shadow">
        <div class="image"><img src="/Images70th/Store/merch_hat.jpg"</div>
        <div class="info">info</div>
        <div class="cost">cost</div>
        <div class="buttons">
            <div class="name">name</div>
            <div class="shirt_size">shirt</div>
            <div class="add">add</div>
        </div>
    </div>
    <div id="cart" class="box_shadow">cart</div>
</div>
        """)

        return html

# ==================================================================

import unittest
class testStore2017_b(unittest.TestCase):
    def testDump(self):
        store2017Page = bttbStore2017_b()
        print store2017Page.content()
    
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
