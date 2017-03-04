//----------------------------------------------------------------------
//
// Set this to '1' to force alerts on AJAX events.
//
var _debug = 0;

//----------------------------------------------------------------------
//
// Global state information
//
BTTBUserId = -1;
BTTBOnCommittee = false;
BTTBFirstName = '';
BTTBFullName = '';

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
// For spam protection of email addresses
//
makeEmail = function(name,host)
{
    name = name.replace('__NOSPAM__', '')
    host = host.replace('__NOSPAM__', '')
    document.location.href='mailto:'+name+'@'+host; 
}

//----------------------------------------------------------------------
//
// For some reason embedding this script right in the link causes IE to
// crash so I moved it here. It gives a generic link back to the Cluster
// Map website if there is a problem in the counter for this page.
//
clustrMapError = function()
{
    this.onError = null;
    this.src = 'http://clustrmaps.com/images/clustrmaps-back-soon.jpg';
	var clustrMapsLink = document.getElementById( 'clustrMapsLink' );
    clustrMapsLink.href = 'http://clustrmaps.com';
    return true;
}

//----------------------------------------------------------------------
//
// For opening up new pages in the content area
//
var _openingPage = false;
openPage = function(url)
{
    dismissAll();
    var p = new BTTBUrl.BTTBURLParser(url);
    if( BTTBUserId >= 0 )
    {
        p.setUser( BTTBUserId)
    }
    //
    // Links within this site go through AJAX, others work as usual
    //
    if( (p.getHost().search('bttbalumni') >= 0)
    ||  (p.getHost() == 'localhost')
    ||  (p.getHost() == 'band.local')
    ||  (p.getHost() == '') )
    {
        _openingPage = true;
        pageUrl = p.assembledURL(false);
        hashUrl = p.assembledURL(true);
        if( useHistory )
        {
            dhtmlHistory.add(hashUrl[0], pageUrl[1]);
        }
		var content = document.getElementById( 'content' );
        if( _debug)
        {
            content.innerHTML = "<h2>AJAX</h2>" + pageUrl[0] + '<br>' + hashUrl[0];
        }
        else
        {
            content.innerHTML = "Loading...";
        }
        new Ajax.Request(pageUrl[1],
        {
            method: 'get',
            onComplete: function (req)
            {
                if( req.status == undefined
                ||  req.status == 0
                ||  (req.status >= 200 && req.status < 300) )
                {
                    var response = req.responseText.split('|', 3);
                    var title = response[0];
                    var scriptList = response[1].split('@');
                    if( /MSIE/.test(navigator.userAgent) && !window.opera )
                    {
                        // Try to force IE to not cache this information
                        content.innerHTML = "<META HTTP-EQUIV='Pragma' CONTENT='no-cache'>";
                        content.innerHTML += "<META HTTP-EQUIV='Expires' CONTENT='-1'>";
                        content.innerHTML += response[2];
                    }
                    else
                    {
                        content.innerHTML = response[2];
                    }
                    if( title.length > 0 ) document.title = title;
                    if( scriptList.length > 0 ) loadScripts( scriptList );
                    if( useHistory )
                    {
                        document.location.hash = hashUrl[0];
                    }
                    _openingPage = false;
                    if( initializePanel ) initializePanel()
                }
                else
                {
                    content.innerHTML = '<div class="outlinedTitle">Page Load Error</div>' + req.responseText;
                    content.innerHTML += '<p>Please try again. If problem persists please notify the webmaster</p>';
                    _openingPage = false;
                }
            }
          });
        onSizeChange();
    }
    else
    {
        window.open( url, 'external' );
    }
}

//----------------------------------------------------------------------
//
// For processing form data then opening up a follow-up page.
// Do not use dhtmlHistory on this page since a user will never want
// to go back to this intermediate state, only back to their form input.
//
openForm = function(url,parameters,followUp)
{
	var content = document.getElementById( 'content' );
    _openingPage = true;
    if( _debug)
    {
        content.innerHTML = "<h2>AJAX FORM</h2>" + url + '<br>' + parameters;
    }
    else
    {
        content.innerHTML = "Processing...";
    }
    // Force the POST method on forms since the general case will not know
    // how much data is being sent.
    new Ajax.Request(url,
      {
        method: 'post',
        postBody: parameters,
        onComplete: function (req)
        {
            if( req.status == undefined
            ||  req.status == 0
            ||  (req.status >= 200 && req.status < 300) )
            {
                _openingPage = false;
                if( followUp )
                {
                    content.innerHTML = 'Form accepted. Forwarding to ' + followUp
                    if( _debug ) alert( 'Following up to ' + followUp + '\nResults : ' + req.responseText );
                    openPage( followUp );
                }
                else
                {
                    if( _debug ) alert( 'Staying Here with: ' + req.responseText );
                    // Default to the openPage() behaviour if there is no
                    // followUp page specified.
                    var response = req.responseText.split('|', 3);
                    var title = response[0];
                    var scriptList = response[1].split('@');
                    content.innerHTML = response[2];
                    if( title.length > 0 ) document.title = title;
                    if( scriptList.length > 0 ) loadScripts( scriptList );
                    document.location.hash = hashUrl[0];
                    if( initializePanel ) initializePanel()
                }
            }
            else
            {
                content.innerHTML = '<div class="outlinedTitle">Forms Processing Error</div>' + req.responseText;
                content.innerHTML += '<p>Please try again. If problem persists please notify the webmaster</p>';
                _openingPage = false;
                if( _debug ) alert( 'Check errors please' );
            }
        },
        onFailure: function (req)
        {
            content.innerHTML = 'ERROR: ' + req.responseText;
            _openingPage = false;
            if( _debug ) alert( 'Check errors please' );
        }
    });
}

//----------------------------------------------------------------------
//
// Preprocess the form data into a parameter string suitable for passing
// to AJAX requests.  Keeps the form submission process within the page.
//
submitForm = function(form,url,followUp)
{
    var poststr = Form.serialize( form );
    openForm(url, poststr, followUp);
}


//----------------------------------------------------------------------
//
// Function to dynamically add Javascript and CSS files. Required because
// doing an AJAX load does not seem to execute them when they are embedded
// within a loaded file.
//
var _loadedScripts = '';
loadScripts = function(scripts)
{
    var head = document.getElementsByTagName("head").item(0);
    for( i=0; i<scripts.length; i++ )
    {
        var file     = scripts[i];
        var fileRef  = "";
        var isScript = false;

        // Only load the file if it has not already been loaded.
        if( _loadedScripts.indexOf(file) >= 0 )
            continue;

		// Raw script code
		if( file.indexOf("JS:") != -1 )
		{
            fileRef = document.createElement('script')
			if( _debug ) alert( 'Raw Javascript:\n' + file );
            fileRef.innerHTML = file.substring( file.indexOf("JS:") + 3 );
		}
		// Raw CSS code
		else if( file.indexOf("CSS:") != -1 )
		{
            fileRef = document.createElement('style')
			if( _debug ) alert( 'Raw CSS:\n' + file );
            fileRef.innerHTML = file.substring( file.indexOf("CSS:") + 4 );
		}
		// Reference to a Javascript file
        else if( file.indexOf(".js") != -1 )
        {
            // Javascript files have to create a <script> tag
            fileRef = document.createElement('script')
			if( _debug ) alert( 'Javascript file:\n' + file );
            fileRef.setAttribute("type", "text/javascript");
            fileRef.setAttribute("src", file);
        	isScript = true;
        }
		// Reference to a CSS file
        else if( file.indexOf(".css") != -1 )
        {
            // CSS files have to create a <link> tag
            fileRef=document.createElement("link")
			if( _debug ) alert( 'CSS file:\n' + file );
            fileRef.setAttribute("rel",  "stylesheet");
            fileRef.setAttribute("type", "text/css");
            fileRef.setAttribute("href", file);
        	isScript = true;
        }

        if( fileRef != "" )
        {
            head.appendChild(fileRef);

            // Remember this script being already added to page
			if( isScript )
			{
				_loadedScripts += file + " "
			}
        }
    }
}

//----------------------------------------------------------------------
//
// Our callback to receive history change events.
//
historyChange = function(newLocation, historyData)
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

// the onload event handler that starts the fading.
initialize = function()
{
    if( createMenu ) createMenu();
    //setInterval('swapFade()',wait);

    //----------------------------------------------------------------------
    if( useHistory )
    {
        dhtmlHistory.initialize();
        if( dhtmlHistory.isFirstLoad() )
        {
            if( document.location.hash )
            {
                if( _debug ) alert('INITIAL history' + document.location );
                openPage(document.location.hash + document.location.search);
            }
            else
            {
                if( _debug ) alert('INITIAL DEFAULT history');
                openPage("/cgi-bin/page.cgi?page=home");
            }
        }
 
        //----------------------------------------------------------------------
        // subscribe to DHTML history change events
        dhtmlHistory.addListener(historyChange);
    }
    else
    {
        if( document.location.hash )
        {
            if( _debug ) alert('INITIAL no history' + document.location.search);
            openPage(document.location.hash + document.location.search);
        }
        else
        {
            if( _debug ) alert('INITIAL DEFAULT no history');
            openPage("/cgi-bin/page.cgi?page=home");
        }
    }

    //----------------------------------------------------------------------
    // The main menu has a highlight along the edge. Randomly use one of 3
    // smooth transitions to make this highlight appear.
    //
	var mainMenuHighlight = document.getElementById( 'mainMenuHighlight' );
    if( mainMenuHighlight )
    {
        var rnd = Math.random() * 4;
        if( rnd < 2 )
        {
            Effect.Appear( "mainMenuHighlight", { duration:1, from:0.0, to:1.0 } );
        }
        else if( rnd < 3 )
        {
            Effect.BlindDown( "mainMenuHighlight", { duration:1, from:0.0, to:1.0 } );
        }
        else
        {
            Effect.SlideDown( "mainMenuHighlight", { duration:1, from:0.0, to:1.0 } );
        }
    }
}

//----------------------------------------------------------------------
//
// For repositioning the content subframe when the user changes window size
//
onSizeChange = function()
{
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
    var content = document.getElementById('content');
    content.style.width = (myWidth - _contentXPadding) + 'px';
    content.style.height = (myHeight - _contentYPadding) + 'px';

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
    var logo = $(groupImgName());
    logo.width = _currentImgWidth;
    logo.height = _currentImgHeight;

    Effect.Appear(groupDivName(), { duration:1, from:0.0, to:1.0 });
}
var _currentImgWidth = 174;
var _currentImgHeight = 119;
function bigLogo()
{
    var logo = $(groupImgName());
    _currentImgWidth = 348;
    _currentImgHeight = 238;
    logo.width = _currentImgWidth;
    logo.height = _currentImgHeight;
    return true;
}
function smallLogo()
{
    var logo = $(groupImgName());
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

