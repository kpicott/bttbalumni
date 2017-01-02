//
// Validate the input in the registration form. Uses the canned validation
// scriptsion in formValidation.js
//
var ticketShown = -1;
showTicket = function(dir,which)
{
	// Avoid work if it is the same ticket info already showing
	if( which == ticketShown )
	{
		return;
	}

	var textA = Element.getOpacity( 'ticketText' );
	var imageA = Element.getOpacity( 'ticketImage' );
	eval( 'replaceDetail("' + dir + "/" + which + '.jpg", show' + which + '())' );
	Effect.Appear('ticketText', { duration:0.2, from:0.5, to:1.0 });
	Effect.Appear('ticketImage', { duration:0.2, from:0.5, to:1.0 });

	ticketShown = which;
	return true;
}

//----------------------------------------------------------------------
replaceDetail = function(imageSrc, textSrc)
{
	var imageFile = '/Images/' + imageSrc;
	$('ticketImage').src = imageFile;
	$('ticketText').innerHTML = textSrc;
}

//----------------------------------------------------------------------
showPrideOfBurlington = function()
{
	return "Enjoy the royal treatment with this package. It's a full weekend, starting Friday night with a Social Event (the Band Boosters will be on hand selling their famous barbecued cuisine, plus there will be a special musical surprise), then don your uniform Saturday morning to take part in the Sound of Music parade (don't forget to download your music and show up to practice Friday night at 7), then after a relaxing afternoon at the festival return to Central Arena for the Saturday night Homecoming featuring the Eddie Graf Band and a few special performers of our own.  Then wind it all up Sunday with a delicious lunch after the concert band practice, then play or listen to the combined Alumni/BTTB band playing in the park. Take home your uniform, a nice souvenir DVD package, and a ton of unforgettable new memories.";
}

//----------------------------------------------------------------------
showStrikeUpTheBand = function()
{
	return "Some of you may have busy weekends planned so this package is set to start off your weekend right. You'll attend the Friday night Social Event, then don your uniform Saturday morning to join the Alumni band in the Sound of Music Festival parade.  Then the rest of the weekend is yours to enjoy, along with your souvenir DVD package.";
}

//----------------------------------------------------------------------
showTheSoundOfMusic = function()
{
	return "This package is great for both Alumni and guests who would rather watch the parade than hit the pavement themselves. It includes tickets to the Friday night Social Event, the Saturday night Homecoming Celebration, and the Sunday afternoon concert lunch.";
}

//----------------------------------------------------------------------
showWeAreFamily = function()
{
	return "Even those not in the band themselves were greatly affected by it so it's only right that they get to take part in the celebrations as well.  With this package you'll get in to the Friday night Social event, the Saturday night Homecoming, get a nice Sunday lunch and watch the concert, and go home with a 60<sup>th</sup> Anniversary Hat as souvenir.";
}

//----------------------------------------------------------------------
showFridaySocial = function()
{
	return "A great start to the weekend in familiar territory. Pick up your registration package at the Music Centre or Central Arena, enjoy a Band Booster barbecue (not included in price of admission), socialize with old friends, cash bar, and browse through the collection of band memorabilia.  There will also be a musical surprise so be sure to check it out!";
}

//----------------------------------------------------------------------
showParade = function()
{
	return "Dust off the instrument, or just tag along (flatbed float available for those who would rather ride) for the annual Sound of Music Parade in the special 60th Anniversary Alumni Band. Everyone in the parade will need a uniform, and don’t forget the practice Friday evening at 7 p.m. at the Music Centre!";
}

//----------------------------------------------------------------------
showSaturdayHomecoming = function()
{
	return "The 60<sup>th</sup> Anniversary Party - A Homecoming Celebration, featuring live entertainment of various types and featuring the Eddie Graf Band. Enjoy gourmet finger food, cash bar, some special presentations celebrating our 60 years and a guest performance by the guests of honour - the 2007 BTTB!";
}

//----------------------------------------------------------------------
showSundayLunch = function()
{
	return "Bring your entire family for a BBQ Lunch in front of the Music Centre.  Sit back, relax (unless you're playing) and enjoy the BTTB and Alumni for a concert in the park.  Order individual tickets for your family if you've purchased a package for yourself.";
}

//----------------------------------------------------------------------
showShirt = function()
{
	return "Can’t make the parade but want to get into the spirit? This is a high quality golf shirt with the band logo on it. We’d like to keep this exclusive to the alumni as numbers are limited but keep an eye out after the celebration!";
}

//----------------------------------------------------------------------
showHat = function()
{
	return "A lasting souvenir for you to take home. High quality cap with the logo on the front and '60<sup>th</sup> Anniversary' stitched into the bill.";
}


// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
