"""
Collection of utilities for generating common formatting
"""
import datetime

__all__ = [ "date_image"
          , "date_css"
          ]

YEARS_SUPPORTED = [1947,1970,1980,1987,2007,2017,2018,2019]

#======================================================================
def date_css():
    """
    :return: CSS code to create a date image that looks like this:

          +---------+---+
          |   MM    | Y |
          +---------| Y |
          |         | Y |
          |   DD    | Y |
          |         |   |
          +---------+---+
    """
    css = '''
.postdate
{
  position: relative;
  width: 50px;
  height: 50px;
  float: left;
}
.month, .day, .year
{ 
  position:          absolute; 
  text-indent:       -1000em;
  background-image:  url(http://bttbalumni.ca/Images/dates.png);
  background-repeat: no-repeat;
}
.month	{ top: 2px;  left: 0;  width: 32px; height: 24px;}
.day	{ top: 25px; left: 0;  width: 32px; height: 25px;}
.year	{ bottom: 0; right: 0; width: 17px; height: 48px;}
'''
    offset = 0
    for month in range(1,13):
        css += '.m-%02d { background-position: 0 %dpx;	}\n' % (month, offset)
        offset -= 31
    offset = 0
    for day in range(1,17):
        css += '.d-%02d { background-position: -50px %dpx;}\n' % (day, offset)
        offset -= 31
    offset = 0
    for day in range(17,32):
        css += '.d-%02d { background-position: -100px %dpx;}\n' % (day, offset)
        offset -= 31
    offset = -6
    for year in YEARS_SUPPORTED:
        css += '.y-%d { background-position: -150px %dpx;}\n' % (year, offset)
        offset -= 50
    return css

#======================================================================
def date_image(date_to_format=None):
    """
    :param date_to_format: Date to be formatted. If None then use today.
    :return: HTML implementing a date button formatted with date_css().
    """
    if date_to_format is None:
        date_to_format = datetime.datetime.now()

    return '''<div class="postdate">
  <div class="month m-%02d">%02d</div>
  <div class="day d-%02d">%02d</div> 
  <div class="year y-%d">%d</div> 
</div>''' % ( date_to_format.month, date_to_format.month
            , date_to_format.day, date_to_format.day
            , date_to_format.year, date_to_format.year
            )

#======================================================================
#
# Test by running this script directly. It will generate 31 images that
# will include every day, month, and year at least once.
#
if __name__ == '__main__':
    print '<html><head><style>'
    print date_css()
    print '</style></head><body>'
    month = 1
    year_index = 0
    for day in range(1, 32):
        print '<p>%s</p>\n' % date_image( datetime.datetime(YEARS_SUPPORTED[year_index], month, day) )

        # Increment both month and year so that all will be seen
        month += 1
        if month > 12:
            month = 1

        year_index += 1
        if year_index >= len(YEARS_SUPPORTED):
            year_index = 0
    print '</body></html>'

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
