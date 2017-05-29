# -*- coding: utf-8 -*-
"""
Placeholder for global configuration variables
"""
import re
import os
import os.path
import traceback
from urlparse import urlparse

# Global testing mode
TEST_MODE = False

MENU_BUTTON_WIDTH = 109
MENU_BUTTON_HEIGHT = 31
SUBMENU_BUTTON_WIDTH = 77
SUBMENU_BUTTON_HEIGHT = 18
ERRORS_IN_HTML = True

__all__ = [ "ArchiveFormat",
            "ArticlePath",
            "AsYYYY",
            "attend_list_2017",
            "AudioPath",
            "Backup",
            "BackupHref",
            "BandImagePath",
            "CSSPath",
            "CelebrationHref",
            "CelebrationPath",
            "CgiHref",
            "CleanupXML",
            "CommitteeAccessRequired",
            "CommitteeMark",
            "DatabasePath",
            "DataHref",
            "DataPath",
            "DbFormat",
            "DearchiveFormat",
            "DownloadLink",
            "EmailLink",
            "EmbeddedJS",
            "EmbeddedCSS",
            "EnableTestMode",
            "Error",
            "ErrorMsg",
            "ErrorsInHtml",
            "FacebookLink",
            "HomeHref",
            "HtmlifyName",
            "ImagePath",
            "InstrumentList",
            "InTestMode",
            "JavascriptPath",
            "MailChair",
            "MapLinks",
            "MemberAccessRequired",
            "MusicPath",
            "MusicURL",
            "NewsletterPath",
            "PackageImagePath",
            "PageLink",
            "PagePath",
            "PhoneFormat",
            "PhoneParts",
            "PhotoPath",
            "Pluralize",
            "PositionList",
            "PrintCGIHeader",
            "SortDictByValue",
            "SponsorImagePath",
            "TableList",
            "TicketItemPath",
            "Warning"]

#======================================================================
def InstrumentList():
    """
    List of all standard band sections
    """
    return {'Flute':1, 'Trumpet':1, 'Clarinet':1, 'French Horn':1, 'Soprano Sax':1, 'Alto Sax':1, 'Tenor Sax':1, 'Baritone Sax':1, 'Colour Guard':1, 'Cymbals':1, 'Bells':1, 'Majorette':1, 'Tuba':1, 'Trombone':1, 'Euphonium':1, 'Triples':1, 'Percussion':1, 'Bass':1, 'Snare':1}

#======================================================================
def PositionList():
    """
    List of all standard band positions
    """
    return { 'Drum Major':1, 'Section Leader':1, 'Loading Crew':1, 'Band Executive':1, 'Yearbook':1, 'Salon Group':1, 'Jazz Band':1, 'Dixieland Band':1, 'Choir':1, 'Dance Band':1 }

#======================================================================
def attend_list_2017():
    """
    List of all events to attend at the 60th. Values are the ID of the event
    in the database.
    """
    #return { 'Golf':3, 'Social':4, 'Parade':1, 'Concert':2 }
    return { 'Social':4, 'Parade':1, 'Concert':2 }

#======================================================================
rootSubst = None
rootMain = None
if not 'SERVER_ADDR' in os.environ:
    current_directory = os.getcwd()
    if current_directory.find('/test') >= 0:
        HOMEHREF = '/test'
        CGIHREF = '/cgi-bin/test'
    else:
        HOMEHREF = ''
        CGIHREF = '/cgi-bin'
    rootSubst = 'bttbalumni.ca.*'
    rootMain = 'bttbalumni.ca'
elif os.environ['SERVER_ADDR'] == '127.0.0.1':
    if 'SCRIPT_FILENAME' in os.environ:
        if os.environ['SCRIPT_FILENAME'].find( '/test/' ) >= 0:
            HOMEHREF = '/test'
            CGIHREF = '/cgi-bin/test'
        else:
            HOMEHREF = ''
            CGIHREF = '/cgi-bin'
    else:
        HOMEHREF = '/ERROR'
        CGIHREF = '/cgi-bin/ERROR'
else:
    HOMEHREF = ''
    CGIHREF = '/cgi-bin'

RE_LINK = re.compile(r'link:\((.*?)\)', re.MULTILINE)
RE_FACEBOOK = re.compile(r'facebook:\((.*?)\)', re.MULTILINE)
RE_DOWNLOAD = re.compile(r'download:\((.*?)\)', re.MULTILINE)
RE_MAIL = re.compile(r'send:\((.*?)\)', re.MULTILINE)
RE_MENU_BUTTON = re.compile(r'button:\((.*?)\)', re.MULTILINE)
RE_SUBMENU_BUTTON = re.compile(r'buttonSub:\((.*?)\)', re.MULTILINE)
#======================================================================
def MapLinks(original):
    """
    Take an HTML string with template locations and return a version with them
    all replaced by the real paths, relative to the current configuration
    """
    resolved = original.replace('__BANDIMAGEPATH__',    BandImagePath())    \
                       .replace('__PACKAGEIMAGEPATH__', PackageImagePath()) \
                       .replace('__SPONSORIMAGEPATH__', SponsorImagePath()) \
                       .replace('__TICKETITEMPATH__',   TicketItemPath())   \
                       .replace('__NEWSLETTERPATH__',   NewsletterPath())   \
                       .replace('__ARTICLEPATH__',      ArticlePath())      \
                       .replace('__BUTTONPATH__',       ButtonPath())       \
                       .replace('__MENUPATH__',         MenuPath())         \
                       .replace('__SUBMENUPATH__',      SubMenuPath())      \
                       .replace('__IMAGEPATH__',        ImagePath())        \
                       .replace('__PAGEPATH__',         PagePath())         \
                       .replace('__PHOTOPATH__',        PhotoPath())        \
                       .replace('__AUDIOPATH__',        AudioPath())        \
                       .replace('__HOMEHREF__',         HomeHref())         \
                       .replace('__DATAHREF__',         DataHref())         \
                       .replace('__BACKUPHREF__',       BackupHref())       \
                       .replace('__CSSPATH__',          CSSPath())          \
                       .replace('__BIOIMAGESPATH__',    BioImagesPath())    \
                       .replace('__INSTRUMENTPATH__',   InstrumentPath())   \
                       .replace('__MUSICPATH__',        MusicPath())        \
                       .replace('__REUNION70THPATH__',  Reunion70thPath())  \
                       .replace('__SHEETMUSICPATH__',   SheetMusicPath())   \
                       .replace('__JAVASCRIPTPATH__',   JavascriptPath())   \
                       .replace('__CELEBRATIONPATH__',  CelebrationPath())  \
                       .replace('__CELEBRATIONHREF__',  CelebrationHref())  \
                       .replace('__CGIHREF__',          CgiHref())          \
                       .replace('__ROOTPATH__',         RootPath())
    # ----------------------------------------
    matches = RE_LINK.findall( resolved )
    for link in matches:
        try:
            (url, text) = link.split(',')
        except:
            url = link
            text = url
        resolved = RE_LINK.sub( PageLink(url, text), resolved, 1 )
    # ----------------------------------------
    matches = RE_FACEBOOK.findall( resolved )
    for link in matches:
        resolved = RE_FACEBOOK.sub( FacebookLink(), resolved, 1 )
    # ----------------------------------------
    matches = RE_DOWNLOAD.findall( resolved )
    for link in matches:
        try:
            (url, text) = link.split(',')
        except:
            url = link
            text = url
        resolved = RE_DOWNLOAD.sub( DownloadLink(url, text), resolved, 1 )
    # ----------------------------------------
    matches = RE_MAIL.findall( resolved )
    for link in matches:
        try:
            (mail, who) = link.split(',')
        except:
            mail = link
            who = mail
        resolved = RE_MAIL.sub( EmailLink(mail, who), resolved, 1 )
    # ----------------------------------------
    matches = RE_MENU_BUTTON.findall( resolved )
    for link in matches:
        try:
            (url, name, title) = link.split(',')
            url = re.sub( r'soon_(.*)', r'soon?\1=1', url )
            if not name: name = url
            if not title: title = name
        except:
            url = link
            name = url
            title = name
        name = name.strip().rstrip()
        title = title.strip()
        img = MapLinks("<img src='__MENUPATH__/" + name + "Normal.png'")
        img += " width='%d'" % MENU_BUTTON_WIDTH
        img += " height='%d'" % MENU_BUTTON_HEIGHT
        img += " border='0'>"
        button_info = PageLink(url, img, title)
        button_info += "\n"
        resolved = RE_MENU_BUTTON.sub( button_info, resolved, 1 )
    # ----------------------------------------
    matches = RE_SUBMENU_BUTTON.findall( resolved )
    for link in matches:
        try:
            (url, name, title) = link.split(',')
            url = re.sub( r'soon_(.*)', r'soon?\1=1', url )
            if not name: name = url
            if not title: title = name
        except:
            url = link
            name = url
            title = name
        name = name.strip().rstrip()
        title = title.strip()
        if url.find('soon') >= 0:
            button_info = "<li class='subSoon'>\n"
        elif url.find('committee') >= 0:
            button_info = "<li class='subCommittee'>\n"
        else:
            button_info = "<li class='subMenuItem'>\n"
        img = MapLinks( "<img src='__SUBMENUPATH__/" + name + "Normal.png'")
        img += " width='%d'" % SUBMENU_BUTTON_WIDTH
        img += " height='%d'" % SUBMENU_BUTTON_HEIGHT
        img += " border='0'>"
        button_info += PageLink(url, img, title)
        button_info += "</li>\n"
        resolved = RE_SUBMENU_BUTTON.sub( button_info, resolved, 1 )
    return resolved

#======================================================================
def RootPath():
    """
    Return the path to the root directory on this machine
    """
    if 'DOCUMENT_ROOT' in os.environ:
        if os.environ['SCRIPT_FILENAME'].find( '/test/' ) >= 0:
            root = os.environ['DOCUMENT_ROOT'] + '/test'
        else:
            root = os.environ['DOCUMENT_ROOT']
    else:
        cd = os.getcwd()
        # Move to the proper directory if down in the cgi-bin area
        root = re.sub('cgi-bin.*', '', cd)
    return root

#======================================================================
def RelativeRoot():
    """
    Return the path to the content directory on this machine, relative to the
    cgi-bin directory.
    """
    root = '.'
    if 'SERVER_ADDR' in os.environ:
        if os.environ['SCRIPT_FILENAME'].find( '/test/' ) >= 0:
            root = '../../test'
        else:
            root = '..'
    else:
        # In the command line - assume at least in the subdirectory tree
        cd = os.getcwd()
        if cd.find('/cgi-bin/test') >= 0:
            root = '../../test'
        elif cd.find('/cgi-bin/') >= 0:
            root = '..'
        elif cd.find('/test/') >= 0:
            root = '.'
        else:
            root = '.'
    return root

#======================================================================
def BandImagePath():
    """ Return the path to the band images directory """
    return HOMEHREF + '/BandImages'

#======================================================================
def PackageImagePath():
    """ Return the path to the package images directory """
    return ImagePath() + '/Packages'

#======================================================================
def SponsorImagePath():
    """ Return the path to the sponsor images directory """
    return ImagePath() + '/Sponsors'

#======================================================================
def TicketItemPath():
    """ Return the path to the ticket item images directory """
    return ImagePath() + '/IndividualItems'

#======================================================================
def NewsletterPath():
    """ Return the path to the newsletter directory """
    return HOMEHREF + '/Newsletters'

#======================================================================
def ArticlePath():
    """ Return the path to the newspaper article directory """
    return HOMEHREF + '/Articles'

#======================================================================
def ButtonPath():
    """ Return the path to the navigation button directory """
    return HOMEHREF + '/Buttons'

#======================================================================
def MenuPath():
    """ Return the path to the navigation menu directory """
    return HOMEHREF + '/Menu'

#======================================================================
def SubMenuPath():
    """ Return the path to the navigation submenu directory """
    return HOMEHREF + '/Menu/SubMenu'

#======================================================================
def ImagePath():
    """ Return the path to the images directory """
    return HOMEHREF + '/Images'

#======================================================================
def PagePath():
    """ Return the path to the raw HTML page directory """
    return os.path.join( RootPath(), 'pages' )

#======================================================================
def PhotoPath():
    """ Return the path to the photos directory """
    return HOMEHREF + '/Photos'

#======================================================================
def AudioPath():
    """ Return the path to the Audio directory """
    return HOMEHREF + '/Audio'

#======================================================================
def JavascriptPath():
    """ Return the path to the Javascript source directory """
    return HOMEHREF + '/js'

#======================================================================
def CelebrationPath():
    """ Return the path to the celebration images directory """
    return os.path.join( RootPath(), 'Celebration' )

#======================================================================
def CelebrationHref():
    """ Return the HREF to the celebration images directory """
    return HOMEHREF + '/Celebration'

#======================================================================
def CSSPath():
    """ Return the path to the CSS directory """
    return HOMEHREF + '/css'

#======================================================================
def BioImagesPath():
    """ Return the path to the Committee bio images """
    return HOMEHREF + '/BioImages'

#======================================================================
def InstrumentPath():
    """ Return the path to the Instrument images """
    return HOMEHREF + '/Instruments'

#======================================================================
def MusicPath():
    """ Return the path to the new music files """
    return os.path.join( RootPath(), 'Music' )

#======================================================================
def MusicURL():
    """ Return the path to the new music files """
    return HOMEHREF + '/Music'

#======================================================================
def Reunion70thPath():
    """ Return the path to the images for the 70th anniversary reunion """
    return HOMEHREF + '/Images70th'

#======================================================================
def SheetMusicPath():
    """ Return the path to the old sheet music files """
    return HOMEHREF + '/SheetMusic'

#======================================================================
def DataHref():
    """ Return the href to the data files """
    return HOMEHREF + '/Alumni'

#======================================================================
def BackupHref():
    """ Return the href to the data file backups """
    return DataHref() + '/History'

#======================================================================
def CgiHref():
    """ Return the URL path to the main cgi-bin directory on this machine """
    return CGIHREF

#======================================================================
def HomeHref():
    """ Return the URL path to the main web directory on this machine """
    return HOMEHREF

#======================================================================
def DataPath():
    """ Return the path to the data (BTTB/Alumni) directory on this machine """
    return os.path.join( RootPath(), 'Alumni' )

#======================================================================
def HtmlifyName(name):
    """ Return the name, converted to HTML """
    html_name = name.replace( ' ', '&nbsp;' )
    html_name = html_name.replace( 'â', '&acirc;' )
    html_name = html_name.replace( 'à', '&agrave;' )
    html_name = html_name.replace( 'è', '&egrave;' )
    html_name = html_name.replace( 'á', '&aacute;' )
    html_name = html_name.replace( 'é', '&eacute;' )
    return html_name

#======================================================================
def DatabasePath():
    """ Return the path to the database backup directory on this machine """
    return os.path.join( RootPath(), 'Database' )

#======================================================================
def Pluralize(word, number):
    """ Return the word, adjusted for the plurality of the number """
    if number == 1:
        return word
    return word + 's'

#======================================================================
def AsYYYY(number):
    """ Return the number in standard YYYY format """
    if not number:    return number
    number = int(number)
    if number < 100:
        number = int(number) + 1900
    return ('%4d') % (number)

#======================================================================
def Backup(file):
    """ Backup the given file just in case it gets corrupted """
    found = False
    (bkdir,baseFile) = os.path.split(file)
    bkdir = os.path.join(bkdir, 'History')
    copiedFile = None
    if not os.path.exists(bkdir):    os.mkdir(bkdir, 0777)
    bkfile = os.path.join(bkdir, baseFile)
    if os.path.exists(bkfile):
        for i in range(0,1000):
            bkfile = os.path.join(bkdir, baseFile + '.' + (('%d') % (i)))
            if not os.path.exists(bkfile):
                found = True
                break
        if not found:
            bkfile = os.path.join(bkdir, baseFile + '.0')
            try:
                os.unlink( bkfile )
            except:
                pass
    try:
        os.rename( file, bkfile )
        copiedFile = bkfile
    except:
        pass
    return copiedFile

#======================================================================
def TableList():
    """
    Return a list of all of the tables used by the website.
    Order is important because of foreign key dependencies in the DB.
    Delete in reverse order of return.
    """
    return [ "events"
           , "instruments"
           , "music"
           , "2017_concert"
           , "2017_parade"
           , "2017_social"
           , "alumni"
           , "attendance"
           , "contact"
           , "memorials"
           , "memories"
           , "drum_majors"
           , "executive_positions"
           , "past_executive"
           , "news"
           , "pages"
           , "paid"
           , "volunteers"
           , "wallace" ]

#======================================================================
def DbFormat(src):
    """
    Return the 'src' string, formatted for entry into the database
    """
    if not src: return ''
    dst = src
    dst = dst.replace("'", "\\'").replace('%25%20', ' ').replace('%20', ' ').replace('%21', '!').replace('%2C', ',').replace('%0A', '\n').replace('%25', '%').replace('%28', '(').replace('%29', ')').replace('%27', "''").replace('%22', '"').replace('%24', '$').replace('&nbsp;', ' ')
    return dst

#======================================================================
def ArchiveFormat(src):
    """
    Return the 'src' string, formatted for entry into the archive text format
    """
    if not src: return ''
    dst = src
    dst = dst.replace('\t', '%0D').replace('\n', '%0A')
    return dst

#======================================================================
def DearchiveFormat(src):
    """
    Return the 'src' string, formatted for extraction from text into DB format
    """
    if not src: return ''
    dst = src
    dst = dst.replace('%0D', '\t').replace('%0A', '\n')
    return dst

#======================================================================
def CommitteeMark():
    """ Return some HTML marking a committee member.  """
    return '<a title="This indicates a committee member">&hearts;</a>&nbsp;'

#======================================================================
def CleanupXML(rawXml):
    """ Removes the multiple linefeeds from the rawXML prettyprint """
    return rawXml.replace('><', '>\n<')

#======================================================================
def PrintCGIHeader():
    print "Content-type: text/html"
    print "Cache-Control: no-cache, must-revalidate, no-store"
    print "Expires: Mon, 26 Jul 1997 05:00:00 GMT"
    print "Pragma: no-cache\n"

#======================================================================
def ErrorsInHtml(newFlag):
    global ERRORS_IN_HTML
    ERRORS_IN_HTML = newFlag

#======================================================================
def ErrorMsg(msg,info):
    """
    Return an error in HTML format
    """
    if ERRORS_IN_HTML:
        return "<br><font size='+3' color='red'>ERROR:</font> %s %s <br> <p>Reload this page in a few seconds to try again.</p> <p>If problem persists contact the %s .</p></body>" % (msg, info, EmailLink("web@bttbalumni.ca", "webmaster") )
    return "*** ERROR: %s\n           %s " % (msg, info)

#======================================================================
def Error(msg,info):
    """
    Print out an error in HTML format and exit
    """
    #print traceback.extract_stack()
    print ErrorMsg(msg,info)
    exit

#======================================================================
def Warning(msg,info):
    """
    Print out a warning in HTML format and return
    """
    if ERRORS_IN_HTML:
        return r"<br><font size='+3' color='red'>WARN:</font>%s %s<br> <p>Reload this page in a few seconds to try again.</p> <p>If problem persists contact the %s.</p>" % (msg, info, EmailLink("web@bttbalumni.ca", "webmaster") )
    return "*** WARNING: %s\n             %s " % (msg, info)

from binascii import hexlify
#======================================================================
def EmailLink(address, whom=None):
    """
    Returns a Javascript snippet which contains an encrypted href=mailto link
    which should protect email from spambots.
    """
    (email, location) = address.split('@')
    if not whom:
        decversion = []
        for a in address:
            decversion.append( '%d' % int(hexlify( a ),16) )
        whom = '&#' + ';&#'.join(decversion) + ';'
    email = re.sub("'", "\\'", email)
    location = re.sub("'", "\\'", location)
    return "<a class='email' href=\"javascript:makeEmail('__NOSPAM__" + email + "','__NOSPAM__" + location + "')\" title=\"send email\">" + whom + "</a>"

#======================================================================
def PageLink(newUrl, link=None, tooltip=None, colour=''):
    """
    All page switching should go through here (as opposed to an
    explicit <a> tag) so that the proper cookies and parameters are
    passed on.
    """
    (scheme, netloc, url, params, query, fragment) = urlparse(newUrl)
    if query:
        query = '/?' + query
    if len(fragment) > 0:
        newUrl = query + '#' + fragment
        if link is None:
            link = newUrl
        if tooltip is None:
            tooltip = newUrl
    if link is None:
        link = newUrl
    if tooltip is None:
        tooltip = link
    if len(colour) > 0:
        colour = "style='background:%s;'" % colour
    newUrl = re.sub("'", "\\'", newUrl)
    href = "<a class='non-link' title='%s' %s onclick=\"javascript:open_page('%s')\"" % (tooltip, colour, newUrl)
    href += ">%s</a>" % link
    return href

#======================================================================
def DownloadLink(newUrl, text=None, partial=False, colour=''):
    """
    Special link which will not open a page, but will instead request
    the user allow it to download.  Relies on it doing just that since
    I really can't check that here.
    """
    title = text
    if not text: text = newUrl
    if not title: title = text
    if len(colour) > 0: colour = "style='background:%s;'" % colour
    newUrl = re.sub("'", "\\'", newUrl)
    link = "<a target='download' %s title=\"%s\" href=\"%s\"" % (colour, title, newUrl)
    if not partial:
        link += ">%s</a>" % text
    return link

#======================================================================
def FacebookLink():
    """
    Special link to the alumni Facebook group. It's always at the same
    place so this will keep it consistent.
    """
    return "<a target='facebook' title='Alumni on Facebook' href='https://www.facebook.com/groups/2218469082/'>the alumni Facebook group</a>"

#======================================================================
def PhoneFormat(phone):
    """
    Reformat something that kind of looks like a phone number
    into a standard (AAA) XXX-NNNN format.
    """
    if phone == 'No Phone': return ''
    newPhone = re.sub( '[^0123456789]', '', phone )
    digitCount = len(newPhone)
    if digitCount == 7:
        newPhone = "(905) %s-%s" % (newPhone[0:3], newPhone[3:])
    elif digitCount == 10:
        newPhone = "(%s) %s-%s" % (newPhone[0:3], newPhone[3:6], newPhone[6:])
    elif digitCount == 12:
        newPhone = "011 %s %s %s %s" % (newPhone[0:2], newPhone[2:4], newPhone[4:8], newPhone[8:])
    elif digitCount == 15:
        newPhone = "%s %s %s %s %s" % (newPhone[0:3], newPhone[3:5], newPhone[5:7], newPhone[7:11], newPhone[11:])
    else:
        newPhone = phone
    return newPhone

#======================================================================
def PhoneParts(phone):
    """
    Analyze the phone number and return a list of two elements, comprising
    [AREA_CODE, NUMBER]
    """
    if phone == 'No Phone': return ['','','']
    newPhone = re.sub( '[^0123456789]', '', phone )
    digitCount = len(newPhone)
    if digitCount == 7:
        newPhone = ['905', newPhone[0:3], newPhone[3:]]
    elif digitCount == 10:
        newPhone = [newPhone[0:3], newPhone[3:6], newPhone[6:]]
    else:
        # Other formats are not understood by PayPal so just return blanks
        newPhone = ['','','']
    return newPhone

#======================================================================
def SortDictByValue(dict):
    """ Returns the keys of the dictionary sorted by their values """
    items = dict.items()
    backitems = [ [v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]

#======================================================================
def EmbeddedCSS(style):
    """
    Print out HTML which will embed the given style in the middle of a file.
    Mainly used to cut down on duplication of the style tags.

    If this is called with a file then make a suitable import declaration
    and make the filename relative to the root CSS directory.
    """
    html = '<style type="text/css" media="all">'
    if style[-4:] == '.css':
        html += '@import url( "%s" );' % os.path.join( CSSPath(), style )
    else:
        html += MapLinks( style )
    html += '</style>'
    return html

#======================================================================
def EnableTestMode():
    """
    Set the global state to be in testing mode
    """
    global TEST_MODE
    TEST_MODE = True

#======================================================================
def InTestMode():
    """
    Check the global test mode state
    """
    return TEST_MODE

#======================================================================
def EmbeddedJS(script):
    """
    Print out HTML which will embed the given script in the middle of a file.
    Mainly used to cut down on duplication of the script tags.

    If this is called with a file then make a suitable import declaration
    and make the filename relative to the root JS directory.
    """
    html = '<script type="text/javascript"'
    if script[-3:] == '.js':
        html += ' src="%s">' % os.path.join( JavascriptPath(), script )
    else:
        html += '>'
        html += MapLinks( script )
    html += '</script>'
    return html

#======================================================================
def CommitteeAccessRequired(title):
    """
    Return a string with the HTML for a warning that the current page with
    given title requires a committee login to access.
    """
    return """
    <h1>Committee Only Page - %s</h1>
    <p>
    Sorry, but this page is only accessible to committee members.
    </p>
    """ % title

#======================================================================
def MemberAccessRequired(title):
    """
    Return a string with the HTML for a warning that the current page with
    given title requires a member login to access.
    """
    return """
    <h1>Member Only Page - %s</h1>
    <p>
    Sorry, but this page is only accessible to logged-in members. Use the
    "LOGIN" or "REGISTER" buttons at the top of the page to gain access.
    </p>
    <p>&nbsp;</p>
    <div class="box_shadow" style="padding: 10px;">
    <h1>NOTE:</h1>
    <p>
    Login requires registration. After you have registered use
    first and last name as USERNAME - your default password is blank.
    <br>
    You may set your password (and update any other information) through
    the 'My Profile' link after you login.
    </p>
    </div>
    """ % title

import smtplib

#======================================================================
def MailChair(subject='', text='', to='web@bttbalumni.ca'):
    """
    Usage:
        MailChair('subject', 'Body of the mail')
    Send mail to one of the email addresses from the website.
    """
    subject = subject.replace( '&nbsp;', ' ' )
    text = text.replace( '&nbsp;', ' ' )

    mailContent = """From: The BTTB Alumni Website (web@bttbalumni.ca)
To: %s
Subject: %s

%s""" % (to, subject, text)

    try:
        if os.environ['REMOTE_ADDR'] != '127.0.0.1':
            mailServer = smtplib.SMTP('bttbalumni.ca')
            mailServer.sendmail('web@bttbalumni.ca', to, mailContent)
            mailServer.quit()
        else:
            print 'MAIL: ' + mailContent.replace('\n','<br>\n')
    except:
        # Mail can fail silently because it's not absolutely necessary
        pass

#==================================================================

import unittest
class testConfig(unittest.TestCase):
    def testError(self):
        error = ErrorMsg('hello', 'world')
        self.assertEqual( error, r"<br><font size='+3' color='red'>ERROR:</font> hello world <br> <p>Reload this page in a few seconds to try again.</p> <p>If problem persists contact the %s .</p></body>" % EmailLink("web@bttbalumni.ca", "webmaster") )

    def testEmail(self):
        mailto = EmailLink('web@bttbalumni.ca')
        self.assertEqual( mailto, "<a class='email' href=\"javascript:makeEmail('__NOSPAM__web','__NOSPAM__bttbalumni.ca')\" title=\"send email\">&#98;&#116;&#116;&#98;&#64;&#112;&#105;&#99;&#111;&#116;&#116;&#46;&#99;&#97;</a>" )

    def testPhone(self):
        self.assertEqual( PhoneFormat('1234567890'), '(123) 456-7890' )
        self.assertEqual( PhoneFormat('---1234567890'), '(123) 456-7890' )
        self.assertEqual( PhoneFormat('123456-7890'), '(123) 456-7890' )
        self.assertEqual( PhoneFormat('abcdefghijklj123456789!@#0$%^&*()_-+='), '(123) 456-7890' )
        self.assertEqual( PhoneFormat('---1---2---3---4---5---6---7---8---9-0--'), '(123) 456-7890' )
        self.assertEqual( PhoneFormat('4567890'), '(905) 456-7890' )
        self.assertEqual( PhoneFormat('---4567890'), '(905) 456-7890' )
        self.assertEqual( PhoneFormat('456-7890'), '(905) 456-7890' )
        self.assertEqual( PhoneFormat('abcdefghijklj456789!@#0$%^&*()_-+='), '(905) 456-7890' )
        self.assertEqual( PhoneFormat('---4---5---6---7---8---9-0--'), '(905) 456-7890' )
        self.assertEqual( PhoneParts('1234567890'), ['123','456', '7890'] )
        self.assertEqual( PhoneParts('011234567890'), ['','', ''] )
        self.assertEqual( PhoneParts('011234567890123'), ['','', ''] )
        self.assertEqual( PhoneParts('No Phone'), ['','', ''] )
        self.assertEqual( PhoneParts('---1234567890'), ['123','456', '7890'] )
        self.assertEqual( PhoneParts('123456-7890'), ['123','456', '7890'] )
        self.assertEqual( PhoneParts('abcdefghijklj123456789!@#0$%^&*()_-+='), ['123','456', '7890'] )
        self.assertEqual( PhoneParts('---1---2---3---4---5---6---7---8---9-0--'), ['123','456', '7890'] )
        self.assertEqual( PhoneParts('4567890'), ['905','456', '7890'] )
        self.assertEqual( PhoneParts('---4567890'), ['905','456', '7890'] )
        self.assertEqual( PhoneParts('456-7890'), ['905','456', '7890'] )
        self.assertEqual( PhoneParts('abcdefghijklj456789!@#0$%^&*()_-+='), ['905','456', '7890'] )
        self.assertEqual( PhoneParts('---4---5---6---7---8---9-0--'), ['905','456', '7890'] )

    def testLinks(self):
        mail1 = EmailLink('web@bttbalumni.ca', 'web@bttbalumni.ca')
        mail2 = EmailLink('web@bttbalumni.ca', 'me')
        mail3 = EmailLink('web@bttbalumni.ca', 'let me know')
        url1 = PageLink('http://url1', 'http://url1')
        url2 = PageLink('http://url1', 'who')
        url3 = PageLink('#thanks', 'thanks')
        mapping = {
            'abc 123 def 234 ': 'abc 123 def 234 '
,            'abc 123 link:(http://url1) def 234 ': 'abc 123 ' + url1 + ' def 234 '
,            'abc 123 link:(http://url1,who) def 234 ': 'abc 123 ' + url2 + ' def 234 '
,            'abc 123 link:(#thanks,thanks) def 234 ': 'abc 123 ' + url3 + ' def 234 '
,            'link:(http://url1,who) link:(#thanks,thanks)': url2 + ' ' + url3
,            'abc 123 send:(web@bttbalumni.ca) def 234 ': 'abc 123 ' + mail1 + ' def 234 '
,            'abc 123 send:(web@bttbalumni.ca,me) def 234 ': 'abc 123 ' + mail2 + ' def 234 '
,            'abc 123 send:(web@bttbalumni.ca,let me know) def 234 ': 'abc 123 ' + mail3 + ' def 234 '
            }
        for map in mapping:
            self.assertEqual( mapping[map], MapLinks(map) )

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
