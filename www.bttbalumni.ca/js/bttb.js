//----------------------------------------------------------------------
//
// Set this to '1' to force alerts on AJAX events.
//
var _debug = 0;

//----------------------------------------------------------------------
//
// Global state information
//
var BTTBUserId = -1;
var BTTBOnCommittee = false;
var BTTBFirstName = '';
var BTTBFullName = '';

//----------------------------------------------------------------------
//
// Set padding in content pane to allow viewing full content with scrollbar
// that appears to be part of the main window.
// For some bizarre reason spacing is different on IE
//
var _contentXPadding = 135;
var _contentYPadding = 75;
if( /MSIE/.test(navigator.userAgent) && !window.opera )
{
    _contentXPadding = 157;
    _contentYPadding = 70;
}
// Safari is not fully supported by the dhtmlHistory mechanism
// so ignore all history change requests.
var useHistory = true;
if( navigator.userAgent.toLowerCase().indexOf('safari') != -1 )
{
    useHistory = false;
}

//----------------------------------------------------------------------
//
// Checking to see if an element was defined as a function
//
function isFunction(possibleFunction)
{
  return typeof(possibleFunction) === typeof(Function);
}

//----------------------------------------------------------------------
//
// For spam protection of email addresses
//
function makeEmail(name,host)
{
    name = name.replace('__NOSPAM__', '');
    host = host.replace('__NOSPAM__', '');
    document.location.href='mailto:'+name+'@'+host; 
}

//----------------------------------------------------------------------
//
// For some reason embedding this script right in the link causes IE to
// crash so I moved it here. It gives a generic link back to the Cluster
// Map website if there is a problem in the counter for this page.
//
function clustrMapError()
{
    this.onError = null;
    this.src = 'http://clustrmaps.com/images/clustrmaps-back-soon.jpg';
	var clustrMapsLink = document.getElementById( 'clustrMapsLink' );
    clustrMapsLink.href = 'http://clustrmaps.com';
    return true;
}

//----------------------------------------------------------------------
//
// For processing form data then opening up a follow-up page.
//   form_url:  The form handler
//   form_id:   The ID of the form on the page
//   follow_up: The URL to go to after the form has been handled (home page if null)
//
// Form processing must return the string "OK" if there is a follow_up, otherwise the
// return value from the processing will be printed and the follow_up will not be invoked
//
function submit_form(form_url,form_id,follow_up)
{
	var form = $(form_id);
    if( _debug) alert( "AJAX openForm " + form_id + " at " + form_url + ' to return to ' + follow_up );
    if( _debug) alert( "Form data is : " + form.serializeArray() );

	$("#content").html( "Processing " + form.attr('method') + " request..." );
	$.ajax( {
		type	:	form.attr('method'),
		url		:	form_url,
		data	:	form.serializeArray(),
		success	:	function(return_data)
					{
						if( _debug ) alert( 'Successful submit: ' + return_data );
						if( (follow_up === null) || (return_data.substr(0,2) !== "OK") )
						{
							$("#content").html( return_data );
						}
						else
						{
							$("#content").html( 'Form accepted. Forwarding to ' + follow_up );
							if( _debug ) alert( 'Following up to ' + follow_up );
							open_page( follow_up );
						}
					},
		error	:	function(return_data)
					{
						if( _debug ) alert( 'Submit failed: ' + return_data );
						alert( 'Form submission failed, please try again.' );
					}
	} );
}

//----------------------------------------------------------------------
//
// Our callback to receive history change events.
//
function historyChange(newLocation, historyData)
{
    if( ! useHistory )
    {
        return;
    }

    // If a page is in the middle of being opened ignore the history
    // change it generates.
    if( _openingPage )
    {
        if( _debug ) alert('HISTORY BYPASS ' + newLocation + ' = ' + historyData);
        return;
    }

    if( _debug ) alert('HISTORY CHANGE ' + newLocation + ' = ' + historyData);
    if( historyData )
    {
        openPage( historyData );
    }
    else
    {
        // When there was no historyData that means the user typed in
        // something, so translate that into a direct link.
        openPage( '/#' + newLocation );
    }
}

//----------------------------------------------------------------------
//
// For repositioning the content subframe when the user changes window size
//
function onSizeChange()
{
	/*  Old school manual sizing of the content pane
    var myWidth = 0, myHeight = 0;
    if( typeof( window.innerWidth ) == 'number' )
    {
        //Non-IE
        myWidth = window.innerWidth;
        myHeight = window.innerHeight;
    }
    else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) )
    {
        //IE 6+ in 'standards compliant mode'
        myWidth = document.documentElement.clientWidth;
        myHeight = document.documentElement.clientHeight;
    }
    else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) )
    {
        //IE 4 compatible
        myWidth = document.body.clientWidth;
        myHeight = document.body.clientHeight;
    }
	*/
    var content = document.getElementById('content');
	/*
    content.style.width = (myWidth - _contentXPadding) + 'px';
    content.style.height = (myHeight - _contentYPadding) + 'px';
	*/

	// Force a redraw
	content.className = content.className;
}

// the starting index in the group images array.
// It should be set to the value of the div which does
// not have the CSS Display property set to "none"
var currentImage = 0;

// the number of milliseconds between swaps.  Default is five seconds.
var wait = 5000;

var growEffect = null;
var shrinkEffect = null;

function groupDivName() { return 'box-' + currentImage; }
function groupImgName() { return 'img-' + currentImage; }
// the function that performs the fade
function swapFade()
{
    Effect.Fade(groupDivName(), { duration:1, from:1.0, to:0.0 });
    currentImage++;
    if (currentImage == groupImages.length) currentImage = 0;

    // Set to current size before bringing it back
    var logo = document.getElementById(groupImgName());
    logo.width = _currentImgWidth;
    logo.height = _currentImgHeight;

    Effect.Appear(groupDivName(), { duration:1, from:0.0, to:1.0 });
}
var _currentImgWidth = 174;
var _currentImgHeight = 119;
function bigLogo()
{
    var logo = document.getElementById(groupImgName());
    _currentImgWidth = 348;
    _currentImgHeight = 238;
    logo.width = _currentImgWidth;
    logo.height = _currentImgHeight;
    return true;
}
function smallLogo()
{
    var logo = document.getElementById(groupImgName());
    _currentImgWidth = 174;
    _currentImgHeight = 119;
    logo.width = _currentImgWidth;
    logo.height = _currentImgHeight;
    return true;
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================

