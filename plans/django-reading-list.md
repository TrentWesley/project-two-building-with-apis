# Plan: Personal Reading List (Django + DRF)

> Source PRD: `prd/django-reading-list.md` (approved 2026-11-14)
> Design decisions: `docs/plans/django-reading-list-decisions.md` · Prototype: `prototypes/README.md` · Research: `docs/research/api-options.md`
> Status: **Approved by the student (2026-11-14).** 11 implementation phases, plus Phase 0 for `CLAUDE.md`.

**About file names:** the "Expected files" lists show where work is *likely* to land, so each phase's scope is clear. Names the PRD and decisions fix (`config/`, `books/`, `templates/`, `api_script.py`, `SavedBook`, URL paths) are durable. Other file names may change during implementation, and that's fine as long as the acceptance criteria are met.

---

## Architectural decisions

Durable decisions that apply across all phases:

- **Project layout:** `manage.py` at the repo root. `config/` holds the Django project (settings, root URLs). **One app, `books`**, owns everything: model, website views, forms, the shared filtering helper, the Open Library service module, the API serializer and views, the admin, and app templates. Project-level `templates/` holds the base layout, the home page, and the auth pages. `main.py` (script 1) is unchanged. `api_script.py` (script 2) is at the repo root.
- **URLs** (the website uses the `books` app namespace):

  | Path | Purpose | Access |
  |---|---|---|
  | `/` | Home | Public |
  | `/accounts/signup/` | Sign up | Public (logged-in users redirected to `/books/`) |
  | `/accounts/login/` | Log in (built-in `LoginView`) | Public (logged-in users redirected to `/books/`) |
  | `/accounts/logout/` | Log out (built-in `LogoutView`, `POST` only) | Logged in |
  | `/search/?title=...` | Search Open Library | Login required |
  | `/books/save/` | Save a search result (`POST` only) | Login required |
  | `/books/?q=&status=&sort=&page=` | My Reading List | Login required |
  | `/books/<id>/edit/` | Edit status/rating/notes | Owner only (404 otherwise) |
  | `/books/<id>/delete/` | Delete confirmation (deletes on `POST`) | Owner only (404 otherwise) |
  | `/api/books/` | API list (`GET`) | Token or session |
  | `/api/books/<id>/` | API detail (`GET`, `PATCH`, `DELETE`; **`PUT` disabled**) | Token or session, owner only (404 otherwise) |
  | `/admin/` | Django admin | Staff only |

  Integer primary keys (`<id>`), with no slugs.
- **Model:** `SavedBook` with a `ForeignKey` to Django's built-in `User` (`on_delete=CASCADE`). Fields: `work_key`, `title`, `author`, `first_publish_year` (optional), `cover_id` (optional), `status` (`want_to_read` / `reading` / `finished`, default `want_to_read`), `rating` (optional, 1–5), `notes` (optional), `created_at` (auto). A unique constraint on (`user`, `work_key`). One initial migration in Phase 2. Later phases should not need model changes.
- **Work key format:** `/works/OL`, then one or more digits, then `W`, with nothing else.
- **Authentication and authorization:**
  - **Website:** Django sessions, `LoginRequiredMixin` on protected views, and every book lookup filtered by `request.user` (404 for others). Settings for `LOGIN_URL`, `LOGIN_REDIRECT_URL` (`/books/`), and `LOGOUT_REDIRECT_URL` (`/`).
  - **API:** DRF `TokenAuthentication` **first**, then `SessionAuthentication` (so unauthenticated requests get 401). `IsAuthenticated` on all endpoints, and querysets limited to the requesting user.
- **Shared filtering helper:** one function in `books` takes (queryset, search, status, sort). It's used by the website list (Phase 5) and the API list (Phase 8). Parameters are `q`, `status`, `sort`, and `page`. Page size is 10 everywhere.
- **Open Library access:** only through the `books` service module (Phase 3). Views and tests never call the real API.
- **Settings:** `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` from environment variables. A fake dev key is used only when `DEBUG` is on, and startup fails if `DEBUG` is off with no key.
- **Frontend:** Django templates with Bootstrap 5 from a CDN, in Layout B (dark navbar, card grid + sidebar, status badges). No JavaScript for filtering.
- **Feedback:** Django messages framework, shown as Bootstrap alerts in the base layout.

## Commands

| Purpose | Command |
|---|---|
| Install / sync dependencies | `uv sync` |
| Run all tests (scripts + Django) | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format check | `uv run ruff format --check .` |
| Apply formatting (only when the check fails) | `uv run ruff format .` |
| Create / apply migrations | `uv run manage.py makemigrations` · `uv run manage.py migrate` |
| Check migrations are up to date | `uv run manage.py makemigrations --check --dry-run` |
| Run the dev server | `uv run manage.py runserver` → http://127.0.0.1:8000 |
| Create an admin user | `uv run manage.py createsuperuser` |
| Create an API token | `uv run manage.py drf_create_token <username>` |
| Run script 1 | `uv run main.py` |
| Run script 2 | `uv run api_script.py` (with `READING_LIST_TOKEN` set) |

## Standard phase workflow

Every phase follows the same steps:

1. **Start** with `/implement`, naming the phase (for example, "Phase 3 of `plans/django-reading-list.md`").
2. **`/tdd`:** `/implement` invokes it. Confirm the phase's **at most 3** TDD behaviors (listed below), and approve each test at RED and each implementation at GREEN.
3. **Build the rest** of the phase's acceptance criteria with normal tests written in the same phase.
4. **Automated checks:** `uv run pytest`, `uv run ruff check .`, and `uv run ruff format --check .` must all pass. From Phase 2 on, `makemigrations --check` must report no changes.
5. **Manual browser verification:** the student runs the phase's checklist and confirms it passes. Nothing is committed before that confirmation.
6. **Docs:** update `PROMPTS.md` (prompts, decisions, **actual bugs and fixes**, test results). Update `CLAUDE.md` if commands, structure, or conventions changed.
7. **Commit and push:** one commit per phase, staging files by name. Never commit `.venv/`, `db.sqlite3`, tokens, or secrets.

**Evidence rule (every phase):** save screenshots to `docs/screenshots/` using the names suggested in each phase. Screenshots must never show a token or password. Record every real bug (what happened, the error or failing test, and the fix) in that phase's `PROMPTS.md` entry.

## Phase dependencies

```
Phase 0 (CLAUDE.md)
  └─ 1 Skeleton & accounts
       └─ 2 SavedBook & basic list
            ├─ 3 Search Open Library ── 4 Save from search
            ├─ 5 Filter/sort/paginate list ─┐
            ├─ 6 Edit & delete              │
            ├─ 7 Logged-in Home             │
            └─ 8 API list & detail ◄────────┘ (reuses the Phase 5 helper)
                 └─ 9 API update & delete
                      └─ 10 Script 2
                           └─ 11 Docs & final check (needs everything)
```

Phases run in numeric order. Phases 3–7 depend only on Phase 2 (plus 4 on 3), so their order could change if needed. Phase 8 needs Phase 5's helper. Phase 10 needs Phase 9's `PATCH`.

---

## Phase 0: Prepare CLAUDE.md (before any Django code)

**User stories:** none (assignment requirement).

### What to build
A `CLAUDE.md` at the repo root that gives future Claude Code sessions the project's context:
- the project summary
- the stack (Python 3.14, uv, Django, DRF, pytest + pytest-django, Ruff, Bootstrap via CDN)
- the folder layout and the architectural decisions above
- the commands table
- the standard phase workflow (`/implement`, `/tdd` limit, checks, manual verification, `PROMPTS.md`, one commit per phase)
- security rules (no secrets, tokens, or passwords in code, docs, screenshots, or commits; stage files by name)
- pointers to the PRD, this plan, the decisions doc, and the research

It also states that script 1 (`main.py`) is finished and must stay independent.

### Expected files
`CLAUDE.md` (new), `PROMPTS.md`.

### Acceptance criteria
- [ ] `CLAUDE.md` matches the approved PRD and this plan, without inventing anything new.
- [ ] It contains no secrets or personal contact details.
- [ ] `PROMPTS.md` records the session.

### Commit checkpoint
`docs: add CLAUDE.md for the reading list project`

---

## Phase 1: Project skeleton and accounts

**User stories:** 1–12, 51, 68, 69

### What to build
- Add Django, DRF, and pytest-django with uv, after **verifying in the official release notes or compatibility tables that the chosen Django and DRF versions support Python 3.14** (record the versions and the source in `PROMPTS.md`).
- Create the `config` project and the `books` app. Configure pytest-django so `uv run pytest` runs the existing script 1 tests and the new Django tests.
- Settings come from environment variables. Remove the generated secret key before the first commit. Add the production safety check. Confirm `db.sqlite3` is gitignored.
- The base layout follows Layout B: dark navbar (brand, and Log in/Sign up or username + Log out `POST` button), a message alert area, and a footer with the "Data from Open Library" link.
- Home page, logged-out view: intro text plus Sign Up and Log In buttons. (The logged-in view comes in Phase 7. For now, logged-in users just see a simple welcome.)
- Sign up (`UserCreationForm`, logs in automatically, redirects to Home with a welcome message), login (built-in, safe `next`, otherwise `/books/`), and logout (`POST`, redirects to Home with "You have been logged out."). Logged-in users are redirected away from Login and Sign up.
- `/books/` exists as a login-required placeholder page so that login redirects and `next` can be tested. Phase 2 replaces it.

### Expected files
`pyproject.toml`, `uv.lock`, `manage.py`, `config/` (settings, urls, wsgi, asgi), `books/` (app config, views, urls, tests), `templates/base.html`, `templates/home.html`, `templates/registration/login.html`, `templates/registration/signup.html`, `CLAUDE.md` (commands), `PROMPTS.md`.

### `/tdd` behaviors (3)
1. With `DEBUG` off and no `DJANGO_SECRET_KEY`, the settings refuse to load (`ImproperlyConfigured`).
2. A successful sign-up creates the user, logs them in, and redirects to Home.
3. Logout only works by `POST`, logs the user out, and redirects to Home.

### Other tests required
- Home loads for anonymous users and shows Sign Up and Log In.
- Login with a valid `next` redirects there. Without `next`, it goes to `/books/`. A failed login stays on the page with an error.
- Logged-in users visiting Login or Sign up are redirected to `/books/`.
- An anonymous user visiting `/books/` is redirected to Login with `next`.
- The existing 5 script 1 tests still pass.

### Manual browser verification
1. Run the server and open `/`. The intro and both buttons appear, styled with Bootstrap.
2. Sign up a new user. You're logged in automatically, land on Home, and see the welcome message.
3. Log out using the navbar button. You land on Home with "You have been logged out."
4. Log in with the wrong password (error shown), then the right one (you land on `/books/`).
5. While logged in, visit `/accounts/login/` and `/accounts/signup/`. Both redirect to `/books/`.
6. Log out and visit `/books/`. You're redirected to Login. Log in, and you return to `/books/`.
7. Narrow the window to phone width. The navbar and pages remain usable.

### Evidence to collect
Screenshots: `01-home-logged-out.png`, `01-signup.png`, `01-login-error.png`, `01-logged-out-message.png`. Record the Django and DRF versions chosen and how compatibility was verified.

### Commit checkpoint
`feat: add Django project skeleton and user accounts`

---

## Phase 2: SavedBook model and basic reading list

**User stories:** 13, 34, 35, 67

### What to build
- The `SavedBook` model exactly as described in the architectural decisions (choices, default, 1–5 validators, `created_at`, the unique constraint, cascade delete) and its initial migration.
- Admin registration with `list_display` (title, user, status, rating, created_at), `list_filter` (status, created_at), and `search_fields` (title, author, user__username).
- `/books/` replaces the placeholder: a `ListView` showing **only the logged-in user's** books as Layout B cards (cover or a clean "No cover" placeholder, title, author, status badge, stars or "Not rated"), newest first. Empty list: "Your reading list is empty. Search Open Library to add books." with a link to `/search/` (the link works from Phase 3 on). The sidebar and pagination come in Phase 5. Edit and Delete buttons come in Phase 6.
- Books are added through the admin for now, which is how this phase is demonstrated.

### Expected files
`books/models.py`, `books/migrations/0001_initial.py`, `books/admin.py`, `books/views.py`, `books/urls.py`, `books/templates/books/` (list template), `books/tests/`, `PROMPTS.md`.

### `/tdd` behaviors (3)
1. Saving the same `work_key` twice for the same user is rejected, but two different users can each save it.
2. A rating outside 1–5 fails validation, and a blank rating is allowed.
3. `/books/` shows only the logged-in user's books.

### Other tests required
- Defaults: a new book has status `want_to_read` and `created_at` set.
- Deleting a user deletes their books.
- The empty-list message appears when the user has no books.
- `makemigrations --check` reports no changes.

### Manual browser verification
1. `createsuperuser`, then log into `/admin/` and add 2–3 books for yourself (use real work keys and cover IDs from the prototype data) and 1 book for a second user.
2. In the admin, check the columns, the status and date filters, and search by title, author, and username.
3. As yourself, open `/books/`. Only your books appear, as cards, and a book without a cover shows the placeholder.
4. Log in as the second user. You see only their book. Remove all books from a user and check the empty message.
5. Try adding a duplicate work key for the same user in the admin. It's rejected.

### Evidence to collect
Screenshots: `02-admin-savedbook.png`, `02-reading-list-cards.png`, `02-empty-list.png`.

### Commit checkpoint
`feat: add SavedBook model, admin, and basic reading list`

---

## Phase 3: Search Open Library

**User stories:** 18–27

### What to build
- The Open Library service module: title search, `fields=key,title,author_name,first_publish_year,cover_i`, `limit=10`, the `CIDM3312-BookSearch/1.0` User-Agent, `timeout=10`, `raise_for_status()`. `RequestException` and `ValueError` become a single "unavailable" result, with details logged. Raw results become clean records (`work_key`, title or "Unknown title", authors comma-joined or "Unknown author", year or none, cover ID or none) plus the total `numFound`.
- `/search/` (login required, `GET`): the first visit shows the form. Blank or spaces-only shows "Please enter a book title." with no call. Otherwise "Found N matches. Showing the first M." (singular for 1), with up to 10 Layout B cards (cover thumbnail or placeholder, title, authors, year or "Year unknown"). No results: `No books found for "<title>".` Unavailable: a friendly red alert. The navbar link becomes active. No Save buttons yet.

### Expected files
`books/openlibrary.py` (service module), `books/views.py`, `books/urls.py`, `books/templates/books/` (search template), `books/tests/`, `PROMPTS.md`.

### `/tdd` behaviors (3)
1. Converting raw Open Library results gives clean records, including Unknown title, Unknown author for missing or empty lists, joined authors, and missing year or cover.
2. A blank or spaces-only search shows "Please enter a book title." and never calls the service.
3. When the service reports "unavailable", the page shows the friendly alert (HTTP 200, no traceback, no technical details).

### Other tests required
- The search page requires login.
- Results with the service faked: the total line, singular wording for 1 match, the no-results message.
- The service module turns a faked `requests` exception and invalid JSON into "unavailable" (`monkeypatch`, no network).
- No test calls the real Open Library.

### Manual browser verification
1. Search `dune`: the total and 10 cards with covers appear.
2. Search `the relentless moon`: "Found 1 match."
3. Search `xyzqqnotabook`: the no-results message with your search term.
4. Search blank, then spaces only: "Please enter a book title."
5. Simulate an outage (temporarily start the server with `HTTPS_PROXY=http://127.0.0.1:9`): the friendly alert appears, and the details are only in the server console. **Remove the proxy setting afterward and confirm it's cleared.**
6. Bookmark or refresh a search URL. The same results appear.
7. Check phone width.

### Evidence to collect
Screenshots: `03-search-results.png`, `03-search-one-match.png`, `03-search-no-results.png`, `03-search-unavailable.png`.

### Commit checkpoint
`feat: add Open Library search page`

---

## Phase 4: Save from search

**User stories:** 28–33

### What to build
- Each search result card has a Save form (`POST` to `/books/save/`, CSRF) with hidden work key, title, author, year, and cover ID, plus a hidden "return to" search URL (only a safe, same-site URL is accepted).
- A Django form validates the work key format, a required title and author, and integer-or-blank year and cover. The view sets `user=request.user` and the status `want_to_read`, and never reads a user from the form.
- Success: redirect to the same search results with "Saved *<title>* to your reading list." A duplicate shows "*<title>* is already in your reading list." and creates nothing. Invalid or tampered data shows a friendly error message and redirects, never a 500.
- Search results the user has already saved show an "In your list" label instead of Save (one query for the user's saved work keys).

### Expected files
`books/forms.py`, `books/views.py`, `books/urls.py`, `books/templates/books/` (search template), `books/tests/`, `PROMPTS.md`.

### `/tdd` behaviors (3)
1. A valid save creates a `SavedBook` owned by the logged-in user, with status `want_to_read`, and redirects back with a success message.
2. Saving a book the user already has shows the duplicate message and creates no second row.
3. An invalid work key (or another invalid field) is rejected with a friendly message and no new row.

### Other tests required
- Save requires login and `POST` (`GET` is not allowed).
- A `user` value submitted in the form is ignored.
- An unsafe "return to" URL falls back to `/search/`.
- Already-saved results show "In your list" instead of a Save button.

### Manual browser verification
1. Search `dune`, then save *Dune*. You return to the same results with the success message, and *Dune* now shows "In your list."
2. Open `/books/`. *Dune* is there as Want to Read.
3. Use the browser's back button to resubmit the save form. You see the duplicate message, and the list still has one *Dune*.
4. Using the browser's developer tools, change a hidden work key to `abc` and submit. You see the friendly error, and nothing is saved.
5. Save a book with no cover, then check its placeholder in the list.

### Evidence to collect
Screenshots: `04-save-success.png`, `04-in-your-list.png`, `04-duplicate-message.png`.

### Commit checkpoint
`feat: save Open Library search results to the reading list`

---

## Phase 5: Search, filter, sort, and paginate my list

**User stories:** 36–43, 50

### What to build
- The shared filtering helper (Q-object search on title OR author, case-insensitive, stripped; status filter with blank or unknown meaning all; sort by `title`/`author`/`newest`/`oldest` with unknown falling back to `newest`).
- The `/books/` sidebar (Layout B): one `GET` form with a search box (`q`), status radio buttons with **whole-list** counts, a sort dropdown, and an **Apply** button. Current values are kept in the form.
- Pagination: 10 per page (Django `Paginator` / `ListView` pagination), Bootstrap page links that keep `q`, `status`, and `sort`. Invalid or out-of-range `page` values show a valid page instead of an error. A "no books match" message appears when filters exclude everything (separate from the empty-list message).
- Responsive: the sidebar stacks above the cards on small screens, with one card per row on phones.

### Expected files
`books/filters.py` (shared helper), `books/views.py`, `books/templates/books/` (list template and pagination partial), `books/tests/`, `PROMPTS.md`.

### `/tdd` behaviors (3)
1. Search matches title OR author, ignoring capitalization and surrounding spaces. A blank search returns everything.
2. An unknown or blank status returns all statuses, and a valid status filters.
3. An unknown sort falls back to newest first, and each valid sort orders correctly.

### Other tests required
- Search, status, and sort combined.
- 11 books → page 1 has 10 and page 2 has 1. Page links keep `q`, `status`, and `sort`.
- `?page=abc` and `?page=999` don't error.
- Sidebar counts reflect the whole list, even while filtered.
- "No books match" vs. "empty list" messages.

### Manual browser verification
1. Save (or add in the admin) at least 11 books with mixed statuses.
2. Search `le guin` (or a word in one author's name). Only matching titles or authors appear, and capitalization doesn't matter.
3. Filter to Finished, then sort by Title A–Z, and click Apply.
4. Go to page 2. The search, filter, and sort are still applied.
5. Edit the URL to `?sort=banana`, `?status=xyz`, `?page=abc`, and `?page=999`. Each one loads without an error.
6. Check that the counts don't change when filtering.
7. Check phone width: the sidebar is above the cards, with one card per row.

### Evidence to collect
Screenshots: `05-list-filtered-sorted.png`, `05-list-page-2.png`, `05-list-mobile.png`, `05-no-matches.png`.

### Commit checkpoint
`feat: add search, filter, sort, and pagination to the reading list`

---

## Phase 6: Edit and delete books

**User stories:** 14, 44–49

### What to build
- Edit and Delete buttons on each list card.
- `/books/<id>/edit/` (`UpdateView`): read-only cover, title, author, and year shown above a form with **only** status, rating (blank or 1–5), and notes. On success: redirect to `/books/` with "Updated *<title>*."
- `/books/<id>/delete/` (`DeleteView`): a `GET` shows "Remove *<title>* from your reading list?" with Delete (`POST`) and Cancel. On success: redirect to `/books/` with "Removed *<title>*."
- Both views look up books in the current user's queryset only, so other users' books return 404.

### Expected files
`books/forms.py`, `books/views.py`, `books/urls.py`, `books/templates/books/` (edit and delete templates, list card buttons), `books/tests/`, `PROMPTS.md`.

### `/tdd` behaviors (3)
1. Editing changes status, rating, and notes, and ignores any submitted title, author, year, cover, work key, or user.
2. Another user's book returns 404 on both the edit and delete URLs, for `GET` and `POST`.
3. A `GET` on the delete URL only shows the confirmation, and the book is deleted only on `POST`.

### Other tests required
- Both pages require login.
- A rating of 0 or 6 is rejected with a form error.
- Success messages and redirects for edit and delete.

### Manual browser verification
1. Edit a book: change the status to Reading, the rating to 4, and add notes. Save. You see the message, and the card shows the changes.
2. Try a rating of 6 (via developer tools or the form). You get a validation error.
3. Click Delete, then Cancel. The book is still there. Delete again and confirm. You see the message, and the book is gone.
4. As user B, paste user A's edit and delete URLs. Both return 404.

### Evidence to collect
Screenshots: `06-edit-page.png`, `06-delete-confirm.png`, `06-other-user-404.png`.

### Commit checkpoint
`feat: add edit and delete pages for saved books`

---

## Phase 7: Logged-in Home page

**User stories:** 15–17

### What to build
For logged-in users, Home shows "Welcome back, <username>", buttons for Search Open Library and My Reading List, and counts of **their own** books for Want to Read, Reading, and Finished (zeros shown). The logged-out view is unchanged. It's styled consistently with Layout B.

### Expected files
`books/views.py` (or the home view's location), `templates/home.html`, `books/tests/`, `PROMPTS.md`.

### `/tdd` behaviors (2)
1. The status counts on Home include only the logged-in user's books.
2. Logged-in users see the welcome message and quick links, and logged-out users see the intro and the Sign Up/Log In buttons.

### Other tests required
- Counts show 0 for statuses with no books.

### Manual browser verification
1. Log in as a user with mixed statuses. The counts match `/books/` filtered by each status.
2. Log in as another user. You see different counts.
3. Log out. You see the intro view.

### Evidence to collect
Screenshots: `07-home-logged-in.png`.

### Commit checkpoint
`feat: show welcome and status counts on the home page`

---

## Phase 8: API: authentication, list, and detail

**User stories:** 52–55, 59, 60

### What to build
- Enable `rest_framework` and `rest_framework.authtoken` (migration). DRF settings: `TokenAuthentication` then `SessionAuthentication`, `IsAuthenticated`, and page-number pagination with a page size of 10.
- The serializer exposes `id`, `work_key`, `title`, `author`, `first_publish_year`, `cover_id` (all read-only), `status`, `rating`, `notes`, and `created_at`. It never exposes `user`.
- `GET /api/books/` (the user's books via the shared helper, using `q`, `status`, `sort`, and `page`) and `GET /api/books/<id>/` (404 for other users). The browsable API works when logged into the website.

### Expected files
`config/settings.py`, `config/urls.py`, `books/serializers.py`, `books/api.py` (or API views in `books`), `books/urls.py` or a separate API URL module, `books/tests/`, `CLAUDE.md` (token command), `PROMPTS.md`.

### `/tdd` behaviors (3)
1. A request without a token, or with an invalid one, gets **401**.
2. With a valid token, the list contains only the user's books in DRF's paginated format (`count`, `next`, `previous`, `results`), 10 per page.
3. A detail request for another user's book returns 404.

### Other tests required
- `q`, `status`, and `sort` on the API behave the same as on the website (shared helper).
- The serializer output has no `user` field.
- A session-authenticated request (logged-in client) can list books.

### Manual browser verification
1. Logged in on the website, open `/api/books/`. The browsable API shows your books, paginated, and `?status=finished&sort=title` works.
2. Open `/api/books/<id>/` for your book (works) and for another user's book (404).
3. Log out and open `/api/books/`. You get an authentication error.
4. Create a token with `drf_create_token`. In a terminal, call the API with and without the `Authorization: Token ...` header and compare the 200 and 401 responses. **Don't paste the token into `PROMPTS.md` or screenshots.**

### Evidence to collect
Screenshots: `08-browsable-api-list.png`, `08-api-401.png` (token hidden).

### Commit checkpoint
`feat: add token-authenticated API for listing saved books`

---

## Phase 9: API: update and delete

**User stories:** 56–58

### What to build
- `PATCH /api/books/<id>/` updates `status`, `rating`, and/or `notes`, with validation (status choices, rating 1–5 or null). Open Library fields stay read-only.
- `DELETE /api/books/<id>/` removes the user's own book (204). Both actions return 404 for other users' books.
- No create (`POST` to the list returns 405).
- **`PUT` is disabled (approved 2026-11-14):** `PUT /api/books/<id>/` returns 405. Only `PATCH` (partial updates to status, rating, and notes) can change a book.

### Expected files
`books/api.py` (or API views), `books/serializers.py`, `books/tests/`, `PROMPTS.md`.

### `/tdd` behaviors (3)
1. `PATCH` changes status, rating, and notes, while submitted Open Library fields are ignored and unchanged.
2. An invalid status or a rating outside 1–5 returns 400 and changes nothing.
3. `DELETE` removes only the requesting user's book, and another user's book returns 404 and is not deleted.

### Other tests required
- `POST /api/books/` returns 405.
- `PUT /api/books/<id>/` returns 405.
- `PATCH` without authentication returns 401.

### Manual browser verification
1. In the browsable API (logged in), use the form on a book's detail page to change its status. Then check that the website card updated.
2. Try an invalid status in the form. You see a 400 with an error message.
3. Delete a book through the browsable API. It's gone from `/books/`.

### Evidence to collect
Screenshots: `09-api-patch.png`, `09-api-validation-error.png`.

### Commit checkpoint
`feat: allow updating and deleting saved books through the API`

---

## Phase 10: Script 2 (`api_script.py`)

**User stories:** 61–66

### What to build
An interactive script in the same style as script 1:
- **Configuration:** reads `READING_LIST_TOKEN` (required) and `READING_LIST_API_URL` (default `http://127.0.0.1:8000`).
- **Functions:** `list_books()` gets the first page and returns `results`. `update_status()` sends the `PATCH`. `main()` runs the flow. The standard main guard.
- **Flow:** prints ID / title / status with a "Showing the first page only" note. Asks for an ID (must be a number) and a status (one of the three codes), validated before any request. Then `PATCH`es and prints `Before:` (from the list) and `After:` (from the `PATCH` response).
- **Errors:** friendly messages for a missing token (no request), 401, server unreachable, an empty list, a non-numeric ID, a 404 (missing or not owned), an invalid status, and network errors or invalid JSON. Never a traceback. `timeout=10`.

### Expected files
`api_script.py` (new), `test_api_script.py` (new, at the root alongside `test_main.py`), `CLAUDE.md` (script command), `PROMPTS.md`.

### `/tdd` behaviors (3)
1. When `READING_LIST_TOKEN` is not set, the script prints the setup message and sends no request.
2. A successful run prints the list, then `Before:` and `After:` lines using the faked API responses.
3. A 404 from `PATCH` prints `No book with ID <id> in your reading list.`

### Other tests required
(All with `monkeypatch` to fake HTTP and `input()`, so no server is needed.)
- 401 → the token-rejected message.
- A connection error → the could-not-reach message.
- An empty `results` list → the empty message.
- A non-numeric ID → the validation message with no `PATCH`.
- An invalid status → the validation message with no `PATCH`.
- Invalid JSON → a friendly message.
- `READING_LIST_API_URL` overrides the base URL.

### Manual browser / terminal verification
1. Run the server. Create a token. Set `READING_LIST_TOKEN` in the terminal (not in any file).
2. Run `uv run api_script.py`, pick a book, and change it to Finished. Check the before and after lines, then refresh `/books/` in the browser to see the change.
3. Run without the token set, with a wrong token, with the server stopped, with ID `abc`, with an ID that isn't yours, and with status `done`. Check each message.
4. Run once with a user who has no books.
5. **Unset the token afterward.**

### Evidence to collect
Screenshots: `10-script2-success.png`, `10-script2-errors.png` (token never visible).

### Commit checkpoint
`feat: add API script to list books and update reading status`

---

## Phase 11: Documentation and final check

**User stories:** 70 (plus reflection evidence)

### What to build
- **README:** what the project is; requirements (Python 3.14, uv); setup (`uv sync`, `migrate`, `createsuperuser`); environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `READING_LIST_TOKEN`, `READING_LIST_API_URL`) with PowerShell and Bash examples; running the server; creating a token; running script 1 and script 2; running tests, lint, and format checks; deployment notes (HTTPS, a strong secret key, `DEBUG=False`, `ALLOWED_HOSTS`); Open Library attribution, rate limits, and the User-Agent limitation.
- Final polish for consistency and responsiveness across all pages (only fixes, no new features).
- Run the final regression checklist below and capture any missing screenshots.
- Make sure `CLAUDE.md` matches the final project.

### Expected files
`README.md`, `CLAUDE.md`, templates (polish only), `docs/screenshots/`, `PROMPTS.md`.

### `/tdd` behaviors
None. This phase is documentation and polish, so it has no clear testable behavior (allowed by the `/tdd` skill).

### Tests required
The full suite, Ruff lint, Ruff format check, and the migration check all pass.

### Manual verification
The complete **Final regression checklist** below.

### Evidence to collect
Any screenshots still missing from earlier phases, plus final passing check output.

### Commit checkpoint
`docs: add README and complete final regression check`

---

## Final regression checklist

Run with a fresh database (`migrate` on an empty `db.sqlite3`) and two users (A and B).

**Automated**
- [ ] `uv run pytest`: all tests pass (script 1, script 2, Django)
- [ ] `uv run ruff check .`: all checks passed
- [ ] `uv run ruff format --check .`: all files formatted
- [ ] `uv run manage.py makemigrations --check --dry-run`: no changes
- [ ] `git status` shows no `db.sqlite3`, `.venv/`, tokens, or secrets

**Accounts and access**
- [ ] Home (logged out) shows the intro and buttons. Sign up → auto-login → Home welcome.
- [ ] Log out (`POST`) → Home with a message. A bad login shows an error. A good login goes to `/books/` (or `next`).
- [ ] Logged-in users visiting Login or Sign up are redirected. Logged-out users visiting protected pages are redirected to Login.

**Open Library search and save**
- [ ] Results with covers, singular wording, no results, blank input, and the outage alert (proxy cleared afterward)
- [ ] Save → message + "In your list". Duplicate → message. Tampered work key → friendly error.

**Reading list**
- [ ] Cards, placeholders, empty message
- [ ] Search, filter, sort, Apply. Pagination keeps the parameters. Bad `sort`/`status`/`page` values don't error. Counts reflect the whole list.
- [ ] Edit (allowed fields only, rating validation) and delete (confirmation, `POST`), with messages
- [ ] User B gets 404 for user A's edit and delete URLs
- [ ] Home counts match each user's list
- [ ] Phone-width layout works on every page

**API and scripts**
- [ ] 401 without a token. The list is paginated and only shows your own books. Other users' books → 404.
- [ ] `PATCH` (allowed fields only, validation 400) and `DELETE` work. `POST` and `PUT` → 405.
- [ ] The browsable API works with your website login
- [ ] Script 1: the normal search, no results, blank input, and a network error
- [ ] Script 2: success before/after plus every error message. Token unset afterward.

**Admin and docs**
- [ ] The admin list, filters, and search work. Non-staff users can't access `/admin/`.
- [ ] The README instructions work when followed step by step. `CLAUDE.md` and `PROMPTS.md` are accurate.

## Reflection reminder

The final reflection must be written **in your own words**. Claude can help gather evidence (the `PROMPTS.md` bug and fix records, test output, and screenshots in `docs/screenshots/`), but it must not write the reflection's answers. Provide the **five required reflection questions** from the course instructions before Phase 11 ends, so the collected evidence matches what they ask.
