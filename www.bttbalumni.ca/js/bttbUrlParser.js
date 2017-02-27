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
// Throws an exception if the specified url is invalid
//
BTTBUrl.BTTBURLParser = function(url)
{
	this._urlFields = {'Port' : 4, 'Protocol' : 2, 'Host' : 3, 'Pathname' : 5, 'URL' : 0, 'QueryString' : 6, 'Page' : 7, 'User' : 8, 'PageQuery' : 9};
	this._urlExp = /^((\w+):\/\/)?([^\/\?:#]+)?:?(\d+)?(\/*?[^\?#]+)?\??([^#]+)?#?([^\?:]*):?(\d*)?\??([^#]+)?/;
	this._pageExp = /page=(\w+)(&?user=(\d+))?&?(.*)?/;
	this._pageFields = {'PageQuery' : 4, 'Page' : 1, 'User' : 3};
	this._values = {};
	for( var f in this._urlFields )
	{
		this['get' + f] = this._makeGetter(f);
		this['set' + f] = this._makeSetter(f);
	}
	if (typeof url != 'undefined')
	{
		this._parse(url);
	}
}
 
//----------------------------------------------------------------------
//
// setURL is a method to set new URL values on the same object and re-parse.
//
BTTBUrl.BTTBURLParser.prototype.setURL = function(url)
{
	this._parse(url);
}

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._initValues = function()
{
	for(var f in this._urlFields)
	{
		this._values[f] = '';
	}
}

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
		if( typeof r[this._urlFields[f]] != 'undefined' )
		{
			this._values[f] = r[this._urlFields[f]];
		}
	}
	// Check for the alternate form and convert into page form if found
	// Technically this makes the getXXX() fields not match the URL but
	// that is the point.
	if( (typeof r[this._urlFields['Pathname']] != 'undefined')
	&&  (r[this._urlFields['Pathname']].search('page.cgi') > 0) )
	{
		if( typeof r[this._urlFields['QueryString']] != 'undefined' )
		{
			var p = this._pageExp.exec(r[this._urlFields['QueryString']]);
			if( p )
			{
				this._values['Pathname'] = '/cgi-bin/page.cgi';
				this._values['QueryString'] = '';
				for( var pf in this._pageFields )
				{
					this._values[pf] = '';
					if( typeof p[this._pageFields[pf]] != 'undefined' )
					{
						this._values[pf] = p[this._pageFields[pf]];
					}
				}
			}
		}
		else
		{
			this._values['Page'] = 'home';
		}
	}
}

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._makeGetter = function(field)
{
	return function()
	{
		return this._values[field];
	}
}

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype._makeSetter = function(field)
{
	return function(newValue)
	{
		this._values[field] = newValue;
	}
}

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype.assembledURL = function(asHash)
{
	var shortName = '';
	var url = this.getProtocol();
	if( url.length > 0 )
		url = url + '://'
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
		shortName = '/cgi-bin/page.cgi?page=';
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
}

//----------------------------------------------------------------------
//
BTTBUrl.BTTBURLParser.prototype.debug = function()
{
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
		'http://www.bttbalumni.ca:8080/cgi-bin/page.cgi?page=frag&b=5':1,
		'http://www.bttbalumni.ca:8080/cgi-bin/page.cgi?page=frag&user=123&b=5':1,
		'/#frag':1,
		'/#frag:123?b=5':1,
		'#frag:123?b=5':1
	};
	testURLs[this.getURL()] = 1;
	var u1 = new BTTBUrl.BTTBURLParser( 'http://www.bttbalumni.ca' );
	document.write( '<table border="1"><tr bgcolor="#ddddff">' );
	document.write( '<th>URL</th>\n' );
	document.write( '<th>PORT</th>\n' );
	document.write( '<th>PROTOCOL</th>\n' );
	document.write( '<th>HOST</th>\n' );
	document.write( '<th>PATHNAME</th>\n' );
	document.write( '<th>QUERY STRING</th>\n' );
	document.write( '<th>PAGE</th>\n' );
	document.write( '<th>USER</th>\n' );
	document.write( '<th>PAGE QUERY</th>\n' );
	document.write( '<th>ASSEMBLED HASH</th>\n' );
	document.write( '<th>ASSEMBLED URL</th>\n' );
	document.write( '</tr>\n' );
	for( var url in testURLs )
	{
		u1.setURL(url);
		document.write( '<tr><th>' + u1.getURL() + '</th>' );
		document.write( '<td>' + u1.getPort() + '</td>\n' );
		document.write( '<td>' + u1.getProtocol() + '</td>\n' );
		document.write( '<td>' + u1.getHost() + '</td>\n' );
		document.write( '<td>' + u1.getPathname() + '</td>\n' );
		document.write( '<td>' + u1.getQueryString() + '</td>\n' );
		document.write( '<td>' + u1.getPage() + '</td>\n' );
		document.write( '<td>' + u1.getUser() + '</td>\n' );
		document.write( '<td>' + u1.getPageQuery() + '</td>\n' );
		document.write( '<td>' + u1.assembledURL(true)[0] + '</td>\n' );
		document.write( '<td>' + u1.assembledURL(false)[0] + '</td>\n' );
		document.write( '</tr>\n' );
	}
	document.write( '</table\n' );
}

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
}

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

	u1.setURL( 'http://www.bttbalumni.ca:8080/cgi-bin/page.cgi?page=frag&b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '' );

	u1.setURL( 'http://www.bttbalumni.ca:8080/cgi-bin/page.cgi?page=frag&user=123&b=5' );
	errors = errors + u1._testEqual( bttbHost, 'frag', 'b=5', '123' );

	u1.setURL( '#frag:123?b=5' );
	errors = errors + u1._testEqual( '', 'frag', 'b=5', '123' );

	if( errors.length > 0 )
	{
		document.write( '<h1>BTTB URL Parser Errors</h1>' );
		document.write( errors );
	}
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
