//
// Modify the instructions on output format to correspond to what changing the
// checkbox actually does.
//
outputTypeChanged = function()
{
	if( $('outputType').checked )
	{
		$('outputTypeInfo').innerHTML = 'Output will downloaded as text. Uncheck this box to see results onscreen.';
		$('dbQueryForm').action = "/cgi-bin/bttbDbQuery.cgi";
	}
	else
	{
		$('outputTypeInfo').innerHTML = 'Output will be shown on the screen. Check this box to download a text file.';
		$('dbQueryForm').action = "javascript:submitForm(\'dbQueryForm\', \'/cgi-bin/bttbDbQuery.cgi\', null);";
	}
}

//
// Modify the query to be executed based on a pre-canned selection
//
querySelect = function(whichQuery)
{
	switch( whichQuery )
	{
		case 'all':
			$('queryText').value = 'SELECT * FROM alumni';
		break;

		case 'committee':
			$('queryText').value = 'SELECT * FROM alumni WHERE onCommittee = 1';
		break;

		case 'parade':
			$('queryText').value = 'SELECT alumni.first,alumni.last,alumni.email,alumni.phone FROM alumni WHERE alumni.id IN (SELECT alumni_id FROM attendance WHERE event_id = 1) AND alumni.id NOT IN (SELECT alumni_id FROM parade);';
		break;

		case 'friday':
			$('queryText').value = 'SELECT alumni.first,alumni.last,alumni.email,alumni.phone FROM alumni WHERE alumni.id IN (SELECT alumni_id FROM attendance WHERE event_id = 4) AND alumni.id NOT IN (SELECT alumni_id FROM payments WHERE event_id = 4);';
		break;

		case 'saturday':
			$('queryText').value = 'SELECT alumni.first,alumni.last,alumni.email,alumni.phone FROM alumni WHERE alumni.id IN (SELECT alumni_id FROM attendance WHERE event_id = 5) AND alumni.id NOT IN (SELECT alumni_id FROM payments WHERE event_id = 5);';
		break;

		case 'drumline':
			$('queryText').value =  'SELECT alumni.first,alumni.nee,alumni.last,alumni.email,alumni.firstYear,alumni.lastYear, alumni.instruments FROM parade INNER JOIN alumni ON alumni.id = parade.alumni_id WHERE instruments LIKE \'%ercussion%\' OR instruments LIKE \'%Snare%\' OR instruments LIKE \'%Cymbals%\';';
		break;

		case 'contactMissing':
			$('queryText').value = 'SELECT contact.first,contact.nee,contact.last,contact.firstYear,contact.lastYear,contact.email,contact.phone FROM contact where contact.id NOT IN (SELECT contact.id FROM contact INNER JOIN alumni ON alumni.first = contact.first AND (alumni.last = contact.last OR alumni.nee = contact.last)) ORDER BY contact.last,contact.first';
		break;

		case 'duplicate':
			$('queryText').value = 'SELECT a1.*\nFROM alumni AS a1,alumni AS a2\nWHERE a1.first LIKE a2.first\n    AND a1.last LIKE a2.last\n    AND a1.id <> a2.id\nORDER BY a1.last';
		break;

		case 'qname':
			$('queryText').value = 'select * from alumni where last=\'XXX\'';
		break;

		case 'reset':
			$('queryText').value = 'update alumni set password=Null where id=XXX';
		break;
	}
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
