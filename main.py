import os
from enum import Enum, auto
from loguru import logger

class TokenType(Enum):
    """
    Enum class to represent token types for this Prolog grammar
    """
    PLUS = auto()               # +
    MINUS = auto()              # -
    MULTIPLY = auto()           # *
    DIVIDE = auto()             # /
    ESCAPE = auto()             # \
    CARET = auto()              # ^
    TILDE = auto()              # ~
    COLON = auto()              # :
    COLON_DASH = auto()         # :-
    PERIOD = auto()             # .
    COMMA = auto()              # ,
    OPEN_PAREN = auto()         # (
    CLOSE_PAREN = auto()        # )
    QUERY = auto()              # ?-

    ATOM = auto()               # Atoms (here we'll have `criminal`, `american`, etc.)
    VARIABLE = auto()
    NUMERAL = auto()

    EOF = auto()
    INVALID = auto()            # Other misc. chars go here

class Lexeme:
    """
    Class representing a Lexeme
    """
    def __init__(self, token_type, value, line, char_position):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.char_position = char_position

    def __str__(self):
        return f"Lexeme({self.token_type}, '{self.value}', Line: {self.line}, Char: {self.char_position})"

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.position = 0
        self.line = 1
        self.char_position = 0
        self.length = len(code)

    def get_next_char(self):
        if self.position >= self.length:
            return None
        char = self.code[self.position]
        self.position += 1
        self.char_position += 1
        if char == '\n':
            self.line += 1
            self.char_position = 0
        return char

    def peek_next_char(self):
        if self.position >= self.length:
            return None
        return self.code[self.position]

    def tokenize(self):
        while True:
            char = self.get_next_char()
            if char is None:
                yield Lexeme(TokenType.EOF, "EOF", self.line, self.char_position)
                break

            if char.isspace():
                continue

            elif char == '+':
                yield Lexeme(TokenType.PLUS, char, self.line, self.char_position)
            elif char == '-':
                yield Lexeme(TokenType.MINUS, char, self.line, self.char_position)
            elif char == '*':
                yield Lexeme(TokenType.MULTIPLY, char, self.line, self.char_position)
            elif char == '/':
                yield Lexeme(TokenType.DIVIDE, char, self.line, self.char_position)
            elif char == '\\':
                yield Lexeme(TokenType.ESCAPE, char, self.line, self.char_position)
            elif char == '^':
                yield Lexeme(TokenType.CARET, char, self.line, self.char_position)
            elif char == '~':
                yield Lexeme(TokenType.TILDE, char, self.line, self.char_position)
            elif char == "'":
                yield self.tokenize_string()
            elif char == ':':
                if self.peek_next_char() == '-':
                    yield Lexeme(TokenType.COLON_DASH, ":-", self.line, self.char_position)
                    self.get_next_char()
                else:
                    yield Lexeme(TokenType.COLON, ":", self.line, self.char_position)
            elif char == '?':
                if self.peek_next_char() == '-':
                    yield Lexeme(TokenType.QUERY, "?-", self.line, self.char_position)
                    self.get_next_char()
                else:
                    yield Lexeme(TokenType.INVALID, char, self.line, self.char_position)
            elif char == '.':
                yield Lexeme(TokenType.PERIOD, char, self.line, self.char_position)
            elif char == ',':
                yield Lexeme(TokenType.COMMA, char, self.line, self.char_position)
            elif char == '(':
                yield Lexeme(TokenType.OPEN_PAREN, char, self.line, self.char_position)
            elif char == ')':
                yield Lexeme(TokenType.CLOSE_PAREN, char, self.line, self.char_position)
            elif char.isdigit():
                yield self.tokenize_numeral(char)
            elif char.islower():
                yield self.tokenize_atom(char)
            elif char.isupper() or char == '_':
                yield self.tokenize_variable(char)
            else:
                yield Lexeme(TokenType.INVALID, char, self.line, self.char_position)

    def tokenize_numeral(self, char):
        start_position = self.char_position
        value = char
        while self.peek_next_char() and self.peek_next_char().isdigit():
            value += self.get_next_char()
        return Lexeme(TokenType.NUMERAL, value, self.line, start_position)

    def tokenize_atom(self, char):
        start_position = self.char_position
        value = char
        while self.peek_next_char() and (self.peek_next_char().isalnum() or self.peek_next_char() == '_'):
            value += self.get_next_char()
        return Lexeme(TokenType.ATOM, value, self.line, start_position)

    def tokenize_variable(self, char):
        start_position = self.char_position
        value = char
        while self.peek_next_char() and (self.peek_next_char().isalnum() or self.peek_next_char() == '_'):
            value += self.get_next_char()
        return Lexeme(TokenType.VARIABLE, value, self.line, start_position)

    def tokenize_string(self):
        start_position = self.char_position
        value = ""
        while True:
            char = self.get_next_char()
            if char is None:  # End of file before closing quote
                raise ValueError(f"Unterminated string starting at line {self.line}, char {start_position}")
            if char == "'":  # Closing quote
                break
            value += char
        return Lexeme(TokenType.ATOM, value, self.line, start_position)


class Parser:
    def __init__(self, lexer):
        self.tokens = lexer.tokenize()
        self.current_token = None
        self.errors = []
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = Lexeme(TokenType.EOF, "EOF", -1, -1)

    def match(self, expected_type, ):
        if self.current_token.token_type == expected_type:
            self.advance()
        else:
            self.error(f"Expected {expected_type}, but found {self.current_token.token_type}")

    def parse(self):
        self.program()
        # if self.current_token.token_type != TokenType.EOF:
            # self.error("Expected end of file")

    def program(self):
        if self.current_token.token_type == TokenType.QUERY:
            self.query()
        elif self.current_token.token_type == TokenType.ATOM:
            self.clause_list()
            if self.current_token.token_type == TokenType.QUERY:
                self.query()
            elif self.current_token.token_type != TokenType.EOF:
                self.error("Expected <query> or end of file after clause list")
        else:
            self.error("Expected <clause-list> or <query> at start of program")

    def clause(self):
        try:
            self.predicate()
            if self.current_token.token_type == TokenType.PERIOD:
                self.advance()
            elif self.current_token.token_type == TokenType.COLON_DASH:
                self.advance()
                self.predicate_list()
                self.match(TokenType.PERIOD)
            else:
                self.error("Expected '.' or ':-' after predicate", sync_tokens={TokenType.PERIOD, TokenType.QUERY})
        except Exception as e:
            self.error(f"Error in clause: {e}", sync_tokens={TokenType.PERIOD, TokenType.QUERY})

    def clause_list(self):
        while True:
            try:
                self.clause()
                if self.current_token.token_type != TokenType.ATOM:
                    break
            except Exception as e:
                self.error(f"Error in clause list: {e}", sync_tokens={TokenType.ATOM, TokenType.QUERY})
                if self.current_token.token_type not in {TokenType.ATOM, TokenType.QUERY}:
                    self.advance()

    def query(self):
        if self.current_token.token_type == TokenType.QUERY:
            self.advance()
            self.predicate_list()
            if self.current_token.token_type == TokenType.PERIOD:
                self.advance()
            else:
                self.error("Expected '.' at the end of query", sync_tokens={TokenType.QUERY, TokenType.EOF})
        else:
            self.error("Expected '?-' to start a query", sync_tokens={TokenType.QUERY, TokenType.EOF})

    def predicate_list(self):
        while True:
            try:
                self.predicate()
                if self.current_token.token_type == TokenType.COMMA:
                    self.advance()
                else:
                    break
            except Exception as e:
                self.error(f"Error in predicate list: {e}",
                           sync_tokens={TokenType.COMMA, TokenType.PERIOD, TokenType.QUERY})
                if self.current_token.token_type not in {TokenType.COMMA, TokenType.PERIOD, TokenType.QUERY}:
                    self.advance()

    def term_list(self):
        while True:
            try:
                self.term()
                if self.current_token.token_type == TokenType.COMMA:
                    self.advance()
                else:
                    break
            except Exception as e:
                self.error(f"Error in term list: {e}", sync_tokens={TokenType.COMMA, TokenType.CLOSE_PAREN})
                if self.current_token.token_type not in {TokenType.COMMA, TokenType.CLOSE_PAREN}:
                    self.advance()

    def term(self):
        try:
            if self.current_token.token_type == TokenType.ATOM:
                self.advance()
                if self.current_token.token_type == TokenType.OPEN_PAREN:
                    self.advance()
                    self.term_list()
                    self.match(TokenType.CLOSE_PAREN)
            elif self.current_token.token_type in {TokenType.VARIABLE, TokenType.NUMERAL}:
                self.advance()
            else:
                self.error("Expected <term>", sync_tokens={TokenType.COMMA, TokenType.CLOSE_PAREN})
        except Exception as e:
            self.error(f"Error in term: {e}", sync_tokens={TokenType.COMMA, TokenType.CLOSE_PAREN})

    def predicate(self):
        try:
            if self.current_token.token_type == TokenType.ATOM:
                self.advance()
                if self.current_token.token_type == TokenType.OPEN_PAREN:
                    self.advance()
                    self.term_list()
                    self.match(TokenType.CLOSE_PAREN)
            else:
                self.error("Expected <atom> in predicate", sync_tokens={TokenType.COMMA, TokenType.PERIOD})
        except Exception as e:
            self.error(f"Error in predicate: {e}", sync_tokens={TokenType.COMMA, TokenType.PERIOD})

    def recover(self, sync_tokens):
        # logger.info(f"Recovering from from error at line {self.current_token.line}, char {self.current_token.char_position}")
        while self.current_token.token_type not in sync_tokens and self.current_token.token_type != TokenType.EOF:
            # if self.current_token.token_type == TokenType.INVALID:
                # Log invalid token explicitly during recovery
                # self.error(f"Skipped invalid token '{self.current_token.value}'", sync_tokens=None)
            self.advance()

    def error(self, message, sync_tokens=None):
        if self.current_token.token_type == TokenType.INVALID:
            error_msg = f"Syntax Error: Invalid token '{self.current_token.value}' at line {self.current_token.line}, char {self.current_token.char_position}"
            self.errors.append(error_msg)
            logger.error(error_msg)
        # else:
        error_msg = f"Syntax Error: {message} at line {self.current_token.line}, char {self.current_token.char_position}"

        # # Avoid duplicate error messages
        # if error_msg not in self.errors:
        self.errors.append(error_msg)
        logger.error(error_msg)

        if sync_tokens:
            self.recover(sync_tokens)


def main():
    file_num = 1
    output_filename = "parser_output.txt"
    open(output_filename, "w").close()

    while True:
        logger.info(f"FILE {file_num}")
        filename = f"files/{file_num}.txt"
        if not os.path.isfile(filename):
            break

        with open(filename, 'r') as f:
            code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)
        parser.parse()

        with open(output_filename, "a") as f:
            if parser.errors:
                f.write(f"{filename} contains syntax errors:\n" + "\n".join(parser.errors) + "\n\n")
            else:
                f.write(f"{filename} is syntactically correct\n\n")
        file_num += 1


if __name__ == "__main__":
    main()
