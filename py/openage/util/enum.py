# Copyright 2015-2015 the openage authors. See copying.md for legal info.


class Enum:
    """
    Utility class for generating enums with reverse lookup.
    """

    def __init__(self, name, values):
        """
        Creates a new enumeration with the given name and the given values.
        Values is a list of strings with names for all enumeration members.
        Those will be mapped to their index within the list and can be accessed
        as object members of the created enumeration.
        """
        self.name = name
        enums = dict(zip(values, range(len(values))))
        self.reverse_lookup = dict((value, key)
                                   for key, value in enums.items())
        self.__dict__.update(enums)
