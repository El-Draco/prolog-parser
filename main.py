import os
from enum import Enum, auto

class TokenType(Enum):
    """
    Enumeration for token types in the Prolog grammar.
    Each token type represents a specific grammatical construct or symbol.
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

    ATOM = auto()
    VARIABLE = auto()
    NUMERAL = auto()

    EOF = auto()
    INVALID = auto()            # Other misc. chars go here

class Lexeme:
    """
    Represents a lexical unit in the input source code.

    Attributes:
        token_type (TokenType): The type of token (e.g., PLUS, ATOM).
        value (str): The string representation of the lexeme.
        line (int): The line number where the lexeme appears.
        char_position (int): The character position of the lexeme on the line.
    """
    def __init__(self, token_type, value, line, char_position):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.char_position = char_position

    def __str__(self):
        return f"Lexeme({self.token_type}, '{self.value}', Line: {self.line}, Char: {self.char_position})"

class Lexer:
    """
    Lexical analyzer to tokenize Prolog source code.

    Attributes:
        code (str): The source code to be tokenized.
        position (int): The current position in the source code.
        line (int): The current line number being processed.
        char_position (int): The position of the current character on the line.
        length (int): The total length of the source code.
    """
    def __init__(self, code: str):
        self.code = code
        self.position = 0
        self.line = 1
        self.char_position = 0
        self.length = len(code)

    def get_next_char(self):
        """
        Retrieves the next character in the input code, updating position and line information.

        Returns:
            char (str): The next character, or None if end of code is reached.
        """
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
        """
        Peeks at the next character without advancing the position.

        Returns:
            char (str): The next character, or None if end of code is reached.
        """
        if self.position >= self.length:
            return None
        return self.code[self.position]

    def tokenize(self):
        """
        Generates tokens from the input source code.

        Yields:
            Lexeme: The next lexeme generated from the source code.
        """
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
        """
        Tokenizes a numeral starting with the given character.

        Args:
            char (str): The initial character of the numeral.

        Returns:
            Lexeme: A numeral lexeme.
        """
        start_position = self.char_position
        value = char
        while self.peek_next_char() and self.peek_next_char().isdigit():
            value += self.get_next_char()
        return Lexeme(TokenType.NUMERAL, value, self.line, start_position)

    def tokenize_atom(self, char):
        """
        Tokenizes an atom starting with the given character.

        Args:
            char (str): The initial character of the atom.

        Returns:
            Lexeme: An atom lexeme.
        """
        start_position = self.char_position
        value = char
        while self.peek_next_char() and (self.peek_next_char().isalnum() or self.peek_next_char() == '_'):
            value += self.get_next_char()
        return Lexeme(TokenType.ATOM, value, self.line, start_position)

    def tokenize_variable(self, char):
        """
        Tokenizes a variable starting with the given character.

        Args:
            char (str): The initial character of the variable.

        Returns:
            Lexeme: A variable lexeme.
        """
        start_position = self.char_position
        value = char
        while self.peek_next_char() and (self.peek_next_char().isalnum() or self.peek_next_char() == '_'):
            value += self.get_next_char()
        return Lexeme(TokenType.VARIABLE, value, self.line, start_position)

    def tokenize_string(self):
        """
       Tokenizes a string enclosed in single quotes.

       Returns:
           Lexeme: An atom lexeme representing the string.

       Raises:
           ValueError: If the string is not terminated before the end of the file.
       """
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
    """
       Parser for Prolog grammar.

       Attributes:
           lexer (Lexer): The lexical analyzer providing tokens.
           tokens (generator): The stream of tokens from the lexer.
           current_token (Lexeme): The currently processed token.
           errors (list): A list of syntax error messages.
       """
    def __init__(self, lexer):
        self.tokens = lexer.tokenize()
        self.current_token = None
        self.errors = []
        self.advance()

    def advance(self):
        """
        Advances to the next token in the input.
        """
        try:
            self.current_token = next(self.tokens)
            if self.current_token.token_type == TokenType.INVALID:
                self.error(f"Invalid token '{self.current_token.value}")
        except StopIteration:
            self.current_token = Lexeme(TokenType.EOF, "EOF", -1, -1)

    def match(self, expected_type, ):
        """
        Matches the current token against an expected type and advances if matched.

        Args:
            expected_type (TokenType): The expected token type.

        Raises:
            SyntaxError: If the current token does not match the expected type.
        """
        if self.current_token.token_type == expected_type:
            self.advance()
        else:
            self.error(f"Expected {expected_type}, but found {self.current_token.token_type}")

    def parse(self):
        """
        Initiates parsing of the Prolog program.
        """
        try:
            self.program()
        except Exception as e:
            print(e)

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
                self.error("Expected '.' or ':-' after predicate")
        except Exception as e:
            self.error(f"Error in clause: {e}")

    def clause_list(self):
        while True:
            try:
                self.clause()
                if self.current_token.token_type != TokenType.ATOM:
                    break
            except Exception as e:
                self.error(f"Error in clause list: {e}")
                if self.current_token.token_type not in {TokenType.ATOM, TokenType.QUERY}:
                    self.advance()

    def query(self):
        if self.current_token.token_type == TokenType.QUERY:
            self.advance()
            self.predicate_list()
            if self.current_token.token_type == TokenType.PERIOD:
                self.advance()
            else:
                self.error("Expected '.' at the end of query")
        else:
            self.error("Expected '?-' to start a query")

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
                    )
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
                self.error(f"Error in term list: {e}")
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
                self.error("Expected <term>")
        except Exception as e:
            self.error(f"Error in term: {e}")

    def predicate(self):
        try:
            if self.current_token.token_type == TokenType.ATOM:
                self.advance()
                if self.current_token.token_type == TokenType.OPEN_PAREN:
                    self.advance()
                    self.term_list()
                    self.match(TokenType.CLOSE_PAREN)
            else:
                self.error("Expected <atom> in predicate")
        except Exception as e:
            self.error(f"Error in predicate: {e}")

    def recover(self):
        """
        Attempts to recover from syntax errors by skipping to a synchronization token.
        """
        sync_tokens = {
            TokenType.PERIOD,       # End of a clause
            TokenType.COMMA,
            TokenType.QUERY,        # Start of a query
            TokenType.EOF,          # End of file
            TokenType.CLOSE_PAREN   # End of a term list or predicate
        }

        while self.current_token.token_type not in sync_tokens and self.current_token.token_type != TokenType.EOF:
            self.advance()

    def error(self, message):
        """
        Records a syntax error message and logs it.

        Args:
            message (str): The error message to log and record.
        """
        error_msg = f"Syntax Error: {message} at line {self.current_token.line}, char {self.current_token.char_position}"
        self.errors.append(error_msg)
        print(error_msg)
        self.recover()


def main():
    file_num = 1
    output_filename = "parser_output.txt"
    open(output_filename, "w").close()

    while True:
        filename = f"./{file_num}.txt"
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
                print(f"\n{filename} contains syntax errors:\n" + "\n".join(parser.errors) + "\n\n")
            else:
                f.write(f"{filename} is syntactically correct\n\n")
                print(f"\n{filename} is syntactically correct\n\n")
        file_num += 1


if __name__ == "__main__":
    main()
