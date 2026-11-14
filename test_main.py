from main import format_book


def test_format_book_with_one_author():
    book = {"title": "Dune", "author_name": ["Frank Herbert"]}

    assert format_book(book) == "Dune by Frank Herbert"


def test_format_book_with_multiple_authors():
    book = {"title": "Good Omens", "author_name": ["Terry Pratchett", "Neil Gaiman"]}

    assert format_book(book) == "Good Omens by Terry Pratchett, Neil Gaiman"


def test_format_book_with_missing_author():
    book = {"title": "Dune"}

    assert format_book(book) == "Dune by Unknown author"


def test_format_book_with_missing_title():
    book = {"author_name": ["Frank Herbert"]}

    assert format_book(book) == "Unknown title by Frank Herbert"


def test_format_book_with_empty_author_list():
    book = {"title": "Dune", "author_name": []}

    assert format_book(book) == "Dune by Unknown author"
