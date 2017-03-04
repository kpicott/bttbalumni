// Contents of the current cart, represented as an array of keywords
var cart_contents = [
					,  { "amount"           : "200.00"
					   , "item_name"        : "Golf Tournament Entry"
					   , "on0"              : "Golfer Name"
					   , "os0"              : "Fred Flintstone"
					   , "tax_rate"         : "0"
					   }
					];

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
	cart_contents[0].discount_amount = "20.00";
	cart_contents[1].discount_amount = "15.00";
}

//----------------------------------------------------------------------
//
// Add a new golfer to the cart contents
//
function add_golfer()
{
}

//----------------------------------------------------------------------
//
// Add a new diner to the cart contents
//
function add_diner()
{
}

//----------------------------------------------------------------------
//
// Add a new hole sponsorship to the cart contents
//
function add_sponsor()
{
}

//----------------------------------------------------------------------
//
// Remove an existing item from the cart
//
function remove_item()
{
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
function validate_golf_order()
{
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
// Print out the order form in a separate tab
//
function print_golf_order_form()
{
}

//----------------------------------------------------------------------
//
// Using the current cart contents rebuild the HTML element in id
// "cart_contents" to show the current list of items in the cart.
//
function rebuild_golf_cart()
{
    var cart_element = document.getElementById( "cart_contents" );

    // Empty out any previous cart contents
    while( cart_element.hasChildNodes() )
    {
        cart_element.removeChild( cart_element.firstChild );
    }

    // Just the paypal elements for now
    for( var idx=0; idx<cart_contents.length; ++idx )
    {
        var cart_info = cart_contents[idx];
		var cart_index = 1;
		for( var item_key in cart_info )
		{
		    if( ! cart_info.hasOwnProperty(item_key) )
			{
				continue;
			}
			var item_data = cart_info[item_key];

			var field = document.createElement( "input" );
			field.type = "hidden";
			field.name = item_key + "_" + cart_index;
			field.value = item_data;

			cart_element.appendChild( field );

			cart_index++;
		}
    }
}

