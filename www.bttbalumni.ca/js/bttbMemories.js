//
// Change a start and end year filter, then selectively enable and disable
// the years corresponding to the new year range.
//
// Start > End just flips the years
//
function years_changed()
{
	var new_start_year = $('#start_year').val();
	var new_end_year = $('#end_year').val();
	if( new_start_year > new_end_year )
	{
		var tmp = new_start_year;
		new_start_year = new_end_year;
		new_end_year = tmp;
	}
	var year_filter_list = $(".yearFilter");
	for( var idx=0; idx<year_filter_list.length; ++idx )
	{
		var el = year_filter_list[idx];
		var class_info = el.className.split(':');
		var year = class_info[1];
		if( year < new_start_year || year > new_end_year )
		{
			el.style.display = 'none';
		}
		else
		{
			el.style.display = 'block';
		}
	}
}

//==================================================================
//
// Flip the filter to show all memories in the year range or only
// the ones reported recently.
//
function memory_filter(show_all)
{
	if( show_all )
	{
		$('.old-memory').show();
		$('#recent-link').html( "<button class='shadow_button' onclick='memory_filter(false);'>Show Only Recently Added Memories</button>" );
	}
	else
	{
		$('.old-memory').hide();
		$('#recent-link').html( "<button class='shadow_button' onclick='memory_filter(true);'>Show All Memories In Range</button>" );
	}
}

// Initialize in the show-recent mode
$(document).ready(function() { memory_filter(false); });


// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
