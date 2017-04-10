# -*- coding: iso-8859-15 -*-
"""
BTTB Alumni profile information.
"""
#
from datetime import datetime
from bttbMember import bttbMember, SensibleName
from bttbConfig import Error, Pluralize, PageLink, SortDictByValue, EmailLink, CommitteeMark
from bttbDB import bttbDB

__all__ = ['bttbAlumni']

def field_string(value):
    """
    Utility to return the given string or an empty string if it's 'None'
    """
    return value and value.replace('\n','\\n').replace('\t',' ') or ''

class bttbAlumni(object):
    '''Manage access to the alumni data'''
    def __init__(self):
        self.member_list = []
        try:
            self.__db = bttbDB()
            self.__db.Initialize()
        except Exception, ex:
            Error( 'Connecting to database', ex )

    #----------------------------------------------------------------------
    def __del__(self):
        self.__db.Finalize()

    #----------------------------------------------------------------------
    def sort_inverse(self,sort_index):
        """
        Return the string representing the opposite sorting method (e.g.
        ascending instead of descending)
        """
        forwards = sort_index.replace('_desc','')
        if sort_index == forwards:
            return sort_index + '_desc'
        else:
            return forwards

    #----------------------------------------------------------------------
    def sort_link(self,column_name,column_index,sort_index):
        """
        Construct a link to the table sorted by the column_index, given that
        the current sort is by sort_index
        """
        new_column_link = column_index
        sorted_by = ''
        colour = ''
        if sort_index == column_index:
            sorted_by = '&nbsp;&uarr;'
            colour = '#eeee88'
            new_column_link = self.sort_inverse( new_column_link )
        elif sort_index == self.sort_inverse( column_index ):
            sorted_by = '&nbsp;&darr;'
            colour = '#eeee88'
            new_column_link = self.sort_inverse( new_column_link )
        page = '?sort=%s#profiles' % new_column_link
        link = '%s%s' % (column_name, sorted_by)
        return PageLink( page, link, 'Sort by ' + column_name, colour )

    #----------------------------------------------------------------------
    def sort_link_c(self,column_name,column_index,sort_index):
        """
        Construct a link to the table sorted by the column_index, given that
        the current sort is by sort_index
        """
        new_column_link = column_index
        sorted_by = ''
        colour = ''
        if sort_index == column_index:
            sorted_by = '&nbsp;&uarr;'
            colour = '#eeee88'
            new_column_link = self.sort_inverse( new_column_link )
        elif sort_index == self.sort_inverse( column_index ):
            sorted_by = '&nbsp;&darr;'
            colour = '#eeee88'
            new_column_link = self.sort_inverse( new_column_link )
        return PageLink( '?sort=%s&committee=1#profiles' % new_column_link, '%s%s' % (column_name, sorted_by), 'Sort by ' + column_name, colour )

    #----------------------------------------------------------------------
    def get_alumni_summary(self,sort_column,who_wants_it):
        """
        Display a summary of the alumni so far in HTML format.
        Only show the fields relevant to other alumni (e.g. omit
        address information)
        """
        self.__db.GetPublicMemberKeys()
        descending = False
        sort_key = None
        if sort_column.replace('_desc','') == sort_column:
            sort_key = sort_column
        else:
            descending = True
            sort_key = self.sort_inverse(sort_column)
        (member_list, items) = self.__db.get_public_member_list(sort_key, descending)
        html = ''
        if len(member_list) < 2:
            html += '<h2>No members have registered yet</h2>'
        else:
            html += '<h2>%d Registered Alumni</h2>' % (len(member_list)-1)
            html += 'If you need to correct something '
            html += EmailLink('info@bttbalumni.ca', 'email us')
            html += ' and we will get it fixed right up!'
            html += '<br>'
            html += 'Click on a column heading to sort by that column.'
            html += "<table cellspacing='0' cellpadding='5' border='1'>"
            html += '<tr bgcolor=\'#ffaaaa\'>'
            html += '<th valign="center">%s' % self.sort_link('First', 'first', sort_column)
            html += self.sort_link('&nbsp;(nee)', 'nee', sort_column)
            html += self.sort_link('&nbsp;Last', 'last', sort_column)
            html += '</th>'
            html += '<th valign="center">%s</th>' % self.sort_link('Start&nbsp;Year', 'firstYear', sort_column)
            html += '<th valign="center">%s</th>' % self.sort_link('End&nbsp;Year', 'lastYear', sort_column)
            html += '<th valign="center">%s</th>' % self.sort_link('Email', 'email', sort_column)
            html += '<th valign="center">%s</th>' % self.sort_link('Instrument(s)', 'instruments', sort_column)
            html += '</tr>'
            found_unapproved = 0
            try:
                for member in member_list:
                    if member and member[items['approved']]:
                        html += '<tr>'
                        html += '<td valign=\'top\'>'
                        if member[items['onCommittee']]:
                            html += CommitteeMark()
                        sensible_name = SensibleName( member[items['first']], member[items['nee']], member[items['last']] )
                        html += sensible_name
                        if who_wants_it and who_wants_it.id == member[items['id']]:
                            link = '?id=%d#register' % member[items['id']]
                            html += '<br>' + PageLink(link, 'Click to Edit', 'Edit your profile')
                        html += '</td>'
                        html += '<td valign=\'top\' align=\'center\'>%s</td>' % member[items['firstYear']]
                        html += '<td valign=\'top\' align=\'center\'>%s</td>' % member[items['lastYear']]
                        if member[items['email']] and member[items['emailVisible']]:
                            html += '<td valign=\'top\'>'
                            html += EmailLink( member[items['email']] )
                            html += '</td>'
                        else:
                            html += '<td valign=\'top\' align=\'center\'>---</td>'
                        html += '<td valign=\'top\'>%s</td>' % member[items['instruments']]
                        html += '</tr>'
                    elif member:
                        found_unapproved = found_unapproved + 1
            except Exception, ex:
                Error( 'Displaying list', ex )
            html += "</table>\n"
            if found_unapproved > 0:
                html += '<p>&nbsp;</p>'
                html += '<h2>%d %s Awaiting Confirmation</h2><ol>' % (found_unapproved, Pluralize('Member',found_unapproved))
                for member in member_list:
                    if member and not member[items['approved']]:
                        html += '<li>'
                        html += SensibleName( member[items['first']], member[items['nee']], member[items['last']] )
                        html += '</li>'
                html += '</ol>\n'
            return html

    #----------------------------------------------------------------------
    def process_query(self, query):
        """
        Process a generic query with unknown result type.
        """
        return self.__db.process_query(query)

    #----------------------------------------------------------------------
    def get_alumni_summary_for_committee(self,sort_column):
        """
        Display a summary of the alumni so far in HTML format.
        Only show the fields relevant to other alumni (e.g. omit
        address information)
        """
        self.__db.GetPublicMemberKeys()
        descending = False
        sort_key = None
        if sort_column.replace('_desc','') == sort_column:
            sort_key = sort_column
        else:
            descending = True
            sort_key = self.sort_inverse(sort_column)
        (member_list, items) = self.__db.get_full_member_list(sort_key, descending)
        html = ''
        if len(member_list) < 2:
            html += '<h2>No members have registered yet</h2>'
        else:
            found_unapproved = 0
            try:
                for member in member_list:
                    if member and not member[items['approved']]:
                        found_unapproved = found_unapproved + 1
            except Exception, ex:
                Error( 'Searching for unapproved members', ex )

            if found_unapproved > 0:
                html += '<form name="approveForm" id="approveForm" '
                html += ' action="javascript:submit_form(\'/cgi-bin/bttbApprove.cgi\', \'#approveForm\', \'?committee=1#profiles\');">'
                html += self.get_committee_title( '%d %s %s' % (found_unapproved, Pluralize('Member',found_unapproved), 'Awaiting Confirmation'), sort_column )
                for member in member_list:
                    if member and not member[items['approved']]:
                        member_obj = bttbMember()
                        member_obj.loadFromTuple( items, member )
                        html += member_obj.get_committee_summary_row('XXX')
                html += '</table>'
                html += '<input type="submit" name="submit" value="Approve">'
                html += '</form>'
            else:
                html += '<h2>No New Members</h2>'

            html += '<h2>%d Registered Alumni (click to edit)</h2>' % (len(member_list)-1)
            try:
                column = 0
                html += '<table><tr>'
                for member in member_list:
                    if not member or not member[items['approved']]:
                        continue
                    if column == 4:
                        html += '</tr>\n<tr>'
                        column = 0
                    column = column + 1
                    html += '<td>'
                    link = '?id=%d#register' % member[items['id']]
                    html += PageLink(link, SensibleName( member[items['first']], member[items['nee']], member[items['last']] ))
                    html += '</td>'
            except Exception, ex:
                Error( 'Displaying registered alumni list', ex )
            html += "</tr></table>\n"
            return html

    #----------------------------------------------------------------------
    def get_committee_title(self,title,sort_column):
        """
        Print out the title line of the table showing the profile
        information visible to the committee members.
        """
        html = '<h2>' + title + '</h2>'
        html += '<div class="subtext">Click on a column heading to sort by that column.</div>'
        html += "<table cellspacing='0' cellpadding='5' border='1'>"
        html += '<tr bgcolor=\'#ffaaaa\'>'
        html += '<th>Approve</th>'
        html += '<th>Committee</th>'
        html += '<th>Friend<br>of the<br>Alumni</th>'
        html += '<th>%s %s %s</th>' % (self.sort_link_c('First', 'first', sort_column), self.sort_link_c('&nbsp;(nee)', 'nee', sort_column), self.sort_link_c('&nbsp;Last', 'last', sort_column))
        html += '<th>%s</th>' % self.sort_link_c('Start&nbsp;Year', 'firstYear', sort_column)
        html += '<th>%s</th>' % self.sort_link_c('End&nbsp;Year', 'lastYear', sort_column)
        html += '<th>%s</th>' % self.sort_link_c('Email', 'email', sort_column)
        html += '<th>%s</th>' % self.sort_link_c('Instrument(s)', 'instruments', sort_column)
        html += '<th>%s</th>' % self.sort_link_c('Highest Rank', 'rank', sort_column)
        html += '<th>Address</th>'
        html += '<th>%s</th>' % self.sort_link_c('Positions', 'positions', sort_column)
        html += '<th>%s</th>' % self.sort_link_c('Keep Private?', 'emailVisible', sort_column)
        html += '</tr>'
        return html

    #----------------------------------------------------------------------
    def ArchiveData(self):
        """
        Archive all of the database table information, just in case
        """
        return self.__db.Archive()

    #----------------------------------------------------------------------
    def get_unique_id(self):
        """
        Get back a unique ID for a new member
        """
        return self.__db.get_unique_id()

    #----------------------------------------------------------------------
    def getMemberFromId(self, member_id):
        """
        Get back a bttbMember whose id matches the given one.
        """
        if member_id is None:
            return None
        return self.__db.GetMember(member_id)

    #----------------------------------------------------------------------
    def getMemberFromLogin(self, name, password):
        """
        Get back a bttbMember whose login information matches the given one,
        or None if nobody matches.
        """
        member = self.__db.GetMemberInfo(name)
        if member:
            if member.password and member.password != password:
                member = None
        return member

    #----------------------------------------------------------------------
    def getMostRecent(self, how_many):
        """
        Return a tuple consisting of the list of the most recent 'how_many'
        members to join and the size of the entire membership list.
        """
        (member_list, _) = self.__db.get_public_member_list('joinTime', True)
        return (member_list[0:how_many], len(member_list))

    #----------------------------------------------------------------------
    def getJoinedAfter(self, earliest_time):
        """
        Return a tuple consisting of the list of the members who joined
        after the 'earliest_time' and the size of the entire membership list.
        """
        (member_list, _, total_registration) = self.__db.get_public_member_list_since(earliest_time)
        return (member_list, total_registration)

    #----------------------------------------------------------------------
    def get_committee_text(self):
        """
        Display full text of all alumni in an Excel/Word-friendly format.
        That is, tab-separated text with a heading line.
        """
        (member_list, items) = self.__db.get_full_member_list('last', False)
        html = '\t'.join([a[0].upper()+a[1:] for a in SortDictByValue(items)])
        event_list = self.__db.GetEvents()
        for event in event_list:
            if event.canAttend:
                html += '\tAttend' + event.summary
            if event.canVolunteer:
                html += '\tVolunteer' + event.summary
        html += '\n'

        attendance = self.__db.GetFullEventAttendance()
        volunteers = self.__db.GetFullEventVolunteers()
        if len(member_list) == 0:
            return
        for member in member_list:
            alumni_id = member[items['id']]
            html += '\t'.join([field_string(str(a)) for a in member])
            for event in event_list:
                if event.canAttend:
                    attend = '0'
                    for (aid, eid, _) in attendance:
                        if aid == alumni_id and eid == event.id:
                            attend = '1'
                            break
                    html += '\t' + attend
                if event.canVolunteer:
                    volunteer = '0'
                    for (aid, eid, _) in volunteers:
                        if aid == alumni_id and eid == event.id:
                            volunteer = '1'
                            break
                    html += '\t' + volunteer
            html += '\n'
        return html

    #----------------------------------------------------------------------
    def get_memories(self, member_id=None):
        """
        Return the list of memories from the alumni (or all if id=None).
        """
        return self.__db.get_memories(member_id)

    #----------------------------------------------------------------------
    def get_memories_after(self, earliest_time):
        """
        Return the list of memories from the alumni submitted after the given
        date.
        """
        return self.__db.get_memories_added_after(earliest_time)

    #----------------------------------------------------------------------
    def getConcertInstrumentation(self, concert_table):
        """
        Return the list of current concert participants
        """
        return self.__db.GetConcertInstrumentation(concert_table)

    #----------------------------------------------------------------------
    def get_parade_registration_2017(self):
        """
        Return the list of parade participants for the 2017 reunion
        """
        return self.__db.get_parade_registration_2017()

    #----------------------------------------------------------------------
    def get_parade_part_2017(self, member_id):
        """
        Return the list of parade participants for the 2017 reunion
        """
        return self.__db.get_parade_part_2017(member_id)

    #----------------------------------------------------------------------
    def update_member(self, member, memory, memory_id):
        """
        Add a new member into the database if it isn't there already,
        or replace it's data if it is already there.
        """
        self.__db.update_member( member, True )
        self.__db.update_member_memory( member, memory, memory_id )
        self.ArchiveData()

    #----------------------------------------------------------------------
    def update_memory(self, member, memory, memory_time, memory_id):
        """
        Update the memory in the table. If the memory doesn't exist
        then add a new one to the table.
        """
        self.__db.update_memory( member.id, memory, memory_time, memory_id )

    #----------------------------------------------------------------------
    def remove_memory(self, memory_id):
        """
        Remove the memory from the table.
        """
        self.__db.remove_memory( memory_id )

    #----------------------------------------------------------------------
    def approve_member(self, member_id, is_friend, on_committee):
        """
        Officially approve a new member. The "is_friend" and "on_committee"
        flags are only accessible to committee members so access them
        from here.
        """
        member = self.getMemberFromId( member_id )
        if member:
            member.approved = True
            member.isFriend = is_friend
            member.onCommittee = on_committee
            member.editTime = datetime.now()
            self.__db.update_member( member, True )
        else:
            Error( 'Tried to approve non-existing member', '%d' % member_id )

if __name__ == '__main__':
    ALUM = bttbAlumni()
    print ALUM.get_alumni_summary_for_committee('last')
    print ALUM.approve_member(3, True, True)

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
