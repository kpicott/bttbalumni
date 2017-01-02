//
// Change a start and end year filter, then selectively enable and disable
// the years corresponding to the new year range.
//
// Start > End just flips the years
//
yearsChanged = function()
{
	var newStartYear = $('startYear').value;
	var newEndYear = $('endYear').value;
	if( newStartYear > newEndYear )
	{
		var tmp = newStartYear;
		newStartYear = newEndYear;
		newEndYear = tmp;
	}
	var elList = document.getElementsByName("yearFilter");
	for( var idx=0; idx<elList.length; ++idx )
	{
		var el = elList[idx];
		var classInfo = el.className.split(':');
		var year = classInfo[1];
		if( year < newStartYear || year > newEndYear )
		{
			el.style.display = 'none';
		}
		else
		{
			el.style.display = 'block';
		}
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
