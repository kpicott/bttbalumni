//
// Requires prototype.js and scriptaculous.js
//
// Fade from showing the first div to showing the second div.
// Start from the current opacity of the divs so that the fade is not jumpy.
//
var debug = 0;
function crossFade(divOff, divOn)
{
	var currentOn = Element.getOpacity( divOn );
	var currentOff = Element.getOpacity( divOff );
	if( debug && (currentOn > 1.0 || currentOff > 1.0) )
	{
		alert('CROSS from ' + divOff + ' at ' + currentOff + ' to ' + divOn + ' at ' + currentOn );
	}
	Effect.Fade(divOff, { duration:0.5, from:currentOff, to:0.3 });
	Effect.Appear(divOn, { duration:0.5, from:currentOn, to:1.0 });
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
//

// Alternative versions below, available to use but not tested

/*****

Image Cross Fade Redux
Version 1.0
Last revision: 02.15.2006
steve@slayeroffice.com

Please leave this notice intact. 

Rewrite of old code found here:
	http://slayeroffice.com/code/imageCrossFade/index.html

window.addEventListener ? window.addEventListener("load",so_init,false)
						: window.attachEvent("onload",so_init);

// Shortcut to the document
var d=document;

// Array of images to use in the crossfade
var imgs = new Array();

// Current main image displayed
var current=0;

// Time a single image is paused
var pauseTime = 5000;

// Time between refreshes during cross-fade
var gapTime = 50;

function so_init()
{
	if(!d.getElementById || !d.createElement)return;
	
	imgs = d.getElementById("imageContainer").getElementsByTagName("img");
	for(i=1;i<imgs.length;i++)
	{
		imgs[i].xOpacity = 0;
	}
	imgs[0].style.display = "block";
	imgs[0].xOpacity = .99;
	
	setTimeout(so_xfade,pauseTime);
}

function so_xfade()
{
	cOpacity = imgs[current].xOpacity;
	nIndex = imgs[current+1]?current+1:0;
	nOpacity = imgs[nIndex].xOpacity;
	
	cOpacity-=.05; 
	nOpacity+=.05;
	
	imgs[nIndex].style.display = "block";
	imgs[current].xOpacity = cOpacity;
	imgs[nIndex].xOpacity = nOpacity;
	
	setOpacity(imgs[current]); 
	setOpacity(imgs[nIndex]);
	
	if(cOpacity<=0)
	{
		imgs[current].style.display = "none";
		current = nIndex;
		setTimeout(so_xfade,pauseTime);
	}
	else
	{
		setTimeout(so_xfade,gapTime);
	}
	
	function setOpacity(obj)
	{
		if(obj.xOpacity>.99)
		{
			obj.xOpacity = .99;
			return;
		}
		obj.parentNode.style.opacity = obj.xOpacity;
		obj.parentNode.style.MozOpacity = obj.xOpacity;
		obj.parentNode.style.filter = "alpha(opacity=" + (obj.xOpacity*100) + ")";
	}
}
//--------------------Image Replacement Code Begins--------------------------
//A required Variable for the loadImages() function
loadedImages = null
/**
 * loadImages() accepts a list of file names to load into cache.
 * For each file name it creates a new image object and begins
 * downloading the file into the browser's cache. 
//
function loadImages()
{
   var img
   if (document.images){
      if (!loadedImages) loadedImages = new Array()
      for (var i=0; i < arguments.length; i++){
         img = new Image()
         img.src = arguments[i]
         loadedImages[loadedImages.length] = img
      }
   }   
}

/**
 * flip(imgName, imgSrc) sets the src attribute of a named
 * image in the current document. The function must be passed
 * two strings. The first is the name of the image in the document
 * and the second is the source to set it to.
//
function flip(imgName, imgSrc)
{
   if (document.images)
   {
      document[imgName].src = imgSrc
   }
}
//Fix Netscape resize bug for mouseDown and mouseUp events.
function forceReload() 
{
      location.reload()
}
function fixNetscape4()
{
   NS4 = document.layers
   NSVer = parseFloat(navigator.appVersion)
   if (NSVer >= 5.0 || NSVer < 4.1) NS4 = false

   if (NS4) onresize = forceReload
}
//--------------------Image Replacement Code Ends----------------------------
*****/

