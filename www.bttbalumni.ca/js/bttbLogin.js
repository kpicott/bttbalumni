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
	return [_getCookie('User'),
			_getCookie('OnCommittee'),
			_getCookie('FirstName'),
			_getCookie('FullName')];
};
LastVisitTime = function()
{
	var rightNow = new Date();
	var WWHTime = 0;
	WWHTime = _getCookie('WWhenH');
	WWHTime = WWHTime * 1;
	var lastHereFormatting = new Date(WWHTime);
	var intLastVisit = (lastHereFormatting.getYear() * 10000)+(lastHereFormatting.getMonth() * 100) + lastHereFormatting.getDate();
	var lastHereInDateFormat = "" + lastHereFormatting;
	var dayOfWeek = lastHereInDateFormat.substring(0,3);
	var dateMonth = lastHereInDateFormat.substring(4,11);
	var timeOfDay = lastHereInDateFormat.substring(11,16);
	var year = lastHereInDateFormat.substring(23,25);
	var WWHText = dayOfWeek + ", " + dateMonth + " at " + timeOfDay;
	_setCookie ("WWhenH", rightNow.getTime(), exp);
	return WWHText;
};
AddNewUser = function(user, onCommittee, firstName, fullName)
{ 
	_setCookie ('User', user, exp);
	_setCookie ('OnCommittee', onCommittee, exp);
	_setCookie ('FirstName', firstName, exp);
	_setCookie ('FullName', fullName, exp);
	_setCookie ('WWHCount', 0, exp);
	_setCookie ('WWhenH', 0, exp);
};
RegisterUserVisit = function()
{ 
	var WWHCount = _getCookie('WWHCount');
	if (WWHCount === null)
	{
		WWHCount = 1;
	}
	else
	{
		WWHCount++;
	}
	_setCookie ('WWHCount', WWHCount, exp);
	var rightNow = new Date();
	_setCookie ("WWhenH", rightNow.getTime(), exp);
};

//######################################################################

var expDays = 30;
var exp = new Date();
exp.setTime(exp.getTime() + (expDays*24*60*60*1000));

//----------------------------------------------------------------------
//
// These functions are internal to the implementation which is, not
// surprisingly, cookie-based.
//
function _getCookieVal (offset)
{
	var endstr = document.cookie.indexOf (";", offset);
	if (endstr == -1)
		endstr = document.cookie.length;
	return unescape(document.cookie.substring(offset, endstr));
}
function _getCookie (name)
{
	var arg = name + "=";
	var alen = arg.length;
	var clen = document.cookie.length;
	var i = 0;
	while (i < clen)
	{
		var j = i + alen;
		if (document.cookie.substring(i, j) == arg)
			return _getCookieVal (j);
		i = document.cookie.indexOf(" ", i) + 1;
		if (i === 0) break;
	}
	return null;
}

//----------------------------------------------------------------------
//
// Set the internal cookie value.
//
function _setCookie (name, value)
{
	var argv = _setCookie.arguments;
	var argc = _setCookie.arguments.length;
	var expires = (argc > 2) ? argv[2] : null;
	var path = (argc > 3) ? argv[3] : null;
	var domain = (argc > 4) ? argv[4] : null;
	var secure = (argc > 5) ? argv[5] : false;
	document.cookie = name + "=" + escape (value) +
	((expires === null) ? "" : ("; expires=" + expires.toGMTString())) +
	((path === null) ? "" : ("; path=" + path)) +
	((domain === null) ? "" : ("; domain=" + domain)) +
	((secure === true) ? "; secure" : "");
}
function _deleteCookie (name)
{
	var exp = new Date();
	exp.setTime (exp.getTime() - 1);
	var cval = _getCookie (name);
	document.cookie = name + "=" + cval + "; expires=" + exp.toGMTString();
}

//----------------------------------------------------------------------
//
// Log out the current user and reload the current page
//
function do_logout()
{
	BTTBUserId = -1;
	_deleteCookie ('User');
	_deleteCookie ('OnCommittee');
	_deleteCookie ('FirstName');
	_deleteCookie ('FullName');
    var newUrl = document.location.href.replace( /:[0-9]+/, "" );
	document.location.href = newUrl;
	document.location.reload();
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
