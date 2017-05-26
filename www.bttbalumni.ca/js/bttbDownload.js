//----------------------------------------------------------------------
//
// Function to download multiple files in one shot.
// Recursively calls itself with the first file removed after it used
// a non-DOM link to download that first file.
//
// It supports either a file link location, or embedded data:
//
// download_all( [ ['music.pdf', 'http://bttbalumni.ca/Music/music.pdf'],
// 				   ['music.txt', 'data:text/plain;charset=utr8,'+
// 				   				 encodeURIComponent('Hello world')]
// 				 ] );
//
function download_all(files)
{
	if(files.length === 0)
	{
		return;
	}

	// This jQuery version doesn't work for some reason. The click() function
	// doesn't trigger the anchor.
	/*
	var temp_anchor = $('<a></a>')
            .attr('href', '#')
            .attr('download', null)
            .css({"display":"none"});
	$('body').append( temp_anchor );
	for( var f=0; f<files.length; ++f )
	{
		var file = files[f];
		alert( 'download ' + file[1] + ' to ' + file[0] );
		temp_anchor.attr('href', file[1])
				   .attr('download', file[0]);
		temp_anchor.click();
	}
	temp_anchor.remove();
	*/

	for( var f=0; f<files.length; ++f )
	{
		var file = files[f];

		var temp_anchor = document.createElement('a');
		temp_anchor.setAttribute( 'target', '_downloads' );
		temp_anchor.style.display = 'none';
		temp_anchor.setAttribute( 'download', file[0] );
		temp_anchor.setAttribute( 'href', file[1] );
		document.body.appendChild( temp_anchor );

		alert( 'download ' + file[1] + ' to ' + file[0] );
		temp_anchor.click();
		document.body.removeChild( temp_anchor );
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
