from main import Lexer, Parser

def test_valid_program():
    code = """
    object(candle,red,small,1).
    object(apple,green,small,1).
    ?- location(object(_,red,_,_), kitchen).
    """
    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.parse()

    # Check for no syntax errors and print errors if there are any
    assert parser.errors == [], f"Unexpected errors found: {parser.errors}"

def test_missing_period_error():
    code = """
    object(candle,red,small,1)
    """
    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.parse()

    # Check that the missing period error is present
    assert len(parser.errors) >= 1
    assert "Expected '.' or ':-' after predicate" in parser.errors[0]

def test_unmatched_parenthesis_error():
    code = """
    location(object(candle,red,small,1), kitchen
    """
    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.parse()

    # Check that the unmatched parenthesis error is present as the first error
    assert len(parser.errors) >= 1
    assert "Expected TokenType.CLOSE_PAREN" in parser.errors[0]


def test_invalid_token_in_query():
    code = """
    ?- location(object(apple,red,small,1), !kitchen).
    """
    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.parse()

    # Check for invalid token error in query
    assert len(parser.errors) >= 1
    assert "Expected <term>" in parser.errors[0] or "Syntax Error" in parser.errors[0], f"Error found: {parser.errors[0]}"


def test_valid_clause_structures():
    code = "criminal(X) :- american(X), weapon(Y)."
    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.parse()
    assert parser.errors == []

def test_predicate_list():
    code = "owns(nono, ms1(nono)). missile(ms1)."
    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.parse()
    assert parser.errors == []

def test_term_list_and_nested_structures():
    code = "object(candle, red, small, ms1(nono))."
    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.parse()
    assert parser.errors == []
