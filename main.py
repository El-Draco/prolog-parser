import os
class Lexer:
    def __init__(self, code):
        self.code = code.splitlines()
        self.tokens = []
        self.current_line = 0
        self.current_char = 0
        self.tokenize()

    def tokenize(self):
        pass

    def get_next_token(self):
        pass

    def peek_token(self):
        pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.errors = []
        self.advance()

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        self.program()

    # @TODO: change to enums QUERY, CLAUSE_LIST, etc ?
    def program(self):
        if self.current_token == "query":
            self.query()
        elif self.current_token == "clause-list":
            self.clause_list()
            self.query()
        else:
            self.error("Expected <clause-list> or <query> at start of program")

    def clause_list(self):
        self.clause()
        if self.current_token == "clause-list":
            self.clause_list()

    def clause(self):
        self.predicate()
        if self.current_token == ".":
            self.advance()
        elif self.current_token == ":-":
            self.advance()
            self.predicate_list()
            if self.current_token == ".":
                self.advance()
            else:
                self.error("Expected '.' after predicate list")
        else:
            self.error("Expected '.' or ':-' after predicate")

    def query(self):
        if self.current_token == "?-":
            self.advance()
            self.predicate_list()
            if self.current_token == ".":
                self.advance()
            else:
                self.error("Expected '.' after query")
        else:
            self.error("Expected '?-' to start a query")

    def predicate_list(self):
        self.predicate()
        while self.current_token == ",":
            self.advance()
            self.predicate()

    def predicate(self):
        if self.is_atom():
            self.advance()
            if self.current_token == "(":
                self.advance()
                self.term_list()
                if self.current_token == ")":
                    self.advance()
                else:
                    self.error("Expected ')' after term list")
        else:
            self.error("Expected <atom> in predicate")

    def term_list(self):
        self.term()
        while self.current_token == ",":
            self.advance()
            self.term()

    def term(self):
        if self.is_atom() or self.is_variable() or self.is_structure() or self.is_numeral():
            self.advance()
        else:
            self.error("Expected <term>")

    def is_atom(self):
        pass

    def is_variable(self):
        pass

    def is_structure(self):
        pass

    def is_numeral(self):
        pass

    def error(self, message):
        error_msg = f"Syntax Error: {message} at line {self.lexer.current_line}, char {self.lexer.current_char}"
        self.errors.append(error_msg)
        self.advance()


def main():
    file_num = 1
    output = []

    while True:
        filename = f"{file_num}.txt"
        if not os.path.isfile(filename):
            break

        with open(filename, 'r') as f:
            code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)

        parser.parse()

        if parser.errors:
            output.append(f"{filename} contains syntax errors:\n" + "\n".join(parser.errors))
        else:
            output.append(f"{filename} is syntactically correct")

        file_num += 1

    with open("parser_output.txt", "w") as f:
        f.write("\n\n".join(output))


if __name__ == "__main__":
    main()
