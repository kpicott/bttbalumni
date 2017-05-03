"""
Page that shows the current list of parade participants and lets the currently
signed in user sign up for a specific instrument.
"""
from bttbAlumni import bttbAlumni
from bttbMember import bttbMember
from pages.bttbPage import bttbPage
from bttbConfig import MapLinks, Error
__all__ = ['bttbParade2017']

# Members are [FileName, RealName, DatabaseID]

WOODWINDS = [ ['AltoSax1',      'Alto Sax 1',           1]
            , ['AltoSax2',      'Alto Sax 2',           2]
            , ['TenorSax1',     'Tenor Sax 1',          12]
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
         , [None, 'Marching Without Instrument', 21]
         , [None, None,                          0]
         , [None, 'Will Ride the Float',         31]
         , [None, None,                          0]
         , [None, 'Drum Major',                  29]
         , [None, None,                          0]
         , [None, 'Majorette',                   20]
         , [None, None,                          0]
         , [None, 'Not Specified',               46]
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
    function submit_to_parade()
    {
        var form_url = '/cgi-bin/bttbParade2017.cgi';
        var return_value = 0;
        $.ajax( {
            type    :   "POST",
            url     :   form_url,
            data    :   $('#parade_form').serialize(),
            success :   function(data)
                        {
                            if( data[0] === "0" )
                            {
                                $('#parade-status').attr( 'class', 'status-not' );
                                $('#parade-status').html( 'Not Signed Up' );
                                $('#parade-action').attr( 'value', 'Sign Up' );
                                $('#position-query').html( '-- Select Marching Position --' );
                            }
                            else if( data[0] === "1" )
                            {
                                $('#parade-status').attr( "class", "status-in" );
                                $('#parade-status').html( "Signed Up" );
                                $('#parade-action').attr( "value", "Change Instrument" );
                                $('#position-query').html( '-- Not Going To March --' );
                            }
                            else
                            {
                                $('#parade-status').attr( "class", "status-err" );
                                $('#parade-status').html( "ERR: Try Again" );
                            }
                        },
            error   :   function(data)
                        {
                            $('#parade-status').attr( "class", "status-err" );
                            $('#parade-status').html( "ERR: Try Again" );
                        }
        } );
    }
</script>"""

#----------------------------------------------------------------------
def page_css():
    ''':return: A string with the CSS specific to this page'''
    return """<style>
/* Three status types used for the current parade status */
.status-not /* Not in the parade - red */
{
    font-size:   16pt;
    font-weight: bold;
    color:       #AF4C50;
}
.status-in /* In the parade - green */
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

/* parade-info is a standalone box in the main area */
.parade-info
{
    width:      500px;
    margin:     20px;
    padding:    10px;
}

.parade-info p
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
def instrument_name_from_id(instrument_id):
    '''
    :param instrument_id: The ID in the database of the instrument to find
    :return: The instrument name corresponding to the given id, None if not found
    '''
    for part in WOODWINDS + BRASS + PERCUSSION + OTHERS:
        if part[2] == instrument_id:
            return part[1]
    return None

#----------------------------------------------------------------------
class bttbParade2017(bttbPage):
    '''Class that generates the parade information page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find parade information', ex )

        # Read in the current instrumentation for the parade
        self.instrumentation = {}
        for parade_participant in self.alumni.get_parade_registration_2017():
            first_name,nee_name,last_name,instrument_id,needs_instrument = parade_participant
            full_name = first_name
            if len(nee_name) > 0:
                full_name += " (%s)" % nee_name
            full_name += " %s" % last_name
            self.instrumentation[instrument_id] = self.instrumentation.get(instrument_id, []) + [[full_name,needs_instrument]]

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

        return "<td><a title='%s' target='music' href='/Images70th/ParadeMusic/%s.pdf'>%s</a><span class='count'>&nbsp;(%d)</span></td>" % (tooltip, link, name.replace(' ','&nbsp;'), count)

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
        return '2017 Sound of Music Festival Parade Alumni Band'

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''

        # Initialize status info as being not signed up
        needs_instrument = 0
        instrument_selected = 0
        signup_status = 'Not Signed Up'
        submit_string = 'Sign Up Now'
        signup_class = 'status-not'

        # If the member is signed up then change status strings to indicate that
        signed_up = self.alumni.get_parade_part_2017( self.requestor.id )
        if signed_up is not None:
            signup_status = 'SIGNED UP'
            submit_string = 'Edit My Info'
            signup_class = 'status-in'
            instrument_selected, needs_instrument = signed_up

        # Build the instrument selector from the list of available instruments,
        # using slot 0 to indicate no selection
        instrument_selector = '<select class="dropdown" name="instrument" id="instrument">'
        instrument_selector += '<option id="position-query" value="0">-- Select Marching Position --</option>'
        for part in WOODWINDS + BRASS + PERCUSSION + OTHERS:
            select = ''
            try:
                if part[1] is None:
                    continue
                if part[2] == instrument_selected:
                    select = ' selected'
                instrument_selector += '<option value="%s"%s>%s</option>' % ( part[2], select, part[1] )
            except Exception:
                pass
        instrument_selector += '</select>'

        html = page_css() + page_js()

        html += MapLinks( """
<div>

<div class="main-image"><img src="/Images70th/Parade.jpg"></div>

<div class="main-text">

<h1>Alumni Band, 2017 Sound of Music Festival Parade</h1>
<p>
Below is a list of the instrumentation available for the parade.
Select a part and you will be pointed to a download of the music
for that part in format (see link:(http://www.adobe.com) for
a File Reader called Acrobat if you don't already have it).
</p>
<p>
The number beside each instrument's name indicates how many people
have signed up for that particular part.
</p>
<p>
Drums and Sousaphones will be provided by the BTTB. All other instruments
required can be rented inexpensively (no, seriously, they're dirt cheap) from
Long and McQuade as arranged by alumnus Steve Butterworth of Yamaha, Canada.
</p>
<p>
Listen to the download:(/Images70th/ParadeMusic/TheEricFordConcertMarch.mp3,Eric Ford Concert March)
to hear one of the pieces you'll be playing!
</p>

</div>
<div class='parade-info box_shadow'>
<form method='POST' name='parade_form' id='parade_form' action='javascript:submit_to_parade();'>
<input type='hidden' name='id' value='%d'>
<p>
Your Parade Status : <span id='parade-status' class='%s'>%s</span><br>
</p><p>
Instrument Choice : %s<br>
</p><p>
Need Instrument? : <input type='checkbox' name='needs_instrument' id='needs_instrument' value='%d'><br>
</p><p>
<input id='parade-action' class='shadow_button' type='submit' name='submit' value='%s'><br>
</form>
</div>

</div>
""" % (self.requestor.id, signup_class, signup_status, instrument_selector, needs_instrument, submit_string) )

        html += MapLinks( """
<div class='music'>
<h2>Click an Instrument to Download Your Music</h2>
<table>
    <tr>
        <th>Woodwinds</th>
        <th>Brass</th>
        <th>Percussion</th>
        <th>Others</th>
    </tr>""" )

        # Generate the download table, along with the current instrument counts
        for i in range(0,len(WOODWINDS)):
            html += "<tr>"

            html += self.download_column( WOODWINDS[i] )
            html += self.download_column( BRASS[i] )
            html += self.download_column( PERCUSSION[i] )
            html += self.count_column( OTHERS[i] )

            html += "</tr>"
        html += "</table>"

        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbParade2017()
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
