"""
Web page showing the 70th anniversary reunion store
"""
import datetime
from bttbConfig import *
from bttbPage import bttbPage
__all__ = ['bttbStore2018']

#======================================================================
NO_SHIRT_SELECTED = "-- Select shirt size --"
SHIRT_OPTIONS = [ [ "XXX", NO_SHIRT_SELECTED]
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
    html = '<select id="%s">' % selector_name
    html += '<option value="">---Select Shirt Size---</option>'
    for shirt_info in SHIRT_OPTIONS:
        html += '<option value="%s">%s</option>' % ( shirt_info[0], shirt_info[1] )
    html += '</select>'
    return html

#======================================================================
ITEM_DESCRIPTIONS = { "allin"      : "All Events"
                    , "saturday"   : "Saturday Night Social Event"
                    , "parade"     : "Saturday Morning Parade"
                    , "hat"        : "70th Anniversary Hat"
                    , "shirt"      : "70th Anniversary Golf Shirt"
                    , "golf"       : "Early-Bird Entrance Into the 70th Anniversary Golf Tournament"
                    , "golfHole"   : "Hole Sponsorship for the 70th Anniversary Golf Tournament"
                    , "golfDinner" : "70th Anniverary Golf Tournament Dinner Only"
                    }

#======================================================================
# Compute the early-bird discounts
DISCOUNT_ALL = 20
DISCOUNT_GOLF = 50
ALLIN_CUTOFF = datetime.datetime( 2017, 3, 15 )
GOLF_CUTOFF = datetime.datetime( 2017, 4, 15 )
NOW = datetime.datetime.now()
if NOW > ALLIN_CUTOFF:
    DISCOUNT_ALL = 0
if NOW > GOLF_CUTOFF:
    DISCOUNT_GOLF = 0

#======================================================================
STORE_ITEMS = {  "allin"      : [150 - DISCOUNT_ALL,  ITEM_DESCRIPTIONS["allin"]]
               , "saturday"   : [80,                  ITEM_DESCRIPTIONS["saturday"]]
               , "parade"     : [70,                  ITEM_DESCRIPTIONS["parade"]]
               , "hat"        : [15,                  ITEM_DESCRIPTIONS["hat"]]
               , "golf"       : [175 - DISCOUNT_GOLF, ITEM_DESCRIPTIONS["golf"]]
               , "golfHole"   : [200,                 ITEM_DESCRIPTIONS["golfHole"]]
               , "golfDinner" : [50,                  ITEM_DESCRIPTIONS["golfDinner"]]
               }
for shirt_info in SHIRT_OPTIONS:
    STORE_ITEMS[shirt_info[0]] = [30, shirt_info[1] + " %s" % ITEM_DESCRIPTIONS["shirt"]]
    STORE_ITEMS[shirt_info[0]+'_p'] = [0, shirt_info[1] + " %s (for Parade)" % ITEM_DESCRIPTIONS["shirt"]]
    STORE_ITEMS[shirt_info[0]+'_a'] = [0, shirt_info[1] + " %s (for All Events)" % ITEM_DESCRIPTIONS["shirt"]]

#======================================================================
def add_tax(value):
    '''
    Add HST to a value, rounding it up.
    :param value: Cost to which to add tax.
    :return: value + HST, rounding to the nearest cent
    '''
    return int( value * 113 ) / 100

#======================================================================
def add_link(item):
    '''
    :param item: ID for item to add to cart
    :return: HTML that comprises a button to add the item in the row to the cart
    '''
    return '''<button onclick="add_cart_item('%s');">Add To Cart</button>''' % item

#======================================================================
#
# Page load is a simple template operation with generic pathnames replaced by
# their configured equivalents.
#
class bttbStore2018(bttbPage):
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
    def paypal_member_info(self):
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
    def paypal_preamble(self, shirt_id, item_info):
        '''
        :param shirt_id: Unique ID to identify the shirt selector in the page
        :param item_info: Description of the item owning the form, None if no validation is required
        :return: HTML for the form initialization and hidden fields appearing in all PayPal links
        '''
        html  = '<form target="_self" method="post"'
        if item_info is not None:
            html += ' onsubmit="return validate_shirt_size(\'%s\', \'%s\');"' % (item_info, shirt_id)
        html += ' action="https://www.sandbox.paypal.com/cgi-bin/webscr">'
        html += '<input type="hidden" name="cmd" value="_s-xclick">'
        html += '<input type="hidden" name="currency_code" value="CAD">'
        html += '<input type="hidden" name="shipping" value="0">'
        html += '<input type="hidden" name="shopping_url" value="http://bttbalumni.ca/#store2018?payment=paypal">'
        html += self.paypal_member_info()
        return html

    #======================================================================
    def paypal_view_cart_button(self):
        '''
        :return: HTML that comprises a button to view the Paypal cart
        '''
        return '''%s
    <input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----
    ">
    <input type="image" src="https://www.sandbox.paypal.com/en_US/i/btn/btn_viewcart_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
    <img alt="" border="0" src="https://www.sandbox.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1">
    </form>''' % self.paypal_preamble(None, None)

    #======================================================================
    def paypal_add_to_cart(self,item,shirt_id):
        '''
        :param item: Name of item for which to generate the add_to_cart button.
        :param shirt_id: Unique ID to identify the shirt selector in the page
        :return: HTML code for a Paypal add_to_cart button for the given item.
        '''
        # Button information for each item type. The elements of the list
        # are HOSTED_BUTTON_ID, IS_SHIRT_SIZE_REQUIRED, EARLYBIRD DISCOUNT
        hosted_buttons = { 'allin'      : ['5CKSXSSXFDPNJ', True,  DISCOUNT_ALL]
                         , 'parade'     : ['J6H7RE9FU94AN', True,  0]
                         , 'saturday'   : ['PDSLC8SDDDJWC', False, 0]
                         , 'hat'        : ['4YUPAHHC9HSJS', False, 0]
                         , 'shirt'      : ['5PXQC8FHC4RVQ', True,  0]
                         , 'golf'       : ['CX35JJNMJWZ7S', False, DISCOUNT_GOLF]
                         , 'golfHole'   : ['28E57ZTCZN4YA', False, 0]
                         , 'golfDinner' : ['ZG623EN63C7QN', False, 0]
                         }
        shirt_html = '''
    <table>
    <tr><td><input type="hidden" name="on0" value="Shirt Size"><select id="%%s" name="os0">
    <option value="%s" selected="selected">%s</option>
    <option value="Women's Extra Small">Women's Extra Small</option>
    <option value="Women's Small">Women's Small</option>
    <option value="Women's Medium">Women's Medium</option>
    <option value="Women's Large">Women's Large</option>
    <option value="Women's XL">Women's XL</option>
    <option value="Women's 2XL">Women's 2XL</option>
    <option value="Men's Small">Men's Small </option>
    <option value="Men's Medium">Men's Medium </option>
    <option value="Men's Large">Men's Large </option>
    <option value="Men's XL">Men's XL </option>
    <option value="Men's 2XL">Men's 2XL </option>
    <option value="Men's 3XL">Men's 3XL </option>
    <option value="Men's 4XL">Men's 4XL </option>
    <option value="Men's 5XL">Men's 5XL </option>
    <option value="Men's 6XL">Men's 6XL </option>
    </select> </td></tr>
    </table>
        ''' % (NO_SHIRT_SELECTED, NO_SHIRT_SELECTED )
        if item not in hosted_buttons:
            return 'No Info for %s' % item

        hosted_button_id = hosted_buttons[item][0]

        form  = self.paypal_preamble( shirt_id, ITEM_DESCRIPTIONS[item] )
        form += '<input type="hidden" name="hosted_button_id" value="%s">' % hosted_button_id
        if hosted_buttons[item][1]:
            form += shirt_html % shirt_id
        if hosted_buttons[item][2] > 0:
            form += '<input type="hidden" name="discount_amount" value="%s">' % hosted_buttons[item][2]
        form += '<input align="center" type="image" src="https://www.sandbox.paypal.com/en_US/i/btn/btn_cart_SM.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">'
        form += '<img alt="" border="0" src="https://www.sandbox.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1">'
        form += '</form>'
        return form

    #----------------------------------------
    def paypal_logo(self):
        '''
        :param available: If true then we are accepting PayPal payments,
                          otherwise add a "coming soon" disclaimer.
        :return: HTML code to display a PayPal information button
        '''
        soon = '<div id="comingSoon">Coming Soon...</div>'
        logo = '''<!-- PayPal Logo --><table border="0" cellpadding="10" cellspacing="0" align="center"><tr><td>%s</td></tr><tr><td align="center"><a href="https://www.paypal.com/webapps/mpp/paypal-popup" title="How PayPal Works" onclick="javascript:window.open('https://www.paypal.com/webapps/mpp/paypal-popup','WIPaypal','toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=1060, height=700'); return false;"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/AM_mc_vs_dc_ae.jpg" border="0" alt="PayPal Acceptance Mark"></a></td></tr></table><!-- PayPal Logo -->''' % soon
        return '<div id="paypal-info">' + logo + '<p></p></div>'

    #----------------------------------------
    def choose_content(self):
        ''':return: HTML that comprises the launch page to choose payment method.'''
        
        return MapLinks('''<h2>Welcome to the Store, Please Choose Desired Payment Method</h2>
<table cellpadding='10' width='800'><tr>
<th>link:(/#store2018?payment=paypal,<img src='https://www.paypalobjects.com/webstatic/mktg/logo/AM_mc_vs_dc_ae.jpg' border='0' alt='PayPal Acceptance Mark'>)
<br>Pay Online with Paypal</th>
<th>link:(/#store2018?payment=cheque,<img src='/Images70th/PayByCheque.jpg' border='0' alt='Mail a Cheque'>)
<br>Mail a cheque with an order form.</th>
</tr></table>''')

    #----------------------------------------
    def paypal_content(self):
        ''':return: HTML that comprises the page frame content for PayPal paying.'''
        row_data = [ ['merch_inclusive', self.paypal_add_to_cart('allin', 'add1')]
                   , ['merch_parade',    self.paypal_add_to_cart('parade', 'add2')]
                   , ['merch_saturday',  self.paypal_add_to_cart('saturday', 'add3')]
                   , ['merch_hat',       self.paypal_add_to_cart('hat', 'add4')]
                   , ['merch_shirt',     self.paypal_add_to_cart('shirt', 'add5')]
                   , ['golf',            self.paypal_add_to_cart('golf', 'add6')]
                   , ['golfHole',        self.paypal_add_to_cart('golfHole', 'add7')]
                   , ['golfDinner',      self.paypal_add_to_cart('golfDinner', 'add8')]
                   ]

        html = '<H2>Store (Paypal)</H2>\n'
        html += '<table id="paypal_store">\n'
        html += '<tr><th>Item + Description</th><th>%s</th></tr>\n' % self.paypal_view_cart_button()
        for row in row_data:
            html += '<tr>\n'
            html += '<td align="right"><img height="90" src="/Images70th/%s.jpg"></td>\n' % row[0]
            html += '<td>%s</td>\n' % row[1]
            html += '</tr>\n'
        html += '</table>\n'

        return html

    #----------------------------------------
    def cheque_content(self):
        ''':return: HTML that comprises the page frame content for paying by cheque.'''
        row_data = [ ['merch_inclusive', shirt_options('allin'),  add_link('allin')]
                   , ['merch_parade',    shirt_options('parade'), add_link('parade')]
                   , ['merch_saturday',  '',                      add_link('saturday')]
                   , ['merch_hat',       '',                      add_link('hat')]
                   , ['merch_shirt',     shirt_options('shirt'),  add_link('shirt')]
                   , ['golf',            '',                      add_link('golf')]
                   , ['golfHole',        '',                      add_link('golfHole')]
                   , ['golfDinner',      '',                      add_link('golfDinner')]
                   ]

        total_cost = 0

        # Cart element to be populated by Javascript. Unfortunately due to the
        # page loading sequence I can't just load automatically here, it has
        # to be done manually through a button.
        html = '<div id="cart-contents"><button onclick=\'rebuild_cart()\'>Show Cart</button></div>\n'

        member_name = ''
        member_email = ''
        member_phone = ''
        if self.requestor is not None:
            member_name = self.requestor.fullName()
            member_email = self.requestor.email
            member_phone = self.requestor.phone
        html += '<input type="hidden" id="member_name" value="%s"/>' % member_name
        html += '<input type="hidden" id="member_email" value="%s"/>' % member_email
        html += '<input type="hidden" id="member_phone" value="%s"/>' % member_phone

        html += '<p>&nbsp;</p>\n'

        html += '<H2>Store (Paying by cheque)</H2>\n'
        html += '<table width="800" id="store">\n'
        html += '<tr><th>Item + Description</th><th>Options</th><th></th></tr>\n'
        for row in row_data:
            html += '<tr>\n'
            html += '<td><img height="90" src="/Images70th/%s.jpg"></td>\n' % row[0]
            html += '<td>%s</td>\n' % row[1]
            html += '<td>%s</td>\n' % row[2]
            html += '</tr>\n'
        html += '</table>\n'

        return html

    #----------------------------------------
    def content(self):
        ''':return: HTML that comprises the page frame content.'''
        payment = self.param('payment')

        if payment == 'paypal':
            return self.paypal_content()
        elif payment == 'cheque':
            return self.cheque_content()
        else:
            return self.choose_content()

# ==================================================================

import unittest
class testStore2018(unittest.TestCase):
    '''Simple test class to dump the contents of this page'''
    def testDump(self):
        '''Test method to show the contents of this page's frame'''
        Store2018Page = bttbStore2018()
        print Store2018Page.paypal_content()

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
