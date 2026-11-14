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

---

## Session 8: Phased Implementation Plan

**Date:** November 14, 2026

### Prompts Used
- `/prd-to-plan` to break the approved PRD into a phased implementation plan using vertical slices.
- Reviewed the proposed 11-phase breakdown and approved it without merging or splitting phases.
- Asked for the full plan with files, tests, `/tdd` behaviors, manual verification, the `/implement` workflow, commit checkpoints, documentation updates, reflection evidence, dependencies, commands, a final regression checklist, and a reflection reminder.
- Approved the plan and asked to disable `PUT` on the API.

### Work Completed
- Created `plans/django-reading-list.md` with the architectural decisions (URLs, model, auth, shared helper), the commands, the standard phase workflow, phase dependencies, Phase 0 (`CLAUDE.md`), Phases 1–11, a final regression checklist, and a reflection reminder.
- Each phase lists its user stories, what to build, expected files, at most 3 `/tdd` behaviors, other required tests, manual browser checks, screenshots to collect, and a commit message.

### Decisions
- 11 implementation phases, each a vertical slice with its own commit: skeleton and accounts, SavedBook and basic list, Open Library search, save from search, filter/sort/paginate, edit and delete, logged-in Home, API list and detail, API update and delete, script 2, and docs and final check.
- `CLAUDE.md` is created in Phase 0, after the plan is approved and before any Django code.
- Account URLs are under `/accounts/` (`signup`, `login`, `logout`), and saving uses `POST /books/save/` with a safe "return to" URL.
- Phase 1 uses a placeholder `/books/` page, and Phase 2 adds books through the admin until saving exists in Phase 4.
- Screenshots go in `docs/screenshots/`, and must never show tokens or passwords.
- **`PUT` is disabled on the API** (returns 405). `PATCH` handles partial updates to status, rating, and notes. Open Library fields stay read-only. `GET` and `DELETE` work as planned.

### Next Steps
- Phase 0: create `CLAUDE.md`.
- Phase 1: project skeleton and accounts.

---

## Session 9: Phase 0, CLAUDE.md

**Date:** November 14, 2026

### Prompts Used
- Asked to begin Phase 0 only: create `CLAUDE.md` from the approved PRD and implementation plan, covering project structure, commands, coding conventions, testing requirements, security rules, and the required skill workflow, in a beginner-friendly way.

### Work Completed
- Created `CLAUDE.md` with:
  - the project summary
  - a table of source documents
  - the stack, project structure, and durable design rules (model, work key format, editable fields, ownership, shared filter helper, Open Library rules, API with no create and `PUT` disabled, URLs, Layout B)
  - the commands, coding conventions, and testing requirements
  - the required skill workflow (`/implement` every phase, `/tdd` at most 3 behaviors per phase)
  - security rules and documentation/evidence rules
- Checked `.gitignore`: it already covers `db.sqlite3`, `.venv`, `.env`, `.pytest_cache/`, and `.ruff_cache/`.
- Reviewed the files for credentials. None were found.

### Decisions
- `CLAUDE.md` tells future sessions to read the PRD and plan before changing behavior, and to ask when a request conflicts with them.
- `main.py` (script 1) stays independent and is changed only to fix a real bug.
- Files are always staged by name, never with `git add .`.
- The final reflection is written by the student. Claude only helps collect evidence.

### Next Steps
- Phase 1: project skeleton and accounts (install Django and DRF after verifying Python 3.14 support).

---

## Session 10: Phase 1, Project Skeleton and Accounts

**Date:** November 14, 2026

### Prompts Used
- `/implement` Phase 1 of `plans/django-reading-list.md`, following the approved plan exactly.
- Approved each of the three `/tdd` behaviors at RED and GREEN, then asked to finish the remaining Phase 1 requirements and run all checks.

### Work Completed
- **Verified versions on PyPI (official package metadata):** Django 6.1.3 supports Python 3.12–3.15. DRF 3.18.3 supports Python 3.14 and Django 5.2/6.0/6.1. pytest-django 4.14.0 supports Python 3.14 but only lists Django up to 6.0, so it was confirmed to work with Django 6.1 by running the full test suite.
- Installed `django`, `djangorestframework`, and `pytest-django` (dev) with uv. Created the `config` project and `books` app.
- **Settings:** `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` come from environment variables. Django's generated secret key was removed immediately, and the compiled cache that held it was deleted. SQLite database (`db.sqlite3`, gitignored). Login/logout redirect settings. Bootstrap colors for error messages.
- **Pages:** a Bootstrap 5 base layout (dark navbar with a collapsible menu, message alerts, Open Library footer link), the Home page (intro and buttons for visitors, simple welcome for logged-in users), sign-up, login (with "next" support), `POST`-only logout, and a temporary login-required `/books/` placeholder.
- Bootstrap-styled forms through a small mixin on Django's built-in `UserCreationForm` and `AuthenticationForm`, and a shared form-fields template.
- pytest-django is configured in `pyproject.toml`, so `uv run pytest` runs the script 1 tests and the Django tests together.

### TDD (3 behaviors)
1. **Settings refuse to load with `DEBUG` off and no secret key.** RED: settings loaded (exit code 0). GREEN: an `if` raises `ImproperlyConfigured` when `DEBUG` is off and the key is still the fake development key. The test runs settings in a separate process, so it cannot affect the rest of the suite.
2. **Sign-up creates the user, logs them in, and redirects to Home.** RED: 404 (no sign-up page). GREEN: a function view using `UserCreationForm` and Django's `login()`, plus a welcome message.
3. **Logout requires `POST`, logs out, and redirects to Home.** RED: 404 (no logout URL). GREEN: Django's built-in `LogoutView` (which allows only `POST`), extended to add "You have been logged out."

### Tests
- 23 tests pass: 3 TDD tests, 15 more Phase 1 tests, and the 5 script 1 tests.
- The other Phase 1 tests cover: dev mode still loads with the fake key, the welcome and logout messages, mismatched sign-up passwords, login with and without `next`, unsafe `next` being ignored, failed login errors, logged-in users redirected away from login and sign-up, Home for visitors and for logged-in users, and the `/books/` login redirect with `next`.
- `ruff check`, `ruff format --check`, `manage.py check`, and `makemigrations --check` all pass.

### Bugs and Fixes
- **Weak test caught during review:** the "login with a safe next URL" test used `next=/books/`, which is also the default destination, so it would have passed even if `next` were ignored. Changed it to `next=/` so the test actually proves `next` works.
- **Ruff findings:** unused imports in Django's generated `books/admin.py` and `books/models.py` (fixed with `ruff check --fix`; these files get real code in Phase 2). Rule `PLW1510` asked for an explicit `check=False` on `subprocess.run` in the settings test (added, with a comment). Django's generated files used single quotes and some long lines needed wrapping (fixed with `ruff format .`).
- **Deployment check (informational, not fixed):** `manage.py check --deploy` with production-like settings reports the expected HTTPS and secure-cookie warnings and a console email backend error. Deployment is out of scope for this local project. These will be documented in the README's deployment notes (Phase 11).

### Decisions
- Use Django 6.1 and DRF 3.18 (the latest versions, both officially supporting Python 3.14).
- Bootstrap's JavaScript bundle is loaded only for the collapsible navbar and dismissible alerts. Filtering still uses no JavaScript.
- The sign-up view is a short function view (the standard Django tutorial pattern), so the `GET`/`POST` flow is easy to read.

### Manual Browser Testing Results
The student tested Phase 1 in the browser (`uv run manage.py runserver`). These checks passed:

| Check | Result |
|---|---|
| Account registration and automatic login | Passed |
| Welcome message after registration | Passed |
| Logout and confirmation message | Passed |
| Logging back in and reaching My Reading List | Passed |
| Unauthenticated users redirected to login | Passed |
| `GET` request to the logout URL returns 405 | Passed |
| User stays logged in after the rejected `GET` | Passed |
| Mobile layout and collapsible navigation menu | Passed |

Not included in the reported results: the wrong-password error (step 4), the redirect away from login and sign-up while logged in (step 6), and the mismatched-password sign-up error (step 10). These are covered by automated tests.

### Phase 1 Checkpoint
- Phase 1 complete: automated checks pass and manual browser verification was approved by the student.
- Committed and pushed as the Phase 1 checkpoint.

### Next Steps
- Phase 2: SavedBook model, admin, and basic reading list.
