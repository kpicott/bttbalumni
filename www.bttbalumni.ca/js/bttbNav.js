/*----------------------------------------------------------------------
	Function to populate the #content element with the new page
	 hash_field: #PAGE:USER specification for the page to load
	 search_field: Parameters sent to the page being loaded (?p=1&u=2...)
*/
function load_content(hash_field, search_field)
{
	var show_committee_content = false;

    $('#content').html( 'Loading...' );

	var url_params = [];
	if( search_field.length !== 0 )
	{
		url_params = search_field.substr(1).split('&');
	}

	// Split the hash into the page to load and the user. If no
	// user was defined try to populate it with the cookie value
	var hash_types = hash_field.split(':');
	if( hash_types.length === 2 )
	{
		url_params.push( 'page=' + hash_types[0].substr(1) );
		url_params.push( 'user=' + hash_types[1] );
	}
	else
	{
		if( hash_types.length === 1 )
		{
			url_params.push( 'page=' + hash_types[0].substr(1) );
		}
		var user_info = CurrentUser();
		if( user_info[0] !== null )
		{
			url_params.push( 'user=' + user_info[0] );
			show_committee_content = parseInt(user_info[1]);
		}
	}
	alert( url_params );

	var page = '/cgi-bin/view.cgi?' + url_params.join( '&' );
	alert( page );

	$('#content').load( page );

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
	Navigation menu configuration
*/
var menus = [ ['/#home', '<img src="/Images/icon-home.png">']
	, ['70th Anniversary', [ ['/#store2017', 'Buy Tickets']
						   , ['/#golf2017', 'Golf Tournament']
						   , ['?/#calendar2017', 'Calendar of Events']
						   , ['?/#parade2017', 'Parade']
						   , ['?/#concert2017', 'Concert']
						   , ['?/#news2017', 'Reunion News']
						   ]
	  ]
	, ['Alumni',    [ ['/#profiles', 'Profiles']
					, ['/#register', 'My Profile']
					, ['/#newsletters', 'News']
					, ['/#security', 'Privacy Information']
					]
	  ]
	, ['Memories',  [ ['/#wallaceb', 'Wallace B. Wallace']
					, ['/#drumMajors', 'Drum Majors']
					, ['/#memorials', 'Memorials']
					, ['/#photos', 'Pictures']
					, ['/#memories', 'Memories']
					, ['/#tunes', 'Music Clips']
					, ['?/#headChaperones', 'Former Head Chaperones']
					, ['?/#bandExecutive', 'Former Band Executive']
					, ['?/#boosterExecutive', 'Former Band Booster Executive']
					]
	  ]
	, ['Links',     [ ['http://teentourband.org', 'BTTB']
					, ['http://teentourboosters.com', 'Band Boosters']
					, ['http://www.cbc.ca/archives/entry/doug-wrights-family', 'Doug Wright']
					, ['?bandPhotoAlbums', 'Band Photo Albums']
					, ['?YouTube', 'BTTB on YouTube']
					]
	  ]
	, ['Committee', [ ['/#committee', 'Old Committee Page']
					, ['?/#approve', 'Pending Approvals']
					, ['?/#countdowns', 'Edit Countdowns']
					, ['?/#newsAdd', 'Edit News Items']
					, ['?/#database', 'Database Queries']
					, ['?/#reunionData2017', 'Reunion Data']
					, ['?/#webwork', 'Website Development Plan']
					, ['?/#download', 'Download Alumni Data']
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
        var committee_class = '';
		if( 'Committee' === menu_entry[0] )
		{
			committee_class = ' class="committee-only"';
		}
		if( typeof menu_entry[1] == 'string' )
		{
			menu_html += '<a ' + committee_class;
			menu_html += ' href="' + menu_entry[0] + '">';
			menu_html += menu_entry[1] + '</a>\n';
		}
		else
		{
			var menu_name = menu_entry[0];
			var submenu = menu_entry[1];
			menu_html += '<div class="dropdown"' + committee_class + '>\n';
			menu_html += '  <button class="dropbtn">' + menu_name + '</button>\n';
			menu_html += '  <div class="content">\n';

			submenu.forEach( function(submenu_entry, subindex)
			{
				var link = submenu_entry[0];
				var text = submenu_entry[1];
				// Leading "?" means the link is not yet available
				if( link[0] === '?' )
				{
					menu_html += '    <a href="" class="coming-soon"><span>' + text + '</span></a>\n';
				}
				else
				{
					menu_html += '    <a href="' + link + '">' + text + '</a>\n';
				}
			});
            menu_html += '  </div>\n';
            menu_html += '</div>\n';
		}
	});
	$('.nav').html( menu_html );
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
