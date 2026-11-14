# Plan: Open Library Book Search Script

**Date:** 2026-11-14
**Source:** `/grill-me` planning session (see `PROMPTS.md`, Session 3)
**Related research:** `docs/research/api-options.md`

## Goal

A simple, beginner-friendly Python script that:

1. Asks the user to enter a book title.
2. Searches the Open Library API.
3. Displays matching book titles and authors.
4. Handles searches with no results.
5. Handles API errors without crashing.
6. Runs using uv.

## Setup (uv)

- Run `uv init` in the repo (no `pyproject.toml` exists yet).
- `uv add requests`: runtime dependency.
- `uv add --dev pytest`: development-only dependency.
- Run the script: `uv run main.py`
- Run the tests: `uv run pytest`

## Program Flow

1. Prompt: `Enter a book title: `
2. Remove extra spaces before and after the input.
3. If the result is blank (empty or spaces only), print `Please enter a book title.` and exit **without calling the API**.
4. Search Open Library once, display the results, and exit. There is no loop.

## API Request: `search_books(title)`

| Setting | Value |
|---|---|
| Endpoint | `GET https://openlibrary.org/search.json` |
| Params | `title=<input>`, `limit=5`, `fields=title,author_name` |
| Header | `User-Agent: CIDM3312-BookSearch/1.0` (no personal email; the repo is public) |
| Timeout | `timeout=10` seconds |
| Status check | `response.raise_for_status()` |
| Returns | Parsed JSON (`numFound` and `docs`) |

## Formatting: `format_book(book)`

- Returns `"<title> by <authors>"`.
- `author_name` is a list. Join multiple authors with `", "`.
- Missing `title` → `Unknown title`.
- Missing `author_name` → `Unknown author`.

## Output: `main()`

| Case | Output |
|---|---|
| 5 or more matches | `Found 1,106 matches. Showing the first 5.` |
| 1–4 matches | `Found 3 matches. Showing the first 3.` |
| Exactly 1 match | `Found 1 match. Showing the first 1.` (singular "match") |
| 0 matches | `No books found for "<title>".` |

- The total uses a comma separator (`f"{n:,}"`).
- "Showing the first N" uses the number of books actually returned (`len(docs)`).
- Results are printed as a numbered list:

```
Enter a book title: dune
Found 1,106 matches. Showing the first 5.

1. Dune by Frank Herbert
2. Dune Messiah by Frank Herbert
3. ...
```

## Error Handling

- One `except (requests.exceptions.RequestException, ValueError)` block in `main()`.
  - `RequestException` covers connection errors, timeouts, and bad HTTP status codes from `raise_for_status()`.
  - `ValueError` covers responses that are not valid JSON.
- Message: `Sorry, could not reach Open Library: <error details>`, then exit with no traceback.
- Open Library's error codes are undocumented, so errors are handled generically.

## Code Structure

- One file: `main.py`.
- Three functions, each with one job:
  - `search_books(title)`: calls the API and returns the JSON data.
  - `format_book(book)`: turns one result into a display string.
  - `main()`: handles input, calls the other functions, and prints the results and messages.
- The file ends with `if __name__ == "__main__": main()` so tests can import functions without running the script.

## Testing

### Automated (`test_main.py`, written first with `/tdd`)

| Test | Input (book dict) | Expected |
|---|---|---|
| One author | `{"title": "Dune", "author_name": ["Frank Herbert"]}` | `Dune by Frank Herbert` |
| Multiple authors | `{"title": "Good Omens", "author_name": ["Terry Pratchett", "Neil Gaiman"]}` | `Good Omens by Terry Pratchett, Neil Gaiman` |
| Missing author | `{"title": "Dune"}` | `Dune by Unknown author` |
| Missing title | `{"author_name": ["Frank Herbert"]}` | `Unknown title by Frank Herbert` |

### Manual checklist (`uv run main.py`)

| Input / condition | Expected output |
|---|---|
| `dune` | Total-count line, then 5 numbered results |
| Rare title with 1–4 matches | "Showing the first N", with N equal to the number of books listed |
| Title with exactly 1 match | Singular `1 match` |
| `xyzqqnotabook` | `No books found for "xyzqqnotabook".` |
| Empty input (just Enter) | `Please enter a book title.` |
| Spaces only | `Please enter a book title.` |
| `  dune  ` | Searches `dune` normally |
| Wi-Fi off | `Sorry, could not reach Open Library: ...` and no crash |

## Decisions Log

| # | Question | Decision |
|---|---|---|
| 1 | Program flow | One search, then exit |
| 2 | Blank input | Strip spaces; if blank, show a message and exit without an API call |
| 3 | Search parameter | `title=` |
| 4 | Number of results | `limit=5`, `fields=title,author_name`, plus a total-count line |
| 5 | Authors | Join with commas; `Unknown author` if missing |
| 6 | HTTP library | `requests` (installed with `uv add`) |
| 7 | Errors | One catch for `RequestException` and `ValueError`; friendly message with details; `timeout=10` |
| 8 | User-Agent | `CIDM3312-BookSearch/1.0`, with no personal email |
| 9 | Output wording | As specified above |
| 10 | Code structure | `main.py` with `search_books`, `format_book`, `main` |
| 11 | Testing | pytest for `format_book` (via `/tdd`) plus the manual checklist |

## Next Steps

1. `uv init`, `uv add requests`, `uv add --dev pytest`.
2. `/tdd`: write the four `format_book` tests first, then implement.
3. Implement `search_books` and `main`.
4. Run the manual checklist and record the results.
