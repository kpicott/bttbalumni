//
// Handle music playing icon
//
var currentPage = 1;
var activeElement = 0;
var nextDisabled = 1;
var prevDisabled = 1;
var relHome = "";
if( window.location.protocol == "file:" )
{
	var pathArray = new Array;
	pathArray = window.location.pathname.split("/");
	if( pathArray.length < 3 )
	{
		// Path may have had Windows style backslash separations
		pathArray = window.location.pathname.split("\\");
	}
	pathArray.pop();
	relHome = "file://" + pathArray.join("/") + "/";
}
function link(url)
{
	// Returns a link relative to the current location
	// If in http: world the link itself is relative, but for some
	// reason file links require path prepending.
	return relHome + url;
}
function events()
{
	this.eventNames = new Array;
	this.pageCounts = new Array;
	this.getMethods = new Array;
}
var eventList = new events;
function addEvent(name, count, getMethod)
{
	eventList.eventNames.push( name );
	eventList.pageCounts.push( count );
	eventList.getMethods.push( getMethod );
}
function eventPage()
{
	pageData = eventList.getMethods[activeElement]( currentPage );
	mainFrame = getFrame( "main" );
	var mainDocument = mainFrame.contentDocument;
	if( ! mainDocument )
	{
		mainDocument = parent.frames[2].document;
	}
	mainDocument.open();
	mainDocument.write( "<html>" );
	mainDocument.writeln( "<style type='text/css'>" );
	mainDocument.writeln( "BODY	{ font-family:	'Franklin Gothic', Arial, sans-serif;" );
	mainDocument.writeln( "		  color:	#546b7e; }" );
	mainDocument.writeln( "A:link    { color:	#546b7e; }" );
	mainDocument.writeln( "A:visited { color:	#546b7e; }" );
	mainDocument.writeln( "A:active  { color:	#f46b7e; }" );
	mainDocument.writeln( "H1		{ font-size:	32; }" );
	mainDocument.writeln( "H2		{ font-size:	18; }" );
	mainDocument.writeln( "P		{ font-size:	16;" );
	mainDocument.writeln( "		  font-weight:  bold;" );
	mainDocument.writeln( "		  text-align:	justify; }" );
	mainDocument.writeln( ".video	{ font-size:	16;" );
	mainDocument.writeln( "		  font-weight:  bold;" );
	mainDocument.writeln( "		  text-align:	center; }" );
	mainDocument.writeln( ".navcount	{ font-size:	12;	color: white; }" );
	mainDocument.writeln( ".navmusic	{ font-size:	12;	color: white; }" );
	mainDocument.writeln( "A:link    IMG { border:	1px solid #546b7e; }" );
	mainDocument.writeln( "A:visited IMG { border:	1px solid #546b7e; }" );
	mainDocument.writeln( "A:active  IMG { border:	1px solid #f46b7e; }" );
	mainDocument.writeln( "</style>" );
	mainDocument.write( "<body background='" + link("Frames/frame_right.jpg") + "'>" );
	mainDocument.write( pageData );
	mainDocument.write( "</body></html>" );
	mainDocument.close();
}
function changePage(newPage)
{
	activeElement = newPage;
	gotoPage( 1 );
}
function getElement(name)
{
    if (document[name])
    {
		return document[name];
	}
    if (document.layers)
    {
		return document.layers[name];
	}
	if (document.all)
	{
		return document.all[name];
	}
	return document.getElementById( name );
}
function getFrame(name)
{
	if( parent.document.getElementById )
	{
		return parent.document.getElementById( name );
	}
    if (parent.document[name])
    {
		return parent.document[name];
	}
    if (parent.document.layers)
    {
		return parent.document.layers[name];
	}
	if (parent.document.all)
	{
		return parent.document.all[name];
	}
}
function navOn(name)
{
	if( ((name == "back") && prevDisabled) 
	||  ((name == "forward") && nextDisabled)
	||  ((name == "musicOFF") && (currentMusic == "OFF"))
	||  ((name == "music1") && (currentMusic == 1))
	||  ((name == "music2") && (currentMusic == 2))
	||  ((name == "music3") && (currentMusic == 3))
	||  ((name == "music4") && (currentMusic == 4)) )
	{
		return;
	}
	image = getElement( name );
	image.src = "Navigation/nav_" + name + "_over.gif"
}
function navOff(name)
{
	if( ((name == "back") && prevDisabled) 
	||  ((name == "forward") && nextDisabled)
	||  ((name == "musicOFF") && (currentMusic == "OFF"))
	||  ((name == "music1") && (currentMusic == 1))
	||  ((name == "music2") && (currentMusic == 2))
	||  ((name == "music3") && (currentMusic == 3))
	||  ((name == "music4") && (currentMusic == 4)) )
	{
		return;
	}
	image = getElement( name );
	image.src = "Navigation/nav_" + name + ".gif"
}
function navPress(name)
{
	if( ((name == "back") && prevDisabled) 
	||  ((name == "forward") && nextDisabled)
	||  ((name == "musicOFF") && (currentMusic == "OFF"))
	||  ((name == "music1") && (currentMusic == 1))
	||  ((name == "music2") && (currentMusic == 2))
	||  ((name == "music3") && (currentMusic == 3))
	||  ((name == "music4") && (currentMusic == 4)) )
	{
		return;
	}
	image = getElement( name );
	image.src = "Navigation/nav_" + name + "_press.gif"
}
function navDisabled(name)
{
	image = getElement( name );
	image.src = "Navigation/nav_" + name + "_disabled.gif"
}
function activate(name)
{
	if( eventList.eventNames[activeElement] == name )
	{
		return;
	}
	image = getElement( name );
	image.src = name + "/titleActive.gif"
}
function deactivate(name)
{
	if( eventList.eventNames[activeElement] == name )
	{
		return;
	}
	image = getElement( name );
	image.src = name + "/title.gif"
}
function makeActive(id)
{
	if( eventList.eventNames[activeElement] != "" )
	{
		image = getElement( eventList.eventNames[activeElement] );
		image.src = eventList.eventNames[activeElement] + "/title.gif"
	}
	activeElement = id;
	image = getElement( eventList.eventNames[activeElement] );
	image.src = eventList.eventNames[activeElement] + "/titleOn.gif"
	currentPage = 0;
}
function gotoPage(page)
{
	currentPage = page;
	if( currentPage == 1 )
	{
		prevDisabled = 1;
		navDisabled( "back" );
	}
	else
	{
		prevDisabled = 0;
		navOff( "back" );
	}
	if( currentPage == eventList.pageCounts[activeElement] )
	{
		nextDisabled = 1;
		navDisabled( "forward" );
	}
	else
	{
		nextDisabled = 0;
		navOff( "forward" );
	}
	countHtml = getElement( "count" );
	countHtml.innerHTML = "<img border='0' src='Navigation/clear.gif' height='8'><br>" + page + " of " + eventList.pageCounts[activeElement] + "</th>";

	eventPage();
}
function firstPage()
{
	gotoPage( 1 );
}
function prevPage()
{
	if( currentPage > 1 )
	{
		gotoPage( currentPage - 1 );
	}
}
function nextPage()
{
	if( currentPage < eventList.pageCounts[activeElement] )
	{
		gotoPage( currentPage + 1 );
	}
}
function lastPage()
{
	gotoPage( eventList.pageCounts[activeElement] );
}
function getFrameHeight()
{
	var mainFrame = getFrame( "main" );
	var mainDocument = mainFrame.contentDocument;
	var height = 512;
	if( mainDocument )
	{
		height = window.innerHeight;
		// Give the thumbnail some padding
		height = height - 64;
	}
	else
	{
		mainDocument = parent.frames[2].document;
		height = mainDocument.body.offsetHeight;
		// Give the thumbnail some padding
		height = height - 64;
	}
	return height;
}
function externalLink(href, image, text)
{
	var iLink = link( image );
	return "<a target='image' href='" + href + "'>"
		 + "<img border='1' height='512' src='" + iLink + "'>"
		 + "</a><p>" + text + "</p>";
}
function standardLink(image, text)
{
	var iLink = link( image );
	return "<p>"
		 + text
		 + "</p><a target='image' href='"
		 + iLink
		 + "'><br><img border='1' height='512' src='"
		 + iLink
		 + "'></a>";
}
function movieThumb(movie, thumb, width, text)
{
	var iLink = link( thumb );
	var vLink = link( "loadVideo.html" ) + "?" + movie;
	return	"<a onmouseup='top.frames[\"lower\"].switchTune(\"OFF\")'"
		+	" target='image'"
		+   " href='" + vLink + "'>"
		+	"<img border='1' width='" + width + "' src='" + iLink + "'>"
		+	text + "</a>\n";
}
function movieLink(movie, thumb, text)
{
	return "<p>"
		 + text
		 + "</p>" + movieThumb(movie, thumb, 512, "");
}
