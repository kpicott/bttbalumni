"""
Page that presents a few sample buttons for testing a direct upload of a
multi-item Paypal cart.
"""
import datetime
from bttbPage import bttbPage
from bttbConfig import MapLinks, PhoneParts
__all__ = ['bttbStore2017_c']

#======================================================================
#
# Compute the early-bird discounts
#
EARLYBIRD_CUTOFF = datetime.datetime( 2017, 4, 15 )
NOW = datetime.datetime.now()
EARLY = 'Early'
if NOW > EARLYBIRD_CUTOFF:
    EARLY = ''
    
#======================================================================
#
# List of available shirt options
#
NO_SHIRT_SELECTED = "-- Select Shirt Size --"
SHIRT_OPTIONS = [ [ "",    NO_SHIRT_SELECTED]
                , [ "WXS", "Women's Extra Small"]
                , [ "WS",  "Women's Small"]
                , [ "WM",  "Women's Medium"]
                , [ "WL",  "Women's Large"]
                , [ "WXL", "Women's XL"]
                , [ "W2X", "Women's 2XL"]
                , [ "MS",  "Men's Small"]
                , [ "MM",  "Men's Medium"]
                , [ "ML",  "Men's Large"]
                , [ "MXL", "Men's XL"]
                , [ "M2X", "Men's 2XL"]
                , [ "M3X", "Men's 3XL"]
                , [ "M4X", "Men's 4XL"]
                , [ "M5X", "Men's 5XL"]
                , [ "M6X", "Men's 6XL"]
                ]

def shirt_options(selector_name):
    '''
    :param selector_name: Name of selector dropdown, for Javascript processing.
    :return: the HTML that implements the shirt dropdown selection
    '''
    html = '<select class="dropdown" id="%s">' % selector_name
    html += '<option value="%s" selected="selected">%s</option>' % (NO_SHIRT_SELECTED, NO_SHIRT_SELECTED)
    for shirt_info in SHIRT_OPTIONS:
        html += '<option value="%s">%s</option>' % ( shirt_info[0], shirt_info[1] )
    html += '</select>'
    return html

#======================================================================
def title_html():
    ''':return: HTML implementing the first section with the title information'''
    return MapLinks( '''
<div class='splash box_shadow'>
<img src='/Images70th/golf.jpg' width='800' height='300' usemap='#golfMap'/>
<map name='golfMap'>
    <area shape='rect' coords='10,211,229,236' target='IndianWells' alt='Indian Wells' href='http://www.indianwellsgolfclub.ca/'>
    <area shape='rect' coords='160,266,652,291' alt='Mail us' href='mailto:golf@bttbalumni.ca'>
</map></div>''')

#======================================================================
#
# Data driving the individual cart items
#
CART_DATA = {
                'allin' :    { 'image'        : '/Images70th/Store/merch_inclusive.png'
                             , 'size'         : '_big'
                             , 'info'         : '''<b>All-Inclusive VIP Ticket</b><ul>
                                                   <li>70<sup>th</sup> Anniversary Reunion Shirt</li>
                                                   <li>70<sup>th</sup> Anniversary Reunion Hat</li>
                                                   <li>Marching spot in the SOMF with the Alumni Band</li>
                                                   <li>Saturday Night Social (dinner + entertainment)</li>
                                                   <li>Early-Bird pricing until April 15th!</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceAllIn%sA.png' % EARLY
                             , 'onclick'      : 'add_lunch();'
                             , 'name'         : 'Name of participant'
                             , 'size_select'  : shirt_options( 'allin_size' )
                             }
            ,   'saturday' : { 'image'        : '/Images70th/WinACar.png'
                             , 'size'         : ''
                             , 'info'         : '''<b>Saturday Night Social</b><ul>
                                                   <li>Dinner</li>
                                                   <li>Entertainment (low-key)</li>
                                                   <li>Cash bar</li>
                                                   <li>Non-Alumni Welcome</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceSaturday.png'
                             , 'onclick'      : 'add_golfer();'
                             , 'name'         : 'Name of participant'
                             , 'size_select'  : ''
                             }
            ,   'parade' :   { 'image'        : '/Images70th/WinACar.png'
                             , 'size'         : ''
                             , 'info'         : '''<b>Sound of Music Parade, Alumni Band</b><ul>
                                                   <li>Includes Hat and Shirt as uniform</li>
                                                   <li>Over 300 in the band at the 60<sup>th</sup>!</li>
                                                   <li>Parade music from multiple eras</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceParade.png'
                             , 'onclick'      : 'add_diner();'
                             , 'name'         : 'Name of participant'
                             , 'size_select'  : shirt_options( 'parade_size' )
                             }
            ,   'shirt' :    { 'image'        : '/Images70th/WinACar.png'
                             , 'size'         : ''
                             , 'info'         : '''<b>70<sup>th</sup> Anniversary Reunion Shirt</b><ul>
                                                   <li>High quality golf shirt with special reunion patch</li>
                                                   <li>Wear it as the parade uniform, or just for fun</li>
                                                   <li>Limited edition - you must pre-order!</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceShirt.png'
                             , 'onclick'      : 'sponsor_hole();'
                             , 'name'         : None
                             , 'size_select'  : shirt_options( 'shirt_size' )
                             }
            ,   'hat'   :    { 'image'        : '/Images70th/WinACar.png'
                             , 'size'         : ''
                             , 'info'         : '''<b>70<sup>th</sup> Anniversary Reunion Hat</b><ul>
                                                   <li>Navy Blue with special reunion logo</li>
                                                   <li>Part of the alumni band parade uniform</li>
                                                   <li>Limited edition - you must pre-order!</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceHat.png'
                             , 'onclick'      : 'sponsor_hole();'
                             , 'name'         : None
                             , 'size_select'  : ''
                             }
            }

#======================================================================
def item_html( item_name ):
    ''':return: HTML implementing the given cart item'''
    if item_name not in CART_DATA:
        return ''

    cart_item = CART_DATA[item_name]
    html = "<div class='item%s box_shadow'>" % cart_item['size']
    html += "<div class='image'><img src='%s'></div>" % cart_item['image']
    html += "<div class='info'>%s</div>" % cart_item['info']
    html += "<div class='price'><img src='/Images70th/Store/%s'></div>" % cart_item['cost_image']
    html += "<div class='button_container'><table>"
    html += "<tr><td><button class='shadow_button' onclick='%s'>Add To Cart</button></td></tr>" % cart_item['onclick']
    if cart_item['name'] is not None:
        html += "<tr><td><input type='text' name='%s_name' placeholder='%s' width='32'></td></tr>" % (item_name, cart_item['name'] )
    html += "<tr><td>%s</td></tr>" % cart_item['size_select']
    html += "</table></div></div>"
    return html

#======================================================================
def cart_html():
    ''':return: HTML implement the cart contents (starts blank)'''
    return '''<div id='cart_contents' class='box_shadow'>
              <h2>Your cart is currently empty - add items above.</h2></div>'''

#======================================================================
#
class bttbStore2017_c(bttbPage):
    '''Class that generates the Store page for the 70th Anniversary Reunion'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    #----------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB 70th Anniversary Reunion Events'

    #----------------------------------------
    def scripts(self):
        ''':return: The list of scripts to load in this page'''
        script_list = ['__JAVASCRIPTPATH__/bttbStore2017_c.js'
                      , '__CSSPATH__/bttbEffects.css'
                      , '__CSSPATH__/bttbStore2017_c.css'
                      ]

        first_name = ''
        last_name = ''
        email = ''
        phone = ['','','']
        if self.requestor is not None:
            first_name = self.requestor.first
            last_name = self.requestor.last
            email = self.requestor.email
            phone = PhoneParts( self.requestor.phone )

        script_list.append( '''JS: var member_info = { 'first_name' : '%s'
               , 'last_name'     : '%s'
               , 'email'         : '%s'
               , 'night_phone_a' : '%s'
               , 'night_phone_b' : '%s'
               , 'night_phone_c' : '%s'
               };''' % (first_name, last_name, email, phone[0], phone[1], phone[2]) )

        return script_list

    #----------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''
        html = title_html()
        html += item_html( 'allin' )
        html += item_html( 'saturday' )
        html += item_html( 'parade' )
        html += item_html( 'shirt' )
        html += item_html( 'hat' )
        html += cart_html()

        return html

# ==================================================================

import unittest
class TestGolf2017(unittest.TestCase):
    '''Unit tests for this module'''
    def testDump(self):
        '''Simple test to dump the page content'''
        testPage = bttbStore2017_c()
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
