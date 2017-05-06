"""
Page that shows the alumni reunion concert information
"""

from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from pages.bttbPage import bttbPage
from bttbMusic import BTTBMusic
from bttbConfig import MapLinks, Error
__all__ = ['bttbConcert2017']

# Hardcoded value from the events table
CONCERT_EVENT_ID = 11

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
                                $('#position-query').html( '-- Select Concert Part --' );
                            }
                            else if( data[0] === "1" )
                            {
                                $('#concert-status').attr( "class", "status-in" );
                                $('#concert-status').html( "Signed Up" );
                                $('#concert-action').attr( "value", "Change Instrument" );
                                $('#position-query').html( '-- Not Going To Play --' );
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
        self.parts_available = []
        try:
            self.alumni = bttbAlumni()
        except Exception, ex:
            Error( 'Could not find concert information', ex )

    #----------------------------------------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Reunion Concert'

    #----------------------------------------------------------------------
    @staticmethod
    def get_sidebar():
        ''':return: HTML code to show the instruction paragraph'''
        return '''
<div class="main-image"><img src="/Images70th/Concert.jpg">

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
</div>'''

    #----------------------------------------------------------------------
    @staticmethod
    def get_instructions():
        ''':return: HTML code to show the instruction paragraph'''
        return '''
<div class="main-text">
<p>
Below is a list of the instrumentation available for the concert music.
Select a part and download the music
for that part in PDF format (see link:(http://www.adobe.com) for
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
'''

    #----------------------------------------------------------------------
    def get_signup(self):
        ''':return: HTML code to show the signup information so far and form to change it'''
        # Initialize status info as being not signed up
        instrument_selected = 0
        signup_status = 'Not Signed Up'
        submit_string = 'Sign Up Now'
        signup_class = 'status-not'

        # If the member is signed up then change status strings to indicate that
        signed_up = self.alumni.get_concert_part_2017( self.requestor.id )
        if signed_up is not None:
            signup_status = 'SIGNED UP'
            submit_string = 'Edit My Info'
            signup_class = 'status-in'
            instrument_selected = signed_up

        # Build the instrument selector from the list of available instruments,
        # using slot 0 to indicate no selection
        instrument_selector = '<select class="dropdown" name="instrument" id="instrument">'
        instrument_selector += '<option id="position-query" value="0">-- Select Part --</option>'
        for part in self.parts_available:
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

        return """
<div class='concert-info box_shadow'>
<form method='POST' name='concert_form' id='concert_form' action='javascript:submit_to_concert();'>
<input type='hidden' name='id' value='%d'>
<p>
Your Concert Status : <span id='concert-status' class='%s'>%s</span><br>
</p><p>
Instrument Choice : %s<br>
</p><p>
<input id='concert-action' class='shadow_button' type='submit' name='submit' value='%s'><br>
</form>
</div>""" % (self.requestor.id, signup_class, signup_status, instrument_selector, submit_string)

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks("""
        %s
        <h1>Reunion Concert 7:00 pm - Sunday June 18<sup>th</sup>, 2017</h1>
        """ % page_css() )

        # Show the sidebar, image and tentative lineup
        html += MapLinks( self.get_sidebar() )

        # Show the instructions
        html += MapLinks( self.get_instructions() )

        # Show the signup
        html += MapLinks( self.get_signup() )

        # Read the playlist for the concert
        # Construct the union of all instruments
        # Write (vertically) the name of all songs
        # For each instrument in the list
        #   Write the instrument (with signup count in brackets)
        #   For each song
        #       Write out a download link

        music = BTTBMusic()
        html += '<h2>Playlists</h2><p>%s</p>' % str(music.get_playlist(CONCERT_EVENT_ID))

        # Gather up the union of all songs and instruments.
        # Translate the ID information available into song and instrument names.
        all_songs = []
        all_instruments = []
        for song_id in music.sheet_music_lookup.keys():
            all_songs[music.songs[song_id]] = True
            for instrument_id,_ in music.sheet_music_lookup.values():
                all_instruments[music.instruments[instrument_id]] = True

        # Since it's all automatic use alphabetical order to make parts easier to find
        all_songs.sort( lambda x,y: cmp(y[0], x[0]) ) 
        all_instruments.sort( lambda x,y: cmp(y[0], x[0]) ) 

        html += '<h2>Songs</h2><p>%s</p>' % str(all_songs)
        html += '<h2>Instruments</h2><p>%s</p>' % str(all_instruments)

        # Print out the download table header (song names in columns, instruments in rows)
        html += '<table border="1">'
        html += '<tr>'
        for song in all_songs:
            html += '<th>%s</th>' % song
        html += '</tr>'

        # Build the rows, adding in download links only for the parts available
        for instrument in all_instruments:
            instrument_id = self.instrument_lookup[instrument]
            html += '<tr>'
            for song in all_songs:
                song_id = self.song_lookup[song]
                song_link = 'n/a'
                if instrument_id in self.sheet_music_lookup[song_id]:
                    song_link = '''<a href="%s" download="%s">Download</a>
                    ''' % (self.sheet_music_lookup[song_id][instrument_id], song)
                html += '<td>%s</td>' % song_link
            html += '</tr>'

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
