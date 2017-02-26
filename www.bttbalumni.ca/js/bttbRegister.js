//
// Validate the input in the registration form. Uses the canned validation
// scriptsion in formValidation.js
//
validateRegistration = function()
{
	var errs = 0;
	if( ! validatePresent($('FirstName'), 'inf_firstName') )		errs += 1;
	if( ! validatePresent($('CurrentLastName'), 'inf_lastName') )	errs += 1;
	if( ! validatePresent($('FirstYear'), 'inf_firstYear') )		errs += 1;
	if( ! validatePresent($('LastYear'), 'inf_lastYear') )			errs += 1;
	if( ! validateEmail($('Email'), 'inf_email') )					errs += 1;

	if( errs > 1 ) alert( 'There are ' + errs + ' fields that need correction before sending' );
	if( errs == 1 ) alert( 'There is one field which needs correction before sending' );
	return (errs == 0);
}

// ==================================================================
// Copyright (C) Kevin Peter Picott. All rights reserved. These coded
// instructions, statements and computer programs contain unpublished
// information proprietary to Kevin Picott, which is protected by the
// Canadian and US federal copyright law and may not be  disclosed to
// third  parties  or  duplicated or  copied,  in whole  or in  part,
// without   the  prior  written   consent  of  Kevin  Peter  Picott.
// ==================================================================
