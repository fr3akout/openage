# Copyright 2015-2015 the openage authors. See copying.md for legal info.


class ParserException(Exception):
    """
    A parser exception is raised, if parsing nyan specification files fails.
    """

    def __init__(self, message, token):
        """
        Creates a new parser exception with an error message and the token
        where the error occured.
        """
        super(ParserException, self).__init__(message)
        self.token = token
