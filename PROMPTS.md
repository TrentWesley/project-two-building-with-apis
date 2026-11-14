# Project #2: Building With APIs

## Claude Code Session Log

This file documents the prompts, decisions, and work completed during Project #2.

---

## Session 1: Project Setup

**Date:** November 12, 2026

### Prompts Used
No Claude Code prompts used yet.

### Work Completed
- Created and cloned the GitHub repository.
- Set up the project folder in cidm3312.
- Copied six Claude Code skills from Project #1.
- Created the research skill.
- Created PROMPTS.md.

### Decisions
- Use the required engineering workflow from the course instructions.

### Next Steps
- Finish project setup.
- Research an external API.
- Begin the grill-me interview.

---

## Session 2: API Research

**Date:** November 12, 2026

### Prompts Used
- `/research` to investigate three free public APIs for Project #2. The research checked what data each API provides, cost and API keys, search and pagination, rate limits, local storage terms, and error handling, using official documentation only.
- Asked for a simple summary of the three APIs' advantages, disadvantages, and limitations.
- Asked to record the API decision in `docs/research/api-options.md`.

### Work Completed
- Compared Open Library, Art Institute of Chicago, and TheMealDB.
- Saved the research and decision in `docs/research/api-options.md`.

### Decisions
- Selected Open Library because it is free, requires no API key, supports simple searching and pagination, and allows us to save book information locally.

### Next Steps
- Create and test a beginner-friendly Python script that searches the Open Library API.

---

## Session 3: Planning the Search Script (grill-me)

**Date:** November 14, 2026

### Prompts Used
- `/grill-me` to plan a beginner-friendly Python script that asks for a book title, searches the Open Library API, displays matching titles and authors, handles no results and API errors without crashing, and runs using uv. Claude asked one question at a time with options and a recommendation, and no code was written.
- Asked to save the agreed plan to `docs/plans/open-library-search-script.md` and document this session in `PROMPTS.md`.

### Work Completed
- Answered 11 planning questions covering program flow, input handling, the API request, output, errors, code structure, and testing.
- Saved the full plan in `docs/plans/open-library-search-script.md`.

### Decisions
- **Flow:** One search per run, then exit (no loop).
- **Blank input:** Strip extra spaces. If the title is empty or only spaces, print "Please enter a book title." and exit without calling the API.
- **Search:** Use `search.json` with the `title=` parameter, `limit=5`, and `fields=title,author_name`.
- **Output:** Show the total and how many are displayed (e.g., "Found 1,106 matches. Showing the first 5."), with singular "match" for one result. Number the results as `1. Title by Author`. If nothing matches, print `No books found for "<title>".`
- **Missing data:** Join multiple authors with commas. Use "Unknown author" or "Unknown title" when a field is missing.
- **HTTP library:** `requests`, added with `uv add requests`.
- **Errors:** Use one handler for `requests.exceptions.RequestException` and `ValueError` that prints a friendly message with the error details. Use a 10-second timeout and `raise_for_status()`.
- **User-Agent:** `CIDM3312-BookSearch/1.0`, with no personal email, because the repository is public.
- **Code structure:** One `main.py` with `search_books(title)`, `format_book(book)`, and `main()`, plus `if __name__ == "__main__": main()`.
- **Testing:** Write pytest tests for `format_book()` covering one author, multiple authors, a missing author, and a missing title, using `/tdd` (tests first). Add pytest as a dev dependency with `uv add --dev pytest`. Use a manual checklist for successful searches, no results, blank input, spaces only, and API errors.

### Next Steps
- Set up the project with `uv init`, `uv add requests`, and `uv add --dev pytest`.
- Use `/tdd` to write the `format_book()` tests before implementing the code.
- Implement the script and run the manual testing checklist.

---

## Session 4: Python Setup and TDD for Book Formatting

**Date:** November 14, 2026

### Prompts Used
- Asked to set up the Python project with uv: `uv init`, `uv add requests`, and `uv add --dev pytest`, then verify the dependencies.
- `/tdd` to develop the `format_book()` function test-first, approving each test at RED and each implementation at GREEN before moving on.
- Asked to add two more tests (missing title and empty author list) using the same test-first approach.
- Asked to update the plan, document this session, and commit the work.

### Work Completed
- Initialized the project with `uv init --bare` (to avoid generating a sample `main.py`) and pinned Python 3.14 in `.python-version`.
- Added `requests` as a dependency and `pytest` as a dev dependency. uv recorded them in `pyproject.toml` and `uv.lock`.
- Used the `/tdd` skill to write each test **before** the formatting logic, following RED (test fails) → GREEN (minimum code to pass) for each behavior.
- Wrote five pytest tests for `format_book()` in `test_main.py`:
  1. One author → `Dune by Frank Herbert`
  2. Multiple authors → `Good Omens by Terry Pratchett, Neil Gaiman`
  3. Missing author → `Dune by Unknown author`
  4. Missing title → `Unknown title by Frank Herbert`
  5. Empty author list → `Dune by Unknown author`
- Implemented `format_book()` in `main.py`. All five tests pass with `uv run pytest`.
- Updated `docs/plans/open-library-search-script.md` to include the empty-author-list case.

### Decisions
- Used three TDD behaviors (one author, multiple authors, missing author), as the `/tdd` skill allows at most three. Then added the missing-title and empty-author-list tests with the same test-first approach.
- Accepted a `KeyError` crash as RED for the missing-author test. The `/tdd` skill normally requires an assertion failure, but the crash was the exact missing behavior being tested. Adding a workaround first would have meant writing part of the fix before the test was approved.
- Treat an empty `author_name` list the same as a missing one (`Unknown author`). This case was found during TDD and added to the plan.
- Used `book.get()` with default values and an `if author_names:` check to keep the code short and beginner-friendly.

### Next Steps
- Implement `search_books()` and `main()` according to the plan.
- Run the manual testing checklist for successful searches, no results, blank input, spaces only, and API errors.

---

## Session 5: Implementing the Search Script

**Date:** November 14, 2026

### Prompts Used
- `/implement` to complete the Open Library search script according to `docs/plans/open-library-search-script.md`.
- Confirmed that this phase had no additional TDD behaviors, because `search_books()` and `main()` use the live API and user input, which we agreed to test manually.
- Asked to implement `search_books()` first, verify it with a live API search, and stop for approval before implementing `main()`.
- Asked to implement `main()`, then add Ruff and run the linter, formatter, and tests.
- Ran the manual testing checklist and asked to document, commit, and push the completed script.

### Work Completed
- Implemented `search_books(title)` in `main.py`. It calls `https://openlibrary.org/search.json` with `title`, `limit=5`, and `fields=title,author_name`, sends the `CIDM3312-BookSearch/1.0` User-Agent, uses a 10-second timeout, and calls `raise_for_status()`.
- Verified `search_books()` with live searches: "dune" returned 5 books, and a made-up title returned `numFound: 0`.
- Implemented `main()`. It prompts for a title, strips extra spaces, rejects blank input, searches once, shows the match count (singular "match" for one), prints a numbered list using `format_book()`, shows a "No books found" message, and catches `RequestException` and `ValueError` without crashing.
- Added `if __name__ == "__main__": main()` so the tests can import functions without running the script.
- Installed Ruff as a development dependency with `uv add --dev ruff`.

### Checks
- `uv run pytest`: all 5 tests passed.
- `uv run ruff check .`: all checks passed.
- `uv run ruff format --check .`: all files already formatted. No fixes were needed.

### Manual Testing Results
All 8 manual tests passed using `uv run main.py`:

| # | Test | Result |
|---|---|---|
| 1 | Normal search for "dune" | Passed: total count and 5 numbered books |
| 2 | Search with zero results | Passed: `No books found for "<title>".` |
| 3 | Blank input | Passed: `Please enter a book title.` |
| 4 | Spaces-only input | Passed: `Please enter a book title.` |
| 5 | Search returning exactly one book | Passed: `Found 1 match. Showing the first 1.` |
| 6 | Search returning two books | Passed: `Found 2 matches. Showing the first 2.` |
| 7 | "dune" with extra spaces | Passed: same results as "dune" |
| 8 | Simulated network error | Passed: friendly error message, no Python traceback |

The network error was simulated with a temporary, unreachable `HTTPS_PROXY` setting, which was removed and verified as cleared afterward.

### Decisions
- Kept error handling in `main()` and let `search_books()` raise errors, so one function decides what the user sees.
- Used `data.get()` with defaults for `numFound` and `docs` so an unexpected response cannot cause a `KeyError`.
- Used `if not books:` to detect no results, matching the empty-list check in `format_book()`.
- Added Ruff as the linter and formatter for the project.

### Next Steps
- Begin planning the Django application for Project #2.
