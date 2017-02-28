// Contents of the current cart, represented as an array of keywords
var cart_contents = null;

// Options for shirt sizes
var shirt_sizes = [ [ "WXS", "Women's Extra Small"]
                  , [ "WS",  "Women's Small"]
                  , [ "WM",  "Women's Medium"]
                  , [ "WL",  "Women's Large"]
                  , [ "WXL", "Women's XL"]
                  , [ "W2X", "Women's 2XL"]
                  , [ "MS",  "Men's Small"]
                  , [ "MM",  "Men's Medium"]
                  , [ "ML",  "Men's Large"]
                  , [ "MXL", "Men's XL"]
                  , [ "M2X", "Men's 2XL"]
                  , [ "M3X", "Men's 3XL"]
                  , [ "M4X", "Men's 4XL"]
                  , [ "M5X", "Men's 5XL"]
                  , [ "M6X", "Men's 6XL"]
                  ];

// Possible items for purchase
// Values are [COST, EARLYBIRD DISCOUNT, IS_TAXED, DESCRIPTION]
var store_items = { "allin"      : [150, 20,  true, "All Events"]
                  , "saturday"   : [80,   0,  true, "Saturday Night Social Event"]
                  , "parade"     : [70,   0,  true, "Saturday Morning Parade"]
                  , "hat"        : [15,   0,  true, "70th Anniversary Hat"]
                  , "golf"       : [185, 15, false, "Early-Bird Entrance Into the 70th Anniversary Golf Tournament"]
                  , "golfHole"   : [250,  0, false, "Hole Sponsorship for the 70th Anniversary Golf Tournament"]
                  , "golfDinner" : [60,   0, false, "70th Anniversary Golf Tournament, Dinner Only"]
                  };

// Append the list of shirt options to the cart options that include them
for( var shirt_idx=0; shirt_idx<shirt_sizes.length; ++shirt_idx )
{
    var shirt_info = shirt_sizes[shirt_idx];
    store_items[shirt_info[0]] = [30, 0, true, shirt_info[1] + " 70th Anniversary Shirt"];
    store_items[shirt_info[0]+"_p"] = [0, 0, true, shirt_info[1] + " 70th Anniversary Shirt (for Parade)"];
    store_items[shirt_info[0]+"_a"] = [0, 0, true, shirt_info[1] + " 70th Anniversary Shirt (for All Events)"];
}

//----------------------------------------------------------------------
//
// Figure out if the early-bird discounts apply
//
var today, cutoff;
today = new Date();
cutoff = new Date();
cutoff.setFullYear(2017, 3, 15);
var apply_discounts = (cutoff > today);

//----------------------------------------------------------------------
//
// Take a list of item IDs, which are the keywords of the store_items,
// and return a list of [ [ID, DESCRIPTION, COST, DISCOUNT, TAXABLE] ]
// elements for all of the IDs in the list. Any IDs not recognized will
// not be added to the return list
//
function convert_ids_to_contents(id_list)
{
    var contents = [];
    for( var idx=0; idx<id_list.length; ++idx )
    {
        var id = id_list[idx];
        var store_item = store_items[id] || [0,"Unknown"];
        contents.push( [id, store_item[3], store_item[0], store_item[1], store_item[2]] );
    }
    return contents;
}

//----------------------------------------------------------------------
//
// Return the current contents of the cart in JSON list of lists:
//         [ [ID, DESCRIPTION, COST, DISCOUNT, TAXABLE] ]
//
function get_cart_contents()
{
    // If the cart has nothing in it try to decode the contents from the GET
    // portion of the URL.
    if( cart_contents === null )
    {
        var contents = decodeURIComponent((new RegExp("[?|&]cart=([^&;]+?)(&|#|;|$)").exec(location.href) || [null, ""])[1].replace(/\+/g, "%20")) || null;
        if( contents !== null )
        {
            cart_contents = contents.split( "," );
        }
        else
        {
            cart_contents = [];
        }
    }
    return convert_ids_to_contents( cart_contents );
}
// Index values into the get_cart_contents values
var idx_id  = 0;
var idx_desc = 1;
var idx_cost = 2;
var idx_disc = 3;
var idx_taxed = 4;

//----------------------------------------------------------------------
//
function add_tax(amount)
{
    return Math.round(113.0 * amount) / 100.0;
}

//----------------------------------------------------------------------
//
// Using the current cart contents rebuild the HTML element in id
// "cart_contents" to show the current list of items in the cart.
//
function rebuild_cart()
{
    var cart_info = get_cart_contents();
    var cart_element = document.getElementById( "cart_contents" );

    // Empty out any previous cart contents
    while( cart_element.hasChildNodes() )
    {
        cart_element.removeChild( cart_element.firstChild );
    }

    // Show a special message if the cart is empty
    if( cart_info.length === 0 )
    {
        var p = document.createElement( "p" );
        p.className = "box";
        p.innerHTML = "You have not ordered anything yet. Select an item below to join the fun!";
        cart_element.appendChild( p );
    }
    else
    {
        var cart_title = document.createElement( "h2" );
        cart_title.innerHTML = "Your Cart";
        cart_element.appendChild( cart_title );

        // Build up the cart contents one item at a time
        var cart_table = document.createElement( "table" );
        cart_table.id = "cart";

		var cart_row;
		var description_col;
		var cost_col;
		var remove_col;

        // Table heading
        {
            cart_row = document.createElement( "tr" );

            description_col = document.createElement( "th" );
            description_col.innerHTML = "Description";
            cart_row.appendChild( description_col );

            cost_col = document.createElement( "th" );
            cost_col.innerHTML = "Cost (including HST)";
            cart_row.appendChild( cost_col );

            remove_col = document.createElement( "th" );
            remove_col.innerHTML = "Remove From Cart";
            cart_row.appendChild( remove_col );

            cart_table.appendChild( cart_row );
        }

        // Table contents, one row per item in the cart
        var total_cost = 0.0;
        for( var idx=0; idx<cart_info.length; ++idx )
        {
            var cart_item = cart_info[idx];

            cart_row = document.createElement( "tr" );

            description_col = document.createElement( "td" );
            description_col.innerHTML = cart_item[idx_desc];
            cart_row.appendChild( description_col );

            cost_col = document.createElement( "td" );
            var cost = cart_item[idx_cost];
			if( apply_discounts )
			{
				cost = cost - cart_item[idx_disc];
			}
			if( cart_item[idx_taxed] )
			{
				cost = add_tax(cost);
			}
            cost_col.innerHTML = "$" + cost.toFixed(2);
            total_cost = total_cost + cost;
            cart_row.appendChild( cost_col );

            remove_col = document.createElement( "td" );
            remove_col.innerHTML = "<button onclick='remove_cart_item(\"" + cart_item[idx_id] + "\");'>X</button>";
            remove_col.align = "center";
            cart_row.appendChild( remove_col );

            cart_table.appendChild( cart_row );
        }

        // Total line
        {
            cart_row = document.createElement( "tr" );

            description_col = document.createElement( "td" );
            description_col.innerHTML = "Total";
            cart_row.appendChild( description_col );

            cost_col = document.createElement( "td" );
            cost_col.innerHTML = "$" + total_cost.toFixed(2);
            cart_row.appendChild( cost_col );

            remove_col = document.createElement( "th" );
            remove_col.innerHTML = "";
            cart_row.appendChild( remove_col );

            cart_table.appendChild( cart_row );
        }

        cart_element.appendChild( cart_table );

        var print_button = document.createElement( "button" );
        print_button.innerHTML = "See Printable Form";
        print_button.onclick = print_cart;
        cart_element.appendChild( print_button );
    }
}

//----------------------------------------------------------------------
//
// Create a new window with the contents of the cart in a printable format
//
function print_cart()
{
    var print_wnd = window.open("about:blank", "cart");
    print_wnd.document.write( "<html><head><title>70th Anniversary Reunion Shopping Cart</title></head>\n" );
    print_wnd.document.write( "<body><img src='/Images70th/PrintableFormHeader.jpg'/>\n" );

    // Get the values of the hidden fields containing the logged-in member's
    // information. The odd format is to be consistent with the way PayPal
	// requires these fields to be named.
    var first_name = document.getElementById( "first_name" ).value;
    var last_name = document.getElementById( "last_name" ).value;
	var name = '';
	if( first_name !== null )
	{
		name = first_name;
		if( last_name !== null )
		{
			name = name + " " + last_name;
		}
	}
    var email = document.getElementById( "email" ).value;
    var phone = '';
    var area = document.getElementById( "night_phone_a" ).value;
    var exchange = document.getElementById( "night_phone_b" ).value;
    var number = document.getElementById( "night_phone_c" ).value;
	if( area !== null )
	{
		phone = "(" + area + ") ";
	}
	if( exchange !== null )
	{
		if( number !== null )
		{
			phone = phone + exchange + "-" + number;
		}
	}

    // Populate the purchaser's information
    print_wnd.document.write( "<h2>Your Information</h2>\n" );
    print_wnd.document.write( "<table width='90%' cellpadding='5' border='1'>\n" );
    print_wnd.document.write( "<tr><td width='100'>Name:</td><td>" + name + "</td></tr>\n" );
    print_wnd.document.write( "<tr><td>Email:</td><td>" + email + "</td></tr>\n" );
    print_wnd.document.write( "<tr><td>Phone:</td><td>" + phone + "</td></tr>\n" );
    print_wnd.document.write( "<tr height='150'><td>Special<br/>Instructions:</td><td>&nbsp;</td></tr>\n" );
    print_wnd.document.write( "</table>" );

    print_wnd.document.write( "<h2>Your Order</h2>\n" );
    print_wnd.document.write( "<table width='90%' cellpadding='5' border='1'>" );
    print_wnd.document.write( "<tr><th>Description</th><th width='100'>Cost</th></tr>" );
    var total_cost = 0.0;
    var cart_info = get_cart_contents();
	var discount = 0.0;
	var had_golf = false;
	var had_golf_dinner = false;
	var had_golf_hole = false;
    if( cart_info.length === 0 )
    {
        print_wnd.document.write( "<p>You have not ordered anything yet. Select an item to join the fun!</p>" );
    }
    else
    {
        for( var idx=0; idx<cart_info.length; ++idx )
        {
            var cart_item = cart_info[idx];
			if( cart_item[idx_id] === "golf" )
			{
				had_golf = true;
			}
			else if( cart_item[idx_id] === "golfDinner" )
			{
				had_golf_dinner = true;
			}
			else if( cart_item[idx_id] === "golfHole" )
			{
				had_golf_hole = true;
			}
            var cost = cart_item[idx_cost];
			if( apply_discounts )
			{
				cost = cost - cart_item[idx_disc];
				discount = discount + cart_item[idx_disc];
			}
			if( cart_item[idx_taxed] )
			{
				cost = add_tax(cost);
				discount = discount + add_tax(cart_item[idx_disc]) - cart_item[idx_disc];
			}
            print_wnd.document.write( "<tr>" );
            print_wnd.document.write( "<td>" + cart_item[idx_desc] + "</td>" );
            print_wnd.document.write( "<td align='right'>$" + cost.toFixed(2) + "</td>" );
            total_cost = total_cost + cost;
            print_wnd.document.write( "</tr>\n" );
        }
    }
    print_wnd.document.write( "<tr bgcolor='#d2d2d2'>" );
    print_wnd.document.write( "<td>Total</td>" );
    print_wnd.document.write( "<td align='right'>$" + total_cost.toFixed(2) + "</td>" );
    print_wnd.document.write( "</tr>\n" );
    print_wnd.document.write( "</table>\n" );

	// Congratulate them on their frugality
	if( discount > 0 )
	{
    	print_wnd.document.write( "<p><i>You saved $" + discount.toFixed(2) + " for being an early-bird!</i></p>\n" );
	}

	// Check to see if any further information is required for golf
	if( had_golf )
	{
		print_wnd.document.write( "<table width='90%' cellpadding='5' border='1'>" );
		print_wnd.document.write( "<tr><td width='200'>Golf Partner(s), if any?</td><td>&nbsp;</td></tr>\n" );
		print_wnd.document.write( "</table>\n" );
	}
	if( had_golf || had_golf_dinner )
	{
		print_wnd.document.write( "<p><i>Golf is at Indian Wells Golf Course, 5377 Walker's Line, Burlington</i></p>\n" );
		if( had_golf )
		{
			print_wnd.document.write( "<p><i>BBQ Lunch is at noon, shotgun start is at 1pm</i></p>\n" );
		}
	}
	if( had_golf_dinner )
	{
		print_wnd.document.write( "<p><i>Dinner guests please arrive before 6:30pm for dinner. (Come earlier to watch the golfers!)</i></p>\n" );
	}
	if( had_golf_hole )
	{
		print_wnd.document.write( "<p><i>You will be contacted for further information" );
		print_wnd.document.write( " regarding your hole sponsorship. Send email to" );
		print_wnd.document.write( " golf@bttbalumni.ca if you are not contacted within a week.</i></p>\n" );
	}

    print_wnd.document.write( "</body></html>" );
    print_wnd.document.close();
}

//----------------------------------------------------------------------
//
// Add the item to the cart
//
function add_cart_item(cart_item)
{
    var shirt_select;
    var shirt_option = null;
    var other_item = null;
    // Validate that shirt size was specified if required
    if( cart_item === "allin" )
    {
        shirt_select = document.getElementById( "shirt_size" );
        shirt_option = shirt_select.options[shirt_select.selectedIndex].value;
        if( shirt_option === "" )
        {
            alert( "You must specify a shirt size with the 'All Events' option" );
            return;
        }
        other_item = shirt_option + "_a";
    }
    else if( cart_item === "parade" )
    {
        shirt_select = document.getElementById( "shirt_size" );
        shirt_option = shirt_select.options[shirt_select.selectedIndex].value;
        if( shirt_option === "" )
        {
            alert( "You must specify a shirt size with the 'Parade' option" );
            return;
        }
        other_item = shirt_option + "_p";
    }
    else if( cart_item === "shirt" )
    {
        shirt_select = document.getElementById( "shirt_size" );
        shirt_option = shirt_select.options[shirt_select.selectedIndex].value;
        if( shirt_option === "" )
        {
            alert( "You must specify a shirt size" );
            return;
        }
        cart_item = shirt_option;
    }
    if( cart_contents === null )
    {
        cart_contents = [];
    }
    cart_contents.push( cart_item );
    if( other_item !== null )
    {
        cart_contents.push( other_item );
    }
    rebuild_cart();
}

//----------------------------------------------------------------------
//
// Remove the item from the cart. If the cart item is one of a pair, like
// a shirt and parade, then remove the matching item as well.
//
function remove_cart_item(cart_item)
{
    var cart_el;
    var cart_index;
    cart_index = cart_contents.indexOf( cart_item );
    if( cart_index >= 0 )
    {
        cart_contents.splice( cart_index, 1 );
    }

    // If removing the allin event then remove the shirt for it as well
    //
    if( cart_item === "allin" )
    {
        for( cart_index=0; cart_index<cart_contents.length; ++cart_index )
        {
            cart_el = cart_contents[cart_index];
            if( cart_el.substr(cart_el.length - 2, 2) === "_a" )
            {
                cart_contents.splice( cart_index, 1 );
                break;
            }
        }
    }
    // If removing the parade event then remove the shirt for it as well
    //
    else if( cart_item === "parade" )
    {
        for( cart_index=0; cart_index<cart_contents.length; ++cart_index )
        {
            cart_el = cart_contents[cart_index];
            if( cart_el.substr(cart_el.length - 2, 2) === "_p" )
            {
                cart_contents.splice( cart_index, 1 );
                break;
            }
        }
    }
    // If removing the allin shirt then remove the event as well
    //
    else if( cart_item.substr(cart_item.length - 2, 2) === "_a" )
    {
        cart_index = cart_contents.indexOf( "allin" );
        if( cart_index >= 0 )
        {
            cart_contents.splice( cart_index, 1 );
        }
    }
    // If removing the parade shirt then remove the event as well
    //
    else if( cart_item.substr(cart_item.length - 2, 2) === "_p" )
    {
        cart_index = cart_contents.indexOf( "parade" );
        if( cart_index >= 0 )
        {
            cart_contents.splice( cart_index, 1 );
        }
    }

    rebuild_cart();
}

//----------------------------------------------------------------------
//
// Validate that an item being ordered has had a shirt size selected.
// item is the name of the item being ordered, in a display-friendly
// format - it will be used in the alert if the size is missing.
//
var no_shirt_selected = "-- Select Shirt Size --"; // Same as in bttbStore2017.py
function validate_shirt_size(item)
{
    var shirt_element = document.getElementById( 'shirt' );
	if( shirt_element.value === no_shirt_selected )
	{
		alert( 'Please select a shirt size for "' + item + '"' );
		return false;
	}
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
