# Copyright 2014-2015 the openage authors. See copying.md for legal info.



class NyanSpecAST:
    """
    An AST of a nyan spec.
    """
    def __init__(self):
        self.types = dict()

    def __str__(self):
        result = ""
        for ntype in self.types.values():
            result += str(ntype) + "\n"
        return result


class NyanSpecType:
<<<<<<< HEAD:py/openage/nyan/nyan_spec_ast.py

=======
    """
    Node for a nyan type within an AST.
    """
>>>>>>> 882668a... nyan: added parser documentation and moved parser in own python module:py/openage/nyan/parser/nyan_spec_ast.py
    def __init__(self, name):
        self.name = name
        self.attributes = dict()
        self.dynamic_attributes = False
        self.deltas = dict()

    def __str__(self):
        result = self.name.content + " {\n"
        for attr in self.attributes.values():
            result += "\t" + str(attr) + "\n"
        if self.dynamic_attributes:
            result += "\t...\n"
        for delta in self.deltas.values():
            result += "\t" + str(delta) + "\n"
        result += "}\n"
        return result


class NyanSpecAttribute:
    """
    Node for a nyan attribute within an AST.
    """
    def __init__(self, name):
        self.name = name
        self.is_set = False
        self.atype = None
        self.default_value = None

    def __str__(self):
        result = self.name.content + ": "
        if self.is_set:
            result += "set(" + self.atype.content + ")"
        else:
            result += self.atype.content
        if self.default_value:
            result += " = " + self.default_value.content
        return result


class NyanSpecDelta:
    """
    Node for a nyan runtime delta definition within an AST.
    """
    def __init__(self, delta_type):
        self.delta_type = delta_type

    def __str__(self):
        return "^" + self.delta_type.content
