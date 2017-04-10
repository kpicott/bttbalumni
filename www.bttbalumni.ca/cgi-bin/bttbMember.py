# -*- coding: iso-8859-15 -*-
"""
BTTB member profile information.
"""
from datetime import datetime
from bttbConfig import PhoneFormat

__all__ = ['SensibleName', 'bttbMember']

#
#----------------------------------------------------------------------
def sort_by_nee(lhs,rhs):
    '''Utility for sorting by maiden name'''
    lhs_nee = lhs.nee
    rhs_nee = rhs.nee
    if lhs_nee:
        lhs_nee = lhs_nee.lower()
    if rhs_nee:
        rhs_nee = rhs_nee.lower()
    return cmp(lhs_nee, rhs_nee)

#----------------------------------------------------------------------
def sort_by_first_name(lhs,rhs):
    '''Utility for sorting by first name'''
    return cmp(lhs.first.lower(), rhs.first.lower())

#----------------------------------------------------------------------
def sort_by_last_name(lhs,rhs):
    '''Utility for sorting by last name'''
    return cmp(lhs.last.lower(), rhs.last.lower())

#----------------------------------------------------------------------
def sort_by_first_year(lhs,rhs):
    '''Utility for sorting by year joined'''
    return cmp(lhs.firstYear, rhs.firstYear)

#----------------------------------------------------------------------
def sort_by_last_year(lhs,rhs):
    '''Utility for sorting by year quit'''
    return cmp(lhs.lastYear, rhs.lastYear)

#----------------------------------------------------------------------
def sort_by_email(lhs,rhs):
    '''Utility for sorting by email'''
    lhs_email = lhs.email
    rhs_email = rhs.email
    if not lhs.emailVisible:
        lhs_email = '---'
    if not rhs.emailVisible:
        rhs_email = '---'
    return cmp(lhs_email.lower(), rhs_email.lower())

#----------------------------------------------------------------------
def sort_by_join_date(lhs,rhs):
    '''Utility for sorting by alumni association join date'''
    lhs_join = lhs.joinTime
    rhs_join = rhs.joinTime
    if not lhs.joinTime:
        lhs_join = datetime(2000,1,1)
    if not rhs.joinTime:
        rhs_join = datetime(2000,1,1)
    return cmp(lhs_join, rhs_join)

#----------------------------------------------------------------------
def sort_by_instrument(lhs,rhs):
    '''Utility for sorting by instrument'''
    return cmp(','.join(lhs.instruments).lower(), ','.join(rhs.instruments).lower())

#----------------------------------------------------------------------
def sort_method(sort_column):
    """
    Return a pointer to the 'sort_column'th sort method
    """
    # Default to sorting by last name
    method_to_use = sort_by_last_name
    if sort_column == 1:
        method_to_use = sort_by_first_name
    elif sort_column == 2:
        method_to_use = sort_by_nee
    elif sort_column == 3:
        method_to_use = sort_by_last_name
    elif sort_column == 4:
        method_to_use = sort_by_first_year
    elif sort_column == 5:
        method_to_use = sort_by_last_year
    elif sort_column == 6:
        method_to_use = sort_by_email
    elif sort_column == 7:
        method_to_use = sort_by_instrument
    return method_to_use

#----------------------------------------------------------------------
def SensibleName(first,nee,last):
    """
    Return a string with the full name, formatted sensibly
    """
    full_name = ''
    if nee and (len(nee) > 0):
        full_name = ('%s&nbsp;(%s)&nbsp;%s') % (first,nee,last)
    else:
        full_name = ('%s&nbsp;%s') % (first,last)
    return full_name

#----------------------------------------------------------------------
class bttbMember(object):
    '''Class to manage information on a single alumnus'''
    def __init__(self):
        '''Set up a blank record for population'''
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

    #----------------------------------------------------------------------
    def setLastVisit(self, when):
        """
        Define the time the user was last logged in (page view time).
        """
        self.lastVisitTime = when

    #----------------------------------------------------------------------
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

    #----------------------------------------------------------------------
    def midpoint(self):
        """
        Return a datetime object representing the rough midpoint of the band
        member's tenure (for estimating events they submit without specific
        times)
        """
        middle_year = (int(self.firstYear) + int(self.lastYear)) / 2.0
        if middle_year == int(middle_year):
            return datetime(int(middle_year), 6, 15)
        else:
            return datetime(int(middle_year), 12, 31)

    #----------------------------------------------------------------------
    def setEditTime(self,when):
        """
        Set the member's edit time, creating the XML element if required
        """
        self.editTime = when
        if not self.joinTime:
            self.setJoinTime( when )

    #----------------------------------------------------------------------
    def setJoinTime(self,when):
        """
        Set the member's joining time, creating the XML element if required
        """
        if not when:
            return
        self.joinTime = when

    #----------------------------------------------------------------------
    def setId(self,uniqueId):
        """
        Set the member's unique id.
        """
        self.id = uniqueId

    #----------------------------------------------------------------------
    def setName(self,first,nee,last):
        """
        Set the member's name, creating the XML element if required
        """
        self.first = first
        self.last = last
        if nee != last:
            self.nee = nee

    #----------------------------------------------------------------------
    def setYears(self,first,last):
        """
        Set the member's years, creating the XML element if required
        """
        self.firstYear = first
        self.lastYear = last

    #----------------------------------------------------------------------
    def resetInstruments(self):
        """
        Remove all instruments, in preparation for re-adding all
        """
        self.instruments = []

    #----------------------------------------------------------------------
    def addInstrument(self,instrument):
        """
        Add an instrument to this member's list
        """
        if instrument not in self.instruments:
            self.instruments.append( instrument )

    #----------------------------------------------------------------------
    def addPosition(self,position):
        """
        Add a position to this member's list
        """
        if position not in self.positions:
            self.positions.append( position )

    #----------------------------------------------------------------------
    def setRank(self,rank):
        """
        Set the member's highest rank
        """
        self.rank = rank

    #----------------------------------------------------------------------
    def setPassword(self,password):
        """
        Set the member's new password
        """
        self.password = password

    #----------------------------------------------------------------------
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
        if self.postalCode == 'NO POSTAL':
            self.postalCode = ''
        self.phone = PhoneFormat(phone)
        if self.phone == 'No Phone':
            self.phone = ''
        self.email = email

    #----------------------------------------------------------------------
    def setEmailVisible(self,isVisible):
        """
        Set the member's email visibility, creating the XML element if required
        """
        self.emailVisible = isVisible

    #----------------------------------------------------------------------
    def setMemory(self,memory):
        """
        Set the member's fond memory, creating the XML element if required
        """
        self.memory = memory.strip()

    #----------------------------------------------------------------------
    def fullName(self):
        """
        Return a string with the full name, formatted sensibly
        """
        return SensibleName( self.first, self.nee, self.last )

    #----------------------------------------------------------------------
    def fullAddress(self):
        """
        Return a string with the full address, formatted sensibly
        """
        full_address = []
        if self.street1 and len(self.street1) > 0:
            if self.apt and len(self.apt) > 0:
                full_address.append( ''.join([self.street1, ', Unit ', self.apt]) )
            else:
                full_address.append( self.street1 )
        if self.street2 and len(self.street2) > 0:
            full_address.append( self.street2 )
        if self.city and len(self.city) > 0:
            if self.province and len(self.province) > 0:
                full_address.append( self.city )
            else:
                full_address.append( ''.join([self.city, ', ', self.province]))
        if self.country and len(self.country) > 0:
            full_address.append( self.country )
        if self.postalCode and len(self.postalCode) > 0:
            full_address.append( self.postalCode )
        if self.phone and len(self.phone) > 0:
            full_address.append( self.phone )
        return '<br>'.join( full_address )

    #----------------------------------------------------------------------
    def printFullSummary(self):
        """
        Dump a full summary of the member input information as a block.
        """
        def pfs_row(title,value):
            '''Utility method to dump a single member row'''
            print '<tr><th valign="top">', title, '</th>'
            print '<th valign="top">&nbsp;:&nbsp;</th>'
            print '<td valign="top">', value, '</td></tr>'

        print '<table bgcolor="#ffbbbb" cellpadding="0">'
        pfs_row( 'First Year', self.firstYear )
        pfs_row( 'Last Year', self.lastYear )
        pfs_row( 'Email', self.email )
        pfs_row( 'Share Email?', self.emailVisible )
        pfs_row( 'Instrument(s)', ', '.join(self.instruments) )
        pfs_row( 'Position(s)', ', '.join(self.positions) )
        pfs_row( 'Address', self.fullAddress() )
        pfs_row( 'Memory', self.memory )
        if self.rank:
            pfs_row( 'Boys and Girls Rank', self.rank )
        pfs_row( 'Password', len(self.password)>0 and 'SET' or 'NOT SET' )
        print '</table>'

    #----------------------------------------------------------------------
    def get_committee_summary_row(self,checkPrefix):
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
        if self.email and self.emailVisible:
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
    '''Test class'''
    def testDB(self):
        '''Test method'''
        import bttbDB
        database = bttbDB.bttbDB()
        database.Initialize()
        #keys = db.GetPublicMemberKeys()
        (member_list, items) = database.get_public_member_list(sorted_by='last', descending=False)
        member_object = bttbMember()
        member_object.loadFromTuple( items, member_list[0] )
        member_object.printFullSummary()
        database.Finalize()

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
