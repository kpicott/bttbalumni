/*****

Image Cross Fade Redux
Version 1.0
Last revision: 02.15.2006
steve@slayeroffice.com

Please leave this notice intact. 

Rewrite of old code found here:
	http://slayeroffice.com/code/imageCrossFade/index.html

*****/


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
	
	css = d.createElement("link");
	css.setAttribute("href","imageCrossFade.css");
	css.setAttribute("rel","stylesheet");
	css.setAttribute("type","text/css");

	d.getElementsByTagName("head")[0].appendChild(css);
	
	imgContainer = $('imageContainer');
	imgs = imageContainer.getElementsByTagName('img');
	for(i=1;i<imgs.length;i++)
	{
		imgs[i].xOpacity = 0;
	}
	imgs[0].style.display = 'block';
	imgs[0].xOpacity = .99;
	imgs[0].border = 0;
	
	setTimeout(so_xfade,pauseTime);
}

function so_xfade()
{
	cOpacity = imgs[current].xOpacity;
	nIndex = imgs[current+1] ? current+1 : 0;
	nOpacity = imgs[nIndex].xOpacity;
	
	cOpacity -= .05; 
	nOpacity += .05;
	
	imgs[nIndex].style.display = 'block';
	imgs[current].xOpacity = cOpacity;
	imgs[nIndex].xOpacity = nOpacity;
	
	setOpacity(imgs[current]); 
	setOpacity(imgs[nIndex]);
	
	if(cOpacity<=0)
	{
		imgs[current].style.display = 'none';
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
		obj.style.opacity = obj.xOpacity;
		obj.style.MozOpacity = obj.xOpacity;
		obj.style.filter = "alpha(opacity=" + (obj.xOpacity*100) + ")";
	}
}

