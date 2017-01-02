//
// Set up the animation for the "Priceless" promo.
//

// the starting index in the group images array.
// It should be set to the value of the div which does
// not have the CSS Display property set to "none"
var PcurrentImage = 0;
var PinFade = true;

// the function that performs the fade
function fadePriceless()
{
	if( PinFade )
	{
		$('pricelessImg').src = '/Images/Priceless/Priceless' + (PcurrentImage+1) + '.jpg';
		Effect.Appear('priceless', { duration:6, from:0.0, to:1.0 });
		PinFade = false;
	}
	else
	{
		Effect.Fade('priceless', { duration:6, from:1.0, to:0.01 });
		PcurrentImage++;
		if (PcurrentImage == 5) PcurrentImage = 0;
		PinFade = true;
	}
}

var PloadedImages = null;
initializePriceless = function()
{
	var img;
	// Preload all of the image for performance
	if( document.images )
	{
		if (!PloadedImages) PloadedImages = new Array();
		img = new Image();
		img.src = '/Images/Priceless/Priceless1.jpg';
		PloadedImages[PloadedImages.length] = img;
		img = new Image();
		img.src = '/Images/Priceless/Priceless2.jpg';
		PloadedImages[PloadedImages.length] = img;
		img = new Image();
		img.src = '/Images/Priceless/Priceless3.jpg';
		PloadedImages[PloadedImages.length] = img;
		img = new Image();
		img.src = '/Images/Priceless/Priceless4.jpg';
		PloadedImages[PloadedImages.length] = img;
		img = new Image();
		img.src = '/Images/Priceless/Priceless5.jpg';
		PloadedImages[PloadedImages.length] = img;
	}   
	setInterval('fadePriceless()',Pwait);
}

// the number of milliseconds between swaps.  Default is 6 seconds.
var Pwait = 6000;

// Make sure the image tag is present - if the article is outdated for example
// it will be hidden so there will be no need to update the image.
if( $('pricelessImg') )
{
	initializePriceless();
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
