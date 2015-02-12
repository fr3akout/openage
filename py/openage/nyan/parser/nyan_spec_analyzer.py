# Copyright 2014-2015 the openage authors. See copying.md for legal info.

from .parser_exception import ParserException
from .token import Token


class NyanSpecAnalyzer:
    """
    A nyan spec analyzer executes a semantic analysis on a nyan spec AST..
    """

    def __init__(self, ast):
        """
        Creates a new nyan spec analyzer for the given AST.
        """
        self.ast = ast
        self.errors = []

    def analyze(self):
        """
        Analyzes the whole nyan spec AST for semantic validity. All occured
        errors are returned as list of parser exceptions. If no errors occured
        an empty list will be returned.
        """
        for ntype in self.ast.types.values():
            self.check_type(ntype)
            self.check_default_value(ntype)
        return self.errors

    def check_type(self, ntype):
        """
        Checks whether the given nyan type is well defined.
        """
        self.check_attribute_types_exist(ntype)
        self.check_delta_types_exist(ntype)

    def check_attribute_types_exist(self, ntype):
        """
        Check whether all types within attribute declarations of the given nyan
        type are defined.
        """
        for attr in ntype.attributes.values():
            type_name = attr.atype.content
            if not self.is_primitive_type(type_name):
                if type_name not in self.ast.types:
                    self.error("Type '%s' is undefined" % type_name,
                               attr.atype)
            else:
                if attr.is_set:
                    self.error("Sets of type '%s' are not allowed" % type_name,
                               attr.atype)

    def check_delta_types_exist(self, ntype):
        """
        Checks whether all types within delta declarations of the given nyan
        type are defined.
        """
        for delta in ntype.deltas.values():
            type_name = delta.delta_type.content
            if self.is_primitive_type(type_name):
                self.error("Delta of primitive type '%s' is not allowed" %
                           type_name, delta.delta_type)
            elif type_name not in self.ast.types:
                self.error("Type '%s' is not defined" % type_name,
                           delta.delta_type)

    def check_default_value(self, ntype):
        """
        Checks whether all attribute declarations for the given nyan type
        either have a valid or no default value.
        """
        for attr in ntype.attributes.values():
            if self.is_primitive_type(attr.atype.content) and\
                    not attr.is_set and attr.default_value is not None:
                # if the attribute is a primitive type and no set, we have to
                # check it's default value
                self.match_types(attr.atype, attr.default_value)
            elif attr.default_value is not None:
                # otherwise there must not be a default value
                if attr.is_set:
                    error_msg = "Type 'set(%s)' must not have default value"
                else:
<<<<<<< HEAD:py/openage/nyan/nyan_spec_analyzer.py
                    error_message = "Type '%s' must not have default value"
                self.error(error_message % attr.atype.content,
                           attr.default_value)
=======
                    error_msg = "Type '%s' must not have default value"
                self.error(error_msg % attr.atype.content, attr.default_value)
>>>>>>> 882668a... nyan: added parser documentation and moved parser in own python module:py/openage/nyan/parser/nyan_spec_analyzer.py

    def is_primitive_type(self, type_name):
        """
        Returns whether the given type name is a primitive type.
        """
        return type_name in ["bool", "int", "float", "string"]

    def match_types(self, attr_type, attr_value):
        """
        Returns whether the given attribute value is a valid literal for the
        given attribute type.
        """
        if attr_type.content == "bool":
            if attr_value.ttype == Token.Type.IDENTIFIER and\
                    attr_value.content in ["true", "false"]:
                return
        elif attr_type.content == "int":
            if attr_value.ttype == Token.Type.INTEGER:
                return
        elif attr_type.content == "float":
            if attr_value.ttype in [Token.Type.INTEGER, Token.Type.FLOAT]:
                return
        elif attr_type.content == "string":
            if attr_value.ttype == Token.Type.STRING:
                return
<<<<<<< HEAD:py/openage/nyan/nyan_spec_analyzer.py
        self.error("'%s' is no valid literal for primitive type '%s'"
                   % (attr_value.content, attr_type.content), attr_value)
=======
        self.error("'%s' is no valid literal for primitive type '%s'" %
                   (attr_value.content, attr_type.content), attr_value)
>>>>>>> 882668a... nyan: added parser documentation and moved parser in own python module:py/openage/nyan/parser/nyan_spec_analyzer.py

    def error(self, message, token):
        """
        Adds a new parser exception with the given message and token to the
        error list.
        """
        self.errors.append(ParserException(message, token))
