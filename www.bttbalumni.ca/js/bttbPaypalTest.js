// Contents of the current cart, represented as an array of keywords
var cart_contents = [
					   { "amount"           : "150.00"
					   , "item_name"        : "All-Inclusive Entry"
					   , "on0"              : "Shirt Size"
					   , "os0"              : "Women's Small"
					   , "tax_rate"         : "13"
					   }
					,  { "amount"           : "200.00"
					   , "item_name"        : "Golf Tournament Entry"
					   , "on0"              : "Golfer Name"
					   , "os0"              : "Fred Flintstone"
					   , "tax_rate"         : "0"
					   }
					,  { "amount"           : "30.00"
					   , "item_name"        : "70th Anniversary Golf Shirt"
					   , "on0"              : "Shirt Size"
					   , "os0"              : "Men's Extra Large"
					   , "tax_rate"         : "13"
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
// Using the current cart contents rebuild the HTML element in id
// "cart_contents" to show the current list of items in the cart.
//
function rebuild_paypal_cart()
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

