# Design Decisions: Django Reading List Application

**Date:** 2026-11-14
**Source:** `/grill-me` planning session (see `PROMPTS.md`, Session 6)
**Related:** `docs/research/api-options.md`, `prototypes/README.md`, `docs/plans/open-library-search-script.md` (script 1)

This document records the 22 decisions from the planning interview. It is the input for the PRD (`/to-prd`) and the phased implementation plan (`/prd-to-plan`).

## Assignment Scope (summarized by the student)

A 200-point Django project that:
- consumes an external API (Open Library) and provides its own API with Django REST Framework
- saves and manages data locally in SQLite
- includes authentication and access restrictions
- implements searching, Q objects, filtering, sorting, and pagination
- includes API research from official sources (done) and at least one prototype (done)
- includes two Python scripts: one for the external API (done: `main.py`) and one for our own API that lists records and updates a field
- includes a PRD, a phased implementation plan, `CLAUDE.md`, and `PROMPTS.md`
- uses automated tests, linting, formatting, and manual browser testing
- has separate Git commits for each implementation phase
- documents how to run the application and scripts
- ends with a reflection in the student's own words, with evidence and screenshots

## Decisions

### 1. Requirements source
Plan from the student's summary of the official requirements (above).

### 2. Interface
Django HTML templates styled with Bootstrap for users, plus a separate DRF API for scripts. No JavaScript frontend framework.

### 3. Data model
One model, `SavedBook`. Each row means "this user saved this book" and has a `ForeignKey` to Django's built-in `User`. A unique constraint on (`user`, `work_key`) prevents saving the same work twice.

### 4. Collections
No shelves. Each user has one reading list grouped by status: Want to Read, Reading, Finished.

### 5. Authors
One comma-joined `CharField` (for example, `"Terry Pratchett, Neil Gaiman"`). If the list is missing or empty, store `"Unknown author"`. This matches the `format_book()` rules.

### 6. Field rules

| Field | Type | Required | Rule |
|---|---|---|---|
| `user` | `ForeignKey(User)` | Yes | Set by the server, never from a form |
| `work_key` | `CharField` | Yes | For example, `/works/OL27448W`; unique with `user` |
| `title` | `CharField` | Yes | `"Unknown title"` if missing |
| `author` | `CharField` | Yes | Comma-joined, or `"Unknown author"` |
| `first_publish_year` | `IntegerField` | No | Blank allowed |
| `cover_id` | `IntegerField` | No | Blank allowed |
| `status` | `CharField` with choices | Yes | `want_to_read` / `reading` / `finished`; default `want_to_read` |
| `rating` | `IntegerField` | No | 1–5 (validators) |
| `notes` | `TextField` | No | Blank allowed |
| `created_at` | `DateTimeField` | Auto | `auto_now_add` |

Use built-in field options and validators wherever possible.

### 7. Editable fields
Only `status`, `rating`, and `notes` can be edited, on the website and through the API. Open Library fields are read-only after saving.

### 8. Website authentication and access
- Django's built-in login and logout, plus a sign-up page using `UserCreationForm`.
- **Public:** Home, Login, Sign up.
- **Login required:** Search Open Library, save, reading list, edit, delete. Logged-out visitors are redirected to Login (`LoginRequiredMixin`).
- Every book lookup is filtered by `user=request.user`. Another user's book returns **404**.

### 9. API authentication
- DRF `TokenAuthentication` listed **first**, then `SessionAuthentication`, so unauthenticated API requests return **401** (not 403) and the browsable API works when logged in.
- Tokens are created with `manage.py drf_create_token <username>`.
- Script 2 reads its token from `READING_LIST_TOKEN`. Tokens are never in code, docs, screenshots, or commits.
- If deployed, HTTPS is required.

### 10. API endpoints
| Method | URL | Purpose |
|---|---|---|
| `GET` | `/api/books/` | List the user's books (search, filter, sort, paginated) |
| `GET` | `/api/books/<id>/` | One book |
| `PATCH` | `/api/books/<id>/` | Update `status`, `rating`, `notes` |
| `DELETE` | `/api/books/<id>/` | Remove a book |

No create endpoint (books are saved on the website). The serializer marks the Open Library fields read-only and never exposes or accepts `user`. Other users' books return 404.

### 11. Where search, filter, and sort live
One shared helper, `filter_books(queryset, search, status, sort)`, used by both the website list view and the API list view. Pagination: Django `Paginator` on the website, DRF `PageNumberPagination` on the API.

### 12. Search, filter, sort, and pagination rules
- `q`: strip spaces; case-insensitive `Q(title__icontains=q) | Q(author__icontains=q)`; blank means no search.
- `status`: `want_to_read`, `reading`, or `finished`; blank or invalid means all statuses.
- `sort`: `title` (A→Z), `author` (A→Z), `newest` (default), `oldest`; invalid falls back to `newest`.
- All three combine. 10 per page on both the website and the API. Page links preserve `q`, `status`, and `sort`.
- Lowercase codes in the database; friendly labels on screen.

### 13. Open Library integration
A service module, `books/openlibrary.py`, separate from `main.py` (script 1 stays independent). It reuses the script 1 patterns: `title=` search, `fields=key,title,author_name,first_publish_year,cover_i`, `limit=10`, User-Agent `CIDM3312-BookSearch/1.0`, `timeout=10`, `raise_for_status()`, catching `RequestException` and `ValueError`, and `"Unknown title"`/`"Unknown author"`. Views never call `requests` directly. Formatting logic is testable without the internet.

### 14. Saving a search result
- Each result has a Save form (`POST`, CSRF-protected) with hidden fields: work key, title, author, year, cover ID.
- A Django form validates the data (including the work key format). Invalid or modified data is handled gracefully with a message, not a crash.
- The server sets `user` and the default status `want_to_read`. The user ID is never accepted from the form.
- Duplicates show a friendly message ("*Dune* is already in your reading list.").
- After saving, redirect to the same search results with a success message (Django messages framework).
- Books already saved show "In your list" instead of a Save button.

### 15. Open Library search page
| Situation | Page shows |
|---|---|
| First visit | Search box and button |
| Blank or spaces-only | "Please enter a book title." (no API call) |
| Results | "Found N matches. Showing the first M." plus up to 10 cards: cover thumbnail (or a "No cover" placeholder), title, authors, year (or "Year unknown"), Save button or "In your list" |
| Exactly 1 | Singular "1 match" |
| No results | `No books found for "<title>".` |
| Open Library error | Friendly alert; details go to the server log only |

Searches use `GET` (`/search/?title=...`) so they can be bookmarked. A "Data from Open Library" link appears in the footer.

### 16. Reading-list pages
| Page | URL | View |
|---|---|---|
| My Reading List | `/books/` | `ListView`: cards, sidebar (search, status, sort), 10 per page, Edit/Delete, empty-list message with a link to search |
| Edit Book | `/books/<id>/edit/` | `UpdateView`: read-only book info plus a status/rating/notes form; redirect to the list with a success message |
| Delete Book | `/books/<id>/delete/` | `DeleteView`: confirmation page with Delete/Cancel; deletes only on `POST`; redirect with a success message |

No separate detail page. All pages require login and are restricted to the user's own books (404 otherwise).

### 17. Prototype
Compared three Bootstrap layouts for My Reading List (`prototypes/reading-list-layouts.html`). **Chose Layout B: card grid + sidebar.** Final version: cleaner "No cover" placeholders, a sidebar that stacks above the cards on small screens, and the same style on every page. Full record: `prototypes/README.md`.

### 18. Project structure and tools
```
manage.py
config/        Django settings and root URLs
books/         the one app: models, views, forms, serializers, filters, openlibrary.py, templates
templates/     shared base layout and auth pages
main.py        script 1 (unchanged)
api_script.py  script 2
```
- Packages: `django`, `djangorestframework` (with `rest_framework.authtoken`). Bootstrap via CDN, so no frontend build tools.
- Dev tools: `pytest` + `pytest-django` (configured with the Django settings module), `ruff`. One command runs all tests: `uv run pytest`. Plain `assert` style.
- No extra packages or Django apps beyond these.

### 19. Script 2 (`api_script.py`)
- Interactive, like script 1. Small functions: `list_books()`, `update_status()`, `main()`, with the `__name__` guard.
- Token from `READING_LIST_TOKEN`, sent as `Authorization: Token <token>`. Base URL `http://127.0.0.1:8000`, overridable with `READING_LIST_API_URL`. `timeout=10`.
- Lists the **first page only** (up to 10 books) from the paginated response (`results`), showing ID, title, and status, and says that only the first page is shown.
- Asks for a book ID and a new status, validates both before sending, then `PATCH`es and prints **Before** (from the list data) and **After** (from the `PATCH` response).
- Handles: a missing token, a rejected token (401), the server not running, an empty list, an invalid ID, 404 (missing or not owned), an invalid status, network errors, and invalid JSON.
- Tests use pytest's built-in `monkeypatch` to fake API responses (no extra package, no running server).

### 20. Settings and secrets
- `SECRET_KEY` from `DJANGO_SECRET_KEY`, with a clearly fake development default. `DEBUG` from `DJANGO_DEBUG` (default `True`). `ALLOWED_HOSTS` from `DJANGO_ALLOWED_HOSTS` (default `localhost,127.0.0.1`). Standard library `os` only.
- **Safety check:** if `DEBUG` is False and `DJANGO_SECRET_KEY` is not set, raise `ImproperlyConfigured`, so production cannot silently use the fake key.
- Remove Django's generated key before the first commit. Keep `db.sqlite3` gitignored.
- The README documents the environment variables and deployment needs: HTTPS, a strong secret key, `DEBUG=False`, and correct `ALLOWED_HOSTS`.

### 21. Home page and admin
- **Logged out:** short introduction (track books you want to read, are reading, and have finished) with Sign Up and Log In buttons.
- **Logged in:** "Welcome back, <username>", buttons for Search Open Library and My Reading List, and counts of the user's own books by status.
- **Admin:** register `SavedBook` with `list_display` (title, user, status, rating, created_at), `list_filter` (status, created_at), and `search_fields` (title, author, user__username). Staff-only (Django default).
- Styled to match Layout B.

### 22. Authentication flow
| Action | Result |
|---|---|
| Sign up | Logged in automatically; redirect to Home; "Welcome, <username>! Your account was created." |
| Log in | Redirect to a safe `next` URL, otherwise My Reading List |
| Failed log in | Stay on Login with Django's built-in error |
| Log out | `POST` with CSRF (required by Django 5+); redirect to Home; "You have been logged out." |
| Logged-in user visits Login or Sign up | Redirect to My Reading List |

Built-in `LoginView` (with `redirect_authenticated_user=True`) and `LogoutView`, a small custom sign-up view, and `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and `LOGOUT_REDIRECT_URL` configured.

## Review: Contradictions and Open Items

Found during the final review. These need to be handled in the PRD or plan rather than left implicit.

1. **TDD scope vs. the `/tdd` limit.** The student asked for `/tdd` on many behaviors (model rules, `filter_books`, the Open Library service, saving/duplicates/ownership, search page, edit/delete, home counts, auth flow, and script 2). The `/tdd` skill allows **at most three behaviors per phase**. **Resolution:** the phased plan should spread these across phases (≤3 per phase), and cover the rest with normal tests written in the same phase.
2. **Sidebar filters without JavaScript.** In the prototype, choosing a status or sort applied instantly using JavaScript. **Resolved (approved 2026-11-14):** the sidebar is one normal `GET` form with an **Apply** button. No JavaScript is used for filtering.
3. **What the sidebar status counts mean.** **Resolved (approved 2026-11-14):** the status counts cover the logged-in user's **entire** reading list, not the currently filtered results, matching the Home page counts.
4. **User-Agent contact info.** Open Library asks apps that make "multiple calls per minute" to include contact details in the User-Agent. The student chose a name-only User-Agent to keep personal info out of the public repo. That is reasonable for a locally run class project with one request per search, but it should be noted as a known limitation, along with the 1 request/second rate limit.
5. **Mocking for script 2 vs. the script 1 decision.** Script 1 avoided mocking as too advanced. Script 2 will use pytest's `monkeypatch`. This is a deliberate change, not a contradiction: script 2's behavior depends on API status codes (401/404) that can't be tested reliably without faking responses.
6. **Version check.** The project pins Python 3.14. The Django version installed must support Python 3.14. Verify this when adding Django.
7. **Work key validation pattern.** The save form must validate the work key format (for example, `/works/OL<digits>W`). The exact pattern is to be finalized in the PRD.

No contradictions were found between the 22 decisions themselves. Items 1 and 4–7 carry forward into the PRD and the implementation plan.
