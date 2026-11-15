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

---

## Session 11: Phase 2, SavedBook Model and Basic Reading List

**Date:** November 14, 2026

### Prompts Used
- `/implement` Phase 2 of `plans/django-reading-list.md`, following the approved plan exactly, stopping at each `/tdd` RED for approval.
- Approved each of the three `/tdd` behaviors at RED and GREEN, then asked to finish the remaining Phase 2 work and run all checks.

### Work Completed
- **`SavedBook` model:** owner `ForeignKey` to Django's `User` (`CASCADE`), `work_key`, `title`, `author`, optional `first_publish_year` and `cover_id`, `status` (Want to Read / Reading / Finished, default Want to Read), optional `rating` (1–5 validators), optional `notes`, `created_at`, and a `UniqueConstraint` on (`user`, `work_key`).
- **One migration:** `books/migrations/0001_initial.py`, regenerated after each model change so Phase 2 ends with a single initial migration. Applied to the local database.
- **Admin:** `SavedBook` registered with columns (title, user, status, rating, created_at), filters (status, created_at), and search (title, author, username).
- **My Reading List (`/books/`):** the Phase 1 placeholder was replaced with a login-required `ListView` showing only the logged-in user's books, newest first, as Layout B cards with a cover image (or a cleaner "No cover" placeholder with a book icon and the title), a status badge (gray/blue/green), the author and year, and star ratings or "Not rated". An empty list shows a friendly message with a link to search (the search page arrives in Phase 3).
- Card pieces (cover, status badge, stars) are small reusable template includes for later pages.

### TDD (3 behaviors)
1. **The same user can't save the same work twice, but another user can.** RED: the database saved a duplicate ("DID NOT RAISE IntegrityError"). GREEN: `UniqueConstraint(fields=["user", "work_key"])`.
2. **A rating must be blank or 1–5.** RED: a rating of 0 passed validation. GREEN: `MinValueValidator(1)` and `MaxValueValidator(5)` on `rating`.
3. **`/books/` shows only the logged-in user's books.** RED: the placeholder page showed no books. GREEN: a `ListView` whose queryset is filtered by `request.user`.

### Tests
- 33 tests pass: the 3 TDD tests, 7 more Phase 2 tests, and the 23 earlier tests.
- The other Phase 2 tests cover: defaults (status, `created_at`, blank rating and notes), deleting a user deletes their books, the empty-list message, newest-first order, the card content (status label, stars, "Not rated", cover URL, "No cover"), staff admin search by username, and regular users blocked from the admin.
- `ruff check`, `ruff format --check`, `manage.py check`, and `makemigrations --check` all pass.

### Bugs and Fixes
- **Possible flaky test:** the newest-first test depended on two books getting different `created_at` times when created a split second apart. Fixed by giving them explicit, different timestamps.
- **Ruff `SIM117`:** combined two nested `with` statements in the uniqueness test (auto-fixed).
- **Ruff `RUF012` false alarms:** Ruff flagged Django's standard list class attributes (`list_display`, `Meta.constraints`, and the generated migration). Configured Ruff to skip generated migrations and ignore `RUF012`, with comments explaining why, instead of rewriting idiomatic Django code.
- **Renamed a test:** the Phase 1 test `test_reading_list_placeholder_loads_for_logged_in_user` became `test_reading_list_loads_for_logged_in_user`, because the page is no longer a placeholder (a mechanical rename; its assertions are unchanged).

### Decisions
- A rating is enforced by field validators (used by forms, the admin, and the API), and uniqueness is enforced by the database itself.
- Phase 2 shows cards only. The sidebar (Phase 5) and Edit/Delete buttons (Phase 6) come later, as planned.

### Manual Browser Testing Results
The student tested Phase 2 in the browser (admin superuser plus a second user, `reader2`). These checks passed:

| Check | Result |
|---|---|
| Django admin dashboard and SavedBook registration | Passed |
| Adding books with different statuses and ratings | Passed |
| Book cards, cover images, and "No cover" placeholders | Passed |
| Newest-first reading list order | Passed |
| Duplicate book validation (same user, same work key rejected) | Passed |
| Rating validation (6 rejected) | Passed |
| Separate reading lists for admin and `reader2` | Passed |
| Regular users blocked from the Django admin | Passed |
| Empty reading list for a new user | Passed |
| Responsive mobile layout | Passed |

Not included in the reported results: the admin search and filters (steps 5–6) and a different user saving the same work (step 8). These are covered by automated tests (admin search by username, and the uniqueness test's second-user case).

### Phase 2 Checkpoint
- Phase 2 complete: automated checks pass and manual browser verification was approved by the student.
- Committed and pushed as the Phase 2 checkpoint.

### Next Steps
- Phase 3: Search Open Library.

---

## Session 12: Phase 3, Search Open Library

**Date:** November 14, 2026

### Prompts Used
- `/implement` Phase 3 of `plans/django-reading-list.md`, after re-reading `CLAUDE.md`, the PRD, the plan, and the Open Library research, stopping at each `/tdd` RED and GREEN for approval.
- Approved the three `/tdd` behaviors one at a time, then asked to complete the remaining Phase 3 work with mocked API requests and no Save buttons (Phase 4).

### Work Completed
- **`books/openlibrary.py` (service module, separate from `main.py`):** `search_books(title)` calls the Search API with `title=`, `fields=key,title,author_name,first_publish_year,cover_i`, `limit=10`, User-Agent `CIDM3312-BookSearch/1.0`, `timeout=10`, and `raise_for_status()`. It returns `{"total", "books"}`. Network errors, timeouts, HTTP errors, invalid JSON, and unexpected response shapes all become one `OpenLibraryError`. `clean_book(doc)` converts a raw result into a dictionary using the `SavedBook` field names.
- **`/search/` page (login required, `GET`):** a search form. Blank or spaces-only input shows "Please enter a book title." with no API call. Results show "Found N matches. Showing the first M." (comma-separated total, singular "match" for 1) and Layout B cards with the shared cover include (cover or "No cover" placeholder), title, authors, and year (or "Year unknown"). No results shows `No books found for "<title>".` A failure shows a friendly red alert, and the technical details are logged on the server.
- **Navbar:** a "Search Open Library" link (highlighted on the search page). The empty reading list's link now points to the real search page.
- **Test safety net:** `books/tests/conftest.py` blocks real network calls in every Django test.

### TDD (3 behaviors)
1. **Open Library results are normalized, including missing fields** (3 cases: complete, missing fields, empty author list). RED: the stub returned `{}`. GREEN: `clean_book()` using `.get()` with defaults and an `if author_names:` check.
2. **A blank search shows a message without calling Open Library.** RED: 404 (no search page). GREEN: a login-required view that strips the title and shows the message when it is blank, before any API call.
3. **An Open Library failure shows a friendly alert.** RED: the alert was missing. GREEN: `try`/`except OpenLibraryError` in the view, plus `logger.warning(...)` for the technical details.

### Tests
- 51 tests pass: 5 TDD test cases (behavior 1 has 3 cases), 13 more Phase 3 tests, and the 33 earlier tests.
- The other Phase 3 tests cover:
  - the exact request (URL, params, User-Agent, timeout) and the clean results
  - connection errors and timeouts, HTTP errors, invalid JSON, and unexpected shapes becoming `OpenLibraryError`
  - login required, and a first visit showing no messages and making no call
  - the results line with the comma total, cards, and placeholders
  - singular wording, the no-results message, the search term being stripped, and the error being logged
- `ruff check`, `ruff format --check`, `manage.py check`, and `makemigrations --check` all pass.
- One live smoke test outside the test suite (real API): "dune" returned 21,109 matches and 10 results, "the relentless moon" returned 1, and a made-up title returned 0.

### Bugs and Fixes
- **Wrong test expectation:** the no-results test expected `&quot;` around the search term, but the quote marks are typed directly in the template, so they appear as plain `"`. Django only escapes variables (its protection against code injection). Fixed the test, not the page.
- **Ruff `I001`:** a blank line between two imports in the service tests (auto-fixed).

### Decisions
- One `OpenLibraryError` for every failure, so the view handles a single case.
- The view formats the comma-separated total itself (for example, 21,108) instead of adding Django's `humanize` app, keeping to "no extra apps".
- Search cards use the same shared cover include and Layout B grid as the reading list.

### Manual Browser Testing Results
The student personally tested Phase 3 in the browser against the live Open Library API. All checks passed:

| # | Check | Result |
|---|---|---|
| 1 | Search Open Library navigation link and search page work | Passed |
| 2 | "dune" returns 10 book cards with covers, titles, authors, and years | Passed |
| 3 | "the relentless moon" returns one result with singular wording | Passed |
| 4 | A nonexistent book shows the no-results message | Passed |
| 5 | Empty and spaces-only searches show the warning | Passed |
| 6 | Missing covers, years, and authors show placeholders | Passed |
| 7 | Refreshing a search keeps the query and results | Passed |
| 8 | Logged-out users are redirected to login | Passed |
| 9 | The empty reading list links to the search page | Passed |
| 10 | Responsive mobile layout | Passed |
| 11 | Simulated API failure (`HTTPS_PROXY=http://127.0.0.1:9`) shows the friendly red alert without crashing | Passed |
| 12 | After removing `HTTPS_PROXY`, normal searches work again | Passed |

Not included in the reported results: the `WARNING` line in the server terminal during the simulated failure. Logging is covered by an automated test (`caplog`).

### Phase 3 Checkpoint
- Phase 3 complete: automated checks pass and manual browser verification was approved by the student.
- Committed and pushed as the Phase 3 checkpoint.

### Next Steps
- Phase 4: save Open Library search results to the reading list.

---

## Session 13: Phase 4, Save from Search

**Date:** November 14, 2026

### Prompts Used
- `/implement` Phase 4 of `plans/django-reading-list.md`, after re-reading `CLAUDE.md`, the PRD, the plan, and `PROMPTS.md`, stopping at each `/tdd` RED and GREEN for approval.
- Approved the three `/tdd` behaviors one at a time, including the requirement that a near-simultaneous duplicate save must not crash.
- Approved the remaining Phase 4 work: Save buttons, "In your list" labels, and the remaining tests.

### Work Completed
- **`SaveBookForm`** (a `ModelForm` with only the five Open Library fields): validates the work key with Django's `RegexValidator` (`^/works/OL[0-9]+W$`), requires a title and author, and converts the year and cover ID to integers (blank becomes `None`). `user` and `status` are not form fields, so they cannot be tampered with.
- **`POST /books/save/`** (login required, `POST` only):
  - sets the owner from the login and the status to Want to Read
  - shows "Saved <title> to your reading list."
  - shows "<title> is already in your reading list." for duplicates, with a database-rule backstop for near-simultaneous clicks (`transaction.atomic()` plus `except IntegrityError`)
  - shows "Sorry, that book couldn't be saved because its details were invalid." for any invalid data
  - redirects to a safe same-site `next` URL, otherwise `/search/`
- **Search results:** each card has a "Save to My List" button (CSRF-protected `POST` form with hidden fields and the current search URL as `next`), or a green "✓ In your list" label if the user already saved that work. Saved work keys are looked up with one database query per search.

### TDD (3 behaviors)
1. **A valid save adds the book to my list as Want to Read.** RED: no book saved (404). The first version crashed on `.get()` instead of failing an assertion, so it was changed to assert the count first. GREEN: `SaveBookForm` plus a login-required, `POST`-only view that sets the user, with a safe redirect and a success message.
2. **Saving the same book twice shows a friendly message and creates no duplicate.** RED: 500 Internal Server Error (`IntegrityError` from the Phase 2 unique rule). The test client was set to return server errors as pages, like a real browser. GREEN: an "already saved?" check, plus `transaction.atomic()` and `except IntegrityError` as a backstop.
3. **An invalid work key is rejected without saving** (4 cases: `abc`, `/books/OL123M`, empty, `/works/OLW`). RED: three junk keys were saved, and the empty key was rejected silently with no message. GREEN: `RegexValidator` on the form's `work_key`, and an error message for invalid forms.

### Tests
- 69 tests pass: 6 TDD test cases (behavior 3 has 4 cases), 12 more Phase 4 tests, and the 51 earlier tests.
- The other Phase 4 tests cover:
  - saving requires login, and a `GET` to `/books/save/` returns 405
  - a submitted `user` ID is ignored, and an unsafe `next` URL falls back to `/search/`
  - different users can save the same work, and the duplicate race backstop holds (simulated by making the "already saved?" check miss)
  - an invalid year shows the error, and a book without a year or cover can be saved
  - "In your list" vs. the Save button, and another user's saved book still shows Save
  - the save form is a CSRF-protected `POST` with the correct hidden fields and `next`
  - saved work keys are checked with exactly one query
- `ruff check`, `ruff format --check`, `manage.py check`, and `makemigrations --check` all pass (no model changes).

### Bugs and Fixes
- **Duplicate save crashed (found by TDD behavior 2):** the second save of the same book caused a 500 error. Fixed with the "already saved?" check and the `IntegrityError` backstop.
- **Junk work keys were saved (found by TDD behavior 3):** `abc`, `/books/OL123M`, and `/works/OLW` were all accepted. Fixed with the `RegexValidator`.
- **Invalid saves gave no feedback:** an invalid form redirected silently. Fixed with a friendly error message.
- **Test that crashed instead of failing:** behavior 1's first RED used `.get()`, which raised `DoesNotExist`. Changed to assert the count first (a mechanical change before approval).
- **Hard-to-read formatting:** Ruff's formatter wrapped `book.user = request.user` with a trailing comment into three lines. Moved the comment above the line.

### Decisions
- The work-key format rule lives on the save form, not the model, so no new migration was needed.
- Used `[0-9]` instead of `\d` in the pattern, because `\d` also matches digits from other alphabets.
- Duplicate messages are blue (info), success is green, and invalid data is red (error).
- The race-condition backstop was first checked by hand with a temporary script on a throwaway test database, then saved as a permanent test.

### Manual Browser Testing Results
The student personally tested Phase 4 in the browser. All checks passed:

| # | Check | Result |
|---|---|---|
| 1 | Save to My List buttons appear on search results | Passed |
| 2 | Saving Dune shows the success message and the "In your list" label | Passed |
| 3 | Dune appears in My Reading List with Want to Read status | Passed |
| 4 | Saving a second book works | Passed |
| 5 | Duplicate saves show a friendly message without creating another copy | Passed |
| 6 | Invalid work keys (edited in DevTools) are rejected with a red error message | Passed |
| 7 | Unsafe redirect URLs are blocked | Passed |
| 8 | Books without covers save and display correctly | Passed |
| 9 | Different users can save the same book independently | Passed |
| 10 | `GET /books/save/` returns 405 Method Not Allowed | Passed |
| 11 | The mobile layout works at 375px | Passed |

### Phase 4 Checkpoint
- Phase 4 complete: automated checks pass and manual browser verification was approved by the student.
- Committed and pushed as the Phase 4 checkpoint.

### Next Steps
- Phase 5: search, filter, sort, and paginate the reading list.

---

## Session 14: Phase 5, Search, Filter, Sort, and Paginate My List

**Date:** November 14, 2026

### Prompts Used
- `/implement` Phase 5 of `plans/django-reading-list.md`, after re-reading `CLAUDE.md`, `PROMPTS.md`, the PRD, the plan, and the existing model, list view, templates, and tests, stopping at each `/tdd` RED and GREEN for approval.
- Approved three `/tdd` behaviors (the student's list, which reorganizes the plan's search/status/sort behaviors so pagination is also test-driven):
  1. Q-object search matches title OR author without showing another user's books.
  2. Invalid status and sort values are handled safely, with an invalid sort defaulting to newest.
  3. Pagination shows 10 books per page and keeps the active query parameters.
- Approved the remaining Phase 5 work: the Layout B sidebar, whole-list status counts, the "no matches" message, and the remaining tests.

### Work Completed
- **`books/filters.py`** (shared helper, to be reused by the API in Phase 8):
  - `filter_books(queryset, search, status, sort)`: stripped, case-insensitive `Q(title__icontains) | Q(author__icontains)` search; status filter only for `want_to_read`/`reading`/`finished`; sorts `newest` (default), `oldest`, `title`, `author`, each with a `pk` tie-break.
  - `clean_search`, `clean_status`, `clean_sort`: turn missing, blank, or unknown values into the defaults, so the filter and the sidebar use the same rules.
  - `status_counts(queryset)`: counts per status plus the total in one query (`aggregate` with filtered `Count`).
- **`BookListView`:** starts from only the logged-in user's books, applies `filter_books`, then paginates 10 per page with `Paginator.get_page()` (bad `page` values show a real page). Passes the current values, sort choices, whole-list counts, and a URL-encoded `filter_query` (built with `QueryDict`) to the template.
- **Templates:**
  - `includes/filter_sidebar.html`: one `GET` form with the search box, status radio buttons (All, Want to Read, Reading, Finished) with count badges, the sort dropdown, and an **Apply** button. It shows the values in use, and Apply starts again at page 1.
  - `includes/pagination.html`: Bootstrap Previous / page numbers / Next links that keep `q`, `status`, and `sort`. Hidden when there is only one page, and wraps on phones.
  - `book_list.html`: Layout B. The sidebar is a `col-lg-3` column that stacks above the cards below the large breakpoint, and the cards are one per row on phones. "No books match your filters." (with a Clear filters link) is separate from "Your reading list is empty." The sidebar is hidden when the list is empty, since there is nothing to filter.
- **`CLAUDE.md`:** added the two new includes and a note that search/filter/sort rules live only in `books/filters.py`.

### TDD (3 behaviors)
1. **Search matches title OR author, only my books.** RED: `?q=  LE GUIN  ` returned all four of my books, because `q` was ignored. GREEN: `filter_books` with the stripped `Q`-object search, called from `get_queryset()`.
2. **Invalid status/sort are safe; each valid value works** (12 cases, with explicit save dates a month apart and another user's book that would come first in every order). RED: 6 cases failed (the three status filters, and the `oldest`/`title`/`author` sorts), and the 6 "ignore it, newest first" cases already passed by accident. GREEN: status checked against `SavedBook.Status.values`, a `SORT_ORDERS` dictionary with a `newest` fallback and a `pk` tie-break, and the view's own `order_by` removed.
3. **10 per page, links keep the filters** (13 matching books, 2 of mine filtered out, and another user's matching book). RED: all 13 matches on one page. GREEN: `paginate_by = 10`, `get_page()` for `?page=abc` and `?page=999`, and the pagination partial built from `filter_query`.

### Tests
- 92 tests pass: 14 TDD test cases (behavior 2 has 12 cases), 9 more Phase 5 tests, and the 69 earlier tests.
- The other Phase 5 tests cover:
  - search, status, and sort combined
  - status counts covering the whole list even while filtered, and excluding other users' books
  - "No books match your filters." vs. "Your reading list is empty."
  - the sidebar keeping submitted values, and showing the defaults for unknown values
  - page links safely encoding a search containing `&`
  - the book count showing all matches (12) while the page shows 10
  - no pagination links with 10 or fewer books
- `ruff check`, `ruff format --check`, `manage.py check`, and `makemigrations --check` all pass (no model changes).

### Bugs and Fixes
- **Book count would always say "10 books":** the header counted the cards on the current page (`books|length`). Found while adding pagination. Changed it to the total matching books (`paginator.count`) and added a test.
- **Django's default pagination returns 404 for bad page numbers:** `ListView` raises a 404 for `?page=abc` or `?page=999`. Behavior 3's test required a real page, so the view uses `Paginator.get_page()` instead.
- **Sorting lived in two places:** after behavior 1, the newest-first order was still in the view. Moved into the helper in behavior 2, so the API will sort exactly the same way.
- **Tool problem (not a code bug):** at the start of the session, a shell command meant to update `PROMPTS.md` hung and changed nothing. It was stopped, and the edit was made with the editor.

### Decisions
- Followed the student's three `/tdd` behaviors instead of the plan's (search / status / sort). The plan's status and sort checks are all inside behavior 2, so no acceptance criterion lost its test.
- Title and author sorting uses the database's normal text order (capital letters before lowercase). Lowercasing just for sorting was left out to keep things simple.
- Counts use one database query for the whole list, not one per status.
- The sidebar form has no `page` field, so Apply always starts at page 1 (a narrower filter might have fewer pages).

### Manual Browser Testing Results
The student personally tested Phase 5 in the browser. All checks passed:

| # | Check | Result |
|---|---|---|
| 1 | The sidebar displays correctly | Passed |
| 2 | The reading list shows 10 books per page | Passed |
| 3 | Page 2 displays the remaining book | Passed |
| 4 | Searching by author works | Passed |
| 5 | Sorting by title works | Passed |
| 6 | The no-matches message and Clear filters link work | Passed |
| 7 | Invalid sort values default to newest | Passed |
| 8 | Invalid status values default to All | Passed |
| 9 | Invalid page numbers are handled correctly | Passed |
| 10 | The mobile layout works at 375px | Passed |
| 11 | Reading-status counts add up correctly | Passed |
| 12 | Different users only see their own books and counts | Passed |
| 13 | Filtering by Finished works correctly | Passed |

Not included in the reported results: the counts staying the same while a filter is applied. This is covered by an automated test (`test_status_counts_cover_my_whole_list_even_while_filtered`).

### Phase 5 Checkpoint
- Phase 5 complete: automated checks pass and manual browser verification was approved by the student.
- Committed and pushed as the Phase 5 checkpoint.

### Next Steps
- Phase 6: edit and delete books.

---

## Session 15: Phase 6, Edit and Delete Books

**Date:** November 14, 2026

### Prompts Used
- `/implement` Phase 6 of `plans/django-reading-list.md`, after re-reading `CLAUDE.md`, `PROMPTS.md`, the PRD, the plan, and the existing model, views, forms, templates, and tests, stopping at each `/tdd` RED and GREEN for approval.
- Approved three `/tdd` behaviors:
  1. Editing status, rating, and notes saves correctly, while the Open Library facts stay unchanged.
  2. Users cannot edit or delete another user's book (404).
  3. Deletion requires confirmation and `POST`; `GET` never deletes.
- Chose Option 1 for behavior 3: write it as a regression test and report honestly that it passed immediately, without breaking working code to force a RED.
- Approved the remaining Phase 6 work: read-only book info, validation errors, success messages, card buttons, and the remaining tests.

### Work Completed
- **`EditBookForm`** (`ModelForm` with only `status`, `rating`, `notes`): friendlier labels and help text, a 4-row notes box, and `min`/`max` browser hints on the rating (the model's 1–5 validators are the real rule). `BootstrapFormMixin` now gives dropdowns Bootstrap's `form-select` class.
- **`EditBookView`** (`LoginRequiredMixin`, `SuccessMessageMixin`, `UpdateView`) at `/books/<id>/edit/` (`books:edit`): only the user's own books, "Updated <title>." on success, redirect to `/books/`. Invalid input shows the form again with field errors and "Please fix the errors below. Nothing was changed."
- **`DeleteBookView`** (`LoginRequiredMixin`, `SuccessMessageMixin`, `DeleteView`) at `/books/<id>/delete/` (`books:delete`): only the user's own books, a confirmation page on `GET`, deletion only on the CSRF-protected `POST`, "Removed <title>." and redirect to `/books/`.
- **Templates:**
  - `includes/book_summary.html`: a read-only card (cover, status badge, title, author, first published year) shared by the edit and delete pages.
  - `edit.html` and `delete.html`: the book card next to the form (stacked on phones). The delete page explains that the status, rating, and notes will be deleted too, and Cancel is a plain link.
  - `book_list.html`: Edit and Delete buttons on every card.
- **`CLAUDE.md`:** added `book_summary.html` to the shared includes, the `form-select` styling rule, and the owner-only `get_queryset()` / `SuccessMessageMixin` convention.

### TDD (3 behaviors)
1. **Editing changes only status, rating, and notes.** The test posts the three fields plus tampered `title`, `author`, `work_key`, year, cover, and `user` values. RED: the status was still Want to Read, because `/books/<id>/edit/` didn't exist (404). GREEN: `EditBookForm` with only the three fields, and `EditBookView` limited to the user's own books.
2. **Another user's book returns 404 for edit and delete, `GET` and `POST`, and is never changed; logged-out users go to login** (8 cases). Each 404 case also checks that the owner can open their own page (200), so the 404 comes from the ownership rule, not a missing page. RED: the 4 edit cases already passed (behavior 1's queryset), and the 4 delete cases failed (`assert 404 == 200` and `assert 404 == 302`) because the delete page didn't exist. GREEN: `DeleteBookView` with the same owner-only queryset, the URL, and a basic confirmation page.
3. **`GET` only shows the confirmation; `POST` deletes.** **This was a regression test, not a RED/GREEN cycle.** It passed on its first run, because Django's built-in `DeleteView`, added in behavior 2's GREEN, already shows a confirmation on `GET` and deletes only on `POST`. No working code was broken to force a failure. The test stays as a guard: if a future change made `GET` delete, it would fail.

### Tests
- 118 tests pass: 10 TDD test cases (behavior 2 has 8 cases), 16 more Phase 6 tests, and the 92 earlier tests.
- The other Phase 6 tests cover:
  - ratings of `0`, `6`, `-1`, and `five` rejected with a form error, with nothing saved
  - an invalid status rejected, with nothing saved
  - ratings of 1 and 5 allowed, and the rating and notes optional (and clearable)
  - the "Updated Dune." and "Removed Dune." messages
  - the Edit and Delete links on the list cards
  - the edit page showing the cover, title, author, and year with only three form fields (no inputs for the Open Library facts)
  - the edit form starting with the current values
  - the delete page showing the book info and a Cancel link
  - a missing book ID returning 404
- `ruff check`, `ruff format --check`, `manage.py check`, and `makemigrations --check` all pass (no model changes).

### Bugs and Fixes
- **Status dropdown styling:** `BootstrapFormMixin` gave every field `form-control`, which isn't Bootstrap's class for dropdowns. It now uses `form-select` for `Select` widgets. Found when adding the first form with a dropdown.
- **A delete test that could pass for the wrong reason:** before the delete page existed, another user's delete URL already returned 404 (page not found). An owner control line was added to behavior 2's test so it fails until the ownership rule really exists.

### Decisions
- One owner-only `get_queryset()` per view, instead of checking the owner inside each method, so `GET` and `POST` are protected the same way.
- Success messages use Django's `SuccessMessageMixin`, and the text uses the book title.
- The rating's `min`/`max` HTML attributes are only a browser convenience. The server still rejects anything outside 1–5 (tested by posting `6` directly).

### Manual Browser Testing Results
The student personally tested Phase 6 in the browser. All checks passed:

| # | Check | Result |
|---|---|---|
| 1 | Edit and Delete buttons appear on saved book cards | Passed |
| 2 | The Edit page displays the correct book information | Passed |
| 3 | Editing status, rating, and notes saves successfully | Passed |
| 4 | Saved changes remain when reopening the Edit page | Passed |
| 5 | The browser rejects a rating above 5 | Passed |
| 6 | Rating and notes can be cleared | Passed |
| 7 | The Delete confirmation page displays correctly | Passed |
| 8 | Cancel does not delete the book | Passed |
| 9 | Confirming Delete removes the book and updates the counts | Passed |
| 10 | Another user cannot access my book's Edit page (404) | Passed |
| 11 | Logged-out users are redirected to login | Passed |
| 12 | The Edit page displays correctly at 375px | Passed |
| 13 | The Delete page displays correctly at 375px | Passed |

Not included in the reported results, but covered by automated tests:
- **Server-side rating check:** the reported check was the browser's own `max="5"` limit. The server rejecting a rating of 6 that gets past the browser is covered by `test_invalid_rating_shows_error_and_changes_nothing` (`0`, `6`, `-1`, `five`).
- **Another user's Delete page:** the reported 404 check was for the Edit page. The Delete page (and `POST` to both pages) returning 404 is covered by `test_another_users_book_returns_404_and_is_not_changed`.

### Phase 6 Checkpoint
- Phase 6 complete: automated checks pass and manual browser verification was approved by the student.
- Committed and pushed as the Phase 6 checkpoint.

### Next Steps
- Phase 7: logged-in home page.

---

## Session 16: Phase 7, Logged-in Home Page

**Date:** November 14, 2026

### Prompts Used
- `/implement` Phase 7 of `plans/django-reading-list.md`, after re-reading the plan, the PRD, `CLAUDE.md`, `PROMPTS.md`, the home page, the auth views, the model, and the `status_counts` helper, stopping at each `/tdd` step for approval.
- Approved three `/tdd` behaviors (the student's list; the plan listed two, and the student's version splits "correct counts" from "only my books"):
  1. Logged-in users see their correct reading status counts.
  2. Counts exclude books belonging to other users.
  3. Logged-out visitors see the public home page without private counts.
- Instruction for behaviors that already worked: keep them as regression tests and document that honestly, without breaking working code to force a RED.
- Approved the remaining Phase 7 work: the Search Books link, the zero-books message, responsive layout, and tests.

### Work Completed
- **`home` view:** still public. For logged-in users it passes `status_counts(SavedBook.objects.filter(user=request.user))` to the template, reusing the Phase 5 helper (one query, no new counting logic). Visitors get no counts.
- **`templates/home.html`** (logged-in part):
  - four count boxes (Want to Read, Reading, Finished, Total Saved) with ids `count-want_to_read`, `count-reading`, `count-finished`, `count-all`, colored like the status badges (gray, blue, green)
  - two boxes per row on phones and four on medium screens and up (`row-cols-2 row-cols-md-4`)
  - "You haven't saved any books yet. Search Open Library to get started." when the user has no books
  - **Search Books** (`/search/`) and **My Reading List** (`/books/`) buttons, stacked on phones and side by side from the small breakpoint
  - The welcome message and the whole logged-out part are unchanged.
- **`CLAUDE.md`:** added two testing notes: Django escapes only variables (not text typed in templates), and a `/tdd` behavior that already works is kept as a documented regression test.

### TDD (3 behaviors)
1. **Logged-in users see their correct counts** (3 / 2 / 1, total 6, read from the page HTML by a `shown_count()` helper). RED: `assert None == 3`, because the home page had no count boxes. GREEN: the view calls `status_counts()` on the user's own books, and the template shows the four boxes.
2. **Counts exclude other users' books.** **Regression test, not a RED/GREEN cycle:** it passed on its first run, because behavior 1's view already filtered by the logged-in user. reader1 (1 / 2 / 0, total 3) and reader2 (4 / 0 / 3, total 7) each see only their own numbers. It would fail if the view counted all books (reader1 would see 5 / 2 / 3 / 10).
3. **Logged-out visitors see the public page with no private counts.** **Regression test, not a RED/GREEN cycle:** it passed on its first run, because behavior 1 put the count boxes only inside the logged-in part of the template. It checks the intro, the Sign Up / Log In links, that no `count-...` boxes exist, and that no username or book titles appear.

No working code was broken to force a failure for behaviors 2 or 3.

### Tests
- 125 tests pass: 3 TDD tests (behavior 1 RED/GREEN, behaviors 2 and 3 regression), 4 more Phase 7 tests, and the 118 earlier tests.
- The other Phase 7 tests cover:
  - a new user seeing four zeros and the friendly message
  - the message hidden once the user saves a book
  - the message still shown when only *other* users have books
  - the Search Books and My Reading List links (and no Sign Up button for logged-in users)
- The existing Phase 1 home page tests (visitor intro and buttons, logged-in welcome) still pass.
- `ruff check`, `ruff format --check`, `manage.py check`, and `makemigrations --check` all pass (no model changes).

### Bugs and Fixes
- **Wrong test expectation (repeat of the Phase 3 lesson):** two new tests expected the apostrophe in "haven't" to appear as `&#x27;`. The text is typed directly in the template, so Django doesn't escape it (only variables are escaped). Fixed the test, not the page, and added the rule to `CLAUDE.md` so it isn't repeated.

### Decisions
- Reused `status_counts()` instead of counting again on the home page, so Home and the reading-list sidebar always agree.
- The count boxes are plain bordered boxes, not links. Their colors match the status badges.
- Search Books is the main (filled) button, because a new user's first step is finding books.

### Manual Browser Testing Results
The student personally tested Phase 7 in the browser. All checks passed:

| # | Check | Result |
|---|---|---|
| 1 | Logged-out visitors see the public home page without private counts | Passed |
| 2 | Logged-in users see their welcome message and four reading counts | Passed |
| 3 | Home page counts match the My Reading List sidebar | Passed |
| 4 | The Search Books button opens the Open Library search page | Passed |
| 5 | The My Reading List button opens the saved books page | Passed |
| 6 | Different users see their own reading counts | Passed |
| 7 | A new user sees four zeros and the empty-list message | Passed |
| 8 | Saving a book updates the counts and removes the empty-list message | Passed |
| 9 | At 375px, count boxes show two per row and the buttons stack vertically | Passed |
| 10 | At 1200px, all four count boxes show in one row and the buttons are side by side | Passed |

### Phase 7 Checkpoint
- Phase 7 complete: automated checks pass and manual browser verification was approved by the student.
- Committed and pushed as the Phase 7 checkpoint.

### Next Steps
- Phase 8: API authentication, list, and detail.

---

## Session 17: Phase 8, API Authentication, List, and Detail

**Date:** November 15, 2026

### Prompts Used
- `/implement` Phase 8 of `plans/django-reading-list.md`, after re-reading `CLAUDE.md`, `PROMPTS.md`, the PRD, the plan, the `SavedBook` model, the `filter_books()` helper, the settings, and the URL configuration, stopping at each `/tdd` step for approval.
- Approved three `/tdd` behaviors (the same as the plan):
  1. Unauthenticated API requests (no token or an invalid token) return 401.
  2. An authenticated user gets a paginated list containing only their own books.
  3. Another user's book detail returns 404.
- Approved each test at RED "exactly as written" and each minimum GREEN change.
- Approved the remaining Phase 8 work: connect the API list to `filter_books()` and add normal tests for search, filtering, sorting, invalid values, pagination links, and bad page numbers.
- Asked for the Phase 8 documentation (`CLAUDE.md` and this entry) without committing.

### Work Completed
- **`config/settings.py`:**
  - added `rest_framework` and `rest_framework.authtoken` to `INSTALLED_APPS`
  - `REST_FRAMEWORK`: `TokenAuthentication` then `SessionAuthentication`, `IsAuthenticated`, and `PageNumberPagination` with `PAGE_SIZE` 10
  - `uv run manage.py migrate` applied DRF's own `authtoken` migrations. No new project migration was needed.
- **`books/serializers.py`** (new): `SavedBookSerializer` (`ModelSerializer`) with `id`, `work_key`, `title`, `author`, `first_publish_year`, `cover_id`, `status`, `rating`, `notes`, `created_at`. It never shows `user`. Everything except `status`, `rating`, and `notes` is in `read_only_fields`.
- **`books/api.py`** (new):
  - `BookListAPIView` (`ListAPIView`): starts from `SavedBook.objects.filter(user=request.user)` and passes `q`, `status`, and `sort` to the shared `filter_books()` helper
  - `BookDetailAPIView` (`RetrieveAPIView`): looks the id up only within the user's own books
  - Both views are read-only. `PATCH` and `DELETE` are Phase 9.
- **`books/api_urls.py`** (new, namespace `api`): `books/` (`book-list`) and `books/<int:pk>/` (`book-detail`), included at `/api/` in `config/urls.py`.
- **`books/filters.py`:** docstring only (now says the helper is used by the website and the API).
- **`CLAUDE.md`:** the new API files, the two endpoints, token and session authentication, ownership, pagination, and the API test conventions.

### TDD (3 behaviors)
1. **No token or an invalid token gets 401.** Scaffolding first (installed apps, serializer, list view, URL, and `IsAuthenticated` only), so the test could fail on an assertion. RED: `assert 403 == 401`. DRF's default authentication put Session first, and DRF decides between 401 and 403 from the **first** class. GREEN: list `TokenAuthentication` first, then `SessionAuthentication`. Real responses: no token gives 401 "Authentication credentials were not provided.", and a made-up token gives 401 "Invalid token.", both with `WWW-Authenticate: Token`.
2. **A token user gets only their books, 10 per page.** reader1 has 12 books and reader2 has 4. RED: `assert isinstance(data_1, dict)` failed, because the API returned a plain JSON list with no pagination. GREEN: `DEFAULT_PAGINATION_CLASS` = `PageNumberPagination` and `PAGE_SIZE` = 10. The test checks `count` 12 (not 16), 10 + 2 books, the `next`/`previous` links, no reader2 titles, and exactly the approved fields.
3. **Another user's book detail is 404.** The test checks the user's **own** book (200, approved fields) first, so the 404 can only come from the ownership rule and not from a missing URL. RED: `assert 404 == 200`, because `/api/books/<id>/` didn't exist. GREEN: `BookDetailAPIView` with a user-filtered `get_queryset()` and the `book-detail` URL. The 404 response doesn't include the other user's title.

All three were real RED/GREEN cycles. None passed on its first run, so there are no regression-only tests this phase.

### Tests
- 29 new normal tests in `books/tests/test_api.py`, using the same three books as the website's filter tests:
  - **Search, filter, and sort** (18 cases): title and author search (ignoring capitals and outer spaces), each status, each sort (`newest`, `oldest`, `title`, `author`), all three combined, a search for another user's book finding nothing, and blank or invalid `q`/`status`/`sort` falling back to all books, newest first. `count` matches each time.
  - **API matches the website:** the same parameters give the same books in the same order on `/api/books/` and `/books/`.
  - **Pagination links:** `next` and `previous` keep `q`, `status`, and `sort` and only change `page`.
  - **Stable order:** 12 books with the same save time each appear exactly once across two pages, ordered by id.
  - **Bad pages** (`abc`, `0`, `-1`, `999`, `2.5`): DRF's standard 404 `{"detail": "Invalid page."}`, never a 500.
  - **Session authentication:** a logged-in website user can list books without a token, and the browsable API HTML page loads.
  - **Detail without a token:** 401, without the book's title.
- **Final results: 157 passed, 0 warnings** (125 earlier tests, 3 TDD tests, and 29 new tests).
- `ruff check .` passes, `ruff format --check .` reports all files formatted, `manage.py check` finds no issues, and `makemigrations --check --dry-run` reports no changes.

### Bugs and Fixes
- **Pagination warning (`UnorderedObjectListWarning`):** after behavior 2, pytest warned that the API list was paginated without an order, so a book could in theory appear on two pages. It was left until after behavior 3 to keep each GREEN change minimal. Fixed when the list started using `filter_books()`, which always orders, with the id as a tie-breaker. Confirmed: 0 warnings, and the API tests also pass with that warning turned into an error.
- **Two wrong test expectations (my test data, not the code):** two search cases expected `q="an"` to match "Anathem" and "Brave New World", but only "Anathem" contains "an". Both failed (`assert [] == ['Brave New World']` for the combined case). Fixed the tests to use `q="d"`, which really matches "Cloud Atlas" (Cloud, David) and "Brave New World" (World, Aldous). The code was correct and wasn't changed.

### Decisions
- All DRF settings live in `REST_FRAMEWORK` in `config/settings.py` rather than on each view, so every future API view gets the same login rule, 401 behavior, and pagination.
- Token is listed first so unauthenticated requests get 401 (with `WWW-Authenticate: Token`) instead of 403. Session is second so the browsable API works for website users.
- API URLs are in their own `books/api_urls.py` (namespace `api`), keeping the website's `books/urls.py` unchanged.
- Bad page values use DRF's standard 404 "Invalid page." response, as the PRD allows ("DRF's standard response instead of crashing"). No custom pagination class.
- The API reads parameters with `request.query_params` (DRF's name for `request.GET`).

### Manual Browser Testing Results
The student personally tested Phase 8. All checks passed (student-confirmed):

| # | Check | Result |
|---|---|---|
| 1 | Logged in as reader4, `GET /api/books/` | Passed: HTTP 200 with one saved book, Dune (ID 21), in DRF's paginated JSON format |
| 2 | `GET /api/books/21/` (reader4's own book) | Passed: HTTP 200 with Dune's correct details and no `user` field |
| 3 | Logged in as reader2, `GET /api/books/` | Passed: HTTP 200 with 11 saved books, paginated across two pages |
| 4 | Logged in as reader4, `GET /api/books/20/` (reader2's book) | Passed: HTTP 404, and no private information was exposed |
| 5 | Logged out, `GET /api/books/` | Passed: HTTP 401 Unauthorized with `WWW-Authenticate: Token` |
| 6 | Token authentication: a local PowerShell request with reader4's token | Passed: the request succeeded and returned a book count of 1 (no token value recorded) |
| 7 | Logged in as reader2, `GET /api/books/?q=Harry&status=want_to_read&sort=title` | Passed: HTTP 200 with 9 matching books |

### Phase 8 Checkpoint
- Phase 8 complete: automated checks pass and manual verification was approved by the student.
- Committed and pushed as the Phase 8 checkpoint (`feat: add token-authenticated API for listing saved books`).

### Next Steps
- Phase 9: API update and delete.

---

## Session 18: Phase 9, API Update and Delete

**Date:** November 15, 2026

### Prompts Used
- `/implement` Phase 9 of `plans/django-reading-list.md`, after re-reading the plan and the relevant documents and reviewing the API views, serializer, authentication, ownership rules, and API tests, stopping at each `/tdd` step for approval.
- Three `/tdd` behaviors:
  1. A valid `PATCH` updates only the allowed fields.
  2. Invalid values are rejected.
  3. `DELETE` removes only the authenticated user's book.
- **Conflict raised before any code:** the prompt said protected fields should be "rejected", but the approved plan (Phase 9, behavior 1), PRD story 57, and the decisions doc say Open Library fields are read-only and **ignored**. Two options were offered: **A**, ignore them (the approved design, DRF's built-in `read_only_fields`), or **B**, reject them with 400 (custom serializer code). **The student chose Option A.** Invalid status or rating values still return 400.
- Approved the behavior 1 test with one adjustment: add `"title": "Hacked"` to the `PATCH` and keep the check that the title is unchanged.
- Asked for the remaining normal tests (`POST`/`PUT` 405, `PATCH`/`DELETE` without a token 401, `PATCH` on another user's book 404 with the book unchanged), then this documentation, without committing.

### Work Completed
- **`books/api.py`:** `BookDetailAPIView` changed from `RetrieveAPIView` to `RetrieveUpdateDestroyAPIView`, with `http_method_names = ["get", "patch", "delete", "head", "options"]`. Leaving out `put` makes `PUT` return 405. The user-filtered `get_queryset()` is unchanged, so another user's book is 404 for every method. The docstring was updated.
- **`books/serializers.py`:** no change. Its existing `read_only_fields` already make DRF ignore Open Library fields, and `ModelSerializer` already applies the model's status choices and 1–5 rating validators.
- **No settings, URL, or migration changes.** `BookListAPIView` is still a `ListAPIView` (`GET` only), so `POST` to the list returns 405 and there is no create endpoint.
- **`CLAUDE.md`:** documents `PATCH` and `DELETE`, the ignored read-only fields (Option A), 400 for bad values, 404 for other users' books, 401 without a token for every method, and 405 for `POST` and `PUT`.

### TDD (3 behaviors)
1. **A valid `PATCH` updates only the allowed fields.** The test sends `{"status": "finished", "rating": 5, "notes": "Loved it.", "title": "Hacked"}` with a real token. RED: `assert 405 == 200`, because the detail view was a `RetrieveAPIView` (`GET` only). GREEN: `RetrieveUpdateDestroyAPIView` with `PUT` left out. The new values are returned and saved, while the title ("The Lord of the Rings"), the other Open Library fields, and the owner are unchanged.
2. **An invalid status or rating returns 400 and changes nothing** (5 cases: status `"abandoned"`, rating 0, rating 6, and two cases mixing a valid field with an invalid one). **Regression test, not a RED/GREEN cycle:** it passed on its first run, because the serializer already validates with the model's status choices and rating validators from Phase 2. The real error messages are `"abandoned" is not a valid choice.`, `Ensure this value is greater than or equal to 1.`, and `Ensure this value is less than or equal to 5.` The mixed cases prove the valid field isn't saved either.
3. **`DELETE` removes only the requesting user's book.** **Regression test, not a RED/GREEN cycle:** it passed on its first run, because behavior 1's switch to `RetrieveUpdateDestroyAPIView` also turned on `DELETE`, and the Phase 8 `get_queryset()` already returned 404 for other users' books. Deleting your own book gives 204 and the book is gone. Deleting another user's book gives 404, that book is unchanged, and its owner can still open it with their own token.

No working code was broken to force a failure for behaviors 2 or 3.

### Tests
- 6 more normal tests in `books/tests/test_api.py` (a `dune` fixture and an `assert_dune_unchanged()` helper prove rejected requests change nothing):
  - `POST /api/books/` with a token returns 405, and no book is created
  - `PUT /api/books/<id>/` with a token returns 405, and the book is unchanged
  - `PATCH` without a token returns 401, and the book is unchanged
  - `DELETE` without a token returns 401, and the book still exists
  - `PATCH` on another user's book returns 404, the response doesn't mention the title, and the book is unchanged
  - `PATCH {"rating": null, "notes": ""}` clears both (200), because the plan allows "rating 1–5 or null"
- All authenticated tests use real DRF tokens created inside the test. No token value is printed or recorded.
- All 6 passed on their first run with no application code changes.
- **Final results: 170 passed, 0 warnings** (157 earlier, plus 13 Phase 9 test cases: 1 + 5 + 1 TDD and 6 normal).
- `ruff check .` passes, `ruff format --check .` reports all files formatted, `manage.py check` finds no issues, and `makemigrations --check --dry-run` reports no changes.

### Bugs and Fixes
- No application bugs were found in Phase 9. Every test either reached a real RED (behavior 1) or passed on its first run, for the reasons explained above.

### Decisions
- **Option A (student-approved):** protected Open Library fields sent in a `PATCH` are ignored, not rejected, as in the approved PRD and plan. They can't be changed either way, and A needs no custom code.
- `PUT` is disabled through `http_method_names` instead of a custom method, so the view still uses DRF's built-in generic view.
- Invalid values use DRF's standard 400 response, with field-by-field error messages taken from the model's own rules.
- Another user's book is 404 (not 403) for every method, so the API never confirms that someone else's book exists.

### Manual Browser Testing Results
Phase 9 manual verification is complete. All checks passed. Sources:
- **Student-reported:** the student ran the check in the browser (browsable API or website) or in their own terminal, and reported the result.
- **Terminal (Claude):** Claude ran the check at the student's request against the student's running dev server. The script read reader4's token from the local database inside the script, and the token was never printed, logged, or saved.

| # | Check | Result | Source |
|---|---|---|---|
| 1 | reader4 PATCHes their own book, Dune (ID 21) | Passed: HTTP 200. Dune changed to Finished, 5 stars, notes "Updated via API" | Student-reported |
| 2 | PATCH with a protected `title` | Passed: HTTP 200, title stayed "Dune" | Student-reported |
| 3 | PATCH with an invalid status, and with an invalid rating | Passed: HTTP 400 | Student-reported |
| 4 | GET, PATCH, and DELETE on another user's book | Passed: HTTP 404 | Student-reported |
| 5 | DELETE reader4's own temporary book, The Hobbit (ID 22) | Passed: HTTP 204, and the website then showed only Dune (ID 21) | Student-reported |
| 6 | PATCH and DELETE without authentication | Passed: HTTP 401 | Student-reported |
| 7 | Authenticated PUT to `/api/books/21/` with body `{}` | Passed: HTTP 405. Dune still exists, all 10 fields unchanged | Terminal (Claude) |
| 8 | Authenticated POST to `/api/books/` with body `{}` | Passed: HTTP 405. No book created (20 saved books before and after, highest id 21), and reader4 still has only Dune (ID 21) | Terminal (Claude) |
| 9 | Token-authenticated PATCH to `/api/books/21/` with `{"status":"finished","rating":5,"notes":"Updated via API"}` | Passed: HTTP 200 with the expected values, no `user` field, protected fields unchanged. **Note:** Dune already had these values (from check 1), so this request confirmed the response but didn't visibly change anything | Terminal (Claude) |

No screenshots were captured during this session. The plan's suggested `09-api-patch.png` and `09-api-validation-error.png` are not recorded here.

### Phase 9 Checkpoint
- Phase 9 complete: automated checks pass and manual verification was approved by the student.
- Committed and pushed as the Phase 9 checkpoint (`feat: allow updating and deleting saved books through the API`).

### Next Steps
- Phase 10: script 2 (`api_script.py`).

---

## Session 19: Phase 10, Script 2 (`api_script.py`)

**Date:** November 15, 2026

### Prompts Used
- `/implement` Phase 10 of `plans/django-reading-list.md` with `/tdd`, after re-reading `CLAUDE.md`, `PROMPTS.md`, the PRD, the plan, and the skill instructions. Script 1 (`main.py`) was reviewed for style.
- The student asked for **only the first `/tdd` behavior** in this step (explain it, write a failing test, show RED, then write the minimum code for GREEN), then stop and report.
- Next prompt: **only `/tdd` behavior 2** (a successful run lists the books and updates one status), faking the token, the `GET` response with two books, the `input()` answers, and the `PATCH` response, then stop and report.
- Next prompt: **only `/tdd` behavior 3** (a `PATCH` 404 for ID 99 prints exactly `No book with ID 99 in your reading list.`, with no crash, no `Before:`/`After:` lines, and no real request), then stop and report.
- Next prompt: normal tests for **invalid user input only** (a non-numeric ID, a blank ID, an invalid status, a blank status): a friendly, specific message, no crash, and no `PATCH`. Write the tests first, confirm RED, then make the smallest change. 401, connection errors, empty lists, invalid JSON, and the URL override are left for later steps.
- Next prompt: **HTTP 401 only**, with mocked tests first for a 401 on the `GET` and a 401 on the `PATCH`. The requirements: a friendly token-rejected message, the token value never shown, no crash, no `Before:`/`After:` lines, no input or `PATCH` after a `GET` 401, and a graceful stop after a `PATCH` 401.
- Next prompt: **network connection errors only**, with mocked tests first for `requests.ConnectionError` on the `GET` and on the `PATCH`. The requirements: a friendly could-not-reach message that suggests checking the Django development server is running, no crash, the token never shown, no `Before:`/`After:` lines, no input or `PATCH` after a failed `GET`, and a graceful stop after a failed `PATCH`.
- Next prompt: **an empty reading list only**, with a mocked test first where the `GET` returns 200 with `{"count": 0, "next": null, "previous": null, "results": []}`. The requirements: a friendly empty-list message suggesting adding a book on the website, no ID or status questions, no `PATCH`, no crash, and no `Before:`/`After:` lines.
- Next prompt: **invalid JSON only**, with mocked tests first for a `GET` 200 whose `response.json()` raises a JSON decoding error, and the same for the `PATCH`. The requirements: a friendly invalid-response message, no crash, the token never shown, no `Before:`/`After:` lines, no input or `PATCH` after a bad list, and a graceful stop after a bad `PATCH`.
- Next prompt: **HTTP 500 only**, with mocked tests first for a 500 on the `GET` and on the `PATCH`. The requirements: a friendly server-error message suggesting the Django server terminal, no crash, the token never shown, no `Before:`/`After:` lines, no input or `PATCH` after a failed `GET`, a graceful stop after a failed `PATCH`, and the existing 401 and 404 messages kept.
- Next prompt: **request timeouts only**, with mocked tests first for `requests.Timeout` on the `GET` and on the `PATCH`. The requirements: a friendly timed-out message suggesting checking the Django development server, no crash, the token never shown, no `Before:`/`After:` lines, no input or `PATCH` after a `GET` timeout, a graceful stop after a `PATCH` timeout, and the 10-second timeout kept.
- Next prompt: **the `READING_LIST_API_URL` override only**, with mocked tests first: `http://localhost:9000` is used for both `GET` and `PATCH`, the default `http://127.0.0.1:8000` is used when it's not set, and outer spaces or a trailing slash are cleaned up. The auth header, the 10-second timeout, and all earlier behavior are kept, and the token is never shown.
- Next prompt: **the first-page issue only**. A mocked test first: the list shows IDs 12 and 7, the user enters `99` and `finished`, and the `PATCH` succeeds. The requirements: no crash, a clear explanation that the previous status wasn't on the displayed page, `After: finished`, no guessed status, no `Before: None`, and no extra API request.
- Next prompt: **unexpected HTTP 4xx errors only**, with mocked tests first for a 403 on the `GET` and a 400 on the `PATCH`. The requirements: a friendly rejected-request message that includes the status code, no crash, the token never shown, no `Before:`/`After:` lines, no input or `PATCH` after a failed `GET`, a graceful stop after a failed `PATCH`, and the specific 401, 404, and 5xx messages kept. `CLAUDE.md` and live verification are left for later.
- Next prompt: **documentation only** (no code or test changes). Review the finished `api_script.py` and `test_api_script.py`, update `CLAUDE.md` with concise Script 2 instructions, keep the existing guidance, and update this entry.
- Next prompt: **prepare for live verification** without running the status-changing `PATCH`. Check the server, find a safe test user and book, propose a different valid status, explain how to set `READING_LIST_TOKEN` privately, and record the preparation. No code, test, book, or token changes.
- Next prompt: record the **student-reported live verification results** (Dune 21: `finished` to `reading` and back), keeping student-reported results separate from terminal checks, without claiming any other manual error scenarios, then run all checks.
- Final prompt: the student confirmed that `READING_LIST_TOKEN` was removed from the PowerShell environment and approved the Phase 10 Git checkpoint. Review the changes, run all checks, stage the four Phase 10 files by name, and commit with `feat: add API reading list update script`.

### Work Completed
- **`api_script.py`** (new):
  - first a scaffold (an empty `main()` and the main guard), so the test could import the script and fail on an assertion instead of an import error
  - then the GREEN code: `get_token()` reads `READING_LIST_TOKEN` (spaces trimmed, `""` if unset), and `main()` prints `MISSING_TOKEN_MESSAGE` and stops when the token is missing
- **`test_api_script.py`** (new, at the root next to `test_main.py`):
  - a `sent_requests` fixture replaces `requests.get` and `requests.patch` with fakes that record any call and fail, so nothing can reach a real server
  - `input()` is also faked to fail, proving the script stops before asking anything
- **Behavior 2 additions to `api_script.py`:**
  - `DEFAULT_API_URL` (`http://127.0.0.1:8000`) and `TIMEOUT_SECONDS` (10)
  - `auth_headers()` builds `Authorization: Token <token>`
  - `list_books()` sends the `GET`, calls `raise_for_status()`, and returns `results` (`.get(..., [])`)
  - `update_status()` sends `PATCH {"status": ...}` and returns the updated book
  - `format_book()` builds a line like `[12] Dune - want_to_read`, using `.get()` defaults
  - `find_book()` finds the chosen book in the list, for the `Before:` value
  - `main()` lists the books with the "Showing the first page only" note, asks for the ID and status, sends the `PATCH`, and prints `Before:` (from the list) and `After:` (from the `PATCH` response)
- **Behavior 3 change to `api_script.py`:** `main()` wraps `update_status()` in `try/except requests.HTTPError`. A 404 prints `No book with ID <id> in your reading list.` and returns before any `Before:`/`After:` lines. Any other HTTP error is re-raised for now, to be handled by the planned 401 test.
- **Invalid input change to `api_script.py`:**
  - `STATUSES` lists the three codes
  - `book_id_error()` returns a message for a blank or non-numeric ID (`str.isdigit()`)
  - `status_error()` returns a message for a blank or unknown status, listing the allowed codes
  - `main()` checks the ID right after it's typed (and stops before asking for a status), then checks the status, so nothing is sent for bad input
- **401 change to `api_script.py`:**
  - `TOKEN_REJECTED_MESSAGE` says the token was rejected (HTTP 401), to check `READING_LIST_TOKEN`, and how to create a token. It never includes the token itself.
  - `http_status()` reads the status code from an `HTTPError`
  - `main()` catches a 401 from `list_books()` and stops before any input, and catches a 401 from `update_status()` next to the existing 404 check. The 404 check now also uses `http_status()`.
- **Connection error change to `api_script.py`:**
  - `cannot_reach_message(base_url)` says it couldn't reach the API at that address and to check that the Django development server is running (`uv run manage.py runserver`)
  - `main()` catches `requests.ConnectionError` around both `list_books()` and `update_status()`, prints the message, and stops
  - Only `ConnectionError` is caught, so timeouts and other request errors are still left for later steps
- **Empty list change to `api_script.py`:** `EMPTY_LIST_MESSAGE` ("Your reading list is empty." plus a suggestion to search for and save a book on the website). `main()` prints it and stops right after the list loads, if `results` is empty, before printing the list header or asking anything.
- **Invalid JSON change to `api_script.py`:** `invalid_response_message(base_url)` says the API returned an invalid response (not JSON) and to check that the reading list server is running at that address. `main()` catches `ValueError` around both `list_books()` and `update_status()`. `requests.JSONDecodeError` is a kind of `ValueError`, the same exception `main.py` and the Open Library service catch.
- **HTTP 500 change to `api_script.py`:**
  - `SERVER_ERROR_MESSAGE` says the API had a server error and to check the Django server terminal for details
  - `is_server_error()` is true for status 500 or higher
  - `main()` checks it in both `except requests.HTTPError` blocks, after the existing 401 and 404 checks, which are unchanged
- **Timeout change to `api_script.py`:**
  - `timed_out_message(base_url)` says the request timed out after `TIMEOUT_SECONDS` (10) seconds, shows the address, and asks the user to check that the Django development server is running and responding
  - `main()` catches `requests.Timeout` around both `list_books()` and `update_status()`
  - The `Timeout` block comes **before** the `ConnectionError` block, because `requests.ConnectTimeout` is both, and a connect timeout should get the timeout message
  - The 10-second timeout itself is unchanged
- **URL override change to `api_script.py`:** `get_api_url()` reads `READING_LIST_API_URL`, removes outer spaces and a trailing slash (`.strip().rstrip("/")`), and falls back to `DEFAULT_API_URL` if the result is empty. `main()` uses it as the one `base_url` for both requests and for the address shown in error messages.
- **First-page change to `api_script.py`:** when the `PATCH` succeeds for a book that wasn't in the displayed list (`find_book()` returned `None`), `main()` prints `Before: not available (book <id> is not on the first page shown above)` and then `After: ...`, instead of calling `.get()` on `None`. No extra request is made.
- **Other 4xx change to `api_script.py`:** `rejected_message(error)` builds `The API rejected the request (HTTP <code>).` plus "Check your input and token, then try again." The bare `raise` at the end of both `except requests.HTTPError` blocks in `main()` is replaced by printing that message and returning, so no HTTP error reaches the user as a traceback. The 401, 404, and 5xx checks come first and are unchanged.
- **`CLAUDE.md` (documentation step, no code or test changes):**
  - **Project structure:** now lists `test_api_script.py`.
  - **New "Script 2 (`api_script.py`)" section:**
    - purpose, and the run command (with the server running)
    - `READING_LIST_TOKEN` (required) and `READING_LIST_API_URL` (optional, default `http://127.0.0.1:8000`, cleaned up)
    - never commit, print, or document a real token
    - the flow: `GET` the first page, validated ID and status, `PATCH`, then `Before:`/`After:` ("not available" for a book not on the first page)
    - the token header and `timeout=10`
    - a summary of every handled error, and the function layout
  - **Testing requirements:** says `uv run pytest` includes the script 2 tests, and how they fake HTTP and `input()` with a fake token.
  - Everything already in `CLAUDE.md` was kept. The "Script 1 / Script 2" commands row and the Security rule about `READING_LIST_TOKEN` were already correct.
- **Behavior 2 additions to `test_api_script.py`:** a `FakeResponse` class (`status_code`, `json()`, `raise_for_status()`), a `TWO_BOOKS_PAGE` sample response, a `fake_inputs()` helper, and a clearly fake token string (`fake-test-token`).

### TDD (3 behaviors)
1. **A missing token prints the setup message and sends no request.** The test covers 3 cases: the variable unset, set to `""`, and set to `"   "`. RED (all 3): `AssertionError: assert 'READING_LIST_TOKEN is not set' in ''`, because the scaffold's `main()` printed nothing. GREEN: `get_token()` plus the early return in `main()`. The message tells the user to run `uv run manage.py drf_create_token <your-username>` and set the token in the terminal, not in a file. All 3 cases pass, no request is sent, and no input is asked for.
2. **A successful run lists the books, then shows `Before:` and `After:`.** The faked `GET` returns Dune (ID 12, `want_to_read`) and The Hobbit (ID 7, `reading`). The fake input picks `12` and `finished`, and the faked `PATCH` returns Dune as `finished`. The test checks:
   - the first-page note and both book lines
   - `Before: want_to_read` and `After: finished`
   - exactly one `GET` to `http://127.0.0.1:8000/api/books/`, then one `PATCH` to `.../api/books/12/` with `{"status": "finished"}`
   - the token header and `timeout=10` on both requests

   RED: `AssertionError: assert 'Showing the first page only' in ''`, because `main()` stopped after the token check. GREEN: `list_books()`, `update_status()`, and the rest of the flow in `main()`. The behavior 1 tests still pass.
3. **A `PATCH` 404 prints a friendly message.** The faked list is valid, the input is `99` and `finished`, and the faked `PATCH` returns 404. The test runs `main()` inside `try/except requests.RequestException` and calls `pytest.fail(...)` on a crash, so "no traceback" is a real check. It then checks:
   - the exact line `No book with ID 99 in your reading list.`
   - no `Before:` or `After:` lines
   - only the two faked requests (`GET` the list, `PATCH` `/api/books/99/`)

   RED: `Failed: The script crashed instead of showing a message: HTTPError('404 error')`. GREEN: the `try/except` around `update_status()` in `main()`. Behaviors 1 and 2 still pass.

### Tests
- **Invalid input (normal tests, 5 cases):** a parametrized test covers `abc` as the ID, a blank ID, `abandoned` as the status, and a blank status. Each checks the specific message, that no `PATCH` was sent, and no `Before:`/`After:` lines. A separate test checks that the status message lists `want_to_read, reading, finished`. The faked `PATCH` records calls and returns 404, so the old code finished without crashing and the tests failed on real assertions.
  - **RED (all 5):** the script sent the bad input to the API, and the faked 404 printed `No book with ID abc in your reading list.` (or `No book with ID  in your reading list.` for a blank ID) instead of a validation message.
  - **GREEN:** `book_id_error()`, `status_error()`, and the two checks in `main()`.
- **HTTP 401 (normal tests, 2):** a shared `run_without_crashing()` helper turns any `requests` error escaping `main()` into `pytest.fail(...)`.
  - **List 401:** checks the message, that `READING_LIST_TOKEN` is mentioned, that the fake token isn't printed, that `input()` is never called (faked to fail), that no `PATCH` is sent, and no `Before:`/`After:` lines.
  - **`PATCH` 401** (after a valid list and valid input): checks the message, that the fake token isn't printed, and no `Before:`/`After:` lines.
  - **RED (both):** `Failed: The script crashed instead of showing a message: HTTPError('401 error')`.
  - **GREEN:** `TOKEN_REJECTED_MESSAGE`, `http_status()`, and the two 401 checks in `main()`.
- **Connection errors (normal tests, 2):** a `refuse_connection()` fake raises `requests.ConnectionError("Connection refused")`.
  - **List unreachable:** checks the could-not-reach message, the "Django development server is running" hint, that the fake token isn't printed, that `input()` is never called, that no `PATCH` is sent, and no `Before:`/`After:` lines.
  - **`PATCH` unreachable** (after a valid list and valid input): checks the message, the hint, that the fake token isn't printed, and no `Before:`/`After:` lines.
  - **RED (both):** `Failed: The script crashed instead of showing a message: ConnectionError('Connection refused')`.
  - **GREEN:** `cannot_reach_message()` and the two `except requests.ConnectionError` blocks in `main()`.
- **Empty list (normal test, 1):** the faked `GET` returns the empty page. The faked `input()` records each prompt and returns `""`, so the old code didn't crash and the test failed on its own checks. It checks the message, that the website is mentioned, that no input was asked (`input_prompts == []`), that no `PATCH` was sent, and no `Before:`/`After:` lines.
  - **RED:** `AssertionError: assert 'Your reading list is empty.' in 'Your saved books (Showing the first page only):

Please enter a book ID.
'`. The script printed an empty list header and still asked for a book ID.
  - **GREEN:** `EMPTY_LIST_MESSAGE` and the `if not books:` check in `main()`.
- **Invalid JSON (normal tests, 2):** a `BadJSONResponse` fake (status 200) whose `json()` raises `requests.JSONDecodeError("Expecting value", "<html>Oops</html>", 0)`.
  - **Bad list response:** checks the invalid-response message, that the fake token isn't printed, that `input()` is never called, that no `PATCH` is sent, and no `Before:`/`After:` lines.
  - **Bad `PATCH` response** (after a valid list and valid input): checks the message, that the fake token isn't printed, and no `Before:`/`After:` lines.
  - **RED (both):** `Failed: The script crashed instead of showing a message: JSONDecodeError('Expecting value: line 1 column 1 (char 0)')`.
  - **GREEN:** `invalid_response_message()` and the two `except ValueError` blocks in `main()`.
- **HTTP 500 (normal tests, 2):** the faked response is `FakeResponse(500, "Server Error")`.
  - **List 500:** checks the server-error message, the "Django server terminal" hint, that the fake token isn't printed, that `input()` is never called, that no `PATCH` is sent, and no `Before:`/`After:` lines.
  - **`PATCH` 500** (after a valid list and valid input): checks the message, the hint, that the fake token isn't printed, and no `Before:`/`After:` lines.
  - **RED (both):** `Failed: The script crashed instead of showing a message: HTTPError('500 error')`.
  - **GREEN:** `SERVER_ERROR_MESSAGE`, `is_server_error()`, and the two checks in `main()`. The 401 and 404 tests still pass.
- **Timeouts (normal tests, 2):** each fake records the `timeout` argument it received, then raises `requests.Timeout("Read timed out.")`.
  - **List timeout:** checks the timed-out message, the "Django development server" hint, that the fake token isn't printed, that `timeout=10` was sent, that `input()` is never called, that no `PATCH` is sent, and no `Before:`/`After:` lines.
  - **`PATCH` timeout** (after a valid list and valid input): checks the message, the hint, that the fake token isn't printed, that `timeout=10` was sent, and no `Before:`/`After:` lines.
  - **RED (both):** `Failed: The script crashed instead of showing a message: Timeout('Read timed out.')`.
  - **GREEN:** `timed_out_message()` and the two `except requests.Timeout` blocks in `main()`.
- **`READING_LIST_API_URL` (normal test, 4 cases):** one parametrized test runs a full successful flow for each setting. It checks both request URLs, the token header and `timeout=10` on both, `After: finished`, and that the fake token isn't printed.
  - Cases: `http://localhost:9000`; not set; only spaces (`"   "`); and `"  http://localhost:9000/  "`, expected as `http://localhost:9000`.
  - **RED (2 of 4):** both "set" cases failed with `At index 0 diff: 'http://127.0.0.1:8000/api/books/' != 'http://localhost:9000/api/books/'`, because the script ignored the variable.
  - **Regression cases (2 of 4):** "not set" and "only spaces" passed on their first run, because the script already used the default URL. They're kept to protect the default.
  - **GREEN:** `get_api_url()` and `base_url = get_api_url()` in `main()`.
- **Book not on the first page (normal test, 1):** the list shows IDs 12 and 7, the input is `99` and `finished`, and the faked `PATCH` returns book 99 as `finished`. The test catches `AttributeError` and calls `pytest.fail(...)` on a crash. It checks `Before: not available`, the "not on the first page" explanation, `After: finished`, that `Before: None` is never printed, and that only one `GET` was made.
  - **RED:** `Failed: The script crashed instead of showing a message: AttributeError("'NoneType' object has no attribute 'get'")`.
  - **GREEN:** the `if before is None:` branch in `main()`.
  - The behavior 2 test (a book on the first page shows `Before: want_to_read`) and the behavior 3 test (404) still pass.
- **Other HTTP 4xx (normal tests, 2):**
  - **List 403:** checks `The API rejected the request (HTTP 403)`, that the fake token isn't printed, that `input()` is never called, that no `PATCH` is sent, and no `Before:`/`After:` lines.
  - **`PATCH` 400** (after a valid list and valid input): checks `The API rejected the request (HTTP 400)`, that the fake token isn't printed, and no `Before:`/`After:` lines.
  - **RED (both):** `Failed: The script crashed instead of showing a message: HTTPError('403 error')` and `HTTPError('400 error')`.
  - **GREEN:** `rejected_message()`, replacing both bare `raise` lines. The 401, 404, and 500 tests still pass.
- **198 passed:** 170 earlier, 5 for the three TDD behaviors, 5 invalid-input cases, 2 for 401, 2 for connection errors, 1 for the empty list, 2 for invalid JSON, 2 for HTTP 500, 2 for timeouts, 4 for the URL setting, 1 for a book not on the first page, and 2 for other 4xx. All earlier script tests still pass.
- `ruff check .` and `ruff format --check .` pass.
- Running `uv run api_script.py` without the token prints the setup message. No token was created, used, or recorded.

### Live Verification Preparation
Read-only checks; no book, user, or token was changed:
- **Server:** not running at preparation time. `GET http://127.0.0.1:8000/api/books/` couldn't connect.
- **Users:**

  | User | Saved books | Has a token |
  |---|---|---|
  | admin (staff) | 3 | no |
  | reader1 | 0 | no |
  | reader2 | 11 | no |
  | reader3 | 5 | no |
  | reader4 | 1 | yes |

  Only reader4 has a token. Only the fact that it exists was checked, never its value.
- **Proposed test book:** reader4's only book, **Dune (ID 21)**, currently `finished` (rating 5, notes "Updated via API"). It's the Phase 9 test book, and with one book it's always on the first page, so `Before:` will be shown.
- **Proposed change:** `finished` to **`reading`**, a different valid status, so the update is visible in the database and on `/books/`. Running the script again with `finished` afterwards restores Dune.
- **Private token setup (planned):** load reader4's existing token into `$env:READING_LIST_TOKEN` straight from the database with `uv run manage.py shell -v 0 -c ...`, capturing the output into the variable so it's never displayed. A test with a placeholder value confirmed that `-v 0` prints only the value (exactly one line). Then confirm it's set by showing only its length, and remove it afterwards with `Remove-Item Env:READING_LIST_TOKEN`.
- **Also planned:** the error checks from the plan (no token, a wrong token, the server stopped, ID `abc`, an ID that isn't reader4's, and status `done`) and a run with a user who has no books. reader1 has 0 books but no token, so that check needs a token created for reader1 by the student.

### Live Verification Results
**Sources:**
- **Student-reported:** the student ran the script against the running Django server, using reader4's existing token (set privately; its value was never displayed or recorded).
- **Terminal (Claude):** Claude ran the command directly in this session.

| # | Check | Result | Source |
|---|---|---|---|
| 1 | Run with reader4's token | Passed: listed Dune (ID 21), initially `finished` | Student-reported |
| 2 | Enter ID `21` and status `reading` | Passed: `Before: finished` / `After: reading` | Student-reported |
| 3 | Refresh `/books/` as reader4 | Passed: Dune shows the Reading badge, the Reading count is 1, and the Finished count is 0 | Student-reported |
| 4 | Run again with ID `21` and status `finished` (restore) | Passed: `Before: reading` / `After: finished` | Student-reported |
| 5 | `uv run api_script.py` with no `READING_LIST_TOKEN` (during behavior 1) | Passed: printed the setup message and sent no request | Terminal (Claude) |
| 6 | `uv run api_script.py` with a fake token and `READING_LIST_API_URL=localhost:9000` (during the 4xx step) | Printed the invalid-response message, not a traceback. No request was sent, because `requests` rejected the URL. | Terminal (Claude) |

Dune (ID 21) ends as `finished`, as it was before the live test. Afterwards the student confirmed that `READING_LIST_TOKEN` was removed from the PowerShell environment.

**Not verified yet:** the plan's other manual error checks (a wrong token, the server stopped, ID `abc`, an ID that isn't reader4's, status `done`, and a user with no books) have **not** been run against the live server. Rows 5–6 are the only terminal runs, and the automated tests cover all of these cases with mocked responses. No screenshots were recorded in this entry.

### Bugs and Fixes
- No application bugs so far.
- **Syntax error while editing (my mistake, fixed straight away):** the helper script that inserted `timed_out_message()` turned the `
` inside the message into a real line break, which broke the string. `pytest` and Ruff reported `invalid-syntax: f-string: unterminated string` at `api_script.py:90`. Fixed with an exact edit that restored `
`. All tests then passed and Ruff was clean. No test was changed.
- **Message wording caught before testing:** the first draft of the invalid-JSON message told the user to check `READING_LIST_API_URL`, but the script doesn't read that variable yet (the override is a later step). It was changed to name the address the script actually used, before the tests were run.
- **Lint issue in a test:** the first version of the behavior 3 test used `except Exception`, and Ruff reported `BLE001 Do not catch blind exception`. It now catches `requests.RequestException`, the kind of crash this test guards against. The test still showed RED for the same reason afterwards.

### Decisions
- Book lines show the status **code** (for example `want_to_read`), because that is what the user types at the status prompt.
- Bad input gets a message that says what's wrong:
  - **Blank ID:** "Please enter a book ID."
  - **Non-numeric ID:** `"abc" is not a valid book ID. Enter a number, like 12.`
  - **Blank status:** "Please enter a status. Choose one of: ..."
  - **Unknown status:** `"abandoned" is not a valid status. Choose one of: want_to_read, reading, finished`
- Server errors use "500 or higher" (`status >= 500`), not just 500, so a 502 or 503 from a proxy gets the same friendly message. It's the same single check.
- The script stops at the first bad answer: an invalid ID ends the run before the status question. The status check compares exact codes, as the plan asks ("one of the three codes").
- For a book that isn't on the displayed page, the script says the old status is "not available" instead of making an extra `GET` to look it up. That keeps the script to one list request and one `PATCH`, and never guesses.
- `READING_LIST_API_URL` set to only spaces counts as not set (default URL), the same way a blank `READING_LIST_TOKEN` counts as missing.
- **Remaining known limitation (wording only, no traceback):** a malformed `READING_LIST_API_URL` (for example `localhost:9000`, with no `http://`) makes `requests` raise `InvalidSchema`, `MissingSchema`, or `InvalidURL`. These were checked in the terminal. All three are `ValueError`s, so the existing `except ValueError` catches them and the script prints the invalid-response message instead of a traceback. That message ("not JSON") isn't precise for a bad URL, but it does show the URL that was used. All the error cases listed in the plan and the PRD are handled.
- **Correction in this step:** my first version of this note said a malformed URL would still show a traceback. A terminal check proved that wrong (all three URL errors are `ValueError`s), and the note was corrected before reporting.

### Phase 10 Checkpoint
- Phase 10 complete: all automated checks pass (198 tests), the live update was verified by the student, and the student approved the checkpoint.
- The plan's other manual error checks (a wrong token, the server stopped, ID `abc`, an ID that isn't reader4's, status `done`, a user with no books) were not run live. They are covered by the mocked automated tests.
- Committed and pushed with the student's message `feat: add API reading list update script` (the plan suggested `feat: add API script to list books and update reading status`).

### Next Steps
- Phase 11: documentation and final check.
