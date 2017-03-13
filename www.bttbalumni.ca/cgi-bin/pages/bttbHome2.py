"""
URL page that says thanks for registering to new alumni
"""

import os
from bttbAlumni import bttbAlumni
from bttbMember import *
from bttbPage import bttbPage
from bttbConfig import *
from datetime import datetime,timedelta
__all__ = ['bttbHome2']

class bttbHome2(bttbPage):
    def __init__(self):
        bttbPage.__init__(self)
        try:
            self.alumni = bttbAlumni()
        except Exception, e:
            Error( 'Could not find parade information', e )

    def title(self): return 'BTTB Alumni'

    def scripts(self):    return ['__JAVASCRIPTPATH__/browserWarning.js']

    def getOldNewsList(self, before):
        (interest,description) = self.alumni.processQuery("""
        SELECT appeared,title,description FROM news
        WHERE appeared <= '%s'
        ORDER BY appeared DESC
        """ % before)
        return interest

    def getNewsList(self, asOf):
        (interest,description) = self.alumni.processQuery("""
        SELECT appeared,title,description FROM news
        WHERE appeared > '%s'
        ORDER BY appeared DESC
        """ % asOf)
        return interest

    def getOldNewsCount(self, asOf):
        (interest,description) = self.alumni.processQuery("""
        SELECT COUNT(*) FROM news
        WHERE appeared <= '%s'
        """ % asOf)
        return interest[0][0]

    def getFriendCount(self):
        (friends,description) = self.alumni.processQuery("""
        SELECT COUNT(*) from alumni where isFriend = 1
        """)
        return friends[0]

    def getWallaceCount(self):
        (wallace,description) = self.alumni.processQuery("""
        SELECT COUNT(*)
        FROM wallace
        """)
        return wallace[0]

    def getMemoryCount(self):
        (memory,description) = self.alumni.processQuery("""
        SELECT COUNT(*)
        FROM memories
        """)
        return memory[0]

    def contact_content(self):
        """
        Get the HTML that will populate the contact form.
        """
        return MapLinks("""
Don't want to sign up but still want to get news by email?
Enter your name and email address below to be added to the mailing list:<br/>
<form method='POST' onsubmit='return validateRegistration();' 
      name="contactForm" id="contactForm"
      action="javascript:submitForm('contactForm', '/cgi-bin/bttbContact.cgi', '/#thanksContact');">
<table border='2'>
<tr><th bgcolor='#ffaaaa'><font size='+2'>BAND ALUMNI CONTACT</font></th></tr>
<tr><td>
  <table>
  <tr>
      <th align='right'>First Name:</th>
    <td><input type='text' id='FirstName' onchange="validatePresent(this,'inf_firstName');" name='FirstName' value='' size='32'></td>
    <td id='inf_firstName'>*</td>
  </tr>
  <tr>
      <th align='right'>Current Last Name:</th>
    <td><input type='text' id='CurrentLastName' onchange="validatePresent(this,'inf_lastName');" name='CurrentLastName' value='' size='32'></td>
    <td id='inf_lastName'>*</td>
  </tr>
  <tr>
      <th valign='top' align='right'>Last Name While in Band:</th>
      <td><input type='text' id='LastNameInBand' name='LastNameInBand' value='' size='32'></td>
    <td><i>(if different)</i></td>
  </tr>
  <tr>
      <th align='right'>First Year in Band:</th>
    <td><input type='text' id='FirstYear' onchange="validatePresent(this,'inf_firstYear');" name='FirstYear' value='' size='4'></td>
    <td id='inf_firstYear'>*</td>
  </tr>
  <tr>
    <th align='right'>Last Year in Band</th>
    <td><input type='text' id='LastYear' onchange="validatePresent(this,'inf_lastYear');" name='LastYear' value='' size='4'></td>
    <td id='inf_lastYear'>*</td>
  </tr>
  <tr>
      <th align='right'>Email:</th>
    <td><input type='text' id='Email' onchange="validateEmail(this,'inf_email',true);" name='Email' value='' size='32'></td>
    <td id='inf_email'>*</td>
  </tr>
</table>
<p id='disclaimer' align='center'><b>Please note that this information will only be used for BTTB Alumni purposes.<br/>You may
opt out at any time by sending an email indicating so to send:(info@bttbalumni.ca,the mailing list owner)</b>
</p>
</td></tr></table>

<p><input type='submit' value='Add Me' name='Submit'>
   <input type='reset' value='Reset' name='Reset'>
</p>
</form>""")

    def content(self):
        """
        Return a string with the content for this web page.
        """
        if self.requestor:
            oldNewsTime = self.requestor.lastVisitTime - timedelta(7)
            oldAlumniTime = self.requestor.lastVisitTime - timedelta(3)
        else:
            oldNewsTime = datetime.now() - timedelta(7)
            oldAlumniTime = datetime.now() - timedelta(7)
        html = MapLinks( """
        <NOSCRIPT>
        <p><b>
        <font color='red'>Warning: This site relies heavily on JavaScript,
        which you currently have disabled. Please enable it or use another
        browser in order to enjoy the full experience.</font></b></p>
        </NOSCRIPT>
        """ )
        remaining = datetime(2017,6,14) - datetime.now()
        html += '<div class="countdown">%d days left to the 70<sup>th</sup> Anniversary Celebration!!!</div>' % remaining.days

        news = self.getNewsList( "%s" % (oldNewsTime.strftime('%Y-%m-%d')) )
        oldNews = []
        if 'full' in self.params:
            oldNews = self.getOldNewsList( "%s" % (oldNewsTime.strftime('%Y-%m-%d')) )
            oldArticleCount = len(oldNews)
            showOld = True
        else:
            oldArticleCount = self.getOldNewsCount( "%s" % (oldNewsTime.strftime('%Y-%m-%d')) )
            showOld = False
        #===================================================================
        for when, title, article in news:
            html += "<div class='newsTitle'>"
            if showOld:
                html += "<img border='0' width='33' height='15' src='"
                html += MapLinks("__IMAGEPATH__/New.png'>&nbsp;")
            html += "%s<span class='newsDate'>%s</span></div>" % (title, when.strftime('%Y-%m-%d'))
            html += "<div class='newsArticle'>%s</div></div>" % article
        for when, title, article in oldNews:
            html += "<div class='newsTitle'>"
            html += "%s<span class='newsDate'>%s</span></div>" % (title, when.strftime('%Y-%m-%d'))
            html += "<div class='newsArticle'>%s</div></div>" % article
        #===================================================================
        memberList = []
        (memberList, outOf) = self.alumni.getJoinedAfter( oldAlumniTime )
        count = len(memberList)
        if count > 10:
            count = 10
        html += "<div class='newsTitle'>Member Stats"
        html += "<span class='newsDate'>%s</span></div>" % (oldNewsTime.strftime('%Y-%m-%d'))
        html += MapLinks("<div class='newsArticle'><table background='__IMAGEPATH__/semiOpaque.png' border='1'><tr>")
        if count > 0:
            html += "<td valign='top'><table>"
            for (first, nee, last, firstYear, lastYear, email, instruments, emailVisible, approved, onCommittee, id) in memberList:
                count = count - 1
                if count < 0:
                    continue
                try:
                    html += "<tr>\n"
                    html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
                    html += "<th align='left'>"
                    if onCommittee: html += CommitteeMark()
                    html += SensibleName(first,nee,last) + "</th>\n"
                    html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
                    html += "<td><i>(%d&nbsp;-&nbsp;%d)</i></td>\n" % (firstYear, lastYear)
                    html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
                    html += "<td>" + instruments + "</td>\n"
                    html += "</tr>\n"
                except:
                    html += "<tr><td colspan='4'>Record error</td></tr>"
            if len(memberList) > 0:
                html += "</table></td>"
        html += "<td valign='top'><table>"
        html += "<tr>\n"
        html += "<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
        html += MapLinks("<th>link:(#profiles,%d members signed up)" % outOf)
        html += MapLinks("<br>link:(#profiles,%d are friends)" % self.getFriendCount())
        html += MapLinks("<br>link:(#memories,%d memories added)" % self.getMemoryCount())
        html += MapLinks("<br>link:(#wallaceb,%d Wallace B. Wallace winners)" % self.getWallaceCount())
        #html += MapLinks("<br>link:(#johnNewby, only 345 John Newby prints remain)")
        html += "</tr>\n"
        html += "</table>"
        html += "</td>"

        if self.requestor is None:
            html += "<td>"
            html += self.contact_content()
            html += "</td>"

        html += "</tr></table></div>"
        #===================================================================
        memoryList = self.alumni.getMemoriesAfter(oldAlumniTime)
        count = len(memoryList)
        if count > 10:
            count = 10
        if count > 0:
            html += MapLinks( """
            <div class='newsTitle'>New Memories
            <span class='newsDate'>%s</span></div>
            <div class='newsArticle'><table width='90%%' background='__IMAGEPATH__/semiOpaque.png' border='1'><tr><td>
            """ % oldNewsTime.strftime('%Y-%m-%d') )
            for alumniId, memory, memoryTime, memoryEntryTime, memoryId in memoryList:
                count = count - 1
                if count < 0:
                    continue
                try:
                    member = self.alumni.getMemberFromId( alumniId )
                    html += "<b>%s %s</b>" % (memoryTime.strftime('%Y'), member.fullName())
                    html += "<p>%s</p>\n" % memory
                except:
                    pass
            html += '</td></tr></table></div>'
        #===================================================================
        html += "<div class='newsTitle'>"
        if showOld:
            html += MapLinks("link:(#home, %d of these %d articles are old - click here to hide them)" % (oldArticleCount, len(oldNews) + len(news)))
            for when, title, article in news:
                if (when > oldNewsTime):
                    continue
                html += "<div class='newsTitle'>"
                html += "%s<span class='newsDate'>%s</span></div>" % (title, when.strftime('%Y-%m-%d'))
                html += "<div class='newsArticle'>%s</div></div>" % article
        else:
            html += MapLinks("%d old articles not displayed, link:(#home?full=1,click here to see them)" % oldArticleCount)
        html += MapLinks( """
        <div class='copyright'>Copyright 2006 BTTB Alumni. All rights reserved.
        <br>
        Contact Us: Bob Webb - Organizing Committee Chair: send:(info@bttbalumni.ca),
        Kevin Picott, Webmaster: send:(web@bttbalumni.ca)
        </div>
        """ )
        #html += '<h1>Environment</h1>'
        #for env in os.environ:
        #    html += '<b>'
        #    html += env
        #    html += '</b>='
        #    html += os.environ[env]
        #    html += '<br>'
        return html

# ==================================================================

import unittest
class testHome(unittest.TestCase):
    def testDump(self):
        homePage = bttbHome2()
        print homePage.content()
    
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
