"""
Handler for CGI parameter passing
"""
import cgitb
cgitb.enable()
import cgi
from bttbConfig import Error

__all__ = ['bttbCGI']

class bttbCGI(object):
    '''Class to handle CGI parsing'''

    def __init__(self):
        '''Zero out the data'''
        self.params = None

    def read_cgi(self):
        '''
        Read in the CGI parameters and store for parsing.
        This must be called before anything else. Newer
        versions of Python could just put it in a super
        __init__ method.
        '''
        try:
            self.params = cgi.parse()
        except Exception, ex:
            Error( 'Could not parse CGI parameters', ex )

    #----------------------------------------------------------------------
    def get_param(self,name,default):
        """
        Simple trick to get cgi params using default values
        """
        try:
            value = self.params[name][0].strip()
        except Exception:
            value = default
        return value

    #----------------------------------------------------------------------
    def get_int_param(self, name,default):
        """
        Simple trick to get numeric cgi params using default values
        """
        try:
            value = int( self.params[name][0] )
        except Exception:
            value = default
        return value

    #----------------------------------------------------------------------
    @staticmethod
    def capitalize_first(name):
        """
        Returns a capitalized string, but without changing inner characters
        (the "capitalize()" method messes up "McTavish" to "Mctavish"
        """
        if len(name) < 2:
            return name.capitalize()
        return name[0].upper() + name[1:]

# ==================================================================
# Copyright (C) Kevin Peter Picott. All rights reserved. These coded
# instructions, statements and computer programs contain unpublished
# information proprietary to Kevin Picott, which is protected by the
# Canadian and US federal copyright law and may not be  disclosed to
# third  parties  or  duplicated or  copied,  in whole  or in  part,
# without   the  prior  written   consent  of  Kevin  Peter  Picott.
# ==================================================================
