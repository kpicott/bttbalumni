"""
Page that presents a few sample buttons for testing a direct upload of a
multi-item Paypal cart.
"""

import datetime
from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbGolf2017']

class bttbGolf2017(bttbPage):
    def __init__(self):
        bttbPage.__init__(self)

        # Compute the early-bird discounts
        GOLF_CUTOFF = datetime.datetime( 2017, 4, 15 )
        NOW = datetime.datetime.now()
        self.early = 'Early'
        if NOW > GOLF_CUTOFF:
            self_early = ''
    
    def title(self): return 'BTTB 70th Anniversary Reunion Golf Tournament'

    def scripts(self):
        script_list = ['__JAVASCRIPTPATH__/bttbGolf2017.js', '__CSSPATH__/bttbGolf2017.css']
        script_list.append( '''JS:
            var cart_value = "42";
            function testValues()
            {
                alert( 'Value is ' + cart_value );
            }''' )
        return script_list

    def content(self):
        """
        Return a string with the content for this web page.
        """
        html = MapLinks( """
<div class='splash box_shadow'>
<img src='/Images70th/golf.jpg' width='800' height='300' usemap='#golfMap'/>
<map name='golfMap'>
    <area shape='rect' coords='14,244,247,263' target='IndianWells' alt='Indian Wells' href='http://www.indianwellsgolfclub.ca/'>
</map>
</div>

<div class='instructions box_shadow'>
    <div class='item'>Golf and Dinner, $185 now or $200 after April 15<sup>th</sup><ul>
        <li>Swag bag with mystery gifts</li>
        <li>Shotgun start, 1:00pm. Come early and socialize over lunch!</li>
        <li>Prizes galore</li>
    </ul>
    </div>
    <div class='image'><img src='/Images70th/WinACar.png'></div>
    <div class='price'><img src='/Images70th/Golf%sPrice.png'></div>
</div>

<div class='instructions box_shadow'>
    <div class='item'>Just the Dinner, $60<ul>
        <li>Come early and join the heckler's in the clubhouse!</li>
        <li>Food will be served at 6:30pm</li>
    </ul>
    </div>
    <div class='image'>
    </div>
    <div class='price'><img src='/Images70th/GolfDinnerPrice.png'></div>
</div>

<div class='instructions box_shadow'>
    <div class='item'>Sponsor your very own hole<ul>
        <li>We'll provide a cool sign to post on the tee blocks.</li>
        <li>Contact send:(golf@bttbalumni.ca) if you want more information before committing.</li>
    </ul>
    </div>
    <div class='image'></div>
    <div class='price'><img src='/Images70th/GolfSponsorPrice.png'></div>
</tr>
</table>
</div>

<div class='order_buttons'>
    <button class='order_button shadow_button' onclick='add_golfer();'>Add a Golfer</button>
    <button class='order_button shadow_button' onclick='add_diner();'>Add only Dinner</button>
    <button class='order_button shadow_button' onclick='sponsor_hole();'>Sponsor a Hole</button>
</div>
""" % self.early )
        return html

# ==================================================================

import unittest
class testGolf2017(unittest.TestCase):
    def testDump(self):
        testPage = bttbGolf2017()
        print testPage.content()
    
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
