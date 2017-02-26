"""
Web page showing the 70th anniversary reunion store
"""
import datetime
from bttbConfig import *
from bttbPage import bttbPage
__all__ = ['bttbStore2017']

#======================================================================
# Compute the early-bird discounts
DISCOUNT_ALL = 20
DISCOUNT_GOLF = 10
ALLIN_CUTOFF = datetime.datetime( 2017, 4, 15 )
GOLF_CUTOFF = datetime.datetime( 2017, 4, 15 )
NOW = datetime.datetime.now()
if NOW > ALLIN_CUTOFF:
    DISCOUNT_ALL = 0
if NOW > GOLF_CUTOFF:
    DISCOUNT_GOLF = 0

#======================================================================
#
# Constants representing the type of stores we can generate
#
CHEQUE_STORE = 'cheque'
PAYPAL_STORE = 'paypal'
CART_IMAGES = {
                'addtocart' :
                {
                    CHEQUE_STORE : '/Images70th/AddToCart_BTTB.png'
                ,   PAYPAL_STORE : '/Images70th/AddToCart_PayPal.png'
                }
              , 'viewcart' :
                {
                    CHEQUE_STORE : '/Images70th/ViewCart_BTTB.png'
                ,   PAYPAL_STORE : '/Images70th/ViewCart_PayPal.png'
                }
              }

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
#
# Info driving the store element items. Each item is very specifically
# positioned using CSS class types. The information on which to use, as
# well as text and pricing information for each item is contained here.
#
# Use standard size key names for layout, and for avoiding typos.
#
KEY_DESC = 'description'
KEY_COST = 'cost'
KEY_SIZE = 'image_size'
KEY_SHRT = 'has_shirt'
KEY_BTNS = 'button_class'
KEY_CART = 'cart_align'
KEY_HOST = 'paypal_key'
KEY_DSCT = 'paypal_key'
ITEM_INFO = { 'allin'      : { KEY_DESC : 'All Events'
                             , KEY_COST : 150
                             , KEY_SIZE : 'large'
                             , KEY_SHRT : True
                             , KEY_DSCT : DISCOUNT_ALL
                             , KEY_BTNS : 'large_buttons'
                             , KEY_HOST : '5CKSXSSXFDPNJ'
                             }
            , 'saturday'   : { KEY_DESC : 'Saturday Night Social Event'
                             , KEY_COST : 80
                             , KEY_SIZE : 'medium'
                             , KEY_SHRT : False
                             , KEY_DSCT : 0.0
                             , KEY_BTNS : 'medium_buttons'
                             , KEY_HOST : 'PDSLC8SDDDJWC'
                             }
            , 'parade'     : { KEY_DESC : 'Saturday Morning Parade'
                             , KEY_COST : 70
                             , KEY_SIZE : 'medium'
                             , KEY_SHRT : True
                             , KEY_DSCT : 0.0
                             , KEY_BTNS : 'medium_buttons'
                             , KEY_HOST : '5CKSXSSXFDPNJ'   #'J6H7RE9FU94AN'
                             }
            , 'hat'        : { KEY_DESC : '70th Anniversary Hat'
                             , KEY_COST : 15
                             , KEY_SIZE : 'small'
                             , KEY_SHRT : False
                             , KEY_DSCT : 0.0
                             , KEY_BTNS : 'small_buttons'
                             , KEY_HOST : '4YUPAHHC9HSJS'
                             }
            , 'shirt'      : { KEY_DESC : '70th Anniversary Golf Shirt'
                             , KEY_COST : 30
                             , KEY_SIZE : 'small'
                             , KEY_SHRT : True
                             , KEY_DSCT : 0.0
                             , KEY_BTNS : 'small_buttons'
                             , KEY_HOST : '5PXQC8FHC4RVQ'
                             }
            , 'golf'       : { KEY_DESC : 'Early-Bird Entrance Into the 70th Anniversary Golf Tournament'
                             , KEY_COST : 185
                             , KEY_SIZE : 'medium'
                             , KEY_SHRT : False
                             , KEY_DSCT : DISCOUNT_GOLF
                             , KEY_BTNS : 'medium_buttons_2'
                             , KEY_HOST : 'CX35JJNMJWZ7S'
                             }
            , 'golfHole'   : { KEY_DESC : 'Hole Sponsorship for the 70th Anniversary Golf Tournament'
                             , KEY_COST : 250
                             , KEY_SIZE : 'medium'
                             , KEY_SHRT : False
                             , KEY_DSCT : 0.0
                             , KEY_BTNS : 'medium_buttons'
                             , KEY_HOST : '28E57ZTCZN4YA'
                             }
            , 'golfDinner' : { KEY_DESC : '70th Anniverary Golf Tournament Dinner Only'
                             , KEY_COST : 60
                             , KEY_SIZE : 'medium'
                             , KEY_SHRT : False
                             , KEY_DSCT : 0.0
                             , KEY_BTNS : 'medium_buttons'
                             , KEY_HOST : 'ZG623EN63C7QN'
                             }
            }

#======================================================================
#
# Page load is a simple template operation with generic pathnames replaced by
# their configured equivalents.
#
class bttbStore2017(bttbPage):
    def __init__(self):
        '''Initialize the page information'''
        bttbPage.__init__(self)

    #----------------------------------------
    def title(self):
        ''':return: Title for this page'''
        return 'BTTB Alumni Association 70th Anniversary Reunion Store'

    #----------------------------------------
    def scripts(self):
        ''':return: List of Javascript and CSS scripts to be included in this page'''
        return ['__CSSPATH__/bttbStore2017.css'
               ,'__JAVASCRIPTPATH__/bttbStore2017.js'
               ]

    #----------------------------------------
    def member_info(self):
        '''
        :return: HTML comprising hidden buttons populated with known member info
        The hidden buttons must correspond to PayPal's naming scheme so they are
        first_name, last_name, night_phone_a, night_phone_b, night_phone_c, and email
        '''
        if self.requestor is None:
            return ''

        first_name = self.requestor.first
        last_name = self.requestor.last
        email = self.requestor.email
        phone = PhoneParts( self.requestor.phone )

        html  = '<input type="hidden" id="first_name" value="%s"/>' % first_name
        html += '<input type="hidden" id="last_name" value="%s"/>' % last_name
        html += '<input type="hidden" id="email" value="%s"/>' % email
        html += '<input type="hidden" id="night_phone_a" value="%s"/>' % phone[0]
        html += '<input type="hidden" id="night_phone_b" value="%s"/>' % phone[1]
        html += '<input type="hidden" id="night_phone_c" value="%s"/>' % phone[2]
        return html

    #----------------------------------------
    def paypal_preamble(self, shirt_id, description):
        '''
        :param shirt_id: Unique ID to identify the shirt selector in the page
        :param description: Description of the item owning the form, None if no validation is required
        :return: HTML for the form initialization and hidden fields appearing in all PayPal links
        '''
        html  = '<form target="_self" method="post"'
        if description is not None:
            html += ' onsubmit="return validate_shirt_size(\'%s\', \'%s\');"' % (description, shirt_id)
        html += ' action="https://www.sandbox.paypal.com/cgi-bin/webscr">'
        html += '<input type="hidden" name="cmd" value="_s-xclick">'
        html += '<input type="hidden" name="currency_code" value="CAD">'
        html += '<input type="hidden" name="shipping" value="0">'
        html += '<input type="hidden" name="cancel_return" value="http://bttbalumni.ca/#store2017?payment=paypal">'
        html += '<input type="hidden" name="cbt" value="Return to the BTTB 70th Anniversary Reunion Store">'
        html += '<input type="hidden" name="return" value="http://bttbalumni.ca/#thanks2017">'
        html += '<input type="hidden" name="image_url" value="http://bttbalumni.ca/Images2017/SiteLogo.png">'
        html += '<input type="hidden" name="shopping_url" value="http://bttbalumni.ca/#store2017?payment=paypal">'
        html += self.member_info()
        return html

    #----------------------------------------
    @staticmethod
    def paypal_postamble():
        '''
        :return: HTML for the form completion in Paypal
        '''
        return '</form>'

    #----------------------------------------
    def paypal_view_cart_button(self):
        '''
        :return: HTML that comprises a button to view the Paypal cart
        '''
        return '''%s
    <input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----
    ">
    <input type="image" src="%s" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
%s''' % (self.paypal_preamble(None, None), CART_IMAGES['viewcart'][PAYPAL_STORE], self.paypal_postamble())

    #----------------------------------------
    def generate_add_to_cart(self, item_type, store_type):
        '''
        :param item_type: Type of item to add to the cart
        :param store_type: Type of store being built, CHEQUE_STORE or PAYPAL_STORE
        :return: HTML implementing a button control to add the current element to the cart
        '''
        html = ''
        item_info = ITEM_INFO[item_type]

        # No shirt option means the button floats to the center
        add_to_cart_class = 'addtocart'
        if not item_info[KEY_SHRT]:
            add_to_cart_class += '_center'
        elif item_type == 'shirt':
            add_to_cart_class += '_center_2'

        if store_type == PAYPAL_STORE:
            html += '<input type="hidden" name="hosted_button_id" value="%s">' % item_info[KEY_HOST]
            if item_info[KEY_DSCT] > 0:
                html += '<input type="hidden" name="discount_amount" value="%s">' % item_info[KEY_DSCT]
            html += '<input class="%s" align="center" type="image"' % add_to_cart_class
            html += ' src="%s" border="0" name="submit" alt="Add To Cart">' % CART_IMAGES['addtocart'][PAYPAL_STORE]
            # html += '<img alt="" border="0" src="https://www.sandbox.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1">'
        else:
            html += '<a href="javascript:add_cart_item(\'%s\');">' % item_type
            html += '<img alt="Add To Cart" class="%s"' % add_to_cart_class
            html += ' border="0" src="%s"></a>' % CART_IMAGES['addtocart'][store_type]

        return html

    #----------------------------------------
    def generate_shirt_options(self, shirt_id, store_type):
        '''
        :param shirt_id: Unique ID for the shirt selection list HTML element
        :param store_type: Type of store being built, CHEQUE_STORE or PAYPAL_STORE
        :return: HTML implementing a dropdown to select a shirt
        '''
        html = ''
        if store_type == PAYPAL_STORE:
            # For Paypal the value is the shirt description, needed for the cart
            value_list = [[shirt_info[1], shirt_info[1]] for shirt_info in SHIRT_OPTIONS]
            html += '<input type="hidden" name="on0" value="Shirt Size">'
        else:
            # Otherwise the value is a short id, used for populating the internal cart
            value_list = [[shirt_info[0], shirt_info[1]] for shirt_info in SHIRT_OPTIONS]

        # Paypal required name
        html += '<select id="%s" class="dropdown" name="os0">\n' % shirt_id

        for value in value_list:
            html += '<option value="%s">%s</option>\n' % (value[0], value[1])

        html += '</select>\n'

        return html

    #----------------------------------------
    def show_all_store_items(self, store_type):
        '''
        :param store_type: Type of store being built, CHEQUE_STORE or PAYPAL_STORE
        :return: HTML implementing all store elements
        '''
        html = ''

        html += '<div class="container">'

        # The internal store will show the cart contents at the top. Create
        # a bootstrap location for it, to be populated by the rebuild_cart
        # Javascript function
        html += '<div class="cart_container">\n'
        if store_type == CHEQUE_STORE:
            html += '  <div id="cart_contents">\n'
            html += '    <input type="image" src="%s" border="0" ' % CART_IMAGES['viewcart'][store_type]
            html += '     onclick="rebuild_cart();" alt="View Cart">'
            html += '  </div>\n'
        else:
            html += self.paypal_view_cart_button()
        html += '</div>\n'

        html += '<div class="store_container">'

        for (store_item,item_info) in ITEM_INFO.iteritems():
            # All store items are enclosed with an outlined box with a shadow
            html += '  <div class="box_shadow %s_item">\n' % store_item
            html += '    <div class="fix_top %s_image" id="%s">\n' % (item_info[KEY_SIZE], store_item)
            html += '      <div class="%s">\n' % item_info[KEY_BTNS]

            if store_type == PAYPAL_STORE:
                html += self.paypal_preamble( '%s_shirt' % store_item, item_info[KEY_DESC] )

            if item_info[KEY_SHRT]:
                html += self.generate_shirt_options( '%s_shirt' % store_item, store_type )

            html += self.generate_add_to_cart( store_item, store_type )

            if store_type == PAYPAL_STORE:
                html += self.paypal_postamble()

            html += '      </div>\n'
            html += '    </div>\n'
            html += '  </div>\n'

        html += '</div>\n'

        html += '</div>\n'

        # Paypal has to add the member information in multiple locations but
        # the regular store can't, so handle that here.
        if store_type == CHEQUE_STORE:
            html += self.member_info()

        return html

    #----------------------------------------
    def choose_content(self):
        ''':return: HTML that comprises the launch page to choose payment method.'''
        
        return MapLinks('''<h2>Welcome to the Store, Please Choose Desired Payment Method</h2>
<table cellpadding='10' width='800'><tr>
<th>link:(/#store2017?payment=paypal,<img src='https://www.paypalobjects.com/webstatic/mktg/logo/AM_mc_vs_dc_ae.jpg' border='0' alt='PayPal Acceptance Mark'>)
<br>Pay Online with Paypal</th>
<th>link:(/#store2017?payment=cheque,<img src='/Images70th/PayByCheque.jpg' border='0' alt='Mail a Cheque'>)
<br>Mail a cheque with an order form.</th>
</tr></table>''')

    #----------------------------------------
    def content(self):
        ''':return: HTML that comprises the page frame content.'''
        payment = self.param('payment')

        if payment in [PAYPAL_STORE, CHEQUE_STORE]:
            return self.show_all_store_items( payment )
        else:
            return self.choose_content()

# ==================================================================

import unittest
class testStore2017(unittest.TestCase):
    '''Simple test class to dump the contents of this page'''
    def testDump(self):
        '''Test method to show the contents of this page's frame'''
        Store2017Page = bttbStore2017()
        print Store2017Page.show_all_store_items( PAYPAL_STORE )
        print Store2017Page.show_all_store_items( CHEQUE_STORE )
        print Store2017Page.content()

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
