"""
Page that presents a few sample buttons for testing a direct upload of a
multi-item Paypal cart.
"""
import datetime
from bttbPage import bttbPage
from bttbConfig import MapLinks
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
    
    #----------------------------------------
    def title(self): return 'BTTB 70th Anniversary Reunion Golf Tournament'

    #----------------------------------------
    def content(self):
        """
        Return a string with the content for this web page.
        """
        html = """
<script type='text/javascript' src='/js/bttbGolf2017.js'></script>
<link rel='stylesheet' href='/css/bttbGolf2017.css'>
<script> %s </script>""" % self.requestor_as_member_info()

        html += MapLinks( """
<div class='splash box_shadow'>
<img src='/Images70th/golf.jpg' width='800' height='300' usemap='#golfMap'/>
<map name='golfMap'>
    <area shape='rect' coords='10,211,229,236' target='IndianWells' alt='Indian Wells' href='http://www.indianwellsgolfclub.ca/'>
    <area shape='rect' coords='160,266,652,291' alt='Mail us' href='mailto:golf@bttbalumni.ca'>
</map>
</div>

<div class='golf_item box_shadow'>
    <div class='golf_info'>All you can eat BBQ Lunch, $20<ul>
        <li>Hamburger, Hot Dog, Sausage, Salads</li>
        <li>BBQ opens at 11:30am</li>
        <li>Come early and socialize! Cash bar available</li>
    </ul>
    </div>
    <div class='golf_image'></div>
    <div class='golf_price'><img src='/Images70th/GolfLunchPrice.png'></div>
    <div class='golf_button_container'><button class='shadow_button' onclick='add_lunch();'>Add a Lunch</button></div>
</div>

<div class='golf_item box_shadow'>
    <div class='golf_info'>Golf and Dinner, $185 now or $200 after April 15<sup>th</sup><ul>
        <li>Create your own foursome</li>
        <li>Registration opens at noon - Shotgun start, 1:00pm</li>
        <li>Cash bar</li>
    </ul>
    </div>
    <div class='golf_image'><img src='/Images70th/WinACar.png'></div>
    <div class='golf_price'><img src='/Images70th/Golf%sPrice.png'></div>
    <div class='golf_button_container'><button class='shadow_button' onclick='add_golfer();'>Add a Golfer</button></div>
</div>

<div class='golf_item box_shadow'>
    <div class='golf_info'>Just the Dinner, $60<ul>
        <li>Buffet opens at 7:00pm</li>
        <li>Limited to 36 people so sign up early</li>
        <li>Come early and watch the golfers finishing</li>
    </ul>
    </div>
    <div class='golf_image'></div>
    <div class='golf_price'><img src='/Images70th/GolfDinnerPrice.png'></div>
    <div class='golf_button_container'><button class='shadow_button' onclick='add_diner();'>Add only Dinner</button></div>
</div>

<div class='golf_item box_shadow'>
    <div class='golf_info'>Sponsor your very own hole, $250<ul>
        <li>We'll provide a cool sign to post on the tee blocks.</li>
        <li>Contact send:(golf@bttbalumni.ca) for more information, or buy now</li>
        <li>Sponsor as many as you want</li>
    </ul>
    </div>
    <div class='golf_image'></div>
    <div class='golf_price'><img src='/Images70th/GolfSponsorPrice.png'></div>
    <div class='golf_button_container'><button class='shadow_button' onclick='sponsor_hole();'>Sponsor a Hole</button></div>
</tr>
</table>
</div>
<div id='cart_contents' class='box_shadow'>
<h2>Your cart is currently empty - add items above.</h2>
</div>
""" % self.early )
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbGolf2017()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
