var browser=navigator.appName
var b_version=navigator.appVersion
var version=parseFloat(b_version)

var userInfo = CurrentUser();
// Only warn the user once
if( userInfo[0] != null )
{
	if( navigator.userAgent.toLowerCase().indexOf('safari') != -1 )
	{
		alert( 'Safari users note: Your browser does not properly support the back button so your navigation experience will be different. Watch for a newer release from Apple coming soon that will fix this problem.' );
	}
	else if( /MSIE 7/.test(b_version) )
	{
		// No problems, these are the supported versions
	}
	else if( /MSIE 6/.test(b_version) )
	{
		// No problems, these are the supported versions
	}
	else if( /Mozilla/.test(browser) && version > 4 )
	{
		// No problems, these are the supported versions
	}
	else if( /Netscape/.test(browser) && version > 4 )
	{
		// No problems, these are the supported versions
	}
	else if(/MSIE/.test(b_version))  
	{
		alert( 'Internet Explorer version 6 is required for correct operation, you only have version ' + b_version + '.  You may experience problems with this website unless you upgrade.' );
	}
	else
	{
		alert( 'Warning: Your browser - ' + browser + ' version ' + b_version + ' - may not be fully supported by this website. Report any particular problems found to the webmaster.' );
	}
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without the prior written consent  of  Kevin  Peter  Picott, which
// you  will  almost certainly get if you just ask bttb@picott.ca
// ==================================================================
