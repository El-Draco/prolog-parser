from main import Lexer, TokenType


def test_basic_tokens():
    code = """+ - * / ^ ~ : :- . , ( ) ?-"""
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    expected_tokens = [
        TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
        TokenType.CARET, TokenType.TILDE, TokenType.COLON, TokenType.COLON_DASH,
        TokenType.PERIOD, TokenType.COMMA, TokenType.OPEN_PAREN,
        TokenType.CLOSE_PAREN, TokenType.QUERY
    ]
    assert [token.token_type for token in tokens[:-1]] == expected_tokens
    assert tokens[-1].token_type == TokenType.EOF


def test_special_characters():
    code = "# $ & !"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    for token in tokens[:-1]:
        assert token.token_type == TokenType.INVALID
    assert tokens[-1].token_type == TokenType.EOF

def test_complex_atoms_and_variables():
    code = "object_name Variable_Name_1"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    assert tokens[0].token_type == TokenType.ATOM
    assert tokens[1].token_type == TokenType.VARIABLE
    assert tokens[-1].token_type == TokenType.EOF

def test_numerals():
    code = "42 1024"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    assert tokens[0].token_type == TokenType.NUMERAL
    assert tokens[1].token_type == TokenType.NUMERAL
    assert tokens[-1].token_type == TokenType.EOF

def test_tokenize_atoms():
    code = "object(candle,red,small,1)."
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    assert tokens[0].token_type == TokenType.ATOM
    assert tokens[0].value == "object"
    assert tokens[1].token_type == TokenType.OPEN_PAREN
    assert tokens[2].token_type == TokenType.ATOM
    assert tokens[2].value == "candle"
    assert tokens[-2].token_type == TokenType.PERIOD
    assert tokens[-1].token_type == TokenType.EOF


def test_tokenize_query_with_anonymous_var():
    code = "?- location(object(_name,red,_,_), kitchen)."
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    assert tokens[0].token_type == TokenType.QUERY
    assert tokens[0].value == "?-"
    assert tokens[1].token_type == TokenType.ATOM
    assert tokens[1].value == "location"
    assert tokens[2].token_type == TokenType.OPEN_PAREN
    assert tokens[3].token_type == TokenType.ATOM
    assert tokens[3].value == "object"
    assert tokens[4].token_type == TokenType.OPEN_PAREN
    assert tokens[5].token_type == TokenType.VARIABLE
    assert tokens[5].value == "_name"
    assert tokens[6].token_type == TokenType.COMMA
    assert tokens[7].token_type == TokenType.ATOM
    assert tokens[7].value == "red"
    assert tokens[8].token_type == TokenType.COMMA
    assert tokens[9].token_type == TokenType.VARIABLE
    assert tokens[9].value == "_"
    assert tokens[10].token_type == TokenType.COMMA
    assert tokens[11].token_type == TokenType.VARIABLE
    assert tokens[11].value == "_"
    assert tokens[12].token_type == TokenType.CLOSE_PAREN
    assert tokens[13].token_type == TokenType.COMMA
    assert tokens[14].token_type == TokenType.ATOM
    assert tokens[14].value == "kitchen"
    assert tokens[15].token_type == TokenType.CLOSE_PAREN
    assert tokens[16].token_type == TokenType.PERIOD
    assert tokens[17].token_type == TokenType.EOF


def test_tokenize_numerals():
    code = "object(apple,green,small,1)."
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    assert tokens[0].token_type == TokenType.ATOM
    assert tokens[0].value == "object"
    assert tokens[1].token_type == TokenType.OPEN_PAREN
    assert tokens[2].token_type == TokenType.ATOM
    assert tokens[2].value == "apple"
    assert tokens[3].token_type == TokenType.COMMA
    assert tokens[4].token_type == TokenType.ATOM
    assert tokens[4].value == "green"
    assert tokens[5].token_type == TokenType.COMMA
    assert tokens[6].token_type == TokenType.ATOM
    assert tokens[6].value == "small"
    assert tokens[7].token_type == TokenType.COMMA
    assert tokens[8].token_type == TokenType.NUMERAL
    assert tokens[8].value == "1"
    assert tokens[9].token_type == TokenType.CLOSE_PAREN
    assert tokens[10].token_type == TokenType.PERIOD
    assert tokens[11].token_type == TokenType.EOF
