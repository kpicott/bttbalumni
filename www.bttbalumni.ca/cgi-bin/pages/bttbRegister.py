#!env python
"""
Show the registration page
"""
import re
import bttbMember
from bttbAlumni import bttbAlumni
from bttbConfig import ErrorMsg, MapLinks, InstrumentList, PositionList
from pages.bttbPage import bttbPage

__all__ = ['bttbRegister']

#----------------------------------------------------------------------
def htmlify(orig):
    '''Turn a string into an HTML-friendly format'''
    try:
        return orig.replace("'", "\\'").replace('\n','\\n')
    except Exception:
        return orig

#----------------------------------------------------------------------
def default_text(orig,if_no_value):
    '''Format text, defaulting if empty'''
    if orig and len(orig) > 0:
        return htmlify(orig)
    return if_no_value

#----------------------------------------------------------------------
def default_checked(orig,if_no_value):
    '''Format a check status, defaulting if empty'''
    try:
        if orig:
            return 'checked'
        else:
            return ''
    except Exception:
        pass
    if if_no_value:
        return 'checked'
    return ''

#----------------------------------------------------------------------
def checkbox_code(element_id, element_name):
    '''Return HTML implementing a standard checkbox with the given ID and name'''

    name = element_name.replace( ' ', '&nbsp;' )
    return """
<td>
  <input %s_CHECK type='checkbox' class='regular-checkbox' value='1' id='%s' name='%s'/>
  <label for='%s'></label>
</td>
<td>
  <div class='tag'>%s</div>
</td>""" % (element_id,element_id,element_id,element_id,name)

#----------------------------------------------------------------------
class bttbRegister(bttbPage):
    '''Class that generates the page in which people can register for the 60th celebration'''
    def __init__(self):
        '''Set up the page'''
        bttbPage.__init__(self)

    #----------------------------------------------------------------------
    def title(self):
        ''':return: The page title'''
        return 'BTTB Alumni Registration'

    #----------------------------------------------------------------------
    @staticmethod
    def style():
        ''':return: The HTML code with the CSS that implements the page styles'''

        return """<script type='text/javascript' src='/js/bttbRegister.js'></script>
<style>
label
{
    display: inline;
}

.required
{
    color:          red;
    font-weight:    bold;
}

.regular-checkbox
{
    display: none;
}

.regular-checkbox + label
{
    background-color: #fafafa;
    border: 1px solid #cacece;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05), inset 0px -15px 10px -12px rgba(0,0,0,0.05);
    padding: 9px;
    border-radius: 3px;
    display: inline-block;
    position: relative;
}

.regular-checkbox + label:active, .regular-checkbox:checked + label:active
{
    box-shadow: 0 1px 2px rgba(0,0,0,0.05), inset 0px 1px 3px rgba(0,0,0,0.1);
}

.regular-checkbox:checked + label
{
    background-color: #e9ecee;
    border: 1px solid #adb8c0;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05), inset 0px -15px 10px -12px rgba(0,0,0,0.05), inset 15px 10px -12px rgba(255,255,255,0.1);
    color: #99a1a7;
}

.regular-checkbox:checked + label:after
{
    content:    '\\2714';
    font-size:  14px;
    position:   absolute;
    top:        -3px;
    left:       6px;
    color:      #99a1a7;
}


.tag
{
    width:          250px;
    position:       relative;
    top:            0px;
    display:        inline-block;
    float:          right;
}

.button-holder
{
    float: left;
}
</style>
"""

    #----------------------------------------------------------------------
    @staticmethod
    def vitals():
        ''':return: The HTML code implementing the table section with personal information'''

        return MapLinks(r"""
<form method='POST' accept-charset='utf-8' onsubmit='return validateRegistration();'
      name="registerForm" id="registerForm" '
      action="javascript:submit_form('/cgi-bin/bttbRegister.cgi', '#registerForm', null);">
<table cellpadding='5' width='800' class='box_shadow' border='2'>
<tr><th bgcolor='#ffaaaa'><font size='+2'>BAND ALUMNI INFORMATION</font></th></tr>
<tr><td>
  <table width='750'>
  <tr>
    <td width='350'><input type='text' placeholder='First Name' id='FirstName' name='FirstName' value='FirstNameValue' size='32'/></td>
    <td width='25'><span id='inf_FirstName' class='required'>*</span></td>
    <td width='350'><input type='text' placeholder='Current Last Name' id='CurrentLastName' name='CurrentLastName' value='CurrentLastNameValue' size='32'/></td>
    <td width='25'><span id='inf_LastName' class='required'>*</span></td>
  </tr>
  <tr>
    <td colspan='3'><input type='text' placeholder='Last Name In Band (if different)' id='LastNameInBand' name='LastNameInBand' value='LastNameInBandValue' size='32'/></td>
    <td></td>
  </tr>
  <tr>
    <td><input type='password' placeholder='Create a Password' id='Password' name='Password' value='PasswordValue' size='32'/></td>
    <td></td>
    <td><input type='text' placeholder='User ID (default is "First Last")' id='UserID' name='UserID' value='UserIDValue' size='32'/></td>
    <td></td>
  </tr>
  <tr>
    <td><input type='text' id='FirstYear' placeholder='Year Joined' name='FirstYear' value='FirstYearValue' size='4'/></td>
    <td width='25'><span id='inf_FirstYear' class='required'>*</span></td>
    <td><input type='text' id='LastYear' placeholder='Year Left' name='LastYear' value='LastYearValue' size='4'/></td>
    <td width='25'><span id='inf_LastYear' class='required'>*</span></td>
  </tr>
  <tr>
    <td><input type='text' placeholder='Highest Rank Achieved (Boys and Girls Band)' id='HighestRank' name='HighestRank' value='HighestRankValue' size='64'/></td>
    <td></td>
    <td><i>(Boys and Girls Band only)</i></td>
    <td></td>
  </tr>
  </table>
</td></tr>
""" )

    #----------------------------------------------------------------------
    @staticmethod
    def instruments():
        ''':return: HTML with the instrument section of the table.'''

        instrument_map = [ [ 'I_Flute'         , 'Flute/Piccolo' ]
                         , [ 'I_Trumpet'       , 'Trumpet/Cornet' ]
                         , [ 'I_Clarinet'      , 'Bb/Eb/Bass Clarinet' ]
                         , [ 'I_French Horn'   , 'French Horn/Mellophone' ]
                         , [ 'I_Soprano Sax'   , 'Soprano Sax' ]
                         , [ 'I_Alto Sax'      , 'Alto Sax' ]
                         , [ 'I_Tenor Sax'     , 'Tenor Sax' ]
                         , [ 'I_Baritone Sax'  , 'Baritone Sax' ]
                         , [ 'I_Colour Guard'  , 'Colour Guard' ]
                         , [ 'I_Cymbals'       , 'Cymbals' ]
                         , [ 'I_Bells'         , 'Bells/Glockenspiel' ]
                         , [ 'I_Majorette'     , 'Majorette' ]
                         , [ 'I_Tuba'          , 'Tuba/Sousaphone' ]
                         , [ 'I_Trombone'      , 'Trombone/Valve Trombone' ]
                         , [ 'I_Euphonium'     , 'Euphonium/Baritone' ]
                         , [ 'I_Triples'       , 'Triple/Quad/Quint Drums' ]
                         , [ 'I_Percussion'    , 'Other Percussion' ]
                         , [ 'I_Bass'          , 'Bass Drum' ]
                         , [ 'I_Snare'         , 'Snare Drum' ]
                         ]

        instrument_checkboxes = []
        for instrument_info in instrument_map:
            instrument_checkboxes.append( checkbox_code( instrument_info[0], instrument_info[1] ) )

        return MapLinks( """
<tr><th bgcolor='#dddddd'><font size='+2'>INSTRUMENT(S) PLAYED</font></th></tr>
<tr><td>
    <table>
      <tr>%s%s%s</tr>
      <tr>%s%s%s</tr>
      <tr>%s%s%s</tr>
      <tr>%s%s%s</tr>
      <tr>%s%s%s</tr>
      <tr>%s%s%s</tr>
      <tr>
          %s
        <td></td> <td></td>
        <td></td> <td></td>
      </tr>
      <tr>
        <td colspan='6' valign='top'><input type='text' placeholder='Other Instrument?' id='other_instrument' name='other_instrument' value='other_instrumentValue' size='32'/></td>
      </tr>
    </table>
</td></tr>
""" % tuple(instrument_checkboxes) )

    #----------------------------------------------------------------------
    @staticmethod
    def positions():
        ''':return: the HTML with the positions-held section of the table.'''

        position_map = [ [ 'P_Drum Major',     'Drum Major'     ]
                       , [ 'P_Section Leader', 'Section Leader' ]
                       , [ 'P_Loading Crew',   'Loading Crew'   ]
                       , [ 'P_Band Executive', 'Band Executive' ]
                       , [ 'P_Yearbook',       'Yearbook'       ]
                       , [ 'P_Salon Group',    'Salon Group'    ]
                       , [ 'P_Jazz Band',      'Jazz Band'      ]
                       , [ 'P_Dixieland Band', 'Dixieland Band' ]
                       , [ 'P_Choir',          'Choir'          ]
                       , [ 'P_Dance Band',     'Dance Band'     ]
                       , [ 'P_Winter Guard',   'Winter Guard'   ]
                       ]

        position_checkboxes = []
        for position_info in position_map:
            position_checkboxes.append( checkbox_code( position_info[0], position_info[1] ) )

        return MapLinks( """
<tr><th bgcolor='#dddddd'><font size='+2'>OTHER POSITIONS HELD</font></th></tr>
<tr><td>
    <table>
    <tr>%s%s%s</tr>
    <tr>%s%s%s</tr>
    <tr>%s%s%s</tr>
    <tr>
        %s
        %s
        <td></td> <td></td>
    </tr>
    <tr>
        <td colspan='6'><input type='text' placeholder='Any Others?' id='OtherPosition' name='OtherPosition' value='OtherPositionValue' size='32'/></td>
    </tr>
    </table>
</td></tr>
</table>
""" % tuple(position_checkboxes) )

    #----------------------------------------------------------------------
    @staticmethod
    def contact():
        ''':return: HTML with the contact section of the table.'''

        return MapLinks( r"""
<p>&nbsp;</p>

<table width='800' class='box_shadow' border='2'>
<tr><th bgcolor='#ffaaaa'><font size='+2'>CONTACT INFORMATION</font></th></tr>
<tr><td>
  <table width='780'>
  <tr>
    <td width='50%'><input type='text' placeholder='Street Address' id='Street1' name='Street1' value='Street1Value' size='32' \></td>
    <td width='50%'><input type='text' placeholder='Apt/Suite' id='Apt' name='Apt' value='AptValue' size='32' \></td>
  </tr>
  <tr>
    <td><input type='text' placeholder="Street (cont'd)" id='Street2' name='Street2' value='Street2Value' size='32' \></td>
    <td><input type='text' placeholder='City' id='City' name='City' size='32' value='CityValue' \></td>
  </tr>
  <tr>
    <td><input type='text' placeholder='Province/State' id='Province' name='Province' size='32' value='ProvinceValue' \></td>
    <td><input type='text' placeholder='Country' id='Country' name='Country' size='32' value='CountryValue' \></td>
  </tr>
  <tr>
    <td><input type='text' placeholder='PC/Zip' id='PostalCode' name='PostalCode' value='PostalCodeValue' size='32'></td>
    <td><input type='text' placeholder='Phone' id='Phone' name='Phone' value='PhoneValue' size='16'></td>
  </tr>
  <tr>
    <td><input type='text' placeholder='Email' id='Email' name='Email' value='EmailValue' size='32'></td>
    <td width='25'><span id='inf_Email' class='required'>*</span></td>
  </tr>
  </table>

<p id='disclaimer' align='center'><b>Please note that personal information
will only be used for BTTB Alumni planning purposes.</b><br>
<input KeepPrivate_CHECK type='checkbox' value='1' id='KeepPrivate' name='KeepPrivate'>&nbsp;Check here if you
do not wish your information to be visible on the website.</input>
</p>
</td></tr></table>
        """)

    #----------------------------------------------------------------------
    @staticmethod
    def memory():
        ''':return: HTML with the special-memory section of the table.'''

        return MapLinks( """
<table width='800' class='box_shadow' border='2'>
<tr><th bgcolor='#ffaaaa'>SPECIAL MEMORY</font></th></tr>
<tr><td>
    <textarea rows='10' placeholder='Please share a special memory of your time in the band' id='SpecialTime' name='SpecialTime' cols='86'>MemoryValue</textarea><input type='hidden' id='SpecialTimeId' name='SpecialTimeId' value='memory_id'>
</td></tr></table>

<p><input type='submit' value='Submit Profile' name='Submit'>
   <input type='reset' value='Reset All Fields' name='Reset'>
</p>
<br><div class='copyright'>Note: All entries may be reviewed and edited for content, spelling, or other reasons at the sole discretion of the editor.</div>
        """)

    #----------------------------------------------------------------------
    def content(self):
        ''':return: a string with the content for this web page.'''

        html = self.style()

        try:
            member_id = int(self.param('id'))
        except Exception:
            # Set up a fake number
            member_id = -1
        if member_id < 0 and self.requestor:
            member_id = self.requestor.id

        html += "<p><b>"
        if member_id >= 0:
            html += "Thanks for helping to keep your information up to date!"
        else:
            html += "Thanks for taking the time to reconnect!"
        html += "</b></p>"

        html += self.vitals()
        html += self.instruments()
        html += self.positions()
        html += self.contact()
        html += "<p>&nbsp;</p>"
        html += self.memory()

        # If this is an edit then flag it so that the registration processing knows
        if member_id >= 0:
            html += "<input type='hidden' name='edit' value='1' />\n"

        try:
            alumni = bttbAlumni()
            member = alumni.getMemberFromId(member_id)
            # Create a dummy value with all defaults so that the code can be
            # shared whether there is a member as template or not.
            if not member:
                member = bttbMember.bttbMember()
            html += "<input type='hidden' name='id' value='%d' />\n" % member_id
            html = html.replace( 'FirstNameValue', default_text(member.first,'') )
            html = html.replace( 'LastNameInBandValue', default_text(member.nee,'') )
            html = html.replace( 'CurrentLastNameValue', default_text(member.last,'') )
            html = html.replace( 'PasswordValue', default_text(member.password,'') )
            html = html.replace( 'UserIDValue', default_text(member.user_id,'') )
            html = html.replace( 'FirstYearValue', default_text('%s' % member.firstYear,'') )
            html = html.replace( 'LastYearValue', default_text('%s' % member.lastYear,'') )
            html = html.replace( 'Street1Value', default_text(member.street1,'') )
            html = html.replace( 'Street2Value', default_text(member.street2,'') )
            html = html.replace( 'AptValue', default_text(member.apt,'') )
            html = html.replace( 'CityValue', default_text(member.city,'Burlington' ) )
            html = html.replace( 'ProvinceValue', default_text(member.province,'Ontario' ) )
            html = html.replace( 'CountryValue', default_text(member.country,'Canada' ) )
            html = html.replace( 'PostalCodeValue', default_text(member.postalCode,'') )
            html = html.replace( 'EmailValue', default_text(member.email,'') )
            html = html.replace( 'PhoneValue', default_text(member.phone,'') )
            html = html.replace( 'KeepPrivate_CHECK', default_checked(not member.make_public,0) )
            html = html.replace( 'HighestRankValue', default_text(member.rank,'') )
            other_instruments = []
            full_instruments = InstrumentList()
            for instrument in member.instruments:
                if instrument in full_instruments:
                    instrument_name = ' I_%s_CHECK' % (instrument)
                    html = re.sub( instrument_name, ' checked', html )
                else:
                    other_instruments.append( instrument )
            html = html.replace( 'other_instrumentValue', default_text(', '.join(other_instruments),'' ) )
            html = re.sub( ' I_(.*)_CHECK ', ' ', html )
            other_positions = []
            full_positions = PositionList()
            for position in member.positions:
                if position in full_positions:
                    position_name = ' P_%s_CHECK' % (position)
                    html = re.sub( position_name, ' checked', html )
                else:
                    other_positions.append( position )
            html = html.replace( 'OtherPositionValue', default_text(', '.join(other_positions),'' ) )
            html = re.sub( ' P_(.*)_CHECK ', ' ', html )
            memory_list = alumni.get_memories(member_id)
            old_memory = ''
            if len(memory_list) > 0:
                _, the_memory, _, _, memory_id = memory_list[0]
                html = html.replace( 'memory_id', '%d' % memory_id )
                old_memory = the_memory
            else:
                html = html.replace( 'memory_id', '-1' )
            html = html.replace( 'MemoryValue', default_text(old_memory,'') )
        except Exception, ex:
            html += ErrorMsg( 'Form error', ex )

        html += '</form>\n'
        return html

# ==================================================================

if __name__ == '__main__':
    TEST_PAGE = bttbRegister()
    print TEST_PAGE.content()

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
