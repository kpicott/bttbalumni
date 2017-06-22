"""
Page that presents a few sample buttons for testing a direct upload of a
multi-item Paypal cart.
"""
import datetime
from bttbPage import bttbPage
from bttbConfig import MapLinks
__all__ = ['bttbStore2017']

# Enable this when the online registration is disabled
ONLINE_REGISTRATION_CLOSED = '''<h2>Online registration is now closed but you can
still print an order form here to bring with you to registration on Friday or Saturday!
</h2>'''

#======================================================================
#
# Compute the early-bird discounts
#
EARLYBIRD_CUTOFF = datetime.datetime( 2017, 4, 16 )
NOW = datetime.datetime.now()
EARLY = 'Early'
if NOW > EARLYBIRD_CUTOFF:
    EARLY = ''

#======================================================================
#
# List of available shirt options
#
NO_SHIRT_SELECTED = "-- Select Shirt Size --"
SHIRT_OPTIONS = [ NO_SHIRT_SELECTED
                , "Women's Extra Small"
                , "Women's Small"
                , "Women's Medium"
                , "Women's Large"
                , "Women's XL"
                , "Women's 2XL"
                , "Men's Small"
                , "Men's Medium"
                , "Men's Large"
                , "Men's XL"
                , "Men's 2XL"
                , "Men's 3XL"
                , "Men's 4XL"
                , "Men's 5XL"
                ]

def shirt_options(selector_name):
    '''
    :param selector_name: Name of selector dropdown, for Javascript processing.
    :return: the HTML that implements the shirt dropdown selection
    '''
    html = '<select class="dropdown" id="%s">' % selector_name
    for shirt_info in SHIRT_OPTIONS:
        html += '<option value="%s">%s</option>' % ( shirt_info, shirt_info )
    html += '</select>'
    html += '''<br><a target="data" href="/Images70th/LadiesSizingChart.png"><b>W</b></a>
            &nbsp;<-Sizing->&nbsp;<a target="data" href="/Images70th/MensSizingChart.png"><b>M</b></a>
            '''
    return html

#======================================================================
def title_html():
    ''':return: HTML implementing the first section with the title information'''
    return MapLinks( '''
<div class='store-header'>
    send:(info@bttbalumni.ca,<div class='contact-link box_shadow'></div>)
    send:(golf@bttbalumni.ca,<div class='golf-link box_shadow'></div>)
    %s
    <div class='store-title box_shadow'></div>
</div>''' % ONLINE_REGISTRATION_CLOSED )

#======================================================================
#
# Data driving the individual cart items
#
CART_DATA = {
                'allin' :    { 'image'        : 'merch_inclusive.jpg'
                             , 'size'         : '_big'
                             , 'info'         : '''<b>All-Inclusive VIP Ticket</b><ul>
                                                   <li>70<sup>th</sup> Anniversary Reunion Shirt and Hat</li>
                                                   <li>Marching spot in the SOMF with the Alumni Band</li>
                                                   <li>Saturday Night Social (buffet + entertainment)</li>
                                                   <li>$125 Early-Bird until April 15th, $145 after!</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceAllIn%s.png' % EARLY
                             , 'onclick'      : 'add_all_inclusive();'
                             , 'name'         : 'Name of participant'
                             , 'size_select'  : shirt_options( 'allin_size' )
                             }
            ,   'saturday' : { 'image'        : 'merch_saturday.jpg'
                             , 'size'         : ''
                             , 'info'         : '''<b>Saturday Night Social</b><ul>
                                                   <li>Buffet dinner, Cash bar</li>
                                                   <li>Music and Entertainment</li>
                                                   <li>We call this the "Band Booster Special"</li>
                                                   <li>Guests Welcome</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceSaturday.png'
                             , 'onclick'      : 'add_saturday();'
                             , 'name'         : 'Name of participant'
                             , 'size_select'  : ''
                             }
            ,   'parade' :   { 'image'        : 'merch_parade.jpg'
                             , 'size'         : '_tall'
                             , 'info'         : '''<b>Sound of Music Parade, Alumni Band</b><ul>
                                                   <li>Includes Shirt as uniform</li>
                                                   <li>Over 300 in the band at the 60<sup>th</sup>!</li>
                                                   <li>Float seating available if you cannot march</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceParade.png'
                             , 'onclick'      : 'add_parade();'
                             , 'name'         : 'Name of participant'
                             , 'size_select'  : shirt_options( 'parade_size' )
                             }
            ,   'shirt' :    { 'image'        : 'merch_shirt.jpg'
                             , 'size'         : ''
                             , 'info'         : '''<b>70<sup>th</sup> Anniversary Reunion Shirt</b><ul>
                                                   <li>Stormtech Golf shirt with embroidered reunion patch</li>
                                                   <li>Select from a wide variety of sizes</li>
                                                   <li>Limited edition - you must pre-order!</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceShirt.png'
                             , 'onclick'      : 'add_shirt();'
                             , 'name'         : None
                             , 'size_select'  : shirt_options( 'shirt_size' )
                             }
            ,   'hat'   :    { 'image'        : 'merch_hat.jpg'
                             , 'size'         : ''
                             , 'info'         : '''<b>70<sup>th</sup> Anniversary Reunion Hat</b><ul>
                                                   <li>Navy Blue with embroidered reunion logo</li>
                                                   <li>One size fits all</li>
                                                   <li>Limited edition - you must pre-order!</li>
                                                   </ul>'''
                             , 'cost_image'   : 'PriceHat.png'
                             , 'onclick'      : 'add_hat();'
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

    if len(cart_item['size']) > 0:
        item_type = cart_item['size'][1:]
    else:
        item_type = "normal"

    html = "<div class='item %s-item box_shadow'>" % item_type

    html += "<div class='image'><img src='/Images70th/Store/%s'></div>" % cart_item['image']
    html += "<div class='info'>%s</div>" % cart_item['info']
    html += "<div class='price'><img src='/Images70th/Store/%s'></div>" % cart_item['cost_image']
    html += "<div class='button_container'><table>"
    html += "<tr><td><button class='shadow_button' onclick='%s'>Add To Cart</button></td></tr>" % cart_item['onclick']
    if cart_item['name'] is not None:
        html += "<tr><td><input type='text' id='%s_name'" % item_name
        html += " name='%s_name' placeholder='%s' width='32'></td></tr>" % (item_name, cart_item['name'] )
    html += "<tr><td>%s</td></tr>" % cart_item['size_select']
    html += "</table></div></div>"
    return html

#======================================================================
def cart_html():
    ''':return: HTML implement the cart contents (starts blank)'''
    return '''<div id='cart_contents' class='cart_contents box_shadow'>
              <h2>Your cart is currently empty - add items above.</h2></div>'''

#======================================================================
#
class bttbStore2017(bttbPage):
    '''Class that generates the Store page for the 70th Anniversary Reunion'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    #----------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB 70th Anniversary Reunion Events'

    #----------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''

        return MapLinks( """
<h1>Thanks For Everything!</h1>
<p>
The reunion was a great success and there was no swag left over to purchase.
If you have any great ideas for what you might like to see on the store in
the future (the 75<sup>th</sup> or even sooner) then send them to
send:(info@bttbalumni.ca)!
</p>
        """ )

        html = """
<script type='text/javascript' src='/js/bttbStore2017.js'></script>
<link rel='stylesheet' href='/css/bttbStore2017.css'>
<script> %s </script>""" % self.requestor_as_member_info()

        html += title_html()
        html += item_html( 'allin' )
        html += item_html( 'saturday' )
        html += item_html( 'parade' )
        html += item_html( 'shirt' )
        html += item_html( 'hat' )
        html += cart_html()

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbStore2017()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
