//######################################################################

// Standard cookie will last a month
var default_expiration_days = 30;

//----------------------------------------------------------------------
//
// Manage what little user information we keep track of.  For now just
// user id, are they on the committee, first/full name, number of visits,
// and time of last visit.
//
// These functions are the interface used by the web page.
//
CurrentUser = function()
{
	return [get_cookie('User'),
			get_cookie('OnCommittee'),
			get_cookie('FirstName'),
			get_cookie('FullName')];
};
LastVisitTime = function()
{
	var rightNow = new Date();
	var WWHTime = 0;
	WWHTime = get_cookie('WWhenH');
	WWHTime = WWHTime * 1;
	var lastHereFormatting = new Date(WWHTime);
	var intLastVisit = (lastHereFormatting.getYear() * 10000)+(lastHereFormatting.getMonth() * 100) + lastHereFormatting.getDate();
	var lastHereInDateFormat = "" + lastHereFormatting;
	var dayOfWeek = lastHereInDateFormat.substr(0,3);
	var dateMonth = lastHereInDateFormat.substr(4,11);
	var timeOfDay = lastHereInDateFormat.substr(11,16);
	var year = lastHereInDateFormat.substr(23,25);
	var WWHText = dayOfWeek + ", " + dateMonth + " at " + timeOfDay;
	set_cookie ("WWhenH", rightNow.getTime(), default_expiration_days);
	return WWHText;
};
AddNewUser = function(user, onCommittee, firstName, fullName)
{ 
	set_cookie ('User', user, default_expiration_days);
	set_cookie ('OnCommittee', onCommittee, default_expiration_days);
	set_cookie ('FirstName', firstName, default_expiration_days);
	set_cookie ('FullName', fullName, default_expiration_days);
	set_cookie ('WWHCount', 0, default_expiration_days);
	set_cookie ('WWhenH', 0, default_expiration_days);
};
RegisterUserVisit = function()
{ 
	var WWHCount = get_cookie('WWHCount');
	if (WWHCount === null)
	{
		WWHCount = 1;
	}
	else
	{
		WWHCount++;
	}
	set_cookie ('WWHCount', WWHCount, default_expiration_days);
	var rightNow = new Date();
	set_cookie ("WWhenH", rightNow.getTime(), default_expiration_days);
};

//----------------------------------------------------------------------
//
// These functions are internal to the implementation which is, not
// surprisingly, cookie-based.
//
function get_cookie( name )
{
	var encoded_name = encodeURIComponent(name) + "=";
	var cookie_list = document.cookie.split( ';' );
	var cookie_value = null;
	cookie_list.forEach( function(cookie, index)
	{
		// Strip leading spaces
		while( cookie.charAt(0) === ' ')
		{
			cookie = cookie.substr(1);
		}
		if( cookie.indexOf(encoded_name) === 0 )
		{
			cookie_value = decodeURIComponent( cookie.substr(encoded_name.length) );
			return;
		}
	});
	return cookie_value;
}

//----------------------------------------------------------------------
//
// Set the internal cookie value.
//
// If days_before_expiration == 0 then there will be no expiration.
// Use days_before_expiration == -1 to expire it immediately
//
function set_cookie (name, value, days_before_expiration)
{
	var expires;
	if( days_before_expiration !== 0 )
	{
		var expiration_date = new Date();
		expiration_date.setTime(expiration_date.getTime() + (days_before_expiration*24*60*60*1000));
		expires = '; expires=' + expiration_date.toGMTString();
	}
	else
	{
		expires = '';
	}

	document.cookie = name + "=" + encodeURIComponent (value) + expires;
}
function delete_cookie (name)
{
	set_cookie( name, '', -1 );
}

//----------------------------------------------------------------------
//
// Log out the current user and reload the current page
//
function do_logout()
{
	BTTBUserId = -1;
	delete_cookie ('User');
	delete_cookie ('OnCommittee');
	delete_cookie ('FirstName');
	delete_cookie ('FullName');
    var newUrl = location.href.replace( /:[0-9]+/, "" );
	location.href = newUrl;
	location.reload();
	return 1;
}

//----------------------------------------------------------------------
//
// Open the login modal dialog
//
function do_login()
{
	var modal = $('#login-dialog');
	modal.show();

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event)
	{
		if( event.target === modal[0] )
		{
			modal.hide();
		}
	};
	return 1;
}

//----------------------------------------------------------------------
//
// Close the login modal dialog
//
function close_login()
{
	$('#login-error').hide();
	$('#login-dialog').hide();
	window.onclick = null;
}

//----------------------------------------------------------------------
//
// Check to see if user has a valid login. Reload the current page with
// the user ID if so, toggle the error message on if not.
//
function check_login()
{
	var form = $('#login-form');
	form.submit( function(event) {
		action = form.attr('action');
		$.post(action, form.serialize(), function(result) {
					var response = result.split('|');
					if( response.length == 4 )
					{
						var id = response[0];
						var onCommittee = parseInt(response[1]);
						var firstName = response[2];
						var fullName = response[3];
						AddNewUser( id, onCommittee, firstName, fullName );
						// Reload the page so that all of the elements reflect the new user
						close_login();
            			document.location.href = document.location.hash + ':' + id + document.location.search;
						document.location.reload();
					}
					else
					{
						$('#login-error').show();
					}
			});
		event.preventDefault();
	});
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
