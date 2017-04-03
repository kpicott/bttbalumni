//----------------------------------------------------------------------
//
// Set this to '1' to force alerts on AJAX events.
//
var _debug = 0;

//----------------------------------------------------------------------
//
// Global state information
//
var BTTBUserId = -1;
var BTTBOnCommittee = false;
var BTTBFirstName = '';
var BTTBFullName = '';

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
// Checking to see if an element was defined as a function
//
function isFunction(possibleFunction)
{
  return typeof(possibleFunction) === typeof(Function);
}

//----------------------------------------------------------------------
//
// For spam protection of email addresses
//
function makeEmail(name,host)
{
    name = name.replace('__NOSPAM__', '');
    host = host.replace('__NOSPAM__', '');
    document.location.href='mailto:'+name+'@'+host; 
}

//----------------------------------------------------------------------
//
// For some reason embedding this script right in the link causes IE to
// crash so I moved it here. It gives a generic link back to the Cluster
// Map website if there is a problem in the counter for this page.
//
function clustrMapError()
{
    this.onError = null;
    this.src = 'http://clustrmaps.com/images/clustrmaps-back-soon.jpg';
	var clustrMapsLink = document.getElementById( 'clustrMapsLink' );
    clustrMapsLink.href = 'http://clustrmaps.com';
    return true;
}

//----------------------------------------------------------------------
//
// For processing form data then opening up a follow-up page.
// Do not use dhtmlHistory on this page since a user will never want
// to go back to this intermediate state, only back to their form input.
//
function openForm(url,parameters,followUp)
{
    var p = new BTTBUrl.BTTBURLParser(url, 'page2.cgi');
    var hashUrl = p.assembledURL(true);

    _openingPage = true;
    if( _debug) alert( "AJAX openForm:" + url + ' | ' + parameters + ' | ' + followUp );
    $("#content").html( "Processing..." );

    // Force the POST method on forms since the general case will not know
    // how much data is being sent.
    new Ajax.Request(url,
      {
        method: 'post',
        postBody: parameters,
        onComplete: function (req)
        {
            if( req.status === undefined
            ||  req.status === 0
            ||  (req.status >= 200 && req.status < 300) )
            {
                _openingPage = false;
                if( followUp )
                {
                    $("#content").html( 'Form accepted. Forwarding to ' + followUp );
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
                    var scriptList = response[1].split('#!#');
                    $("#content").html( response[2] );
                    if( title.length > 0 )
					{
						$("title").html( title );
					}
                    if( scriptList.length > 0 )
					{
						loadScripts( scriptList );
					}
                    document.location.hash = hashUrl[0];

					var initializePanel = initializePanel || {};
    				if( isFunction(initializePanel) ) initializePanel();
                }
            }
            else
            {
                $("#content").html( '<div class="outlinedTitle">Forms Processing Error</div>'
								  + req.responseText
                				  + '<p>Please try again. If problem persists please notify the webmaster</p>' );
                _openingPage = false;
                if( _debug ) alert( 'Check errors please' );
            }
        },
        onFailure: function (req)
        {
            $("#content").html( 'ERROR: ' + req.responseText );
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
function submitForm(form,url,followUp)
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
function loadScripts(scripts)
{
    for( var i=0; i<scripts.length; i++ )
    {
        var content = scripts[i];

        // Only load the script if it has not already been loaded.
        if( $.inArray(content, _loadedScripts) >= 0 )
		{
            continue;
		}
		_loadedScripts.push( content );

		// Raw script code
		if( content.indexOf("JS:") != -1 )
		{
			if( _debug ) alert( 'Raw Javascript:\n' + content );
            $('<script></script>').html( content.substring( content.indexOf("JS:") + 3 ) )
				.appendTo( "head" );
		}
		// Raw CSS code
		else if( content.indexOf("CSS:") != -1 )
		{
			if( _debug ) alert( 'Raw CSS:\n' + content );
            $('<style></style>').html( content.substring( content.indexOf("CSS:") + 4 ) )
				.appendTo( "head" );
		}
		// Reference to a Javascript file
        else if( content.indexOf(".js") != -1 )
        {
            // Javascript files have to create a <script> tag
			if( _debug ) alert( 'Javascript file:\n' + content );
            $('<script></script>').attr("type", "text/javascript")
					   .attr("src", content)
					   .appendTo( "head" );
        }
		// Reference to a CSS file
        else if( content.indexOf(".css") != -1 )
        {
            // CSS files have to create a <link> tag
			if( _debug ) alert( 'CSS file:\n' + content );
            $("<link></link>").attr("rel",  "stylesheet")
					 .attr("type", "text/css")
            		 .attr("href", content)
					 .appendTo( "head" );
        }
    }
}

//----------------------------------------------------------------------
//
// Our callback to receive history change events.
//
function historyChange(newLocation, historyData)
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

//----------------------------------------------------------------------
//
// For repositioning the content subframe when the user changes window size
//
function onSizeChange()
{
	/*  Old school manual sizing of the content pane
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
	*/

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
    var logo = document.getElementById(groupImgName());
    logo.width = _currentImgWidth;
    logo.height = _currentImgHeight;

    Effect.Appear(groupDivName(), { duration:1, from:0.0, to:1.0 });
}
var _currentImgWidth = 174;
var _currentImgHeight = 119;
function bigLogo()
{
    var logo = document.getElementById(groupImgName());
    _currentImgWidth = 348;
    _currentImgHeight = 238;
    logo.width = _currentImgWidth;
    logo.height = _currentImgHeight;
    return true;
}
function smallLogo()
{
    var logo = document.getElementById(groupImgName());
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

