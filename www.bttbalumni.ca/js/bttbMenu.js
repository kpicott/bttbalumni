// Enter id(s) of UL menus, separated by commas
var menuids = new Array("verticalMenu");

// Offset of submenus from main menu.
var subMenuOffsetWidth = -12;
var subMenuOffsetHeight = -7;

// List of submenus currently visible.
var subMenusUp = new Array();

//----------------------------------------------------------------------
//
// Verify the user information and confirm their status
//
function doLogin(name,isCommittee,id)
{
	$('login').innerHTML = "<label>Welcome " + unescape(name) + "</label><br/><div class='menuLink'><a href=\"javascript:open_page('/#register')\">Edit Profile</a></a><br/>";
	if( isCommittee )
	{
		$('login').innerHTML += "<label>Committee Access</label>";
	}
	$('login').innerHTML += "<form action='javascript:doLogout()'>"
		+ "<input class='label' type='submit' value='Logout' />"
		+ "</form>";
	var newUrl = dhtmlHistory.getCurrentLocation();
	newUrl = newUrl.replace( /:[0-9]*/, ":" + id );
	BTTBUserId = id;
	RegisterUserVisit();
	open_page( '/#' + newUrl );
}

//----------------------------------------------------------------------
//
// Forget the login status and restore the login prompt
//
function doLogout(wasBadLogin)
{
	$('login').innerHTML = 
		"<form name='loginForm' id='loginForm' action='javascript:checkLogin()'>" + 
		"<table width='100%' border='0' cellspacing='0' cellpadding='0'>" + 
		"<tr><td><label>Username</label><br />" + 
		"<input type='text' id='user' name='user' size='10' /><br />" + 
		"<label>Password</label><br />" + 
		"<input type='password' id='password' name='password' size='10' /><br />" + 
		"<input class='label' border='1' type='submit' name='Submit' value='Login' /><br />" + 
		"<div class='menuLink'><a title='Click here to request a password reset' href='javascript:open_page(\"#forgot\")'>Forgot Login?</a><br />" +
		"<a title='Click here to register yourself' href='javascript:open_page(\"/#register\")'>Not Registered?</a></div>" +
		"</td></tr></table></form>";
	if( wasBadLogin )
	{
		$('login').innerHTML += "<label>User/Password<br>Not Recognized</label>";
	}
	else
	{
		var newUrl = dhtmlHistory.getCurrentLocation();
		newUrl = newUrl.replace( /:[0-9]*/, "" );
		BTTBUserId = -1;
		open_page( '/#' + newUrl );
	}
}

//----------------------------------------------------------------------
//
// Check to see if user has a valid login. Populate the login area according
// to the result.
//
function checkLogin()
{
	var postBodyString = Form.serialize( 'loginForm' );
	new Ajax.Request('/cgi-bin/login.cgi',
	{
		method: 'post',
		postBody:	postBodyString,
		onComplete: function (req)
		{
			var response = req.responseText.split('|');
			if( response.length == 4 )
			{
				var id = response[0];
				var onCommittee = parseInt(response[1]);
				var firstName = response[2];
				var fullName = response[3];
				AddNewUser( id, onCommittee, firstName, fullName );
				doLogin(escape(firstName), onCommittee, id);
			}
			else
			{
				doLogout(true);
			}
		}
	});
}

//----------------------------------------------------------------------
//
// When the user moves the mouse between the main menu button and the
// submenu there might be a mouseout() event that will dismiss the
// submenu. To avoid this UI problem the dismissal is delayed by a
// little bit and the submenu gets a window in which to cancel its own
// dismissal.
//
function dismiss()
{
	while( subMenu = subMenusUp.pop() )
	{
		if( ! subMenu.cancelDismiss )
		{
			subMenu.getElementsByTagName("ul")[0].style.display = "none";
		}
	}
}

//----------------------------------------------------------------------
//
// Cleanup after clicking, dismissing all submenus.
//
function dismissAll()
{
	for (var i=0; i<menuids.length; i++)
	{
		var ultags=document.getElementById(menuids[i]).getElementsByTagName("ul")
		for (var t=0; t<ultags.length; t++)
		{
			var subMenu = ultags[t].parentNode.getElementsByTagName("ul")[0];
			if( subMenu )
			{
				subMenu.style.display = "none";
			}
		}
	}
}

//----------------------------------------------------------------------
//
// Create the menu, popping up and dismissing the submenus as needed
//
function createMenu()
{
	for (var i=0; i<menuids.length; i++)
	{
		var ultags=document.getElementById(menuids[i]).getElementsByTagName("ul")
		for (var t=0; t<ultags.length; t++)
		{
			var spanref = document.createElement("span");
			spanref.className = "arrowdiv";
			spanref.innerHTML = "&nbsp;";
			ultags[t].parentNode.getElementsByTagName("a")[0].appendChild(spanref);
			ultags[t].parentNode.onmouseover = function()
				{
					var child = this.getElementsByTagName("ul")[0];
					child.parentNode.cancelDismiss = true;
					child.style.top = subMenuOffsetHeight + "px";
					child.style.left = this.parentNode.offsetWidth + subMenuOffsetWidth + "px";
					child.style.display = "block";
					child.onmouseover = function()
						{
							this.parentNode.cancelDismiss = true;
						}
					child.onmouseout = function()
						{
							setTimeout( 'dismiss()', 1 );
						}
				}
			ultags[t].parentNode.onmouseout = function()
				{
					subMenusUp.push( this );
					this.cancelDismiss = false;
					setTimeout( 'dismiss()', 50 );
				}
		}
	}
	var userInfo = CurrentUser();
	BTTBUserId = userInfo[0];
	BTTBOnCommittee = parseInt(userInfo[1]);
	BTTBFirstName = userInfo[2];
	BTTBFullName = userInfo[3];
	if( BTTBUserId != null )
	{
		doLogin(BTTBFirstName, BTTBOnCommittee, BTTBUserId);
	}
	else
	{
		doLogout(false);
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
