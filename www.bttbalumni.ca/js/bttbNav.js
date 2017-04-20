// Set this to 1 to enable the 'test' parameter in page loads
var is_testing = true;

/*----------------------------------------------------------------------
	Function to populate the #content element with the new page
	 hash_field: #PAGE:USER specification for the page to load
	 search_field: Parameters sent to the page being loaded (?p=1&u=2...)
*/
function load_content(hash_field, search_field)
{
	var show_committee_content = false;

	// Temporary loading message
    $('#content').html( 'Loading...' );

	// Shut off any document-ready processing from this page
	$(document).ready(function() {});

	location.hash = hash_field;

	var url_params = [];
	if( search_field.length !== 0 )
	{
		url_params = search_field.substr(1).split('&');
	}

	// Check for a current user
	var user_info = CurrentUser();
	if( user_info[0] !== null )
	{
		url_params.push( 'user=' + user_info[0] );
		show_committee_content = parseInt(user_info[1]);
	}

	// Reinterpret the hash as a page parameter
	url_params.push( 'page=' + hash_field.substr(1) );

	// Set this up for testing if requested
	if( is_testing )
	{
		url_params.push( 'test=1' );
	}

	// Construct the final URL with the page parameter and the search parameters merged
	var page = '/cgi-bin/view.cgi?' + url_params.join( '&' );

	// Load the page into the content div
	$('#content').load( page );

	// Selectively enable or disable all of the committee content
	if( show_committee_content )
	{
		$('.committee-only').show();
	}
	else
	{
		$('.committee-only').hide();
	}
}

/*----------------------------------------------------------------------
	Callback triggered when the # component of the URL changes. This
	indicates a new page should be loaded.
*/
function hash_changed()
{
	load_content( location.hash, location.search );
}

/*----------------------------------------------------------------------
	Function to load a new page. If the page looks like an internal link
	then embed it into the current page's content div, otherwise take
	over the entire window.

	Due to the way search fields work if you want to include that you have
	to put it before the hash that identifies the page:

		#store            : Open up the page called "store" within the current frame
		http://google.com : Go to Google
		?a=3#store        : Open up the page called "store" using the search field "?a=3"
		?a=3              : Open up the home page using the search field "?a=3"
*/
function open_page(url)
{
    // Links within this site go through AJAX, others work as usual
    //
    if( url[0] === '#' )
    {
		load_content( url, '' );
	}
	else if( url[0] === '?' )
	{
		var url_split = url.split('#');
		if( url_split.length > 1 )
		{
			load_content( '#' + url_split[1], url_split[0] );
		}
		else
		{
			load_content( '#home', url );
		}
    }
    else
    {
        window.open( url, 'external' );
    }
}

/*----------------------------------------------------------------------
	Navigation menu configuration
*/
var menus = [ ['#home', '<img src="/Images/icon-home.png">']
	, ['70th Anniversary', [ ['#store2017', 'Buy Tickets']
						   , ['#golf2017', 'Golf Tournament']
						   , ['#calendar2017', 'Calendar of Events']
						   , ['#parade2017', 'Parade']
						   , ['#social2017', 'Saturday Social']
						   , ['?#concert2017', 'Concert']
						   , ['#newsletters', 'Reunion News']
						   ]
	  ]
	, ['Alumni',    [ ['@#profiles', 'Profiles']
					, ['@#register', 'My Profile']
					, ['#newsletters', 'News']
					, ['#security', 'Privacy Information']
					]
	  ]
	, ['Memories',  [ ['@#wallaceb', 'Wallace B. Wallace']
					, ['@#drumMajors', 'Drum Majors']
					, ['@#memorials', 'Memorials']
					, ['@#photos', 'Pictures']
					, ['@#memories', 'Memories']
					, ['#tunes', 'Music Clips']
					, ['?#headChaperones', 'Former Head Chaperones']
					, ['?#bandExecutive', 'Former Band Executive']
					, ['?#boosterExecutive', 'Former Band Booster Executive']
					]
	  ]
	, ['Links',     [ ['http://teentourband.org', 'BTTB']
					, ['http://teentourboosters.com', 'Band Boosters']
					, ['http://www.cbc.ca/archives/entry/doug-wrights-family', 'Doug Wright']
					, ['https://burlingtonteentourband.smugmug.com/', 'Band Photo Albums']
					, ['https://www.youtube.com/results?search_query=burlington+teen+tour+band', 'BTTB on YouTube']
					]
	  ]
	, ['Committee', [ ['#committee', 'Old Committee Page']
					, ['?#approve', 'Pending Approvals']
					, ['?#countdowns', 'Edit Countdowns']
					, ['?#newsAdd', 'Edit News Items']
					, ['?#database', 'Database Queries']
					, ['?#reunionData2017', 'Reunion Data']
					, ['#webwork', 'Website Development Plan']
					, ['?#download', 'Download Alumni Data']
					]
	  ]
	];

/*----------------------------------------------------------------------
	Build the navigation bar
*/
function build_navigation()
{
	var menu_html = '';
	menus.forEach( function(menu_entry, index)
	{
		if( typeof menu_entry[1] == 'string' )
		{
			menu_html += '<a href="' + menu_entry[0] + '">';
			menu_html += menu_entry[1] + '</a>\n';
		}
		else
		{
			var committee_class = '';
			if( 'Committee' === menu_entry[0] )
			{
				committee_class = ' committee-only';
			}
			var menu_name = menu_entry[0];
			var submenu = menu_entry[1];
			menu_html += '<div class="dropdown' + committee_class + '">\n';
			menu_html += '  <button class="dropbtn">' + menu_name + '</button>\n';
			menu_html += '  <div class="content">\n';

			submenu.forEach( function(submenu_entry, subindex)
			{
				var link = submenu_entry[0];
				var text = submenu_entry[1];
				if( link[0] === '@' )
				{
					text = "<i class='fa fa-user'></i>&nbsp;" + text;
					link = link.substr(1);
				}
				// Leading "?" means the link is not yet available
				if( link[0] === '?' )
				{
					menu_html += '    <a class="coming-soon"><span>' + text + '</span></a>\n';
				}
				else
				{
					menu_html += '    <a class="non-link" onclick="open_page(\'' + link + '\');">' + text + '</a>\n';
				}
			});
            menu_html += '  </div>\n';
            menu_html += '</div>\n';
		}
	});
	$('.nav').html( menu_html );
}

/*----------------------------------------------------------------------
    Return the content of the login area, based on whether someone is
    already logged in or not.
*/
function set_login_or_logout(user)
{
	var op = 'logout';
    if( user === null )
	{
        op = 'login';
    }
    return '\t$("#login").html( \'<button onclick="javascript:do_' + op + '();"><i class="fa fa-key"></i>&nbsp;' + op.toUpperCase() + '</button>\' );\n';
}

/*----------------------------------------------------------------------
    Return the content of the welcome area, based on whether someone is
    already logged in or not.
*/
function set_register_or_welcome(user_name)
{
    var welcome = '\t$("#welcome").html( \'';
    if( user_name === null )
	{
        welcome += '<button onclick="javascript:open_page(\\\'/#register\\\')"><i class="fa fa-user"></i>&nbsp;REGISTER NOW</button>';
    }
	else
	{
        welcome += 'WELCOME ' + user_name.replace( /\s+$/, '' );
    }
    welcome += '\');\n';
    return welcome;
}

/*----------------------------------------------------------------------
    Look at the current configuration and set any scripts or styles needed
    for the page.
*/
function add_preamble()
{
	// User data returns nulls when nobody is signed in
	var user_info = CurrentUser();
	var user_id = user_info[0];
	var user_name = user_info[2];

	var preamble = '$(document).ready(function() {\n'
					   + set_register_or_welcome(user_name)
    				   + set_login_or_logout(user_id)
    				   + '});\n';

	$('#preamble').html( preamble );
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
