#!env python
"""
Show the registration page
"""
import re
import os
import os.path
import bttbMember
from bttbAlumni import *
from bttbConfig import *
from bttbPage import bttbPage

__all__ = ['bttbRegister']

def htmlify(orig):
	try:
		return orig.replace("'", "\\'").replace('\n','\\n')
	except:
		return orig

def defText(orig,ifNoValue):
	if orig and len(orig) > 0:
		return htmlify(orig)
	return ifNoValue

def defCheck(orig,ifNoValue):
	try:
		if orig:
			return 'checked'
		else:
			return ''
	except:
		pass
	if ifNoValue:
		return 'checked'
	return ''

class bttbRegister(bttbPage):
	def __init__(self):
		bttbPage.__init__(self)

	def getField(self,name,value):
		try:
			return "$('" + name + "').value = '" + value.replace("'", "\\'") + "';"
		except:
			return ""

	def title(self):	return 'BTTB Alumni Registration'

	def scripts(self):	return [ '__CSSPATH__/formValidation.css',
								 '__JAVASCRIPTPATH__/formValidation.js',
								 '__JAVASCRIPTPATH__/bttbRegister.js' ]

	def content(self):
		try:
			id = int(self.param('id'))
		except:
			# Set up a fake number
			id = -1
		if id < 0 and self.requestor:
			id = self.requestor.id
		html = "<p><b>"
		if id >= 0:
			html += "Thanks for helping to keep your information up to date!"
		else:
			html += "Thanks for taking the time to reconnect!"
		html += "</b></p>"

		html += MapLinks("""
<form method='POST' onsubmit='return validateRegistration();' 
	  name="registerForm" id="registerForm" '
	  action="javascript:submitForm('registerForm', '/cgi-bin/bttbRegister.cgi', '/#thanks');">
<table border='2'>
<tr><th bgcolor='#ffaaaa'><font size='+2'>BAND ALUMNI INFORMATION</font></th></tr>
<tr><td>
  <table>
  <tr>
  	<th align='right'>First Name:</th>
	<td><input type='text' id='FirstName' onchange="validatePresent(this,'inf_firstName');" name='FirstName' value='FirstNameValue' size='32'></td>
	<td id='inf_firstName'>Required</td>
  </tr>
  <tr>
  	<th align='right'>Current Last Name:</th>
	<td><input type='text' id='CurrentLastName' onchange="validatePresent(this,'inf_lastName');" name='CurrentLastName' value='CurrentLastNameValue' size='32'></td>
	<td id='inf_lastName'>Required</td>
  </tr>
  <tr>
  	<th valign='top' align='right'>Last Name While in Band:</th>
  	<td><input type='text' id='LastNameInBand' name='LastNameInBand' value='LastNameInBandValue' size='32'></td>
	<td><i>(if different)</i></td>
  </tr>
  <tr>
  	<th valign='top' align='right'>Password for website login:</th>
  	<td><input type='password' id='Password' name='Password' value='PasswordValue' size='32'></td>
	<td><i>(login will be 'FIRSTNAME LASTNAME')</i></td>
  </tr>
  <tr>
  	<th align='right'>First Year in Band:</th>
	<td><input type='text' id='FirstYear' onchange="validatePresent(this,'inf_firstYear');" name='FirstYear' value='FirstYearValue' size='4'></td>
	<td id='inf_firstYear'>Required</td>
  </tr>
  <tr>
	<th align='right'>Last Year in Band</th>
	<td><input type='text' id='LastYear' onchange="validatePresent(this,'inf_lastYear');" name='LastYear' value='LastYearValue' size='4'></td>
	<td id='inf_lastYear'>Required</td>
  </tr>
  <tr>
  	<th valign='top' align='right'>Highest rank achieved:</th>
  	<td valign='top'><input type='text' id='HighestRank' name='HighestRank' value='HighestRankValue' size='32'></td>
	<td><i>(Boys and Girls Band only)</i></td>
  </tr>
  <tr>
  	<th valign='top' align='right'>Instrument(s) Played:</th>
	<td colspan='2'><table><tr>
		<td valign='top'><input I_Flute_CHECK type='checkbox' value='1' id='I_Flute' name='I_Flute'>Flute/Piccolo</input></td>
		<td valign='top'><input I_Trumpet_CHECK type='checkbox' value='1' id='I_Trumpet' name='I_Trumpet'>Trumpet/Cornet</input></td>
		<td valign='top'><input I_Clarinet_CHECK type='checkbox' value='1' id='I_Clarinet' name='I_Clarinet'>Clarinet/Bass Clarinet</input></td>
	</tr><tr>
		<td valign='top'><input I_French Horn_CHECK type='checkbox' value='1' id='I_French Horn' name='I_French Horn'>French Horn/Mellophone</input></td>
		<td valign='top'><input I_Soprano Sax_CHECK type='checkbox' value='1' id='I_Soprano Sax' name='I_Soprano Sax'>Soprano Sax</input></td>
		<td valign='top'><input I_Alto Sax_CHECK type='checkbox' value='1' id='I_Alto Sax' name='I_Alto Sax'>Alto Sax</input></td>
	</tr><tr>
		<td valign='top'><input I_Tenor Sax_CHECK type='checkbox' value='1' id='I_Tenor Sax' name='I_Tenor Sax'>Tenor Sax</input></td>
		<td valign='top'><input I_Baritone Sax_CHECK type='checkbox' value='1' id='I_Baritone Sax' name='I_Baritone Sax'>Baritone Sax</input></td>
		<td valign='top'><input I_Colour Guard_CHECK type='checkbox' value='1' id='I_Colour Guard' name='I_Colour Guard'>Colour Guard</input></td>
	</tr><tr>
		<td valign='top'><input I_Cymbals_CHECK type='checkbox' value='1' id='I_Cymbals' name='I_Cymbals'>Cymbals</input></td>
		<td valign='top'><input I_Bells_CHECK type='checkbox' value='1' id='I_Bells' name='I_Bells'>Bells</input></td>
		<td valign='top'><input I_Majorette_CHECK type='checkbox' value='1' id='I_Majorette' name='I_Majorette'>Majorette</input></td>
	</tr><tr>
		<td valign='top'><input I_Tuba_CHECK type='checkbox' value='1' id='I_Tuba' name='I_Tuba'>Tuba/Sousaphone</input></td>
		<td valign='top'><input I_Trombone_CHECK type='checkbox' value='1' id='I_Trombone' name='I_Trombone'>Trombone/Valve Trombone</input></td>
		<td valign='top'><input I_Euphonium_CHECK type='checkbox' value='1' id='I_Euphonium' name='I_Euphonium'>Euphonium/Baritone</input></td>
	</tr><tr>
		<td valign='top'><input I_Triples_CHECK type='checkbox' value='1' id='I_Triples' name='I_Triples'>Triple/Quad Drums</input></td>
		<td valign='top'><input I_Percussion_CHECK type='checkbox' value='1' id='I_Percussion' name='I_Percussion'>Other Percussion</input></td>
		<td valign='top'><input I_Bass_CHECK type='checkbox' value='1' id='I_Bass' name='I_Bass'>Bass Drum</input></td>
	</tr><tr>
		<td valign='top'><input I_Snare_CHECK type='checkbox' value='1' id='I_Snare' name='I_Snare'>Snare Drum</input></td>
		<td valign='top' colspan='2'>Other? <input type='text' id='OtherInstrument' name='OtherInstrument' value='OtherInstrumentValue' size='32'/></td>
	</tr></table></td>
  </tr>

  <tr><td colspan='3'>&nbsp;</td></tr>

  <tr>
	<th valign='top' align='right'>Other positions held:</th>
	<td colspan='2'><table><tr>
		<td><input P_Drum Major_CHECK type='checkbox' value='1' id='P_Drum Major' name='P_Drum Major'>Drum Major</input></td>
		<td><input P_Section Leader_CHECK type='checkbox' value='1' id='P_Section Leader' name='P_Section Leader'>Section Leader</input></td>
		<td><input P_Loading Crew_CHECK type='checkbox' value='1' id='P_Loading Crew' name='P_Loading Crew'>Loading Crew</input></td>
	</tr><tr>
		<td><input P_Band Executive_CHECK type='checkbox' value='1' id='P_Band Executive' name='P_Band Executive'>Band Executive</input>
		<td><input P_Yearbook_CHECK type='checkbox' value='1' id='P_Yearbook' name='P_Yearbook'>Yearbook</input></td>
		<td><input P_Salon Group_CHECK type='checkbox' value='1' id='P_Salon Group' name='P_Salon Group'>Salon Group</input></td>
	</tr><tr>
		<td><input P_Jazz Band_CHECK type='checkbox' value='1' id='P_Jazz Band' name='P_Jazz Band'>Jazz Band</input></td>
		<td><input P_Dixieland Band_CHECK type='checkbox' value='1' id='P_Dixieland Band' name='P_Dixieland Band'>Dixieland Band</input></td>
		<td><input P_Choir_CHECK type='checkbox' value='1' id='P_Choir' name='P_Choir'>Choir</input>
	</tr><tr>
		<td><input P_Dance Band_CHECK type='checkbox' value='1' id='P_Dance Band' name='P_Dance Band'>Dance Band</input></td>
		<td colspan='2'>Other? <input type='text' id='OtherPosition' name='OtherPosition' value='OtherPositionValue' size='32'/></td>
	</tr></table></td>
  </tr>
  </table>
</td></tr>
</table>

<p>&nbsp;</p>

<table border='2'>
<tr><th bgcolor='#ffaaaa'><font size='+2'>CONTACT INFORMATION</font></th></tr>
<tr><td>
  <table>
  <tr>
  	<th align='right'>Street Address:</th>
	<td><input type='text' id='Street1' name='Street1' value='Street1Value' size='32' \></td>
	<th align='right'>Apt/Suite:</th>
	<td><input type='text' id='Apt' name='Apt' value='AptValue' size='32' \></td>
  </tr>
  <tr>
  	<th align='right'>Street (cont'd):</th>
	<td><input type='text' id='Street2' name='Street2' value='Street2Value' size='32' \></td>
  	<th align='right'>City:</th>
	<td><input type='text' id='City' name='City' size='32' value='CityValue' \></td>
  </tr>
  <tr>
  	<th align='right'>Province/State:</th>
	<td><input type='text' id='Province' name='Province' size='32' value='ProvinceValue' \></td>
  	<th align='right'>Country:</th>
	<td><input type='text' id='Country' name='Country' size='32' value='CountryValue' \></td>
  </tr>
  <tr>
  	<th align='right'>Postal Code/Zip:</th>
	<td><input type='text' id='PostalCode' name='PostalCode' value='PostalCodeValue' size='32'></td>
  	<th align='right'>Phone:</th>
	<td><input type='text' id='Phone' name='Phone' value='PhoneValue' size='16'></td>
  </tr>
  <tr>
  	<th align='right'>Email:</th>
	<td><input type='text' id='Email' onchange="validateEmail(this,'inf_email',true);" name='Email' value='EmailValue' size='32'></td>
  	<td colspan='2' id='inf_email'>&nbsp;</td>
  </tr>
</table>
<p id='disclaimer' align='center'><b>Please note that personal information
will only be used for BTTB Alumni planning purposes.</b><br>
<input KeepPrivate_CHECK type='checkbox' value='1' id='KeepPrivate' name='KeepPrivate'>&nbsp;Check here if you
do not wish your email visible on the 'Profiles' page.</input>
</p>
</td></tr></table>

<p>&nbsp;</p>

<table border='2'>
<tr><th bgcolor='#ffaaaa'>SPECIAL MEMORY</font></th></tr>
<tr><td>
  	Please share a special memory of your time in the band:
	<br/>
	<textarea rows='10' id='SpecialTime' name='SpecialTime' cols='86'>MemoryValue</textarea><input type='hidden' id='SpecialTimeId' name='SpecialTimeId' value='MEMORYID'
</td></tr></table>

<p><input type='submit' value='Submit Profile' name='Submit'>
   <input type='reset' value='Reset All Fields' name='Reset'>
</p>
<br><div class='copyright'>Note: All entries may be reviewed and edited for content, spelling, or other reasons at the sole discretion of the editor.</div>
		""")
		try:
			alumni = bttbAlumni()
			member = alumni.getMemberFromId(id)
			# Create a dummy value with all defaults so that the code can be
			# shared whether there is a member as template or not.
			if not member:
				member = bttbMember.bttbMember()
			html += "<input type='hidden' name='id' value='%d' />\n" % (-id)
			html = html.replace( 'FirstNameValue', defText(member.first,'') )
			html = html.replace( 'LastNameInBandValue', defText(member.nee,'') )
			html = html.replace( 'CurrentLastNameValue', defText(member.last,'') )
			html = html.replace( 'PasswordValue', defText(member.password,'') )
			html = html.replace( 'FirstYearValue', defText('%s' % member.firstYear,'') )
			html = html.replace( 'LastYearValue', defText('%s' % member.lastYear,'') )
			html = html.replace( 'Street1Value', defText(member.street1,'') )
			html = html.replace( 'Street2Value', defText(member.street2,'') )
			html = html.replace( 'AptValue', defText(member.apt,'') )
			html = html.replace( 'CityValue', defText(member.city,'Burlington' ) )
			html = html.replace( 'ProvinceValue', defText(member.province,'Ontario' ) )
			html = html.replace( 'CountryValue', defText(member.country,'Canada' ) )
			html = html.replace( 'PostalCodeValue', defText(member.postalCode,'') )
			html = html.replace( 'EmailValue', defText(member.email,'') )
			html = html.replace( 'PhoneValue', defText(member.phone,'') )
			html = html.replace( 'KeepPrivate_CHECK', defCheck(not member.emailVisible,0) )
			html = html.replace( 'HighestRankValue', defText(member.rank,'') )
			otherInstruments = []
			fullInstruments = InstrumentList()
			for instrument in member.instruments:
				if instrument in fullInstruments:
					iName = ' I_%s_CHECK' % (instrument)
					html = re.sub( iName, ' checked', html )
				else:
					otherInstruments.append( instrument )
			html = html.replace( 'OtherInstrumentValue', defText(', '.join(otherInstruments),'' ) )
			html = re.sub( ' I_(.*)_CHECK ', ' ', html )
			otherPositions = []
			fullPositions = PositionList()
			for position in member.positions:
				if position in fullPositions:
					pName = ' P_%s_CHECK' % (position)
					html = re.sub( pName, ' checked', html )
				else:
					otherPositions.append( position )
			html = html.replace( 'OtherPositionValue', defText(', '.join(otherPositions),'' ) )
			html = re.sub( ' P_(.*)_CHECK ', ' ', html )
			memoryList = alumni.getMemories(id)
			oldMemory = ''
			if len(memoryList) > 0:
				alumniId, oldMemory, memoryTime, memoryEntryTime, memoryId = memoryList[0]
				html = html.replace( 'MEMORYID', '%d' % memoryId );
			else:
				html = html.replace( 'MEMORYID', '-1' )
			html = html.replace( 'MemoryValue', defText(oldMemory,'') )
		except Exception, e:
			html += ErrorMsg( 'Form error', e )
			pass

		html += '</form>\n'
		return html

# ==================================================================

import unittest
class testRegister(unittest.TestCase):
	def testDump(self):
		page = bttbRegister()
		print page.content()
	
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
