var currentMusic = "OFF";
//
// Mouse button image switches
//
function musicOver(button)
{
	$(button).src = "/Music/Navigation/nav" + button + "Over.gif";
}
function musicUp(button)
{
	$(button).src = "/Music/Navigation/nav" + button + "Normal.gif";
}
function musicDown(button)
{
	$(button).src = "/Music/Navigation/nav" + button + "Active.gif";
}
function setDisable(button,state)
{
	if( state )
	{
		$(button).src = "/Music/Navigation/nav" + button + "Disabled.gif";
	}
	else
	{
		$(button).src = "/Music/Navigation/nav" + button + "Normal.gif";
	}
}
function writeMusicNav(name, navFunc, initialState, width, alt)
{
	document.write( "<th height='19' width='" + width + "'>" );
	document.write( "<a onmouseover='musicOver(\"" + name + "\")'" );
	document.write( "   onmousedown='musicDown(\"" + name + "\")'" );
	document.write( "   onmouseup='musicUp(\"" + name + "\")'" );
	document.write( "   onmouseout='musicUp(\"" + name + "\")'" );
	document.write( "   href='javascript:" + navFunc + "'>" );
	document.write( "   <img id='" + name + "' src='/Music/Navigation/nav" );
	document.write( name + initialState + ".gif' " );
	document.write( "border='0'></a>" );
	document.write( "</th>\n" );
}

//----------------------------------------------------------------------
function switchTune(newMelody)
{
	// Switch off the previous tune
	lastTune = $( "Music" + currentMusic );
	lastTune.src = "/Music/Navigation/navMusic" + currentMusic + ".gif"

	// Change the tune title
	tuneNameHtml = $( "tuneName" );
	tuneNameHtml.innerHTML = "Tune " + newMelody

	// Reload the music
	embedMusicHtml = $( "tuneEmbed" );
	musicFile = "/Music/MUTE.mov";
	autoStart = "true";
	volume = 50;
	switch( newMelody )
	{
		case 1:
			musicFile = "/Music/ConcertVariations.wma";
			break;
		case 2:
			musicFile = "/Music/WashingtonPost.wma";
			break;
		case 3:
			musicFile = "/Music/ManciniSpectacular.wma";
			break;
		case "OFF":
			musicFile = "/Music/MUTE.mov";
			autoStart = "false";
			image = $( "MusicOFF" );
			image.src = "/Music/Navigation/navMusicOFFActive.gif"
			break;
	}
	embedMusicHtml.innerHTML = "<embed volume='" + volume + "' src='"
			+ musicFile
			+ "' height='16' width='190' loop='false' controls='smallconsole' autostart='"
			+ autoStart + "' id='Music'/>";

	// Set the current tune
	currentMusic = newMelody;
}

//----------------------------------------------------------------------
function writeMusicControls()
{
	document.write( "<p>&nbsp;</p><div id='buttonMusic'>" );
	document.write( "<table cellspacing='0' cellpadding='0' border='0' width='100%'>" );
	document.write( "<tr>" );
	document.write( "	<th id='tuneEmbed' width='212' colspan='5'>" );
	document.write( "<embed volume='50' src='/Music/MUTE.mov' height='16'" );
	document.write( " width='190' loop='false' controls='smallconsole'" );
	document.write( " autostart='false' id='Music'/></th>" );
	document.write( "</tr>" );
	//----------------------------------------------------------------------
	document.write( "<tr>" );
	writeMusicNav( "Music1", "switchTune(1)", "Normal", 41, "ConcertVariations" );
	writeMusicNav( "Music2", "switchTune(2)", "Normal", 31, "WashingtonPost" );
	document.write( "<th height='19' width='68' class='navMusic' id='tuneName' valign='center'" );
	document.write( " background='/Music/Navigation/nav_music_middle.gif'>" );
	document.write( "Tune OFF</th>" );
	writeMusicNav( "Music3", "switchTune(3)", "Normal", 31, "ManciniSpectacular" );
	writeMusicNav( "MusicOFF", "switchTune(\"OFF\")", "Active", 41, "MUTE" );
	document.write( "</tr>" );
	document.write( "</table>" );
	document.write( "</div>" );
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
