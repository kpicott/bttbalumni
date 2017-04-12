//
// Validate the input in the registration form.
//
function validateRegistration()
{
	var form_url = '/cgi-bin/bttbVerifyRegistration.cgi';
	var return_value = false;
	$.ajax( {
		type    :   "POST",
		url     :   form_url,
		async	:	false,	// To make sure it finishes before returning
		data    :   $('#registerForm').serialize(),
		success :   function(data)
					{
						var error_messages = [];
						var return_fields = data.split( '\n' );
						return_fields.forEach( function(field_data, field_index) {
							var error_info = field_data.split( ':' );
							if( error_info.length == 3 )
							{
								// if( error_info[0] === "ERROR" )
								// else if( error_info[0] === "WARNING" )
								// var error_fields = error_info[1].split(',');
								error_messages.push( error_info[2] );
							}
						});
						if( error_messages.length > 0 )
						{
							alert( 'There were some errors in your form. Please correct them and try again.\n' + error_messages.join( '\n' ) );
						}
						else
						{
							return_value = true;
						}
					},
		error   :   function(data)
					{
						alert( 'Server verification failed, may be temporarily offline. Try again.' );
					}
	} );
	return return_value;
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
