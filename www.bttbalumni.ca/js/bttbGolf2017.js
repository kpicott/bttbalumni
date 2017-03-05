// Contents of the current cart, represented as an array of keywords.
//  	amount           : Dollar amount for the item, not including tax
//		item_name        : Description of item
//		onN              : Name of option N (name or email)
//		osN              : Value of option N
//						   Field containing option = osN_X for item X
//		tax_rate         : Rate of tax to apply to the item, as a percentage
//		discount_amount  : Amount of discount - only non-zero items will have this
//
var cart_contents = [ ];
var empty_cart_msg = "Your cart is currently empty - add items for purchase.";

// Special codes used as identifiable onN options
var golfer_name_code        = "Golfer Name";
var lunch_name_code         = "Lunch Guest Name";
var dinner_name_code        = "Dinner Guest Name";
var hole_sponsor_name_code  = "Sponsor Name";
var hole_sponsor_email_code = "Sponsor Email";

// Special ids to identify the different types of items. They're used for
// printing the form so they should be descriptive.
var golfer_id  = "Golf Tournament Entry";
var lunch_id   = "Golf Tournament Lunch";
var dinner_id  = "Golf Tournament Dinner";
var sponsor_id = "Golf Tournament Hole Sponsorship";
var instructions_id = "Special Instructions";

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
// Add a new golfer to the cart contents
//
function add_golfer()
{
	var golfer = {};
	golfer.amount = 200;
	if( apply_discounts )
	{
		golfer.discount_amount = 15;
	}
	golfer.item_name = golfer_id;
	golfer.on0 = golfer_name_code;
	golfer.os0 = "";
	golfer.tax_rate = 0;

	cart_contents.push( golfer );
	rebuild_golf_cart();
}

//----------------------------------------------------------------------
//
// Add a new diner to the cart contents
//
function add_lunch()
{
	var diner = {};
	diner.amount = 20;
	diner.item_name = lunch_id;
	diner.on0 = lunch_name_code;
	diner.os0 = "";
	diner.tax_rate = 0;

	cart_contents.push( diner );
	rebuild_golf_cart();
}

//----------------------------------------------------------------------
//
// Add a new diner to the cart contents
//
function add_diner()
{
	var diner = {};
	diner.amount = 60;
	diner.item_name = dinner_id;
	diner.on0 = dinner_name_code;
	diner.os0 = "";
	diner.tax_rate = 0;

	cart_contents.push( diner );
	rebuild_golf_cart();
}

//----------------------------------------------------------------------
//
// Add a new hole sponsorship to the cart contents
//
function sponsor_hole()
{
	var sponsor = {};
	sponsor.amount = 250;
	sponsor.item_name = sponsor_id;
	sponsor.on0 = hole_sponsor_name_code;
	sponsor.os0 = "";
	sponsor.on1 = hole_sponsor_email_code;
	sponsor.os1 = "";
	sponsor.tax_rate = 0;

	cart_contents.push( sponsor );
	rebuild_golf_cart();
}

//----------------------------------------------------------------------
//
// Remove an existing item from the cart.
// Does nothing if the item does not exist.
//
function remove_cart_item(item_idx)
{
	if( cart_contents.length > item_idx )
	{
		cart_contents.splice( item_idx, 1 );
		rebuild_golf_cart();
	}
}

//----------------------------------------------------------------------
//
// Look through the fields on the form and ensure they are all consistent.
// Things to check are:
//		- Every golfer has a name
//		- Every diner has a name
//		- Every hole sponsorship has a name and an email
//		- Every hole sponsorship has non-zero quantity
//
function validate_cart_contents()
{
	var cart_item;
    for( var idx=0; idx<cart_contents.length; ++idx )
    {
		var cart_info = cart_contents[idx];
		if( cart_info.hasOwnProperty("on0") )
		{
			cart_item = document.getElementById( "os0_" + idx );
			if( cart_item )
			{
				if( cart_item.value.length === 0 )
				{
					alert( 'You must fill in all of the "' + cart_info.on0 + '" fields' );
					return false;
				}
				cart_info.os0 = cart_item.value;
			}
		}
		if( cart_info.hasOwnProperty("on1") )
		{
			cart_item = document.getElementById( "os1_" + idx );
			if( cart_item )
			{
				if( cart_item.value.length === 0 )
				{
					alert( 'You must fill in all of the "' + cart_info.on1 + '" fields' );
					return false;
				}
				cart_info.os1 = cart_item.value;
			}
		}
	}

	return true;
}

//----------------------------------------------------------------------
//
// Build the Paypal order button using the current cart contents,
// omitting any fields that are not fully filled in.
//
function rebuild_golf_paypal_button()
{
	// Common cart boilerplate

	// tax_cart = "0"
	// amount
	// item_name
	// on0
	// os0
}

//----------------------------------------------------------------------
//
// Using the current cart contents rebuild the HTML element in id
// "cart_contents" to show the current list of items in the cart.
//
function rebuild_golf_cart()
{
    var cart_element = document.getElementById( "cart_contents" );

	// Get the current instructions, if any, so that they are up to date
	var instructions = '';
	var instructions_el = document.getElementById( "instructions" );
	if( instructions_el )
	{
		instructions = instructions_el.value;
	}

    // Empty out any previous cart contents
    while( cart_element.hasChildNodes() )
    {
        cart_element.removeChild( cart_element.firstChild );
    }

	// If the cart is empty just show the empty cart message
	if( cart_contents.length === 0 )
	{
		var msg = document.createElement( "h2" );
		msg.innerHTML = empty_cart_msg;
		cart_element.addChild( msg );
		return;
	}

    // Build up the cart contents one item at a time
    var cart_table = document.createElement( "table" );
    cart_table.width = "100%";
    cart_table.id = "cart";

	// Add a title row
	var title_row = document.createElement( "tr" );
	var title_col = document.createElement( "th" );
	title_col.innerHTML = "Item";
	title_row.appendChild( title_col );
	title_col = document.createElement( "th" );
	title_col.innerHTML = "Required Information";
	title_row.appendChild( title_col );
	title_col = document.createElement( "th" );
	title_col.innerHTML = "Cost";
	title_row.appendChild( title_col );
	title_col = document.createElement( "th" );
	title_col.innerHTML = "Remove";
	title_row.appendChild( title_col );
	cart_table.appendChild( title_row );

    // Just the paypal elements for now
	var total_cost = 0;
    for( var idx=0; idx<cart_contents.length; ++idx )
    {
		var cart_row = document.createElement( "tr" );
        var cart_info = cart_contents[idx];

		// Paypal stuff
		//var cart_index = 1;
		//for( var item_key in cart_info )
		//{
		//    if( ! cart_info.hasOwnProperty(item_key) )
		//	{
		//		continue;
		//	}
		//	var item_data = cart_info[item_key];

		//	var field = document.createElement( "input" );
		//	field.type = "hidden";
		//	field.name = item_key + "_" + cart_index;
		//	field.value = item_data;

			// cart_element.appendChild( field );

		//	cart_index++;
		//}
		var cart_col = document.createElement( "td" );
		cart_col.innerHTML = cart_info.item_name;
		cart_row.appendChild( cart_col );

		cart_col = document.createElement( "td" );
		cart_col.innerHTML = "<input type='text' size='32' maxlength='64' id='os0_" + idx + "' placeholder='" + cart_info.on0 + "'>";
		if( cart_info.hasOwnProperty("on1") )
		{
			cart_col.innerHTML += "<br><input type='text' size='32' maxlength='64' id='os1_" + idx + "' placeholder='" + cart_info.on1 + "'>";
		}
		cart_row.appendChild( cart_col );

		cart_col = document.createElement( "td" );
		cart_col.innerHTML = "$" + cart_info.amount;
		cart_row.appendChild( cart_col );
		total_cost += cart_info.amount;

        var remove_col = document.createElement( "td" );
        remove_col.innerHTML = "<button onclick='remove_cart_item(\"" + idx + "\");'>X</button>";
        remove_col.align = "center";
        cart_row.appendChild( remove_col );

		cart_table.appendChild( cart_row );
    }

	// If the cart has elements then include isntructions, a total line, and payment buttons
	var instructions_row = document.createElement( "tr" );
	var instructions_col = document.createElement( "td" );
	instructions_col.innerHTML = instructions_id;
	instructions_row.appendChild( instructions_col );
	//
	instructions_col = document.createElement( "td" );
	instructions_col.colSpan = 3;
	instructions_col.innerHTML = "<textarea rows='4' cols='64' maxlength='256' id='instructions' placeholder='Enter instructions here...'>" + instructions;
	instructions_row.appendChild( instructions_col );
	//
	cart_table.appendChild( instructions_row );

	// Totals row
	var total_row = document.createElement( "tr" );
	//
	var total_col = document.createElement( "th" );
	total_col.innerHTML = "Total";
	total_row.appendChild( total_col );
	//
	total_col = document.createElement( "th" );
	total_col.innerHTML = "";
	total_row.appendChild( total_col );
	//
	total_col = document.createElement( "th" );
	total_col.innerHTML = "$" + total_cost;
	total_row.appendChild( total_col );
	//
	total_col = document.createElement( "th" );
	total_col.innerHTML = "";
	total_row.appendChild( total_col );
	//
	cart_table.appendChild( total_row );

	// Separate the table of items from the payment buttons
	cart_element.appendChild( cart_table );

	// Payment buttons
	var button_container = document.createElement( "div" );
	button_container.className = "golf_payment_buttons";

		var form_button = document.createElement( "button" );
		form_button.className = "shadow_button";
		form_button.onclick = function() { print_golf_cart(); };
		form_button.innerHTML = 'Pay Online With Paypal';
		button_container.appendChild( form_button );

		form_button = document.createElement( "button" );
		form_button.className = "shadow_button";
		form_button.onclick = function() { print_golf_cart(); };
		form_button.innerHTML = "View Printable Order";
		button_container.appendChild( form_button );

	cart_element.appendChild( button_container );
}

//----------------------------------------------------------------------
//
// Create a new window with the contents of the cart in a printable format
//
function print_golf_cart()
{
	if( ! validate_cart_contents() )
	{
		return;
	}

	// Special instructions are not stored anywhere so get them out first.
	var instructions = '';
	var instructions_el = document.getElementById( "instructions" );
	if( instructions_el )
	{
		instructions = instructions_el.value;
	}

    var print_wnd = window.open("about:blank", "golf_cart");
    print_wnd.document.write( "<html><head><title>70th Anniversary Reunion Golf Shopping Cart</title></head>\n" );
    print_wnd.document.write( "<body><img src='/Images70th/PrintableFormHeader.jpg'/>\n" );

    // Get the values of the hidden fields containing the logged-in member's
    // information. The odd format is to be consistent with the way PayPal
	// requires these fields to be named.
    var first_name = member_info.first_name;
    var last_name = member_info.last_name;
	var name = '';
	if( first_name !== null )
	{
		name = first_name;
		if( last_name !== null )
		{
			name = name + " " + last_name;
		}
	}
    var email = member_info.email;
    var phone = '';
    var area = member_info.night_phone_a;
    var exchange = member_info.night_phone_b;
    var number = member_info.night_phone_c;
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
    print_wnd.document.write( "<tr height='150'><td>Special<br/>Instructions:</td><td>" + instructiosn + "</td></tr>\n" );
    print_wnd.document.write( "</table>" );

    print_wnd.document.write( "<h2>Your Order</h2>\n" );
    print_wnd.document.write( "<table width='90%' cellpadding='5' border='1'>" );
    print_wnd.document.write( "<tr><th>Item</th><th>Information</th><th width='100'>Cost</th></tr>" );
    var total_cost = 0.0;
	var discount = 0.0;
	var had_golf = false;
	var had_golf_dinner = false;
	var had_golf_hole = false;
    if( cart_contents.length === 0 )
    {
        print_wnd.document.write( "<p>" + empty_cart_msg + "</p>" );
    }
    else
    {
        for( var idx=0; idx<cart_contents.length; ++idx )
        {
            var cart_item = cart_contents[idx];

            print_wnd.document.write( "<tr>" );
            print_wnd.document.write( "<td>" + cart_item[idx_desc] + "</td>" );

			switch( cart_item.item_name )
			{
				case golfer_id:
            		print_wnd.document.write( "<td>Golfer Name</td>" );
					break;
				case lunch_id:
            		print_wnd.document.write( "<td>Lunch Guest Name</td>" );
					break;
				case dinner_id:
            		print_wnd.document.write( "<td>Dinner Guest Name</td>" );
					break;
				case sponsor_id:
            		print_wnd.document.write( "<td>Sponsor Name<br>Sponsor Email</td>" );
					break;
			}
            print_wnd.document.write( "<td align='right'>$" + cost.toFixed(2) + "</td>" );
            total_cost = total_cost + cost;
            print_wnd.document.write( "</tr>\n" );

//  	amount           : Dollar amount for the item, not including tax
//		item_name        : Description of item
//		onN              : Name of option N (name or email)
//		osN              : Value of option N
//						   Field containing option = osN_X for item X
//		tax_rate         : Rate of tax to apply to the item, as a percentage
//		discount_amount  : Amount of discount - only non-zero items will have this

//			if( cart_item[idx_id] === "golf" )
//			{
//				had_golf = true;
//			}
//			else if( cart_item[idx_id] === "golfDinner" )
//			{
//				had_golf_dinner = true;
//			}
//			else if( cart_item[idx_id] === "golfHole" )
//			{
//				had_golf_hole = true;
//			}
//            var cost = cart_item[idx_cost];
//			if( apply_discounts )
//			{
//				cost = cost - cart_item[idx_disc];
//				discount = discount + cart_item[idx_disc];
//			}
//			if( cart_item[idx_taxed] )
//			{
//				cost = add_tax(cost);
//				discount = discount + add_tax(cart_item[idx_disc]) - cart_item[idx_disc];
//			}
//            print_wnd.document.write( "<tr>" );
//            print_wnd.document.write( "<td>" + cart_item[idx_desc] + "</td>" );
//            print_wnd.document.write( "<td align='right'>$" + cost.toFixed(2) + "</td>" );
//            total_cost = total_cost + cost;
//            print_wnd.document.write( "</tr>\n" );
        }
    }
    print_wnd.document.write( "<tr bgcolor='#d2d2d2'>" );
    print_wnd.document.write( "<td>Total</td>" );
    print_wnd.document.write( "<td></td>" );
    print_wnd.document.write( "<td></td>" );
    print_wnd.document.write( "<td align='right'>$" + total_cost.toFixed(2) + "</td>" );

    print_wnd.document.write( "</tr>\n" );
    print_wnd.document.write( "</table>\n" );
//
//	// Congratulate them on their frugality
//	if( discount > 0 )
//	{
//    	print_wnd.document.write( "<p><i>You saved $" + discount.toFixed(2) + " for being an early-bird!</i></p>\n" );
//	}
//
//	// Check to see if any further information is required for golf
//	if( had_golf )
//	{
//		print_wnd.document.write( "<table width='90%' cellpadding='5' border='1'>" );
//		print_wnd.document.write( "<tr><td width='200'>Golf Partner(s), if any?</td><td>&nbsp;</td></tr>\n" );
//		print_wnd.document.write( "</table>\n" );
//	}
//	if( had_golf || had_golf_dinner )
//	{
//		print_wnd.document.write( "<p><i>Golf is at Indian Wells Golf Course, 5377 Walker's Line, Burlington</i></p>\n" );
//		if( had_golf )
//		{
//			print_wnd.document.write( "<p><i>BBQ Lunch is at noon, shotgun start is at 1pm</i></p>\n" );
//		}
//	}
//	if( had_golf_dinner )
//	{
//		print_wnd.document.write( "<p><i>Dinner guests please arrive before 6:30pm for dinner. (Come earlier to watch the golfers!)</i></p>\n" );
//	}
//	if( had_golf_hole )
//	{
//		print_wnd.document.write( "<p><i>You will be contacted for further information" );
//		print_wnd.document.write( " regarding your hole sponsorship. Send email to" );
//		print_wnd.document.write( " golf@bttbalumni.ca if you are not contacted within a week.</i></p>\n" );
//	}

    print_wnd.document.write( "</body></html>" );
    print_wnd.document.close();
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
