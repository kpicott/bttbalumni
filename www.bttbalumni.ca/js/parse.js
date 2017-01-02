//
// queryString(KEY) figures out the key value in the current page.
// queryNoPage() returns the query string with the "page=" value removed.
//
function PageQuery(q,ignorePage)
{
	if(q.length > 1) this.q = q.substring(1, q.length);
	else this.q = null;
	this.keyValuePairs = new Array();
	if(q)
	{
		for(var i=0; i < this.q.split("&").length; i++)
		{
			var param = this.q.split("&")[i];
			if( ! ignorePage || param.split("=")[0] != "page" )
				this.keyValuePairs[i] = param;
		}
	}
	this.getKeyValuePairs = function() { return this.keyValuePairs; }
	this.getValue = function(s)
	{
		for(var j=0; j < this.keyValuePairs.length; j++)
		{
			if(this.keyValuePairs[j].split("=")[0] == s)
				return this.keyValuePairs[j].split("=")[1];
		}
		return false;
	}
	this.getParameters = function()
	{
		var a = new Array(this.getLength());
		for(var j=0; j < this.keyValuePairs.length; j++)
		{
			a[j] = this.keyValuePairs[j].split("=")[0];
		}
		return a;
	}
	this.assembledQueryString = function()
	{
		return this.keyValuePairs[j].join("&");
	}
	this.getLength = function() { return this.keyValuePairs.length; }
}

function queryNoPage()
{
	var page = new PageQuery(window.location.search,1);
	return page.assembledQueryString();
}

function queryString(key)
{
	if( window.location.search )
	{
		var page = new PageQuery(window.location.search,0);
		return unescape(page.getValue(key));
	}
	return "";
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
