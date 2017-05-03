"""
Page that shows the alumni reunion concert information
"""

from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from bttbPage import bttbPage
from bttbConfig import MapLinks, Error, FacebookLink
__all__ = ['bttbConcert2017']

# Members are [FileName, RealName, DatabaseID]

WOODWINDS = [ ['AltoSax1',      'Alto Sax 1',           1]
            , ['AltoSax2',      'Alto Sax 2',           2]
            , ['TenorSax1',     'Tenor Sax',            12]
            , ['BaritoneSax',   'Baritone Sax',         28]
            , [None,            None]
            , ['Clarinet1',     'Clarinet 1',           5]
            , ['Clarinet2',     'Clarinet 2',           6]
            , ['Clarinet3',     'Clarinet 3',           7]
            , ['ClarinetEb',    'Clarinet in E&#9837;', 45]
            , ['BassClarinet',  'Bass Clarinet',        33]
            , [None,            None,                   0]
            , ['Flute1',        'Flute 1',              10]
            , ['Flute2',        'Flute 2',              34]
            , ['Piccolo',       'Piccolo',              11]
            , [None,            None,                   0]
            , ['Bassoon',       'Bassoon',              38]
            , ['Oboe',          'Oboe',                 39]
            ]

BRASS = [ ['Trumpet1',  'Trumpet 1',                      16]
        , ['Trumpet2',  'Trumpet 2',                      17]
        , ['Trumpet3',  'Trumpet 3',                      18]
        , [None,        None,                              0]
        , ['FHorn1',    'French Horn/Mellophone 1',        8]
        , ['FHorn2',    'French Horn/Mellophone 2',        9]
        , ['FHorn3',    'French Horn/Mellophone 3',       35]
        , ['FHorn4',    'French Horn/Mellophone 4',       36]
        , [None,        None,                              0]
        , ['Trombone1', 'Trombone 1',                     13]
        , ['Trombone2', 'Trombone 2',                     14]
        , ['Trombone3', 'Trombone 3',                     15]
        , ['Trombone4', 'Trombone 4',                     42]
        , [None,        None,                              0]
        , ['Baritone',  'Baritone/Euphonium Bass Clef',    3]
        , ['Euphonium', 'Baritone/Euphonium Treble Clef', 27]
        , ['Tuba',      'Tuba/Sousaphone',                 4]
        ]

PERCUSSION = [ ['SnareDrum', 'Snare Drum',          24]
             , [None,        None,                  0]
             , ['Bells',     'Bells/Glockenspiel',  26]
             , [None,        None,                  0]
             , ['Cymbals',   'Cymbals',             23]
             , [None,        None,                  0]
             , ['BassDrum',  'Bass Drum',           25]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             , [None,        None,                  0]
             ]

OTHERS = [ [None, 'Twirler',                     40]
         , [None, None,                          0]
         , [None, 'Colour Guard',                19]
         , [None, None,                          0]
         , [None, 'Majorette',                   20]
         , [None, None,                          0]
         , [None, 'Not Specified',               46]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         , [None, None,                          0]
         ]

#----------------------------------------------------------------------
def page_js():
    ''':return: A string with the Javascript specific to this page'''
    return """<script>
    //
    // Method called when the form to set an instrument is submitted.
    // Use the POST method to avoid exposing any information in the submission.
    // Updates the button and status information based on the returned value.
    //
    function submit_to_concert()
    {
        var form_url = '/cgi-bin/bttbConcert2017.cgi';
        var return_value = 0;
        $.ajax( {
            type    :   "POST",
            url     :   form_url,
            data    :   $('#concert_form').serialize(),
            success :   function(data)
                        {
                            if( data[0] === "0" )
                            {
                                $('#concert-status').attr( 'class', 'status-not' );
                                $('#concert-status').html( 'Not Signed Up' );
                                $('#concert-action').attr( 'value', 'Sign Up' );
                                $('#position-query').html( '-- Select Marching Position --' );
                            }
                            else if( data[0] === "1" )
                            {
                                $('#concert-status').attr( "class", "status-in" );
                                $('#concert-status').html( "Signed Up" );
                                $('#concert-action').attr( "value", "Change Instrument" );
                                $('#position-query').html( '-- Not Going To March --' );
                            }
                            else
                            {
                                $('#concert-status').attr( "class", "status-err" );
                                $('#concert-status').html( "ERR: Try Again" );
                            }
                        },
            error   :   function(data)
                        {
                            $('#concert-status').attr( "class", "status-err" );
                            $('#concert-status').html( "ERR: Try Again" );
                        }
        } );
    }
</script>"""

#----------------------------------------------------------------------
def page_css():
    ''':return: A string with the CSS specific to this page'''
    return """<style>
/* Three status types used for the current concert status */
.status-not /* Not in the concert - red */
{
    font-size:   16pt;
    font-weight: bold;
    color:       #AF4C50;
}
.status-in /* In the concert - green */
{
    font-size:   16pt;
    font-weight: bold;
    color:       #4CAF50;
}
.status-err /* Processing error - italic red */
{
    font-size:   16pt;
    font-weight: bold;
    font-style:  italic;
    color:       #AF4C50;
}

/* Format for the current instrumentation count */
.count
{
    font-size:   16pt;
    font-weight: bold;
    color:       #AF4C50;
}

/* The music block contains the table with the download links */
.music
{
    clear:      both;
    display:    block;
    margin-top: 20px;
}

.music table
{
    border-collapse:  collapse;
    border:           1px solid #d2d2d2;
    margin-below:     20px;
}

.music th, td
{
    text-align:     left;
    padding:        4px;
    border-right:   2px solid #d2d2d2;
    width:          33%%;
}

.music th
{
    background-color: #AF4C50;
    color:            white;
}

/* Main block is the info to the left */
.main-text
{
    width:  600px;
    margin: 20px;
}
.main-text p
{
    margin-top: 20px;
}

/* concert-info is a standalone box in the main area */
.concert-info
{
    width:      500px;
    margin:     20px;
    padding:    10px;
}

.concert-info p
{
    margin:   5px;
}

/* main-image floats to the right in the main area */
.main-image
{
    float:         right;
    margin-bottom: 20px;
}
</style>"""

#----------------------------------------------------------------------
class bttbConcert2017(bttbPage):
    '''Class that generates the concert information page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find concert information', ex )

    #----------------------------------------------------------------------
    def download_column(self, instrument_info):
        '''
        :param instrument_info: Instrument information tuple (instrument_link, instrument_name, instrument_id)
        :return: HTML representing the column with a download link for the given instrument
        '''
        link = instrument_info[0]
        name = instrument_info[1]
        count = 0
        if name is None:
            return "<td></td>"

        tooltip = ''
        if instrument_info[2] in self.instrumentation:
            for player_name,_ in self.instrumentation[instrument_info[2]]:
                tooltip += '%s\n' % player_name
                count += 1
            tooltip = tooltip.replace( "'", "&quot;" )

        return "<td><a title='%s' target='music' href='/Images70th/ConcertMusic/%s.pdf'>%s</a><span class='count'>&nbsp;(%d)</span></td>" % (tooltip, link, name.replace(' ','&nbsp;'), count)

    #----------------------------------------------------------------------
    def count_column(self, part_info):
        '''
        :param part_info: Part information tuple (part_link, part_name, part_id)
        :return: HTML representing the column with no download link for the given part
        '''
        name = part_info[1]
        count = 0
        if name is None:
            return "<td></td>"

        tooltip = ''
        if part_info[2] in self.instrumentation:
            for player_name,_ in self.instrumentation[part_info[2]]:
                tooltip += '%s\n' % player_name
                count += 1
            tooltip = tooltip.replace( "'", "&quot;" )

        return "<td><a title='%s'>%s</a><span class='count'>&nbsp;(%d)</span></td>" % (tooltip, name.replace(' ','&nbsp;'), count)

    #----------------------------------------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Reunion Concert'

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks("""
        <h1>Reunion Concert 7:00 pm - Sunday June 18<sup>th</sup>, 2017</h1>
        """ )

        music = BTTBMusic()
        html += '<h2>Song Info</h2><p>%s</p>' % str(music.songs)
        html += '<h2>Instrument Info</h2><p>%s</p>' % str(music.instruments)
        html += '<h2>Sheet Music Info</h2><p>%s</p>' % str(music.sheet_music)

        html += MapLinks( """
<p>
Still to come - music download, instrument part signup, and rehearsal times. Watch for announcements on
link:(#home, the home page!) or %s.
</p>

<p>
We'll have percussion available, and keep in mind only one person can
play the set. <br>To ensure you have any other instrument you need
link:(http://www.longandmcquade.com/pdf/lmbandrentbrochure0607-insideON-FINAL.pdf, Long and McQuade in Burlington)
is offering a rental program the alumni can take advantage of.
</p>

<h1>Tentative Concert Lineup</h1>
<div class='indented'>
    <li>Eric Ford Concert March</li>
    <li><i>Drum line & Colour Guard enter.</i></li>
    <li><i>M.C. Welcome and Please Stand</i></li>
    <li>O Canada</li>
    <li>Strike up the Band</li>
    <li><i>Drum line & Colour Guard exit</i></li>
    <li>Crown Imperial</li>
    <li>Highlights from Brave</li>
    <li><i>Raffle #1 (4 prizes)</i></li>
    <li>Drum Line Feature</li>
    <li>Russian Sailors Dance </li>
    <li>Lassus Trombone (Trombone Section Feature)</li>
    <li>Junior Redcoats Music ( 2 pieces) Conducted by Bill Rolfe</li>
    <li>Big Noise (Colour Guard Feature)</li>
    <li>A Night at the Movies</li>
    <li>Raindrops Keep Falling on my Head (Alumni Majorette Feature)</li>
    <li>Dvorak Symphony #9</li>
    <li><i>Raffle #2 (3 prizes)</i></li>
    <li>Highland Cathedral</li>
    <li>Band of Brothers</li>
    <li>World in Union - <i>Colour Guard / Drum Line / Drum Majors enter</i></li>
    <li>Pride of Burlington</li>
</div>
""" % FacebookLink() )

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbConcert2017()
    TEST_PAGE.requestor = bttbMember()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
