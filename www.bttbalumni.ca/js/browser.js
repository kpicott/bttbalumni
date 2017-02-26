// This script and many more are available free online at
// The JavaScript Source!! http://javascript.internet.com

function setBrowserInfo()
{
	$('browserInfo').innerHTML = browserInfo();
}
function browserInfo()
{
	var xy = navigator.appVersion;
	xz = xy.substring(0,4);
	var info = "<center><table border=1 cellpadding=2><tr><td>";
	info += "<center><b>" + navigator.appName + "</b>";
	info += "</td></tr><tr><td>";
	info += "<center><table border=1 cellpadding=2><tr>";
	info += "<td>Code Name: </td><td><center>";
	info += "<b>" + navigator.appCodeName + "</td></tr>";
	info += "<tr><td>Version: </td><td><center>";
	info += "<b>" + xz + "</td></tr>";
	info += "<tr><td>Platform: </td><td><center>";
	info += "<b>" +  navigator.platform + "</td></tr>";
	info += "<tr><td>Pages Viewed: </td><td><center>";
	info += "<b>" + history.length + " </td></tr>";
	info += "<tr><td>Java enabled: </td><td><center><b>";
	if (navigator.javaEnabled()) info += "sure is!</td></tr>";
	else info += "not today</td></tr>";
	info += "<tr><td>Screen Resolution: </td><td><center>";
	info += "<b>" + screen.width + " x " + screen.height + "</td></tr>";
	info += "</table></tr></td></table></center>";
	return info;
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
