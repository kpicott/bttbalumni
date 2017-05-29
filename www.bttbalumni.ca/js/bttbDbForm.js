//
// Modify the instructions on output format to correspond to what changing the
// checkbox actually does.
//
function output_type_changed()
{
	if( $('#outputType').checked )
	{
		$('#outputTypeInfo').html( 'Output will downloaded as text. Uncheck this box to see results onscreen.' );
		$('#dbQueryForm').action = "/cgi-bin/bttbDbQuery.cgi";
	}
	else
	{
		$('#outputTypeInfo').html( 'Output will be shown on the screen. Check this box to download a text file.' );
		$('#dbQueryForm').action = "javascript:submitForm(\'dbQueryForm\', \'/cgi-bin/bttbDbQuery.cgi\', null);";
	}
}

var queries = {
		'all'           : 'SELECT * FROM alumni',
		'committee'     : 'SELECT * FROM alumni WHERE onCommittee = 1',
		'parade'       : 'SELECT alumni.first,alumni.last,alumni.email,alumni.phone FROM alumni WHERE alumni.id IN (SELECT alumni_id FROM 2017_parade WHERE registered = 0)',
		// 'friday'       : 'SELECT alumni.first,alumni.last,alumni.email,alumni.phone FROM alumni WHERE alumni.id IN (SELECT alumni_id FROM attendance WHERE event_id = 4) AND alumni.id NOT IN (SELECT alumni_id FROM payments WHERE event_id = 4)',
		// 'saturday'     : 'SELECT alumni.first,alumni.last,alumni.email,alumni.phone FROM alumni WHERE alumni.id IN (SELECT alumni_id FROM attendance WHERE event_id = 5) AND alumni.id NOT IN (SELECT alumni_id FROM payments WHERE event_id = 5)',
		// 'drumline'     : 'SELECT alumni.first,alumni.nee,alumni.last,alumni.email,alumni.firstYear,alumni.lastYear, alumni.instruments FROM parade INNER JOIN alumni ON alumni.id = parade.alumni_id WHERE instruments LIKE \'%ercussion%\' OR instruments LIKE \'%Snare%\' OR instruments LIKE \'%Cymbals%\'',
		'contactMissing': 'SELECT contact.first,contact.nee,contact.last,contact.firstYear,contact.lastYear,contact.email,contact.phone\n' +
						  '  FROM contact\n' +
						  ' WHERE contact.id NOT IN\n' +
						  '   (SELECT contact.id FROM contact INNER JOIN alumni\n' +
						  '     ON alumni.first = contact.first\n' +
						  '        AND (alumni.last = contact.last OR alumni.nee = contact.last))\n' +
						  'ORDER BY contact.last,contact.first',
		'duplicate'     : 'SELECT a1.*\n' +
						  '  FROM alumni AS a1,alumni AS a2\n' +
						  ' WHERE a1.first LIKE a2.first\n' +
						  '   AND a1.last LIKE a2.last\n' +
						  '   AND a1.id <> a2.id\n' +
						  'ORDER BY a1.last',
		'remove'        : 'DELETE\n  FROM alumni\n WHERE id IN (XX, XX)',
		'qname'         : 'SELECT *\n  FROM alumni\n WHERE last=\'XXX\'',
		'reset'         : 'UPDATE alumni\n  SET password=Null\n WHERE id=XXX'
	};

//
// Modify the query to be executed based on a pre-canned selection
//
function query_select(which_query)
{
	var query_value = queries[which_query];
	if( query_value !== null )
	{
		$('#queryText').val( query_value );
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
