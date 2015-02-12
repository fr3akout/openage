# Copyright 2014-2015 the openage authors. See copying.md for legal info.

from .token import Token
from openage.util import Enum


class Tokenizer:
    """
    A tokenizer creates a list of tokens from a nyan specification file.
    """

    # All possible states of the tokenizer's internal state machine.
    State = Enum(name="State",
                 values=[
                     "START",
                     "COMMENT",
                     "DOT",
                     "DOT_DOUBLE",
                     "IDENTIFIER",
                     "ZERO",
                     "INTEGER",
                     "FLOAT",
                     "PLUS",
                     "MINUS",
                     "STRING",
                     "STRING_RAW",
                     "FINISHED"
                 ])

    def __init__(self, input_data):
        """
        Creates a new tokenizer for the given input data. input_data is the
        string representation of a nyan specification file.
        """
        self.input_data = input_data

        self.state = Tokenizer.State.START

        self.index = 0
        self.line = 0
        self.offset = 0

        self.token_begin = 0
        self.token_offset = 0
        self.token_line = 0
        self.token_length = 0

        self.tokens = []

    def tokenize(self):
        """
        Tokenizes the input data and returns a list of tokens.
        """
        self.tokens = []
        self.index = 0
        input_length = len(self.input_data)

        while self.index < input_length:
            c = self.input_data[self.index]
            self.process(c)

            if c == '\n':
                self.line += 1
                self.offset = 0
            else:
                self.offset += 1
            self.index += 1

        self.process('\0')
        if self.state != Tokenizer.State.FINISHED:
            self.unexpected()
        else:
            self.tokens.append(Token(Token.Type.END, '', self.line,
                                     self.offset))
        return self.tokens

    def is_identifier_begin(self, c):
        """
        Returns whether the given character is allowed at the beginning of
        identifiers.
        """
        return c.isalpha() or c == '_'

    def is_identifier(self, c):
        """
        Returns whether the given character is allowed within identifiers.
        """
        return c.isalnum() or c == '_'

    def is_separator(self, c):
        """
        Returns whether the given character is a valid separator. A separator
        is a single character that can always be directly converted to a token.
        """
        return c in "^:,()[]{}="

    def process(self, c):
        """
        Makes a transition of the internal state machine for the given input
        character.
        """

        if self.state == Tokenizer.State.START:
            if c == '#':
                self.state = Tokenizer.State.COMMENT
            elif c.isspace():
                pass
            elif c == '.':
                self.begin_token()
                self.state = Tokenizer.State.DOT
            elif self.is_separator(c):
                self.add_token(Token.get_type_for_character(c))
            elif self.is_identifier_begin(c):
                self.begin_token()
                self.state = Tokenizer.State.IDENTIFIER
            elif c == '+':
                self.begin_token()
                self.state = Tokenizer.State.PLUS
            elif c == '-':
                self.begin_token()
                self.state = Tokenizer.State.MINUS
            elif c == '0':
                self.begin_token()
                self.state = Tokenizer.State.ZERO
            elif c.isdigit():  # and not zero, as it is checked before
                self.begin_token()
                self.state = Tokenizer.State.INTEGER
            elif c == '"':
                self.begin_token(use_current=False)
                self.state = Tokenizer.State.STRING
            elif c == '\'':
                self.begin_token(use_current=False)
                self.state = Tokenizer.State.STRING_RAW
            elif c == '\0':
                self.state = Tokenizer.State.FINISHED
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.COMMENT:
            if c == '\n':
                self.state = Tokenizer.State.START
            elif c == '\0':
                self.state = Tokenizer.State.FINISHED
        elif self.state == Tokenizer.State.DOT:
            if c == '.':
                self.continue_token()
                self.state = Tokenizer.State.DOT_DOUBLE
            elif c.isdigit():
                self.continue_token()
                self.state = Tokenizer.State.FLOAT
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.DOT_DOUBLE:
            if c == '.':
                self.finish_token(Token.Type.ELLIPSIS)
                self.state = Tokenizer.State.START
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.IDENTIFIER:
            if self.is_identifier(c):
                self.continue_token()
            else:
                self.finish_token(Token.Type.IDENTIFIER, False)
                self.step_back()
        elif self.state == Tokenizer.State.ZERO:
            if c == '.':
                self.continue_token()
                self.state = Tokenizer.State.FLOAT
            elif self.is_separator(c) or c.isspace() or c == '\0':
                self.finish_token(Token.Type.INTEGER, False)
                self.step_back()
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.INTEGER:
            if c.isdigit():
                self.continue_token()
            elif c == '.':
                self.continue_token()
                self.state = Tokenizer.State.FLOAT
            elif self.is_separator(c) or c.isspace() or c == '\0':
                self.finish_token(Token.Type.INTEGER, False)
                self.step_back()
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.FLOAT:
            if c.isdigit():
                self.continue_token()
            elif self.is_separator(c) or c.isspace() or c == '\0':
                self.finish_token(Token.Type.FLOAT, False)
                self.step_back()
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.PLUS:
            if c == '.':
                self.continue_token()
                self.state = Tokenizer.State.FLOAT
            elif c == '0':
                self.continue_token()
                self.state = Tokenizer.State.ZERO
            elif c.isdigit():
                self.continue_token()
                self.state = Tokenizer.State.INTEGER
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.MINUS:
            if c == '.':
                self.continue_token()
                self.state = Tokenizer.State.FLOAT
            elif c == '0':
                self.continue_token()
                self.state = Tokenizer.State.ZERO
            elif c.isdigit():
                self.continue_token()
                self.state = Tokenizer.State.INTEGER
            else:
                self.unexpected()
        elif self.state == Tokenizer.State.STRING:
            # TODO handle string, parse escape sequences
            pass
        elif self.state == Tokenizer.State.STRING_RAW:
            if c == '\'':
                self.finish_token(Token.Type.STRING, False)
                self.state = Tokenizer.State.START
            elif c == '\n':
                self.unexpected()
            else:
                self.continue_token()
        elif self.state == Tokenizer.State.FINISHED:
            pass
        else:
            assert "Invalid Tokenizer state"

    def begin_token(self, use_current=True):
        """
        Tells the tokenizer to begin a new token at the currently processed
        character. use_current specifies, whether the current character is part
        of the token's content.
        """
        self.token_begin = self.index
        self.token_offset = self.offset
        self.token_length = 1
        if not use_current:
            self.token_begin += 1
            self.token_offset += 1
            self.token_length = 0

        # this works because no token begins at a '\n'
        self.token_line = self.line

    def continue_token(self):
        """
        Tells the tokenizer to append the currently processed character to the
        token.
        """
        self.token_length += 1

    def finish_token(self, ttype, add_current=True):
        """
        Tells the tokenizer to finish the current token and add it to the
        result token list. The token's type is set to the specified one.
        add_current specifies, whether the currently processes character is
        part of the finished token.
        """
        if add_current:
            self.token_length += 1
        token_end = self.token_begin + self.token_length
        self.tokens.append(
                Token(ttype, self.input_data[self.token_begin:token_end],
                      self.token_line, self.token_offset))
        self.token_begin = self.index
        if add_current:
            self.token_begin += 1

    def add_token(self, ttype):
        """
        Tells the tokenizer to add a token with the given type and the
        currently processes character as content.
        """
        self.tokens.append(Token(ttype, self.input_data[self.index], self.line,
                                 self.offset))

    def step_back(self):
        """
        Tells the tokenizer to process the currently processed character again
        in the START state.
        """
        if not self.input_data[self.index].isspace():
            self.offset -= 1
            self.index -= 1
        self.state = Tokenizer.State.START

    def unexpected(self):
        """
        Tells the tokenizer to append a FAIL token and change its state to
        FINISHED.
        """
        self.tokens.append(
                Token(Token.Type.FAIL,
                      self.input_data[self.token_begin:self.index],
                      self.token_line, self.token_offset))
        self.state = Tokenizer.State.FINISHED
