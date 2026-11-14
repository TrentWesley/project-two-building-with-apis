def format_book(book):
    """Turn one Open Library search result into a display string."""
    title = book.get("title", "Unknown title")
    author_names = book.get("author_name", [])
    if author_names:
        authors = ", ".join(author_names)
    else:
        authors = "Unknown author"
    return f"{title} by {authors}"
