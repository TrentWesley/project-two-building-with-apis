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

---

## Session 6: Planning the Django Application (grill-me)

**Date:** November 14, 2026

### Prompts Used
- `/grill-me` to plan the Django + Django REST Framework reading-list application, one question at a time.
- Summarized the 200-point assignment requirements for Claude instead of pasting the instructions.
- `/prototype` to compare three Bootstrap layouts for the My Reading List page before building any Django pages.
- Asked for a summary of all 22 decisions, a review for contradictions, and the decisions recorded in the planning documentation.

### Work Completed
- Answered all 22 planning questions covering the interface, data model, authentication, API, search/filter/sort/pagination, Open Library integration, saving, pages, prototype, project structure, script 2, settings and secrets, the home page and admin, and the authentication flow.
- Built a UI prototype, `prototypes/reading-list-layouts.html`, with three layouts (table, card grid + sidebar, compact list grouped by status) and a variant switcher.
- Recorded the prototype question, the layouts compared, the decision, and its impact in `prototypes/README.md`.
- Recorded all 22 decisions and a contradictions review in `docs/plans/django-reading-list-decisions.md`.

### Decisions
- **Interface:** Django templates with Bootstrap for users, plus a separate DRF API for scripts.
- **Data model:** One `SavedBook` model owned by a user (`ForeignKey`), with Open Library fields (work key, title, author, first publish year, cover ID), user fields (status, rating 1–5, notes), and `created_at`. A user cannot save the same work twice. No shelves: books are grouped by status (Want to Read, Reading, Finished).
- **Authors:** One comma-joined `CharField`, with "Unknown author" when missing or empty.
- **Editing:** Only status, rating, and notes are editable. Open Library fields are read-only.
- **Website auth:** Django's built-in login/logout plus a `UserCreationForm` sign-up page. Home, login, and sign-up are public. Everything else requires login. Other users' books return 404.
- **API auth:** DRF token authentication (listed first, so unauthenticated requests get 401) plus session authentication for the browsable API. Script 2 reads its token from `READING_LIST_TOKEN`.
- **API endpoints:** List, detail, `PATCH`, and `DELETE` on `/api/books/`. No create endpoint.
- **Search/filter/sort:** One shared `filter_books` helper (Q objects on title or author, a status filter, sort by title/author/newest/oldest, default newest, invalid values ignored), used by both the website and the API. 10 per page on both.
- **Open Library integration:** A `books/openlibrary.py` service module, separate from `main.py`, showing 10 results with cover thumbnails and a "Data from Open Library" link.
- **Saving:** A hidden-field `POST` form validated by a Django form, with the user set by the server, friendly duplicate messages, and "In your list" labels.
- **Pages:** My Reading List (`ListView`), Edit (`UpdateView`), and Delete confirmation (`DeleteView`). No detail page.
- **Prototype decision:** Chose **Layout B (card grid + sidebar)** because covers and book information are easy to see, the sidebar keeps searching, filtering, and sorting organized, statuses, ratings, and actions are clearly visible, and it looks like a complete reading-list website. Final version: cleaner "No cover" placeholders, good small-screen behavior, and consistent design across all pages.
- **Project structure:** `config/` (settings), one `books/` app, shared `templates/`, `main.py` (script 1), and `api_script.py` (script 2). Packages: Django and DRF, with Bootstrap via CDN. Tests: pytest + pytest-django (`uv run pytest` runs everything). Ruff for linting and formatting.
- **Script 2:** Interactive prompts. Lists the first page of books, asks for a book ID and a new status, validates both, sends a `PATCH`, and prints the before and after values from real API data. Handles missing or rejected tokens, the server being down, an empty list, invalid IDs, 404s, invalid statuses, and network errors. Tests use pytest's `monkeypatch`.
- **Settings and secrets:** `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` come from environment variables, with a fake development key. Django refuses to start with the fake key when `DEBUG` is False. The generated key is never committed, and `db.sqlite3` stays gitignored.
- **Home and admin:** The home page changes based on login (intro and buttons for visitors; a welcome message, links, and the user's status counts for logged-in users). `SavedBook` is registered in the admin with columns, filters, and search.
- **Auth flow:** Sign-up logs in automatically and goes to Home. Login goes to a safe `next` URL or My Reading List. Logout uses `POST` and goes to Home with a message. Logged-in users are redirected away from Login and Sign up.
- **Review:** No contradictions between the decisions. Seven open items were recorded for the PRD and plan, including spreading `/tdd` behaviors across phases (at most 3 per phase), using a no-JavaScript Apply button for the sidebar, and checking that the Django version supports Python 3.14.

### Next Steps
- Review the planning summary, then commit the planning documents.
- Run `/to-prd` to create the PRD from these decisions.
- Run `/prd-to-plan` to create the phased implementation plan, then create `CLAUDE.md`.

---

## Session 7: Writing the PRD

**Date:** November 14, 2026

### Prompts Used
- Approved the 22 `/grill-me` decisions and two recommendations (an Apply button for sidebar filters, and status counts for the whole reading list), then asked to commit the planning files.
- `/to-prd` to create the PRD from the approved decisions and assignment requirements.
- Reviewed the PRD, approved it and two added details, and asked Claude to check it against every assignment requirement before committing.

### Work Completed
- Created `prd/django-reading-list.md` with the problem statement, solution, 70 user stories, implementation decisions, out-of-scope items, and further notes.
- Added an **Assignment Requirements Coverage** table that maps every requirement to where the PRD addresses it.
- During the final check, found and fixed four gaps: SQLite was not named as the database, recording bugs and fixes was missing, screenshots and reflection evidence were only mentioned as out of scope, and keeping `CLAUDE.md` accurate was missing.

### Decisions
- If a user account is deleted, their saved books are deleted too.
- Invalid or out-of-range page numbers are handled gracefully, never with a server error.
- Open Library work keys must match `/works/OL`, then digits, then `W`. Invalid save data gets a friendly error.
- Django and DRF versions must officially support Python 3.14, verified when installing.
- The name-only Open Library User-Agent is documented as a known limitation, along with Open Library's rate limits and contact-info guidance.
- The `/tdd` limit of 3 behaviors per phase is a requirement for the implementation plan.
- Every phase records actual bugs and fixes in `PROMPTS.md` and captures screenshots (with no tokens or passwords) as evidence for the reflection.

### Next Steps
- Provide the five required reflection questions before the reflection phase.
- Run `/prd-to-plan` to create the phased implementation plan, then review it before any coding.
