"""
Page that shows the alumni reunion Sound of Music Festival parade information
"""

from bttbMember import bttbMember
from bttbAlumni import bttbAlumni
from pages.bttbPage import bttbPage
from bttbMusic import BTTBMusic
from bttbConfig import MapLinks, Error
__all__ = ['bttbParade2017']

# Hardcoded value from the events table
PARADE_EVENT_ID = 12

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
                                $('#parade-action').attr( 'value', 'Sign Up Now' );
                                $('#position-query').html( '-- Select Parade Part --' );
                            }
                            else if( data[0] === "1" )
                            {
                                $('#parade-status').attr( "class", "status-in" );
                                $('#parade-status').html( "Signed Up" );
                                $('#parade-action').attr( "value", "Change Instrument" );
                                $('#position-query').html( '-- Not Going To Play --' );
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
    font-size:   10pt;
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
    width:      100%;
    margin:     20px auto;
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

th.rotate
{
  height: 140px;
  white-space: nowrap;
}

th.rotate > div
{
  transform: 
    /* Magic Numbers */
    translate(25px, 51px)
    /* 45 is really 360 - 45 */
    rotate(315deg);
  width: 30px;
}

th.rotate > div > span
{
  border-bottom: 1px solid #ccc;
  padding: 5px 10px;
}

th.row-header
{
    padding: 0 10px;
    border-bottom: 1px solid #ccc;
}
</style>"""

#----------------------------------------------------------------------
class bttbParade2017(bttbPage):
    '''Class that generates the parade information page'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)
        self.members_only = True
        self.parts_available = []
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
            self.instrumentation[instrument_id] = self.instrumentation.get(instrument_id, []) + [full_name]

    #----------------------------------------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Reunion Parade Band'

    #----------------------------------------------------------------------
    @staticmethod
    def get_sidebar():
        ''':return: HTML code to show the instruction paragraph'''
        return '<div class="main-image"><img src="/Images70th/Parade.jpg"></div>'

    #----------------------------------------------------------------------
    @staticmethod
    def get_instructions():
        ''':return: HTML code to show the instruction paragraph'''
        return '''
<div class="main-text">
<p>
Below is a list of the instrumentation available for the parade music.
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
<p>
Here are some of the songs you will be playing:<ol>
<li>download:(/Music/TheEricFordConcertMarch.mp3,Eric Ford Concert March)</li>
<li>download:(/Music/Singing In The Rain.mp3,Singing In The Rain)</li>
<li>download:(/Music/PrinceOfThieves.mp3,Prince of Thieves)</li>
</ol>
</p>
'''

    #----------------------------------------------------------------------
    def get_signup(self, all_instruments, instrument_map):
        '''
        :param all_instruments: Sorted list of instrument keys
        :param instrument_map: Map of instrument name to instrument ID
        :return: HTML code to show the signup information so far and form to change it
        '''
        # Initialize status info as being not signed up
        instrument_selected = 0
        signup_status = 'Not Signed Up'
        submit_string = 'Sign Up Now'
        signup_class = 'status-not'

        # If the member is signed up then change status strings to indicate that
        signed_up = self.alumni.get_parade_part_2017( self.requestor.id )
        if signed_up is not None:
            signup_status = 'Signed Up'
            submit_string = 'Edit My Info'
            signup_class = 'status-in'
            instrument_selected = signed_up[0]

        # Build the instrument selector from the list of available instruments,
        # using slot 0 to indicate no selection
        instrument_selector = '<select class="dropdown" name="instrument" id="instrument">'
        instrument_selector += '<option id="position-query" value="0">-- Select Part --</option>'
        for instrument in all_instruments:
            select = ''
            instrument_id = instrument_map[instrument]
            try:
                if instrument_id == instrument_selected:
                    select = ' selected'
                instrument_selector += '<option value="%s"%s>%s</option>' % ( instrument_id, select, instrument )
            except Exception:
                pass
        instrument_selector += '</select>'

        return """
<div class='parade-info box_shadow'>
<form method='POST' name='parade_form' id='parade_form' action='javascript:submit_to_parade();'>
<input type='hidden' name='id' value='%d'>
<p>
Your parade Status : <span id='parade-status' class='%s'>%s</span><br>
</p><p>
Instrument Choice : %s<br>
</p><p>
<input id='parade-action' class='shadow_button' type='submit' name='submit' value='%s'><br>
</form>
</div>""" % (self.requestor.id, signup_class, signup_status, instrument_selector, submit_string)

    #----------------------------------------------------------------------
    def download_header(self, instrument_id, instrument):
        '''
        :param instrument_id: ID of instrument in this row
        :param instrument: Name of instrument in this row
        :return: HTML content showing the instrument row header content
                 including a tooltip with the players and a count
        '''
        # Calculate the tooltip as the names of the current players
        tooltip = ''
        count = 0
        if instrument_id in self.instrumentation:
            for player_name in self.instrumentation[instrument_id]:
                tooltip += '%s\n' % player_name
                count += 1
            tooltip = tooltip.replace( "'", "&quot;" )

        return "<a title='%s'>%s<span class='count'>&nbsp;(%d)</span></a></td>" % (tooltip, instrument.replace(' ','&nbsp;'), count)

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''
        html = MapLinks("""
        %s
        %s
        <h1>Reunion Parade 7:00 pm - Sunday June 18<sup>th</sup>, 2017</h1>
        """ % (page_css(), page_js()) )

        # Read the playlist for the parade
        # Construct the union of all instruments
        # Write (vertically) the name of all songs
        # For each instrument in the list
        #   Write the instrument (with signup count in brackets)
        #   For each song
        #       Write out a download link
        music = BTTBMusic()
        playlist = music.get_playlist(PARADE_EVENT_ID)

        # Gather up the union of all songs and instruments.
        # Translate the ID information available into song and instrument names.
        all_songs = {}
        all_instruments = {}
        instrument_map = {}
        for song_info in playlist:
            song_id = song_info[0]
            song_name = song_info[1]
            all_songs[song_name] = True
            for instrument_id in music.sheet_music_lookup[song_id].keys():
                instrument_map[music.instruments[instrument_id]] = instrument_id

        # Add the non-playing participants
        instrument_map["Colour Guard"] = 19
        instrument_map["Majorette"] = 20
        instrument_map["Marching Without Instrument"] = 21
        instrument_map["Drum Major"] = 29
        instrument_map["Will Ride The Float"] = 31
        instrument_map["Twirler"] = 40

        # Since it's all automatic use alphabetical order to make parts easier to find
        all_songs = all_songs.keys()
        all_instruments = instrument_map.keys()
        all_songs.sort()
        all_instruments.sort()

        # Show the sidebar, image and tentative lineup
        html += MapLinks( self.get_sidebar() )

        # Show the instructions
        html += MapLinks( self.get_instructions() )

        # Show the signup
        html += MapLinks( self.get_signup( all_instruments, instrument_map ) )

        # Close out the main-text area so that the table can extend across
        html += '</div>'

        # Print out the download table header (song names in columns, instruments in rows)
        html += '<table>'
        html += '<tr><th class="row-header">Instrument</th>'
        for song in all_songs:
            html += '<th class="rotate"><div><span>%s</span></div></th>' % song.replace(' ', '&nbsp;')
        html += '</tr>'

        # Build the rows, adding in download links only for the parts available
        for instrument in all_instruments:
            instrument_id = music.instrument_lookup[instrument]
            html += '<tr><th class="row-header">%s</th>' % self.download_header(instrument_id,instrument)
            for song in all_songs:
                song_id = music.song_lookup[song]
                song_link = '-'
                if instrument_id in music.sheet_music_lookup[song_id]:
                    song_link = '''<a href="%s" download="%s"><i class="fa fa-chevron-circle-down"></i></a>
                    ''' % (music.sheet_music_lookup[song_id][instrument_id], song)
                html += '<td align="center">%s</td>' % song_link
            html += '</tr>'

        html += '</table>'

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
