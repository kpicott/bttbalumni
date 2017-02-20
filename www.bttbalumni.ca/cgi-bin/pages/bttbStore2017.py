"""
Web page showing the 70th anniversary reunion store
"""

from bttbConfig import *
from bttbPage import bttbPage
__all__ = ['bttbStore2017']

#======================================================================
SHIRT_OPTIONS = [ [ "WXS", "Women's Extra Small"]
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
STORE_ITEMS = { "allin"       : [130, "All Events"]
               , "saturday"   : [80, "Saturday Night Social Event"]
               , "parade"     : [70, "Saturday Morning Parade"]
               , "hat"        : [15, "70th Anniversary Hat"]
               , "golf"       : [125, "Early-Bird Entrance Into the 70th Anniversary Golf Tournament"]
               , "golfHole"   : [200, "Hole Sponsorship for the 70th Anniversary Golf Tournament"]
               , "golfDinner" : [50, "70th Anniverary Golf Tournament Dinner Only"]
               }
for shirt_info in SHIRT_OPTIONS:
    STORE_ITEMS[shirt_info[0]] = [30, shirt_info[1] + " 70th Anniversary Shirt"]
    STORE_ITEMS[shirt_info[0]+'_p'] = [0, shirt_info[1] + " 70th Anniversary Shirt (for Parade)"]
    STORE_ITEMS[shirt_info[0]+'_a'] = [0, shirt_info[1] + " 70th Anniversary Shirt (for All Events)"]

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
    def paypal_content(self):
        ''':return: HTML that comprises the page frame content for PayPal paying.'''
        return ''

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

        html = self.paypal_logo()

        # Cart element to be populated by Javascript. Unfortunately due to the
        # page loading sequence I can't just load automatically here, it has
        # to be done manually through a button.
        html += '<div id="cart-contents"><button onclick=\'rebuild_cart()\'>Show Cart</button></div>\n'

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
        paypal = self.param('paypal') is not None

        if paypal:
            return self.paypal_content()
        else:
            return self.cheque_content()

# ==================================================================

import unittest
class testStore2017(unittest.TestCase):
    '''Simple test class to dump the contents of this page'''
    def testDump(self):
        '''Test method to show the contents of this page's frame'''
        store2017Page = bttbStore2017()
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
