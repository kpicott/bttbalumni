#!perl

@dirList = ('Homecoming_Andrea');

foreach $dir ( @dirList )
{
	opendir(DIR, $dir);
	my @contents = readdir( DIR );
	closedir( DIR );
	foreach $file ( @contents )
	{
		next if( ! -f "$dir/$file" );
		next if( $file =~ /_Small/ );
		next if( $file =~ /Thumbs.db/ );
		if( $file =~ /.JPG$/ )
		{
			my $dst = $file;
			$dst =~ s/JPG$/jpg/;
			rename( "$dir/$file", "J" );
			rename( "J", "$dir/$dst" );
			$file = $dst;
		}
		if( $file =~ / / )
		{
			my $dst = $file;
			$dst =~ s/ //g;
			rename( "$dir/$file", "J" );
			rename( "J", "$dir/$dst" );
			$file = $dst;
		}
		my $thumb = $file;
		$thumb =~ s/\.jpg/_Small.jpg/;
		system( "convert -resize 150 \"$dir/$file\" \"$dir/$thumb\"" );
		print "Done $dir/$file\n";
	}
}

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
