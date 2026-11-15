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
