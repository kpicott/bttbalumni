# -*- coding: iso-8859-15 -*-
"""
URL page that says thanks for registering to new alumni
"""

from bttbPage import bttbPage
from bttbConfig import MapLinks
__all__ = ['bttbJohnNewby']

class bttbJohnNewby(bttbPage):
    '''Class that generates the John Newby print page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
    
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni John Newby Prints'

    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks( """
        <center>
        <img src='/JohnNewby/Title.png'>
        </center>
        <hr color='#f22288' size='4'>
        <h2>Order Forms</h2>
        <p>
        Order Forms Available from Cheri Morrison, The Music Centre,
        at link:(http://www.teentourboosters.com)
        or by clicking the links below
        </p>
        <table>
        <tr>
        <td>Order form in Word Format</td>
        <td>&nbsp;</td>
        <th align='left'>download:(/JohnNewby/JohnNewbyOrderForm.doc,Download)</th>
        </tr>
        <tr>
        <td>PDF file with this information</td>
        <td>&nbsp;</td>
        <th align='left'>download:(/JohnNewby/MarchingInTime.pdf,Download)</th>
        </tr>
        <tr>
        <td>Interested in a specific print number?</td>
        <td>&nbsp;</td>
        <th align='left'>download:(#printChart,Click here to check availability)</th>
        </tr>
        </table>
        <hr color='#f22288' size='4'>
        <table width='100%'>
        <th valign='center'>
        <img src='/JohnNewby/JohnNewby.png' align='left'>
        </th>
        <td valign='center'>
        <img src='/JohnNewby/JohnNewbyTitle.png'>
        <p>
        Canadian Artist and former Trombonist with the Burlington Boys and
        Girls Band('56 & '57) has been commissioned by the BTTB Boosters Inc.
        with the full support of the BTTB Alumni Committee to commemorate
        the 60<sup>th</sup> Anniversary of the BURLINGTON TEEN TOUR BAND
        with an original painting 'MARCHING IN TIME'.
        </p>
        </td><td valign='center' align='right'>
        <a target='photo' href='/JohnNewby/JohnNewbyPrint.jpg'><img align='left' src='/JohnNewby/JohnNewbyPrint_Small.jpg' width='200' height='157' border='0'></a>
        </td></tr></table>
        <p>
        'Compared favourably with Norman Rockwell, this talented Canadian has
        been praised for his ability to create consistently, uncannily, a
        feeling of familiarity in the beholder - as though these warm and
        cozy images are a glimpse at our very own lives. When feelings of
        our own childhood experiences or thoughts of our beloved children
        are instantly, magically delivered, more than a mere glance is
        invited.' Memories of Childhood, the Art of John Newby,
        link:(http://www.john-newby.com).
        </p>
        <center>
        <img src='/JohnNewby/MarchingInTime.png'>
        </center>
        <p>
        Was unveiled at the '60<sup>th</sup> Anniversary Concert' at
        Hamilton Place April 1st, 2007.
        </p>
        <p>
        The available formats:<ul>
        <img src='/Buttons/bullet.png'>
        Unframed Limited Edition Print of the original painting,
        24" x 16" image size, on acid free paper, signed, and titled by
        the artist @ $125 each, numbered 1/450 through 450/450.
        <br>
        <img src='/Buttons/bullet.png'>
        Unframed Artist's Giclee Proofs (on canvas) of the original painting,
        24" x 16" image size, signed, and titled by the artist @ $250 each,
        only 15 available, numbered 1/15 through 15/15.
        <br>
        <img src='/Buttons/bullet.png'>
        Unframed Giclee (on canvas) prints of the original painting,
        36" x 24" image size, signed, and titled by the artist @ $350 each,
        numbered 1/1, 2/2, 3/3, 4/4, 5/5
        <br>
        <img src='/Buttons/bullet.png'>
        The Boosters have negotiated tax-free framing from BTTB supporter,
        Corby Custom Framing in Carlisle, ON -
        link:(http://www.corbyframing.ca/)
        </ul>
        </p>
        <h2>What is a Giclee?</h2>
        <p>
        Limited edition Giclee prints combine very high resolution printing
        on canvas and on acid-free papers. Pigment-based inks are used which
        produce a superior archival print. Next to the original, a properly
        produced Giclee print is the finest method available today of
        representing the artists original work.
        </p>
        <h2>Draw complete for #1/450 Limited Edition Print</h2>
        <p>
        Congratulations to Lynn Allaster who, at Hamilton Place, won the
        drawing for the right to limited edition print #1.
        </p>
        <p>
        Consider requesting your Limited Edition Print Number to match your
        Band Number.  Any questions, contact Cheri Morrison, BTTB Booster @
        905-336-3917 or by email send:(fmorrison@sympatico.ca)
        """ )

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbJohnNewby()
    print TEST_PAGE.content()
    
# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
