"""
Page that presents a few sample buttons for testing a direct upload of a
multi-item Paypal cart.
"""

from bttbPage import bttbPage
from bttbConfig import *
__all__ = ['bttbPaypalTest']

class bttbPaypalTest(bttbPage):
    def __init__(self):
        bttbPage.__init__(self)
    
    def title(self): return 'BTTB Alumni PaypalTest'

    def scripts(self): return [ '__JAVASCRIPTPATH__/bttbPaypalTest.js' ]

    def content(self):
        """
        Return a string with the content for this web page.
        """
        html = MapLinks( """
<ol>
<li>Test 1: Simple button with only minimal info <br>
<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="bttb-seller@picott.ca">
<input type="hidden" name="item_name" value="This is a ten dollar item">
<input type="hidden" name="currency_code" value="CAD">
<input type="hidden" name="amount" value="10.00">
<input type="image" src="http://www.paypal.com/en_US/i/btn/x-click-but01.gif" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">
</form>
</li>
<li>Test 2: Button with extended info <br>
<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_ext-enter">
<input type="hidden" name="redirect_cmd" value="_xclick">
<input type="hidden" name="business" value="bttb-seller@picott.ca">
<input type="hidden" name="item_name" value="This is a hundred dollar item">
<input type="hidden" name="currency_code" value="CAD">
<input type="hidden" name="amount" value="100.00">
<input type="image" src="http://www.paypal.com/en_US/i/btn/x-click-but01.gif" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">

<input type="hidden" name="email" value="">
<input type="hidden" name="first_name" value="Rich">
<input type="hidden" name="last_name" value="Texan">
<input type="hidden" name="address1" value="123 Oil Street">
<input type="hidden" name="address2" value="Barrel #4">
<input type="hidden" name="city" value="Edmonton">
<input type="hidden" name="state" value="AB">
<input type="hidden" name="country" value="Canada">
<input type="hidden" name="zip" value="O1L OI1">
<input type="hidden" name="night_phone_a" value="222">
<input type="hidden" name="night_phone_b" value="222">
<input type="hidden" name="night_phone_c" value="2222">
</form>
</li>
<li>Test 3: Button with return information <br>
<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_ext-enter">
<input type="hidden" name="redirect_cmd" value="_xclick">
<input type="hidden" name="business" value="bttb-seller@picott.ca">
<input type="hidden" name="item_name" value="This is a hundred dollar item">
<input type="hidden" name="currency_code" value="CAD">
<input type="hidden" name="amount" value="100.00">
<input type="image" src="http://www.paypal.com/en_US/i/btn/x-click-but01.gif" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">

<input type="hidden" name="email" value="">
<input type="hidden" name="first_name" value="Rich">
<input type="hidden" name="last_name" value="Texan">
<input type="hidden" name="address1" value="123 Oil Street">
<input type="hidden" name="address2" value="Barrel #4">
<input type="hidden" name="city" value="Edmonton">
<input type="hidden" name="state" value="AB">
<input type="hidden" name="country" value="Canada">
<input type="hidden" name="zip" value="O1L OI1">
<input type="hidden" name="night_phone_a" value="222">
<input type="hidden" name="night_phone_b" value="222">
<input type="hidden" name="night_phone_c" value="2222">

<input type="hidden" name="image_url" value="http://bttbalumni.ca/Images/SiteLogoSmall.png">
<input type="hidden" name="return" value="http://bttbalumni.ca/#thanks2017">
<input type="hidden" name="cbt" value="Return to BTTB Alumni">
<input type="hidden" name="cancel_return" value="http://bttbalumni.ca/#paypalTest">
</form>
</li>
<li>Test 4: Create a single item shopping cart, no tax specified <br>
<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_ext-enter">
<input type="hidden" name="redirect_cmd" value="_cart">
<input type="hidden" name="business" value="bttb-seller@picott.ca">
<input type="hidden" name="currency_code" value="CAD">
<input type="image" src="http://www.paypal.com/en_US/i/btn/x-click-but01.gif" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">

<input type="hidden" name="email" value="">
<input type="hidden" name="first_name" value="Rich">
<input type="hidden" name="last_name" value="Texan">
<input type="hidden" name="address1" value="123 Oil Street">
<input type="hidden" name="address2" value="Barrel #4">
<input type="hidden" name="city" value="Edmonton">
<input type="hidden" name="state" value="AB">
<input type="hidden" name="country" value="Canada">
<input type="hidden" name="zip" value="O1L OI1">
<input type="hidden" name="night_phone_a" value="222">
<input type="hidden" name="night_phone_b" value="222">
<input type="hidden" name="night_phone_c" value="2222">

<input type="hidden" name="image_url" value="http://bttbalumni.ca/Images/SiteLogoSmall.png">
<input type="hidden" name="return" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="cbt" value="Return to BTTB Alumni">
<input type="hidden" name="cancel_return" value="http://bttbalumni.ca/#paypalTest">

<input type="hidden" name="shopping_url" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="upload" value="1">

<input type="hidden" name="amount_1" value="150.00">
<input type="hidden" name="discount_amount_1" value="20.00">
<input type="hidden" name="item_name_1" value="All-Inclusive Entry">
</form>
</li>
<li>Test 5: Create a two-item shopping cart, tax only on the first one <br>
<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_ext-enter">
<input type="hidden" name="redirect_cmd" value="_cart">
<input type="hidden" name="business" value="bttb-seller@picott.ca">
<input type="hidden" name="currency_code" value="CAD">
<input type="image" src="http://www.paypal.com/en_US/i/btn/x-click-but01.gif" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">

<input type="hidden" name="email" value="">
<input type="hidden" name="first_name" value="Rich">
<input type="hidden" name="last_name" value="Texan">
<input type="hidden" name="address1" value="123 Oil Street">
<input type="hidden" name="address2" value="Barrel #4">
<input type="hidden" name="city" value="Edmonton">
<input type="hidden" name="state" value="AB">
<input type="hidden" name="country" value="Canada">
<input type="hidden" name="zip" value="O1L OI1">
<input type="hidden" name="night_phone_a" value="222">
<input type="hidden" name="night_phone_b" value="222">
<input type="hidden" name="night_phone_c" value="2222">

<input type="hidden" name="image_url" value="http://bttbalumni.ca/Images/SiteLogoSmall.png">
<input type="hidden" name="return" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="cbt" value="Return to BTTB Alumni">
<input type="hidden" name="cancel_return" value="http://bttbalumni.ca/#paypalTest">

<input type="hidden" name="shopping_url" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="upload" value="1">

<input type="hidden" name="amount_1" value="150.00">
<input type="hidden" name="discount_amount_1" value="20.00">
<input type="hidden" name="item_name_1" value="All-Inclusive Entry">
<input type="hidden" name="tax_rate_1" value="13">

<input type="hidden" name="amount_2" value="200.00">
<input type="hidden" name="discount_amount_2" value="15.00">
<input type="hidden" name="item_name_2" value="Golf Tournament Entry">
<input type="hidden" name="tax_rate_2" value="0">
</form>
</li>
<li>Test 6: Create a three-item shopping cart, two with different options<br>
<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_ext-enter">
<input type="hidden" name="redirect_cmd" value="_cart">
<input type="hidden" name="business" value="bttb-seller@picott.ca">
<input type="hidden" name="currency_code" value="CAD">
<input type="image" src="http://www.paypal.com/en_US/i/btn/x-click-but01.gif" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">

<input type="hidden" name="email" value="">
<input type="hidden" name="first_name" value="Rich">
<input type="hidden" name="last_name" value="Texan">
<input type="hidden" name="address1" value="123 Oil Street">
<input type="hidden" name="address2" value="Barrel #4">
<input type="hidden" name="city" value="Edmonton">
<input type="hidden" name="state" value="AB">
<input type="hidden" name="country" value="Canada">
<input type="hidden" name="zip" value="O1L OI1">
<input type="hidden" name="night_phone_a" value="222">
<input type="hidden" name="night_phone_b" value="222">
<input type="hidden" name="night_phone_c" value="2222">

<input type="hidden" name="image_url" value="http://bttbalumni.ca/Images/SiteLogoSmall.png">
<input type="hidden" name="return" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="cbt" value="Return to BTTB Alumni">
<input type="hidden" name="cancel_return" value="http://bttbalumni.ca/#paypalTest">

<input type="hidden" name="shopping_url" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="upload" value="1">

<input type="hidden" name="amount_1" value="150.00">
<input type="hidden" name="discount_amount_1" value="20.00">
<input type="hidden" name="item_name_1" value="All-Inclusive Entry">
<input type="hidden" name="on0_1" value="Shirt Size">
<input type="hidden" name="os0_1" value="Women's Small">
<input type="hidden" name="tax_rate_1" value="13">

<input type="hidden" name="amount_2" value="200.00">
<input type="hidden" name="discount_amount_2" value="15.00">
<input type="hidden" name="item_name_2" value="Golf Tournament Entry">
<input type="hidden" name="tax_rate_2" value="0">

<input type="hidden" name="amount_3" value="30.00">
<input type="hidden" name="item_name_3" value="70th Anniversary Golf Shirt">
<input type="hidden" name="on0_3" value="Shirt Size">
<input type="hidden" name="os0_3" value="Men's XL">
<input type="hidden" name="tax_rate_3" value="13">
</form>
</li>
<li>Test 7: The same cart as above, automatically populated by Javascript through JSON<br>
<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_ext-enter">
<input type="hidden" name="redirect_cmd" value="_cart">
<input type="hidden" name="business" value="bttb-seller@picott.ca">
<input type="hidden" name="currency_code" value="CAD">
<input type="image" src="http://www.paypal.com/en_US/i/btn/x-click-but01.gif" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">

<input type="hidden" name="email" value="">
<input type="hidden" name="first_name" value="Rich">
<input type="hidden" name="last_name" value="Texan">
<input type="hidden" name="address1" value="123 Oil Street">
<input type="hidden" name="address2" value="Barrel #4">
<input type="hidden" name="city" value="Edmonton">
<input type="hidden" name="state" value="AB">
<input type="hidden" name="country" value="Canada">
<input type="hidden" name="zip" value="O1L OI1">
<input type="hidden" name="night_phone_a" value="222">
<input type="hidden" name="night_phone_b" value="222">
<input type="hidden" name="night_phone_c" value="2222">

<input type="hidden" name="image_url" value="http://bttbalumni.ca/Images/SiteLogoSmall.png">
<input type="hidden" name="return" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="cbt" value="Return to BTTB Alumni">
<input type="hidden" name="cancel_return" value="http://bttbalumni.ca/#paypalTest">

<input type="hidden" name="shopping_url" value="http://bttbalumni.ca/#paypalTest">
<input type="hidden" name="upload" value="1">

<div id="cart_contents">
<a onclick="rebuild_paypal_cart();">REBUILD</a>
</div>

</form>
</li>
</ol>
        """)
        return html

# ==================================================================

import unittest
class testPaypalTest(unittest.TestCase):
    def testDump(self):
        paypalTestPage = bttbPaypalTest()
        print paypalTestPage.content()
    
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
