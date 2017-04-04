# -*- coding: iso-8859-15 -*-
"""
BTTB member profile information.
"""
import re
import os.path
from datetime import datetime
from xml.dom import minidom
from bttbConfig import *

__all__ = ['SensibleName', 'bttbMember']

#
def _sortByNee(x,y):
    xNee = x.nee
    yNee = y.nee
    if xNee: xNee = xNee.lower()
    if yNee: yNee = yNee.lower()
    return cmp(xNee, yNee)
def _sortByFirstName(x,y):    return cmp(x.first.lower(), y.first.lower())
def _sortByLastName(x,y):    return cmp(x.last.lower(), y.last.lower())
def _sortByFirstYear(x,y):    return cmp(x.firstYear, y.firstYear)
def _sortByLastYear(x,y):    return cmp(x.lastYear, y.lastYear)
def _sortByEmail(x,y):
    xemail = x.email
    yemail = y.email
    if( not x.emailVisible ): xemail = '---'
    if( not y.emailVisible ): yemail = '---'
    return cmp(xemail.lower(), yemail.lower())
def _sortByJoinDate(x,y):
    xJoin = x.joinTime
    yJoin = y.joinTime
    if( not x.joinTime ): xJoin = datetime.datetime(2000,1,1)
    if( not y.joinTime ): yJoin = datetime.datetime(2000,1,1)
    return cmp(xJoin, yJoin)
def _sortByInstrument(x,y):    return cmp(','.join(x.instruments).lower(), ','.join(y.instruments).lower())

def _sortMethod(sortColumn):
    """
    Return a pointer to the 'sortColumn'th sort method
    """
    if( sortColumn == 1 ):
        return _sortByFirstName
    elif( sortColumn == 2 ):
        return _sortByNee
    elif( sortColumn == 3 ):
        return _sortByLastName
    elif( sortColumn == 4 ):
        return _sortByFirstYear
    elif( sortColumn == 5 ):
        return _sortByLastYear
    elif( sortColumn == 6 ):
        return _sortByEmail
    elif( sortColumn == 7 ):
        return _sortByInstrument
    else:
        # Default to sorting by last name
        return _sortByLastName

def SensibleName(first,nee,last):
    """
    Return a string with the full name, formatted sensibly
    """
    fullName = ''
    if( nee and len(nee) > 0 ):
        fullName = ('%s&nbsp;(%s)&nbsp;%s') % (first,nee,last)
    else:
        fullName = ('%s&nbsp;%s') % (first,last)
    return fullName

class bttbMember:
    def __init__(self):
        self.data = {}
        self.approved = False
        self.onCommittee = False
        self.editTime = datetime(2000, 1, 1)
        self.joinTime = datetime(2000, 1, 1)
        self.lastVisitTime = datetime.now()
        self.first = ''
        self.last = ''
        self.nee = ''
        self.firstYear = ''
        self.lastYear = ''
        self.email = ''
        self.emailVisible = True
        self.isFriend = False
        self.instruments = []
        self.positions = []
        self.rank = ''
        self.password = ''
        self.apt = ''
        self.street1 = ''
        self.street2 = ''
        self.city = ''
        self.province = 'Ontario'
        self.country = 'Canada'
        self.postalCode = ''
        self.phone = ''
        self.memory = ''
        self.id = 9999999

    def setLastVisit(self, when):
        """
        Define the time the user was last logged in (page view time).
        """
        self.lastVisitTime = when

    def loadFromTuple(self, fieldNames, dataTuple):
        """
        Initialize the data fields from the given tuple and it's field names.
        It's semantically equivalent to a dictionary but when calling this
        method there will be many tuples and only one set of common field
        names so this way is more efficient.
        """
        for field in fieldNames:
            value = dataTuple[fieldNames[field]]
            if field == 'instruments' or field == 'positions':
                self.__dict__[field] = value.split(', ')
            else:
                self.__dict__[field] = value

    def midpoint(self):
        """
        Return a datetime object representing the rough midpoint of the band
        member's tenure (for estimating events they submit without specific
        times)
        """
        midYear = (int(self.firstYear) + int(self.lastYear)) / 2.0
        if midYear == int(midYear):
            return datetime(int(midYear), 6, 15)
        else:
            return datetime(int(midYear), 12, 31)

    def setEditTime(self,when):
        """
        Set the member's edit time, creating the XML element if required
        """
        self.editTime = when
        if not self.joinTime:
            self.setJoinTime( when )

    def setJoinTime(self,when):
        """
        Set the member's joining time, creating the XML element if required
        """
        if not when:
            return
        self.joinTime = when

    def setId(self,uniqueId):
        """
        Set the member's unique id.
        """
        self.id = uniqueId

    def setName(self,first,nee,last):
        """
        Set the member's name, creating the XML element if required
        """
        self.first = first
        self.last = last
        if nee != last: self.nee = nee

    def setYears(self,first,last):
        """
        Set the member's years, creating the XML element if required
        """
        self.firstYear = first
        self.lastYear = last

    def resetInstruments(self):
        """
        Remove all instruments, in preparation for re-adding all
        """
        self.instruments = []

    def addInstrument(self,instrument):
        """
        Add an instrument to this member's list
        """
        if instrument not in self.instruments:
            self.instruments.append( instrument )

    def addPosition(self,position):
        """
        Add a position to this member's list
        """
        if position not in self.positions:
            self.positions.append( position )

    def setRank(self,rank):
        """
        Set the member's highest rank
        """
        self.rank = rank

    def setPassword(self,password):
        """
        Set the member's new password
        """
        self.password = password

    def setContact(self,street1,street2,apt,city,province,country,postalCode,phone,email):
        """
        Set the member's contact information, creating the XML element if required
        """
        self.street1 = street1
        self.street2 = street2
        self.apt = apt
        self.city = city
        self.province = province
        self.country = country
        self.postalCode = postalCode.upper()
        if self.postalCode == 'NO POSTAL': self.postalCode = ''
        self.phone = PhoneFormat(phone)
        if self.phone == 'No Phone': self.phone = ''
        self.email = email

    def setEmailVisible(self,isVisible):
        """
        Set the member's email visibility, creating the XML element if required
        """
        self.emailVisible = isVisible

    def setMemory(self,memory):
        """
        Set the member's fond memory, creating the XML element if required
        """
        self.memory = memory.strip()

    def fullName(self):
        """
        Return a string with the full name, formatted sensibly
        """
        return SensibleName( self.first, self.nee, self.last )

    def fullAddress(self):
        """
        Return a string with the full address, formatted sensibly
        """
        fullAddress = []
        if self.street1 and len(self.street1) > 0:
            if self.apt and len(self.apt) > 0:
                fullAddress.append( ''.join([self.street1, ', Unit ', self.apt]) )
            else:
                fullAddress.append( self.street1 )
        if self.street2 and len(self.street2) > 0:
            fullAddress.append( self.street2 )
        if self.city and len(self.city) > 0:
            if self.province and len(self.province) > 0:
                fullAddress.append( self.city )
            else:
                fullAddress.append( ''.join([self.city, ', ', self.province]))
        if self.country and len(self.country) > 0:
            fullAddress.append( self.country )
        if self.postalCode and len(self.postalCode) > 0:
            fullAddress.append( self.postalCode )
        if self.phone and len(self.phone) > 0:
            fullAddress.append( self.phone )
        return '<br>'.join( fullAddress )

    def printFullSummary(self):
        """
        Dump a full summary of the member input information as a block.
        """
        def pfsRow(title,value):
            print '<tr><th valign="top">', title, '</th>'
            print '<th valign="top">&nbsp;:&nbsp;</th>'
            print '<td valign="top">', value, '</td></tr>'

        print '<table bgcolor="#ffbbbb" cellpadding="0">'
        pfsRow( 'First Year', self.firstYear )
        pfsRow( 'Last Year', self.lastYear )
        pfsRow( 'Email', self.email )
        pfsRow( 'Share Email?', self.emailVisible )
        pfsRow( 'Instrument(s)', ', '.join(self.instruments) )
        pfsRow( 'Position(s)', ', '.join(self.positions) )
        pfsRow( 'Address', self.fullAddress() )
        pfsRow( 'Memory', self.memory )
        if self.rank:
            pfsRow( 'Boys and Girls Rank', self.rank )
        pfsRow( 'Password', len(self.password)>0 and 'SET' or 'NOT SET' )
        print '</table>'

    def getCommitteeSummaryRow(self,checkPrefix):
        """
        Get string with full HTML details on this member as a row in a table.
        """
        html = '<tr>'
        html += '<td align=\'center\' valign=\'center\'>'
        html += '<input type="checkbox" value="1" name="A%s%d">' % (checkPrefix,self.id)
        html += '<td align=\'center\' valign=\'center\'>'
        html += '<input type="checkbox" value="1" name="C%s%d">' % (checkPrefix,self.id)
        html += '</td>'
        html += '<td align=\'center\' valign=\'center\'>'
        html += '<input type="checkbox" value="1" name="F%s%d">' % (checkPrefix,self.id)
        html += '</td>'
        html += '<td valign=\'top\'>%s</td>' % self.fullName()
        html += '<td valign=\'top\' align=\'center\'>%s</td>' % self.firstYear
        html += '<td valign=\'top\' align=\'center\'>%s</td>' % self.lastYear
        if( self.email and self.emailVisible ):
            html += '<td valign=\'top\'><a class=\'email\' href=\'mailto:%s\'>%s</td>' % (self.email, self.email)
        else:
            html += '<td valign=\'top\' align=\'center\'>---</td>'
        html += '<td valign=\'top\'>%s</td>' % ', '.join(self.instruments)
        html += '<td valign=\'top\'>%s</td>' % (self.rank and self.rank or '--')
        html += '<td width=\'224\' valign=\'top\'>'
        html += self.fullAddress()
        html += '</td>'
        html += '<td valign=\'top\'>%s</td>' % ', '.join(self.positions)
        html += '<td valign=\'top\'>%s</td>' % (self.emailVisible and 'No' or 'Yes')
        html += '</tr>'
        return html

# ==================================================================

import unittest
class testMember(unittest.TestCase):
    def testDB(self):
        import bttbDB
        db = bttbDB.bttbDB()
        db.Initialize()
        keys = db.GetPublicMemberKeys()
        (memberList, items) = db.get_public_member_list(sorted_by='last', descending=False)
        memberObj = bttbMember()
        memberObj.loadFromTuple( items, memberList[0] )
        memberObj.printFullSummary()
        db.Finalize()

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
