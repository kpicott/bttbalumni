"""
Page that shows the previous newsletters
"""

from bttbPage import bttbPage
from bttbConfig import MapLinks
__all__ = ['bttbNewsletters']

class bttbNewsletters(bttbPage):
    '''Class that generates the newsletter page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Newsletters'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks( """
<style>
.date
{
    font-size:   12pt;
    font-weight: bold;
    color:       blue;
    padding:     10px 0px 0px 0px;
}
</style>
<h1>Previous Newsletters</h1>
<p>
Click on the newsletter to download the PDF file.
</p><ol>
download:(__NEWSLETTERPATH__/Vol2No4.pdf, <div class='date'>June 2017</div>Volume 2 - Number 4)
link:(http://conta.cc/2qO0IFR, <div class='date'>May 2017</div>Volume 2 - Number 3)
link:(http://conta.cc/2papq29, <div class='date'>April 2017</div>Volume 2 - Number 2)
download:(__NEWSLETTERPATH__/Vol2No1.pdf, <div class='date'>March 2017</div>Volume 2 - Number 1)
download:(__NEWSLETTERPATH__/Vol1No6.pdf, <div class='date'>June 2007</div>Volume 1 - Number 6)
download:(__NEWSLETTERPATH__/Vol1No5.pdf, <div class='date'>May 2007</div>Volume 1 - Number 5)
download:(__NEWSLETTERPATH__/Vol1No4.pdf, <div class='date'>April 2007</div>Volume 1 - Number 4)
download:(__NEWSLETTERPATH__/Vol1No3.pdf, <div class='date'>March 2007</div>Volume 1 - Number 3)
download:(__NEWSLETTERPATH__/Vol1No2.pdf, <div class='date'>February 2007</div>Volume 1 - Number 2)
download:(__NEWSLETTERPATH__/Vol1No1.pdf, <div class='date'>December 2006</div>Volume 1 - Number 1)
</ol>
""")
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbNewsletters()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
