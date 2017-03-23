// Change these values to make Paypal live
var PAYPAL_EMAIL = "bttb@burlington.ca";
var PAYPAL_URL   = "https://www.paypal.com/cgi-bin/webscr";
//var PAYPAL_EMAIL = "bttb-seller@picott.ca";
//var PAYPAL_URL   = "https://www.sandbox.paypal.com/cgi-bin/webscr";

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

var no_shirt_selected = "-- Select Shirt Size --"; // Same as in bttbStore2017.py

// Special codes used as identifiable onN options
var all_inclusive_name_code = "Name";
var all_inclusive_size_code = "Shirt Size";
var saturday_name_code      = "Name";
var parade_name_code        = "Name";
var parade_size_code        = "Shirt Size";
var shirt_size_code         = "Shirt Size";

// Special ids to identify the different types of items. They're used for
// printing the form so they should be descriptive.
var all_inclusive_id  = "All-Inclusive Pass, Hat, and Shirt";
var saturday_id       = "Saturday Night Social Ticket";
var parade_id         = "Parade Spot and Shirt";
var shirt_id          = "70th Anniversary Shirt";
var hat_id            = "70th Anniversary Hat";
var instructions_id   = "Special Instructions";

//----------------------------------------------------------------------
//
// Figure out if the early-bird discounts apply
//
var today, cutoff;
today = new Date();
cutoff = new Date();
cutoff.setFullYear(2017, 3, 15);
var apply_discounts = (cutoff > today);
if( apply_discounts )
{
	all_inclusive_id += " (Early-Bird Rate)";
}

//----------------------------------------------------------------------
//
// Add HST to the given amount
//
function add_tax(amount)
{
    return Math.round(113.0 * amount) / 100.0;
}

//----------------------------------------------------------------------
//
// Calculate the tax on a specific item
// tax_rate is a percentage (e.g. 13 for HST)
//
function tax_on_item(amount, tax_rate)
{
    return Math.round(tax_rate * amount) / 100.0;
}

//----------------------------------------------------------------------
//
// Validate that an item being ordered has had a name specified.
//
// name_id : unique ID of the "text" field containing the name.
// item : name of the item being ordered, in a display-friendly
// 		  format - it will be used in the alert if the name is missing.
//
// Returns null if the name was not present, otherwise returns the name
//
function validate_name(name_id, item)
{
	var name = document.getElementById( name_id );
	if( ! name || (name.value.length === 0) )
	{
		alert( 'Please enter a name for the "' + item + '"' );
		return null;
	}
	return name.value;
}

//----------------------------------------------------------------------
//
// Validate that an item being ordered has had a shirt size selected.
//
// shirt_id : unique ID of the "select" field containing the shirt option.
// item : name of the item being ordered, in a display-friendly
//		 format - it will be used in the alert if the size is missing.
//
// Returns null if the size was not specified, otherwise returns the size
//
function validate_size(shirt_id, item)
{
    var shirt_element = document.getElementById( shirt_id );
	if( ! shirt_element || (shirt_element.value === no_shirt_selected) )
	{
		alert( 'Please select a shirt size for the "' + item + '"' );
		return null;
	}
	return shirt_element.value;
}


//----------------------------------------------------------------------
//
// Add a new all-inclusive participant to the cart contents
//
function add_all_inclusive()
{
	var name = validate_name( 'allin_name', 'All-Inclusive Ticket' );
	var size = validate_size( 'allin_size', 'All-Inclusive Ticket' );
	if( ! name || ! size )
	{
		return;
	}

	var attendee = {};
	attendee.amount = 145;
	if( apply_discounts )
	{
		attendee.discount_amount = 20;
	}
	attendee.item_name = all_inclusive_id;
	attendee.on0 = all_inclusive_name_code;
	attendee.os0 = name;
	attendee.on1 = all_inclusive_size_code;
	attendee.os1 = size;
	attendee.tax_rate = 13;

	cart_contents.push( attendee );
	rebuild_cart();
}

//----------------------------------------------------------------------
//
// Add a new Saturday night social ticket to the cart contents
//
function add_saturday()
{
	var name = validate_name( 'saturday_name', 'Saturday Night Social' );
	if( ! name )
	{
		return;
	}

	var socializer = {};
	socializer.amount = 95;
	socializer.item_name = saturday_id;
	socializer.on0 = saturday_name_code;
	socializer.os0 = name;
	socializer.tax_rate = 13;

	cart_contents.push( socializer );
	rebuild_cart();
}

//----------------------------------------------------------------------
//
// Add a new parade participant to the cart contents
//
function add_parade()
{
	var name = validate_name( 'parade_name', 'Parade' );
	var size = validate_size( 'parade_size', 'Parade' );
	if( ! name || ! size )
	{
		return;
	}

	var marcher = {};
	marcher.amount = 45;
	marcher.item_name = parade_id;
	marcher.on0 = parade_name_code;
	marcher.os0 = name;
	marcher.on1 = parade_size_code;
	marcher.os1 = size;
	marcher.tax_rate = 13;

	cart_contents.push( marcher );
	rebuild_cart();
}

//----------------------------------------------------------------------
//
// Add a new shirt to the cart contents
//
function add_shirt()
{
	var size = validate_size( 'shirt_size', '70th Anniversary Golf Shirt' );
	if( ! size )
	{
		return;
	}

	var shirt = {};
	shirt.amount = 35;
	shirt.item_name = shirt_id;
	shirt.on0 = shirt_size_code;
	shirt.os0 = size;
	shirt.tax_rate = 13;

	cart_contents.push( shirt );
	rebuild_cart();
}

//----------------------------------------------------------------------
//
// Add a new hat to the cart contents
//
function add_hat()
{
	var hat = {};
	hat.amount = 15;
	hat.item_name = hat_id;
	hat.tax_rate = 13;

	cart_contents.push( hat );
	rebuild_cart();
}

//----------------------------------------------------------------------
//
// Remove an existing item from the cart.
// Does nothing if the item does not exist.
//
function remove_cart_item(item_el)
{
	var item_idx = item_el.value;
	if( cart_contents.length > item_idx )
	{
		cart_contents.splice( item_idx, 1 );
		rebuild_cart();
	}
}

//----------------------------------------------------------------------
//
// Get any special instructions
//
function get_instructions()
{
	var instructions = '';
	var instructions_el = document.getElementById( "instructions" );
	if( instructions_el )
	{
		instructions = instructions_el.value;
	}
	return instructions;
}

//----------------------------------------------------------------------
//
// Callback for when a cart item had option details modified.
// Updates the Paypal button fields so that it's always ready to go.
//
function update_cart_option(option_el)
{
	var paypal_el = document.getElementById( "paypal_" + option_el.id );
	if( option_el && paypal_el )
	{
		paypal_el.value = option_el.value;
	}
}

//----------------------------------------------------------------------
//
// Build and return a hidden input document element
//
function hidden_input_element(name, value)
{
	return hidden_input_element_with_id(name, value, "paypal_" + name);
}

//----------------------------------------------------------------------
//
// Build and return a hidden input document element
//
function hidden_input_element_with_id(name, value, id)
{
	var input = document.createElement( "input" );
	input.type = "hidden";
	input.name = name;
	input.value = value;
	input.id = id;
	return input;
}

//----------------------------------------------------------------------
//
// Build the Paypal order button using the current cart contents,
// omitting any fields that are not fully filled in.
//
function rebuild_paypal_button()
{
	// Look for the div containing the paypal button. If it could
	// not be found then bail out, there's nowhere to put this.
	var paypal_button = document.getElementById( "paypal_button" );
	if( ! paypal_button )
	{
		return;
	}

	// Common cart boilerplate
    var form  = document.createElement( "form" );
	form.target = "_self";
	form.className = "inline_form";
	form.method = "post";
	form.action = PAYPAL_URL;

	var paypal_info = { "cmd"           : "_ext-enter"
					  , "redirect_cmd"  : "_cart"
    				  , "currency_code" : "CAD"
    				  , "shipping"      : "0"
    				  , "cancel_return" : "http://bttbalumni.ca/#store2017"
    				  , "cbt"           : "Return to the BTTB 70th Anniversary Reunion"
    				  , "return"        : "http://bttbalumni.ca/#thanks2017"
    				  , "image_url"     : "http://bttbalumni.ca/Images/SiteLogoSmall.png"
    				  , "shopping_url"  : "http://bttbalumni.ca/#store2017"

					  , "email"         : member_info.email
					  , "first_name"    : member_info.first_name
					  , "last_name"     : member_info.last_name
					  , "night_phone_a" : member_info.night_phone_a
					  , "night_phone_b" : member_info.night_phone_b
					  , "night_phone_c" : member_info.night_phone_c

					  , "upload"        : "1"
					  , "business"      : PAYPAL_EMAIL
					  };

	// First the boilerplate
	for( var name in paypal_info )
	{
		if( paypal_info.hasOwnProperty(name) )
		{
			form.appendChild( hidden_input_element( name, paypal_info[name] ) );
		}
	}

    for( var idx=1; idx<=cart_contents.length; ++idx )
    {
        var cart_info = cart_contents[idx-1];

		form.appendChild( hidden_input_element( "amount_" + idx, cart_info.amount ) );
		form.appendChild( hidden_input_element( "item_name_" + idx, cart_info.item_name ) );
		form.appendChild( hidden_input_element( "tax_rate_" + idx, cart_info.tax_rate ) );

		// Optional discount amount
		if( cart_info.hasOwnProperty("discount_amount") )
		{
			form.appendChild( hidden_input_element( "discount_amount_" + idx, cart_info.discount_amount ) );
		}

		// Optional option 0
		if( cart_info.hasOwnProperty("on0") )
		{
			form.appendChild( hidden_input_element( "on0_" + idx, cart_info.on0 ) );
			form.appendChild( hidden_input_element( "os0_" + idx, cart_info.os0 ) );
		}

		// Optional option 1
		if( cart_info.hasOwnProperty("on1") )
		{
			form.appendChild( hidden_input_element( "on1_" + idx, cart_info.on1 ) );
			form.appendChild( hidden_input_element( "os1_" + idx, cart_info.os1 ) );
		}
	}

	// Instructions cannot be sent as a separate field in Paypal so they
	// have to be packaged up as a free item.
	var instructions = get_instructions();
	var instructions_idx = cart_contents.length + 1;

	form.appendChild( hidden_input_element( "item_name_" + instructions_idx, instructions_id ) );
	form.appendChild( hidden_input_element( "amount_" + instructions_idx, 0 ) );
	form.appendChild( hidden_input_element( "on0_" + instructions_idx, "Note" ) );
	form.appendChild( hidden_input_element_with_id( "os0_" + instructions_idx, instructions, "paypal_instructions" ) );

	// Payment button
	var form_button = document.createElement( "button" );
	form_button.className = "shadow_button";
	form_button.name = "submit";
	form_button.innerHTML = 'Pay Online With Paypal';
	form.appendChild( form_button );

	// Replace the contents of the paypal button div with the new button
    while( paypal_button.hasChildNodes() )
    {
        paypal_button.removeChild( paypal_button.firstChild );
    }
	paypal_button.appendChild( form );
}

//----------------------------------------------------------------------
//
// Using the current cart contents rebuild the HTML element in id
// "cart_contents" to show the current list of items in the cart.
//
function rebuild_cart()
{
    var cart_element = document.getElementById( "cart_contents" );

	// Get the current instructions, if any, so that they are up to date
	var instructions = get_instructions();

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
		cart_element.appendChild( msg );
		return;
	}

    // Build up the cart contents one item at a time
    var cart_table = document.createElement( "table" );
    cart_table.width = "100%";
    cart_table.id = "cart";
    cart_table.class = "cart";

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

	var update_cart_fn = function() { update_cart_option(this); };
	var remove_cart_fn = function() { remove_cart_item(this); };

    // Build the individual items
	var total_cost = 0;
	var total_tax = 0;
    for( var idx=1; idx<=cart_contents.length; ++idx )
    {
		var cart_row = document.createElement( "tr" );
        var cart_info = cart_contents[idx-1];

		var cart_col = document.createElement( "td" );
		cart_col.innerHTML = cart_info.item_name;
		cart_row.appendChild( cart_col );

		cart_col = document.createElement( "td" );
			if( cart_info.hasOwnProperty("on0") )
			{
				cart_col.innerHTML = "<b>" + cart_info.on0 + ": </b><i>" + cart_info.os0 + "</i>";
				if( cart_info.hasOwnProperty("on1") )
				{
					cart_col.innerHTML += "<br><b>" + cart_info.on1 + ": </b><i>" + cart_info.os1 + "</i>";
				}
			}
		cart_row.appendChild( cart_col );

		cart_col = document.createElement( "td" );
		var cost = cart_info.amount;
		if( cart_info.hasOwnProperty("discount_amount") )
		{
			cost -= cart_info.discount_amount;
		}
		cart_col.innerHTML = "$" + cost;
		cart_row.appendChild( cart_col );
		total_cost += cost;
		total_tax += tax_on_item( cost, cart_info.tax_rate );

        var remove_col = document.createElement( "td" );
			var remove_button = document.createElement( "button" );
			remove_button.innerHTML = "X";
			remove_button.value = idx - 1;
			remove_button.onclick = remove_cart_fn;
			remove_col.appendChild( remove_button );
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
		var instructions_text = document.createElement( "textarea" );
		instructions_text.rows = "4";
		instructions_text.cols = "64";
		instructions_text.maxlength = "256";
		instructions_text.id = "instructions";
		instructions_text.placeholder = "Enter any messages for us here...";
		instructions_text.oninput = update_cart_fn;
		instructions_text.innerHTML += instructions;
		instructions_col.appendChild( instructions_text );
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
	total_col.innerHTML = "plus HST of $" + total_tax.toFixed(2);
	total_row.appendChild( total_col );
	//
	total_cost += total_tax;
	total_col = document.createElement( "th" );
	total_col.innerHTML = "$" + total_cost.toFixed(2);
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
	button_container.className = "payment_buttons";

		// Put in a placeholder for the Paypal button - populate below
		var paypal_div = document.createElement( "div" );
		paypal_div.id = "paypal_button";
		button_container.appendChild( paypal_div );

		// The cheque method will trigger a page build
		var form_button = document.createElement( "button" );
		form_button.className = "shadow_button";
		form_button.onclick = function() { print_cart(); };
		form_button.innerHTML = "View Printable Order Form";
		button_container.appendChild( form_button );

	cart_element.appendChild( button_container );

	rebuild_paypal_button();
}

//----------------------------------------------------------------------
//
// Create a new window with the contents of the cart in a printable format
//
function print_cart()
{
	// Special instructions are not stored anywhere so get them out first.
	var instructions = get_instructions();

    var print_wnd = window.open("about:blank", "cart");
    print_wnd.document.write( "<html><head><title>70th Anniversary Reunion Shopping Cart</title>\n" );
    print_wnd.document.write( "<link href='https://fonts.googleapis.com/css?family=Raleway|Source+Sans+Pro:700' rel='stylesheet'>" );
    print_wnd.document.write( "<style>" );
    print_wnd.document.write( "* { font-family: Raleway; font-size: 12; }" );
    print_wnd.document.write( "</style>" );
    print_wnd.document.write( "</head>" );
    print_wnd.document.write( "<body><img width='90%' src='/Images70th/PrintableFormHeader.jpg'/>\n" );

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
    print_wnd.document.write( "<tr><td>Special<br/>Instructions:</td><td><p>" + instructions + "</p></td></tr>\n" );
    print_wnd.document.write( "</table>" );

    print_wnd.document.write( "<h2>Your Order</h2>\n" );
    print_wnd.document.write( "<table width='90%' cellpadding='5' border='1'>" );
    print_wnd.document.write( "<tr><th>Item</th><th>Information</th><th width='100'>Cost</th></tr>" );
    var total_cost = 0.0;
	var total_tax = 0.0;
	var discount = 0.0;
    if( cart_contents.length === 0 )
    {
        print_wnd.document.write( "<p>" + empty_cart_msg + "</p>" );
    }
    else
    {
		var tax = 0.0;
        for( var idx=1; idx<=cart_contents.length; ++idx )
        {
            var cart_item = cart_contents[idx-1];

			// Calculate the cost of this item
            var cost = cart_item.amount;
			if( cart_item.hasOwnProperty("discount_amount") )
			{
				cost = cost - cart_item.discount_amount;
				discount = discount + cart_item.discount_amount;
			}
			if( cart_item.tax_rate > 0 )
			{
				total_tax += tax_on_item( cost, cart_item.tax_rate );
				discount = discount + add_tax(cart_item.discount_amount) - cart_item.discount_amount;
			}
            total_cost = total_cost + cost;

            print_wnd.document.write( "<tr>" );
            print_wnd.document.write( "<td>" + cart_item.item_name + "</td>" );

			// If there are any information fields add them here
            print_wnd.document.write( "<td>" );
			if( cart_item.hasOwnProperty("on0") )
			{
				print_wnd.document.write( cart_item.on0 );
				print_wnd.document.write( " = " );
				print_wnd.document.write( cart_item.os0 );
			}
			if( cart_item.hasOwnProperty("on1") )
			{
				print_wnd.document.write( "<br>" );
				print_wnd.document.write( cart_item.on1 );
				print_wnd.document.write( " = " );
				print_wnd.document.write( cart_item.os1 );
			}
            print_wnd.document.write( "</td>" );

            print_wnd.document.write( "<td align='right'>$" + cost.toFixed(2) + "</td>" );
            print_wnd.document.write( "</tr>\n" );
        }
    }
    print_wnd.document.write( "<tr bgcolor='#d2d2d2'>" );
    print_wnd.document.write( "<td>Total</td>" );
    print_wnd.document.write( "<td>plus HST of $" + total_tax.toFixed(2) + "</td>" );
	total_cost += total_tax;
    print_wnd.document.write( "<td align='right'>$" + total_cost.toFixed(2) + "</td>" );

    print_wnd.document.write( "</tr>\n" );
    print_wnd.document.write( "</table>\n" );

	// Congratulate them on their frugality
	if( discount > 0 )
	{
    	print_wnd.document.write( "<p><i>You saved $" + discount.toFixed(2) + " by being an early-bird!</i></p>\n" );
	}

	print_wnd.document.write( "<h2><font color='#af4c50'>Thank you for your order, see you in June!</font></h2>\n" );

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
