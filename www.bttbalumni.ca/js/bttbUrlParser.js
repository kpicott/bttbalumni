//----------------------------------------------------------------------
//
// Usage: var p = new BTTBUrl.BTTBURLParser(URL);
//
// Primary form of URL, used to bookmark:
//		http://HOST/#PAGE[:USER]?arg1=1&arg2=2');
// Alternate form, used to load page content directly:
// 		http://HOST/PATH/?page=PAGE&user=USER&arg1=1&arg2=2
//
// p.getHost() == 'HOST';
// p.getPage() == 'PAGE';
// p.getUser() == 'USER';
// p.getPageQuery() == 'arg1=1&arg2=2';
//
if( typeof BTTBUrl == 'undefined' )
{
	var BTTBUrl = {};
}

//----------------------------------------------------------------------
//
// Creates a BTTBURLParser instance
//
// @classDescription	Creates an BTTBURLParser instance
// @return {Object}	return an BTTBURLParser object
// {String} url	The url to parse
// {String} cgi	The CGI script that loads the page
// Throws an exception if the specified url is invalid
//
BTTBUrl.BTTBURLParser = function(url, cgi)
{
	this._urlFields = {'Port' : 4, 'Protocol' : 2, 'Host' : 3, 'Pathname' : 5, 'URL' : 0, 'QueryString' : 6, 'Page' : 7, 'User' : 8, 'PageQuery' : 9};
	this._urlExp = /^((\w+):\/\/)?([^\/\?:#]+)?:?(\d+)?(\/*?[^\?#]+)?\??([^#]+)?#?([^\?:]*):?(\d*)?\??([^#]+)?/;
	this._pageExp = /page=(\w+)(&?user=(\d+))?&?(.*)?/;
	this._pageFields = {'PageQuery' : 4, 'Page' : 1, 'User' : 3};
	this._values = {};
	this._pageCGI = cgi;
	alert( "Opening parser using " + cgi );
	for( var f in this._urlFields )
	{
		if( this._urlFields.hasOwnProperty(f) )
		{
			this['get' + f] = this._makeGetter(f);
			this['set' + f] = this._makeSetter(f);
		}
	}
	if (typeof url != 'undefined')
	{
		this._parse(url);
	}
};
 
//----------------------------------------------------------------------
//
// setURL is a method to set new URL values on the same object and re-parse.
//
BTTBUrl.BTTBURLParser.prototype.setURL = function(url)
{
	this._parse(url);
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._initValues = function()
{
	for(var f in this._urlFields)
	{
		if( this._urlFields.hasOwnProperty(f) )
		{
			this._values[f] = '';
		}
	}
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._parse = function(url)
{
	this._initValues();
	var r = this._urlExp.exec(url);
	if( !r )
	{
		throw "BTTBURLParser::_parse -> Invalid URL";
	}
	for( var f in this._urlFields )
	{
		if( this._urlFields.hasOwnProperty(f) )
		{
			if( typeof r[this._urlFields[f]] != 'undefined' )
			{
				this._values[f] = r[this._urlFields[f]];
			}
		}
	}
	// Check for the alternate form and convert into page form if found
	// Technically this makes the getXXX() fields not match the URL but
	// that is the point.
	if( (typeof r[this._urlFields.Pathname] != 'undefined')
	&&  (r[this._urlFields.Pathname].search(this._pageCGI) > 0) )
	{
		if( typeof r[this._urlFields.QueryString] != 'undefined' )
		{
			var p = this._pageExp.exec(r[this._urlFields.QueryString]);
			if( p )
			{
				this._values.Pathname = '/cgi-bin/' + this._pageCGI;
				this._values.QueryString = '';
				for( var pf in this._pageFields )
				{
					if( this._pageFields.hasOwnProperty(pf) )
					{
						this._values[pf] = '';
						if( typeof p[this._pageFields[pf]] != 'undefined' )
						{
							this._values[pf] = p[this._pageFields[pf]];
						}
					}
				}
			}
		}
		else
		{
			this._values.Page = 'home';
		}
	}
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._makeGetter = function(field)
{
	return function() { return this._values[field]; };
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._makeSetter = function(field)
{
	return function(newValue) { this._values[field] = newValue; };
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype.assembledURL = function(asHash)
{
	var shortName = '';
	var url = this.getProtocol();
	if( url.length > 0 )
	{
		url = url + '://';
	}
	if( this.getHost().length > 0 )
	{
		url = url + this.getHost();
		if( this.getPort().length > 0 )
			url = url + ':' + this.getPort();
	}
	if( asHash )
	{
		url = url + '/cgi-bin/nav.cgi';
		shortName = '#';
		if( this.getPage().length > 0 )
		{
			shortName = shortName + this.getPage();
			if( this.getUser() && (this.getUser().length > 0) )
				shortName = shortName + ':' + this.getUser();
		}
		else
		{
			shortName = shortName + 'home';
		}
		if( this.getPageQuery().length > 0 )
		{
			shortName = shortName + '?' + this.getPageQuery();
		}
	}
	else
	{
		shortName = '/cgi-bin/' + this._pageCGI + '?page=';
		if( this.getPage().length > 0 )
		{
			shortName = shortName + this.getPage();
			if( this.getUser() && (this.getUser().length > 0) )
				shortName = shortName + '&user=' + this.getUser();
		}
		else
		{
			shortName = shortName + 'home';
		}
		if( this.getPageQuery().length > 0 )
		{
			shortName = shortName + '&' + this.getPageQuery();
		}
	}
	url = url + shortName;
	return [shortName, url];
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype.debug = function()
{
	// Object construction doesn't like in-place string building
	var pageUrl1 = 'http://www.bttbalumni.ca:8080/cgi-bin/' + this._pageCGI + '?page=frag&b=5';
	var pageUrl2 = 'http://www.bttbalumni.ca:8080/cgi-bin/' + this._pageCGI + '?page=frag&user=123&b=5';

	var testURLs = {
		'http://www.bttbalumni.ca':1,
		'http://www.bttbalumni.ca/':1,
		'http://www.bttbalumni.ca#home':1,
		'http://www.bttbalumni.ca/#home':1,
		'http://www.bttbalumni.ca:8080/#frag?b=5':1,
		'http://www.bttbalumni.ca:8080/#frag:123?b=5':1,
		'http://www.bttbalumni.ca:8080/cgi-bin/nav.cgi':1,
		'http://www.bttbalumni.ca:8080/cgi-bin/nav.cgi?a=4#frag?b=5':1,
		'http://www.bttbalumni.ca:8080/cgi-bin/nav.cgi?a=4#frag:123?b=5':1,
		pageUrl1:1,
		pageUrl2:1,
		'/#frag':1,
		'/#frag:123?b=5':1,
		'#frag:123?b=5':1
	};
	testURLs[this.getURL()] = 1;
	var u1 = new BTTBUrl.BTTBURLParser( 'http://www.bttbalumni.ca' );
	var table = $('<table></table>' ).attr( "border", "1" );
	var tr = $('<tr></tr>').attr( "bgcolor", "#ddddff" );
	$( '<th></th>\n' ).html( 'URL' ).appendTo( tr );
	$( '<th></th>\n' ).html( 'PORT' ).appendTo( tr );
	$( '<th></th>\n' ).html( 'PROTOCOL' ).appendTo( tr );
	$( '<th></th>\n' ).html( 'HOST' ).appendTo( tr );
	$( '<th></th>\n' ).html( 'PATHNAME' ).appendTo( tr );
	$( '<th>STRING</th>\n' ).html( 'QUERY STRING' ).appendTo( tr );
	$( '<th></th>\n' ).html( 'PAGE' ).appendTo( tr );
	$( '<th></th>\n' ).html( 'USER' ).appendTo( tr );
	$( '<th>QUERY</th>\n' ).html( 'PAGE QUERY' ).appendTo( tr );
	$( '<th>HASH</th>\n' ).html( 'ASSEMBLED HASH' ).appendTo( tr );
	$( '<th>URL</th>\n' ).html( 'ASSEMBLED URL' ).appendTo( tr );
	table.append( tr );

	for( var url in testURLs )
	{
		if( testURLs.hasOwnProperty(url) )
		{
			tr = $('<tr></tr>');
			u1.setURL(url);
			$( '<th></th>' ).html( u1.getURL() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getPort() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getProtocol() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getHost() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getPathname() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getQueryString() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getPage() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getUser() ).appendTo( tr );
			$( '<td></td>' ).html( u1.getPageQuery() ).appendTo( tr );
			$( '<td></td>' ).html( u1.assembledURL(true)[0] ).appendTo( tr );
			$( '<td></td>' ).html( u1.assembledURL(false)[0] ).appendTo( tr );
			table.append( tr );
		}
	}
	$("body").append( table );
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._testEqual = function(host, page, query, user)
{
	var unequal = '';
	if( this.getHost() != host )
	{
		unequal = unequal + "<br>BTTBURLParser::testEqual(host - " + this.url + ") -> " + this.getHost() + " != " + host;
	}
	if( this.getPage() != page )
	{
		unequal = unequal + "<br>BTTBURLParser::testEqual(page - " + this.url + ") -> " + this.getPage() + " != " + page;
	}
	if( this.getPageQuery() != query )
	{
		unequal = unequal + "<br>BTTBURLParser::testEqual(query - " + this.url + ") -> " + this.getPageQuery() + " != " + query;
	}
	if( this.getUser() != user )
	{
		unequal = unequal + "<br>BTTBURLParser::testEqual(user - " + this.url + ") -> " + this.getUser() + " != " + user;
	}
	return unequal;
};

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype.test = function()
{
	var bttbHost = 'www.bttbalumni.ca';
	var errors = '';

	var u1 = new BTTBUrl.BTTBURLParser( 'http://www.bttbalumni.ca' );
	errors = errors + u1._testEqual( bttbHost, '', '', '' );

	u1.setURL( 'http://www.bttbalumni.ca/' );
	errors = errors + u1._testEqual( bttbHost, '', '', '' );

	u1.setURL( 'http://www.bttbalumni.ca#home' );
	errors = errors + u1._testEqual( bttbHost, 'home', '', '' );

	u1.setURL( 'http://www.bttbalumni.ca/#home' );
	errors = errors + u1._testEqual( bttbHost, 'home', '', '' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/#frag?b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/#frag:123?b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '123' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/cgi-bin/nav.cgi' );
	errors = errors + u1._testEqual( bttbHost, '', '', '' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/cgi-bin/nav.cgi?a=4#frag?b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/cgi-bin/nav.cgi?a=4#frag:123?b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '123' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/cgi-bin/' + this._pageCGI + '?page=frag&b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/cgi-bin/' + this._pageCGI + '?page=frag&user=123&b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '123' );

	u1.setURL( '#frag:123?b=5' );
	errors = errors + u1._testEqual( '', 'frag', 'b=5', '123' );

	if( errors.length > 0 )
	{
		$( '<h1></h1>' ).html( 'BTTB URL Parser Errors' ).appendTo( 'body' );
		$( '<div></div>' ).html( errors ).appendTo( 'body' );
	}
};

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
