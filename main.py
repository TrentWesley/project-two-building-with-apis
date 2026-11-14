import requests


def search_books(title):
    """Search Open Library by title and return the JSON response as a dictionary."""
    response = requests.get(
        "https://openlibrary.org/search.json",
        params={"title": title, "limit": 5, "fields": "title,author_name"},
        headers={"User-Agent": "CIDM3312-BookSearch/1.0"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def format_book(book):
    """Turn one Open Library search result into a display string."""
    title = book.get("title", "Unknown title")
    author_names = book.get("author_name", [])
    if author_names:
        authors = ", ".join(author_names)
    else:
        authors = "Unknown author"
    return f"{title} by {authors}"


def main():
    """Ask for a book title, search Open Library, and print the results."""
    title = input("Enter a book title: ").strip()
    if not title:
        print("Please enter a book title.")
        return

    try:
        data = search_books(title)
    except (requests.exceptions.RequestException, ValueError) as error:
        print(f"Sorry, could not reach Open Library: {error}")
        return

    total = data.get("numFound", 0)
    books = data.get("docs", [])

    if not books:
        print(f'No books found for "{title}".')
        return

    if total == 1:
        word = "match"
    else:
        word = "matches"
    print(f"Found {total:,} {word}. Showing the first {len(books)}.")
    print()

    for number, book in enumerate(books, start=1):
        print(f"{number}. {format_book(book)}")


if __name__ == "__main__":
    main()
