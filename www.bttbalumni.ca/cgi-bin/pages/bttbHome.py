"""
URL page that says thanks for registering to new alumni
"""

import os
from bttbAlumni import bttbAlumni
from bttbMember import html_name
from pages.bttbPage import bttbPage
from bttbConfig import MapLinks, RootPath, EmbeddedCSS, Error, ErrorMsg, CommitteeMark
from datetime import datetime,timedelta
__all__ = ['bttbHome']

class bttbHome(bttbPage):
    '''Class that generates the home page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            pass

    #----------------------------------------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni'

    #----------------------------------------------------------------------
    def get_old_news_list(self, before):
        ''':return: List of news older than "before"'''
        (interest,_) = self.alumni.process_query("""
        SELECT appeared,title,description FROM news
        WHERE appeared <= '%s'
        ORDER BY appeared DESC
        """ % before)
        return interest

    #----------------------------------------------------------------------
    def get_news_list(self, as_of):
        ''':return: List of news older than "as_of"'''
        (interest,_) = self.alumni.process_query("""
        SELECT appeared,title,description FROM news
        WHERE appeared > '%s'
        ORDER BY appeared DESC
        """ % as_of)
        return interest

    #----------------------------------------------------------------------
    def get_old_news_count(self, as_of):
        ''':return: Size of news list older than "as_of"'''
        (interest,_) = self.alumni.process_query("""
        SELECT COUNT(*) FROM news
        WHERE appeared <= '%s'
        """ % as_of)
        return interest[0][0]

    #----------------------------------------------------------------------
    def get_friend_count(self):
        ''':return: Number of "Friends of the Alumni"'''
        (friends,_) = self.alumni.process_query("""
        SELECT COUNT(*) from alumni where isFriend = 1
        """)
        return friends[0]

    #----------------------------------------------------------------------
    def get_wallace_count(self):
        ''':return: Number of Wallace B. Wallace winners'''
        (wallace,_) = self.alumni.process_query("""
        SELECT COUNT(*)
        FROM wallace
        """)
        return wallace[0]

    #----------------------------------------------------------------------
    def get_memory_count(self):
        ''':return: Number of available memories'''
        (memory,_) = self.alumni.process_query("""
        SELECT COUNT(*)
        FROM memories
        """)
        return memory[0]

    #----------------------------------------------------------------------
    @staticmethod
    def contact_content():
        ''':return: a string with the content for this web page.'''
        return MapLinks("""
Don't want to sign up but still want to get news by email?
Enter your name and email address below to be added to the mailing list:<br/>
<form method='POST' onsubmit='return validateContact();'
      name="contact_form" id="contact_form"
      action="javascript:submit_form('/cgi-bin/bttbContact.cgi', '#contact_form', null);">
<table width='100%%' border='2'>
<tr><th bgcolor='#ffaaaa'><font size='+2'>BAND ALUMNI CONTACT</font></th></tr>
<tr><td>
  <table width='100%%'>
  <tr>
    <td><input type='text' id='first_name' placeholder='First Name' name='first_name' value='' size='32'></td>
    <td><span id='inf_first_name' class='required'>*</td>
    <td><input type='text' id='last_name' placeholder='Last Name' name='last_name' value='' size='32'></td>
    <td><span id='inf_last_name' class='required'>*</td>
  </tr>
  <tr>
    <td><input type='text' id='email' placeholder='Email Address' name='email' value='' size='32'></td>
    <td><span id='inf_email' class='required'>*</td>
    <td colspan='2'>
        <input type='submit' value='Add Me' name='Submit'>
        <input type='reset' value='Reset' name='Reset'>
    </td>
  </tr>
</table>
<p id='disclaimer' align='center'><b>Please note that this information will only be used for BTTB Alumni purposes.<br/>
You may opt out at any time by sending an email indicating so to send:(info@bttbalumni.ca,the mailing list owner)</b>
</p>
</td></tr></table>

</form>""")

    #----------------------------------------------------------------------
    @staticmethod
    def add_countdowns(countdowns):
        '''Define the Javscript used in this page'''
        # The countdowns want to extend the entire page width, but this page
        # is limited to the 'content' div, which is fixed width. Solve that
        # by adding the countdown dcontainer to the 'header' div.
        if len(countdowns) == 0:
            return ''
        html = '<div class="ribbon-container">\n'
        for (days, title) in countdowns:
            html += '''
            <div class='ribbon one'>
                <div class='bk l shadow'>
                    <div class='arrow top'></div>
                    <div class='arrow bottom'></div>
                </div>
                <div class='skew l shadow'></div>
                <div class='banner shadow'>
                    <div>%s days to go : %s</div>
                </div>
                <div class='skew r shadow'></div>
                <div class='bk r shadow'>
                    <div class='arrow top'></div>
                    <div class='arrow bottom'></div>
                </div>
            </div>
            ''' % (days, title)
        html += "</div>\n"
        return html

    #----------------------------------------------------------------------
    def content(self):
        """
        Return a string with the content for this web page.
        """
        if self.requestor:
            old_news_time = self.requestor.lastVisitTime - timedelta(30)
            old_alumni_time = self.requestor.lastVisitTime - timedelta(14)
        else:
            old_news_time = datetime.now() - timedelta(30)
            old_alumni_time = datetime.now() - timedelta(14)

        html = EmbeddedCSS( 'bttbHome.css' )

        html += MapLinks( """
<script>
function validateContact()
{
    var first_name = $('#first_name').val();
    var last_name = $('#last_name').val();
    var email = $('#email').val().replace(/^\s+|\s+$/g, '');

    var emptyString = /^\s*$/ ;
    if( emptyString.test( first_name ) )
    {
        alert( 'First name required' );
        return false;
    }
    if( emptyString.test( last_name ) )
    {
        alert( 'Last name required' );
        return false;
    }
    if( emptyString.test( email ) )
    {
        alert( 'Email required' );
        return false;
    }
    var email_regex = /^[^@]+@[^@.]+\.[^@]*\w\w$/  ;
    if( !email_regex.test(email) )
    {
        alert( 'Not a valid email' );
        return false;
    }

    return true;
}
</script>
<NOSCRIPT>
<p><b>
<font color='red'>Warning: This site relies heavily on JavaScript,
which you currently have disabled. Please enable it or use another
browser in order to enjoy the full experience.</font></b></p>
<p>
link:(/pages/javascript.html,To learn how to enable Javascript click here.)
</p>
</NOSCRIPT> """ )

        # Add in the active countdowns
        try:
            countdown_fd = open(os.path.join(RootPath(),'countdowns.txt'))
            countdowns = []
            for line in countdown_fd:
                (date, event_title) = line.rstrip().split( ',' )
                (year, month, day) = date.split( '-' )
                remaining = datetime(int(year),int(month),int(day)) - datetime.now()
                countdowns.append( [remaining.days, event_title] )
            countdown_fd.close()
            html += self.add_countdowns( countdowns )
        except Exception:
            pass

        #===================================================================
        # Get the news articles
        try:
            news = self.get_news_list( "%s" % (old_news_time.strftime('%Y-%m-%d')) )
            old_news = []
            if 'full' in self.params:
                old_news = self.get_old_news_list( "%s" % (old_news_time.strftime('%Y-%m-%d')) )
                old_article_count = len(old_news)
                show_old = True
            else:
                old_article_count = self.get_old_news_count( "%s" % (old_news_time.strftime('%Y-%m-%d')) )
                show_old = False
        except Exception, ex:
            news = []
            old_news = []
            html += ErrorMsg( "News articles not available", ex )

        return html

        #===================================================================
        for when, title, article in news:
            html += "<div class='newsTitle'>"
            if show_old:
                html += "<img border='0' width='33' height='15' src='"
                html += MapLinks("__IMAGEPATH__/New.png'>&nbsp;")
            html += "%s<span class='newsDate'>%s</span></div>" % (title, when.strftime('%Y-%m-%d'))
            html += "<div class='newsArticle'>%s</div></div>" % article
        for when, title, article in old_news:
            html += "<div class='newsTitle'>"
            html += "%s<span class='newsDate'>%s</span></div>" % (title, when.strftime('%Y-%m-%d'))
            html += "<div class='newsArticle'>%s</div></div>" % article

        #===================================================================
        # Get the new (to the user) members
        try:
            member_list = []
            (member_list, out_of) = self.alumni.getJoinedAfter( old_alumni_time )
            count = len(member_list)
            if count > 10:
                count = 10
            html += "<div class='newsTitle'>Member Stats"
            html += "<span class='newsDate'>%s</span></div>" % (old_news_time.strftime('%Y-%m-%d'))
            html += MapLinks("<div class='newsArticle'><table background='__IMAGEPATH__/semiOpaque.png' border='1'><tr>")
            if count > 0:
                html += "<td valign='top'>"
                if self.is_member():
                    html += "<table>"
                    for (first, nee, last, first_year, last_year, _, instruments, _, _, on_committee, _) in member_list:
                        count = count - 1
                        if count < 0:
                            continue
                        try:
                            html += "<tr>\n"
                            html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
                            html += "<th align='left'>"
                            if on_committee:
                                html += CommitteeMark()
                            html += html_name(first,nee,last) + "</th>\n"
                            html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
                            html += "<td><i>(%d&nbsp;-&nbsp;%d)</i></td>\n" % (first_year, last_year)
                            html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
                            html += "<td>" + instruments + "</td>\n"
                            html += "</tr>\n"
                        except Exception:
                            html += "<tr><td colspan='4'>Record error</td></tr>"
                    if len(member_list) > 0:
                        html += "</table>"
                else:
                    html += "Sign in to see who the latest members are!"
                html += "</td>"
    
            html += "<td valign='top'><table>"
            html += "<tr>\n"
            html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
            html += MapLinks("<th>link:(#profiles,%d members signed up)" % out_of)
            html += MapLinks("<br>link:(#profiles,%d are friends)" % self.get_friend_count())
            html += MapLinks("<br>link:(#memories,%d memories added)" % self.get_memory_count())
            html += MapLinks("<br>link:(#wallaceb,%d Wallace B. Wallace winners)" % self.get_wallace_count())
            #html += MapLinks("<br>link:(#johnNewby, only 345 John Newby prints remain)")
            html += "</tr>\n"
            html += "</table>"
            html += "</td>"
            html += "</tr>"
    
            html += "<tr>"
            if not self.is_member():
                html += "<td colspan='2'>"
                html += self.contact_content()
                html += "</td>"
            html += "</tr>"
    
            html += "</table></div>"
        except Exception, ex:
            html += ErrorMsg( "Unable to load new member information", ex )

        #===================================================================
        try:
            memory_list = self.alumni.get_memories_after(old_alumni_time)
            count = len(memory_list)
            if count > 10:
                count = 10
            if count > 0:
                html += MapLinks( """
                <div class='newsTitle'>New Memories
                <span class='newsDate'>%s</span></div>
                <div class='newsArticle'><table width='90%%' background='__IMAGEPATH__/semiOpaque.png' border='1'><tr><td>
                """ % old_news_time.strftime('%Y-%m-%d') )
                if self.is_member():
                    for alumni_id, memory, memory_time, _, _ in memory_list:
                        count = count - 1
                        if count < 0:
                            continue
                        try:
                            member = self.alumni.getMemberFromId( alumni_id )
                            html += "<b>%s %s</b>" % (memory_time.strftime('%Y'), member.fullName())
                            html += "<p>%s</p>\n" % memory
                        except Exception:
                            pass
                else:
                    html += "Sign in to see the member's memories"
                html += '</td></tr></table></div>'
        except Exception, ex:
            html += ErrorMsg( "Unable to load new memories", ex )

        #===================================================================
        # The unshown article summary
        try:
            html += "<div class='newsTitle'>"
            if show_old:
                html += MapLinks("link:(#home, %d of these %d articles are old - click here to hide them)" % (old_article_count, len(old_news) + len(news)))
                for when, title, article in news:
                    if when > old_news_time:
                        continue
                    html += "<div class='newsTitle'>"
                    html += "%s<span class='newsDate'>%s</span></div>" % (title, when.strftime('%Y-%m-%d'))
                    html += "<div class='newsArticle'>%s</div></div>" % article
            else:
                html += MapLinks("%d old articles not displayed, link:(?full=1#home,click here to see them)" % old_article_count)
        except Exception, ex:
            html += ErrorMsg( "Unable to find hidden articles", ex )

        #===================================================================
        # And the legal stuff...
        html += MapLinks( """
        <div class='copyright'>Copyright 2006-%d BTTB Alumni Association. All rights reserved.
        <table>
        <tr><td rowspan='3'>Contact Us:</td>
            <td>Bob Webb - Organizing Committee Chair: send:(info@bttbalumni.ca)</td>
        </tr><tr>
            <td>Kevin Picott, Webmaster: send:(web@bttbalumni.ca)</td>
        </tr><tr>
            <td>Gordon Cameron and Paul Fitzgerald, Media: send:(media@bttbalumni.ca)</td>
        </tr></table>
        </div>
        """ % datetime.now().year )

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbHome()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
