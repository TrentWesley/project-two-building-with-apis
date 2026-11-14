# PRD: Personal Reading List (Django + Django REST Framework)

**Date:** 2026-11-14
**Status:** Approved by the student (2026-11-14)
**Sources:** the approved `/grill-me` design decisions (22 decisions, plus the approved sidebar Apply button and whole-list status counts), the selected layout prototype (Layout B: card grid + sidebar), the Open Library API research, and the assignment requirements summarized by the student.

## Problem Statement

Readers who want to keep track of books have no simple, personal place to do it. They can search a large catalog like Open Library, but Open Library doesn't let them record *their own* relationship with a book: whether they want to read it, are reading it, or have finished it, how they'd rate it, and what they thought of it. Without that, readers lose track of recommendations, forget what they've read, and can't easily find a book in their own list again.

The reader also needs this information to be private. One reader shouldn't see or change another reader's list. And someone who prefers automation (such as the developer, using a script) needs a way to read and update their list without clicking through web pages.

From the course's perspective, the project must show that the student can consume an external API, store and manage data locally, protect it with authentication, implement searching, Q objects, filtering, sorting, and pagination, and expose the data through their own REST API.

## Solution

A small website where a reader creates an account, searches Open Library by book title, and saves books to a personal reading list with one click. Each saved book keeps Open Library's facts (title, authors, first publish year, cover) and the reader's own information: a reading status (Want to Read, Reading, Finished), an optional 1–5 rating, and optional notes.

The reader's list is shown as a grid of book cards with a sidebar for searching their own books by title or author, filtering by status, and sorting. It's paginated 10 books per page. The reader can edit a book's status, rating, and notes, or remove a book after confirming. A home page welcomes visitors, or shows a logged-in reader their counts by status.

Alongside the website, a REST API gives each reader programmatic access to their own list (list, view, update, delete) using a personal token. A command-line script uses this API to list the reader's books and change one book's reading status, showing the value before and after.

Every page and endpoint only ever shows the logged-in reader's own books.

## User Stories

### Accounts and access

1. As a visitor, I want to see a home page explaining what the site does, so that I understand it before creating an account.
2. As a visitor, I want Sign Up and Log In buttons on the home page, so that I can get started quickly.
3. As a visitor, I want to create an account with a username and password, so that I can have my own reading list.
4. As a new user, I want to be logged in automatically after signing up, so that I don't have to type my password again.
5. As a new user, I want a welcome message after signing up, so that I know my account was created.
6. As a returning user, I want to log in with my username and password, so that I can reach my reading list.
7. As a user who mistypes my password, I want to stay on the login page with a clear error message, so that I can try again.
8. As a logged-out visitor who tries to open a protected page, I want to be sent to the login page and then returned to the page I wanted, so that I don't lose my place.
9. As a user who logs in without a specific destination, I want to land on My Reading List, so that I see my books right away.
10. As a logged-in user, I want to log out with a button, so that others using my computer can't access my list.
11. As a user who just logged out, I want to return to the home page with a "You have been logged out." message, so that I know it worked.
12. As a logged-in user who visits the login or sign-up page, I want to be sent to My Reading List, so that I don't see pages that no longer apply to me.
13. As a user, I want my reading list to be private, so that other users can't see or change my books.
14. As a user, I want a "not found" response if I (or anyone) try to open a book that isn't mine, so that the existence of other users' books isn't revealed.

### Home page

15. As a logged-in user, I want the home page to welcome me by username, so that the site feels personal.
16. As a logged-in user, I want buttons on the home page for Search Open Library and My Reading List, so that I can jump to what I need.
17. As a logged-in user, I want to see how many of my books are Want to Read, Reading, and Finished, so that I get a quick overview of my reading.

### Searching Open Library

18. As a logged-in user, I want to search Open Library by book title, so that I can find books to add to my list.
19. As a user, I want blank or spaces-only searches to show "Please enter a book title." without searching, so that I don't get confusing results.
20. As a user, I want to see how many matches were found and how many are shown, so that I know whether to refine my search.
21. As a user, I want correct singular wording when exactly one book matches, so that the page reads naturally.
22. As a user, I want up to 10 results, each showing the cover, title, authors, and first publish year, so that I can recognize the book I want.
23. As a user, I want a clean placeholder when a book has no cover, and "Year unknown" when it has no year, so that incomplete data still looks tidy.
24. As a user, I want "Unknown title" or "Unknown author" shown when Open Library doesn't provide them, so that results never break or look empty.
25. As a user, I want a friendly message when no books match, including the title I searched for, so that I can spot a typo.
26. As a user, I want a friendly error message, instead of a crash or error page, when Open Library is unavailable, so that I know to try again later.
27. As a user, I want my search to appear in the page address, so that I can bookmark or refresh it.

### Saving books

28. As a user, I want a Save button on each search result, so that I can add a book to my list with one click.
29. As a user, I want saved books to start as "Want to Read", so that I don't have to choose a status when saving.
30. As a user, I want to return to the same search results with a success message after saving, so that I can keep adding books.
31. As a user, I want books already in my list to show "In your list" instead of a Save button, so that I don't save duplicates.
32. As a user, I want a friendly message if I try to save a book that's already in my list, so that nothing breaks and no duplicate is created.
33. As a user, I want invalid or tampered save requests to be rejected with a friendly message, so that my list only contains valid books.

### Managing my reading list

34. As a user, I want to see my saved books as cards with cover, title, author, status, and rating, so that I can browse my list visually.
35. As a user with no saved books, I want a friendly message with a link to search Open Library, so that I know how to get started.
36. As a user, I want to search my own list by title or author, ignoring capitalization, so that I can quickly find a book.
37. As a user, I want to filter my list by reading status, so that I can focus on what I'm reading or want to read.
38. As a user, I want to sort my list by title, author, newest saved, or oldest saved, with newest first by default, so that I can view my books in a useful order.
39. As a user, I want to combine search, status filter, and sort and apply them with one button, so that I can narrow my list precisely.
40. As a user, I want unknown filter or sort values in the address to be ignored, not cause errors, so that a mistyped link still works.
41. As a user, I want my list split into pages of 10 books, so that long lists stay manageable.
42. As a user, I want page links to keep my search, filter, and sort, so that moving between pages doesn't reset my view.
43. As a user, I want the sidebar to show counts for each status across my whole list, so that I know how many books are in each group.
44. As a user, I want to edit a book's status, rating, and notes, so that my list stays up to date as I read.
45. As a user, I want the book's title, author, year, and cover shown (but not editable) on the edit page, so that I know which book I'm editing and can't accidentally change Open Library's facts.
46. As a user, I want ratings to be optional and limited to 1–5, so that I can save unread books and keep ratings consistent.
47. As a user, I want a success message after editing, so that I know my changes were saved.
48. As a user, I want to confirm before a book is removed, so that I don't lose my notes by mistake.
49. As a user, I want a success message after removing a book, so that I know it worked.
50. As a user on a phone, I want the layout to adapt (sidebar above the cards, one card per row), so that the site is usable on small screens.
51. As a user, I want every page to share the same look and navigation, so that the site feels consistent.

### API and script

52. As an API client, I want to authenticate with a personal token, so that scripts can access my list without my password.
53. As an API client without a valid token, I want a 401 Unauthorized response, so that I know authentication failed.
54. As an API client, I want to list my saved books with the same search, filter, sort, and 10-per-page pagination as the website, so that both behave the same.
55. As an API client, I want to view a single saved book, so that I can inspect its details.
56. As an API client, I want to update a book's status, rating, or notes, so that I can manage my list from a script.
57. As an API client, I want Open Library fields to be read-only, so that scripts can't corrupt book facts.
58. As an API client, I want to delete a saved book, so that I can manage my list from a script.
59. As an API client, I want a 404 response for books that aren't mine, so that other users' data stays private.
60. As a logged-in website user, I want to explore the API in my browser using my existing login, so that I can manually test it.
61. As a script user, I want the script to read my token from an environment variable, so that my token never appears in code.
62. As a script user, I want to see my books' IDs, titles, and statuses (first page only, clearly labeled), so that I can choose which book to update.
63. As a script user, I want to enter a book ID and a new status, and have both validated before anything is sent, so that mistakes are caught early.
64. As a script user, I want to see the book's status before and after the update, from real API data, so that I can confirm the change.
65. As a script user, I want clear messages for a missing or rejected token, the server not running, an empty list, an invalid ID, a book that isn't mine, an invalid status, and network or response errors, so that the script never crashes with a traceback.
66. As a script user, I want to point the script at a different server address with an environment variable, so that it works beyond the default local address.

### Administration and operations

67. As the site administrator (staff), I want to browse all saved books in the admin site with title, user, status, rating, and date added, plus filters and search, so that I can inspect data while testing.
68. As the developer, I want secret settings to come from environment variables, so that no real secret is ever committed to the public repository.
69. As the developer, I want the app to refuse to start in production mode without a real secret key, so that the insecure development key can never be used in production.
70. As the developer or grader, I want documentation explaining how to install, run, and test the application and both scripts, so that the project can be reproduced.

## Implementation Decisions

### Architecture and components
- One Django project (settings and root URLs) with **one app** for books. It holds the model, website views, forms, API serializer and views, the shared filtering helper, the Open Library service module, and the app's templates. Shared layout and authentication templates live in a project-level templates location.
- Website: server-rendered Django templates styled with **Bootstrap 5 via CDN**. No frontend build tools and no JavaScript for filtering.
- API: Django REST Framework, with token authentication from DRF's built-in token app.
- The existing script 1 stays independent and unchanged. Script 2 is a separate script at the repository root.
- Dependencies managed with uv: Django and Django REST Framework (runtime), pytest-django (dev, alongside the existing pytest and Ruff). No other packages or Django apps.
- **Version requirement:** the project pins Python 3.14. The Django and DRF versions installed must officially support Python 3.14 (and DRF must support the chosen Django version). Verify this against the official release notes or compatibility tables when adding them.

### Data model
- Data is stored locally in **SQLite**, Django's default database, managed through Django models and migrations.
- A single model, **SavedBook**, owned by Django's built-in User through a foreign key. **Approved:** if a user is deleted, their saved books are deleted too.
- Fields: Open Library **work key** (required), **title** (required; "Unknown title" if missing), **author** (required; comma-joined names, "Unknown author" if the list is missing or empty), **first publish year** (optional integer), **cover ID** (optional integer), **status** (choices `want_to_read` / `reading` / `finished` with labels Want to Read / Reading / Finished; default `want_to_read`), **rating** (optional integer, validated to 1–5), **notes** (optional text), and **created at** (set automatically).
- A database-level **unique constraint on (user, work key)**.
- No shelves or collections model. Status is the only grouping.

### Work key format
- A valid work key is the literal prefix `/works/OL`, then one or more digits, then the letter `W`, and nothing else (for example, `/works/OL27448W`). This matches the stable work keys observed in Open Library search results.
- The save form rejects any other value, as well as non-integer years or cover IDs and missing titles or authors. A rejected submission produces a friendly error message and a redirect, never a server error.

### Shared filtering helper
- One helper takes a user's queryset plus search, status, and sort values, and returns the filtered, ordered queryset. **Both** the website list view and the API list view use it.
- Search: strip spaces; blank means no search; otherwise a case-insensitive "contains" match on title **or** author, built with **Q objects**.
- Status: one of the three codes filters; blank or unknown means all.
- Sort: `title` (A→Z), `author` (A→Z), `newest` (default), `oldest`. An unknown value falls back to `newest`.
- URL parameters: `q`, `status`, `sort`, and `page`, shared by the website and the API.

### Pagination
- 10 items per page on both sides: Django's Paginator on the website and DRF page-number pagination on the API.
- Website page links preserve `q`, `status`, and `sort`.
- **Approved:** invalid page values (non-numbers) and out-of-range page numbers are handled gracefully, never with a server error. The website shows a valid page; the API returns DRF's standard response instead of crashing.

### Open Library service module
- The only place the application talks to Open Library. Views never make HTTP requests directly.
- Searches the Search API by **title**, requesting only key, title, author name, first publish year, and cover ID, limited to 10 results.
- Sends a name-only User-Agent (the same application name as script 1), uses a 10-second timeout, and treats non-success HTTP status codes as errors.
- Network, timeout, HTTP, and invalid-JSON errors are caught and reported to the view as a single "unavailable" outcome. Technical details are written to the server log, not shown to users.
- Raw results are converted into clean records (with the "Unknown title" and "Unknown author" rules, joined author names, and optional year and cover) by logic that can be unit-tested without internet access.
- Cover thumbnails are displayed straight from Open Library's Covers service, using the stored cover ID.

### Website pages and URL behavior
| Page | Access | Behavior |
|---|---|---|
| Home | Public | Intro with Sign Up and Log In for visitors. For logged-in users: welcome by username, links to search and the list, and counts of their own books by status. |
| Sign up | Public (logged-in users redirected to the list) | Built-in user creation form. On success: log in automatically, redirect to Home, and show a welcome message. |
| Log in | Public (logged-in users redirected to the list) | Built-in login view. Redirect to a safe `next` URL, otherwise the list. Failed login shows the built-in error. |
| Log out | Logged in | `POST` only (button in the navbar, CSRF-protected). Redirect to Home with "You have been logged out." |
| Search Open Library | Login required | `GET` with a `title` parameter. Behavior as described in the user stories (blank, results, singular, none, unavailable). Each result has a Save form or an "In your list" label. |
| Save book | Login required, `POST` only | Hidden fields (work key, title, author, year, cover ID) validated by a Django form. The server sets the user and the default status. Duplicates show a friendly message. Redirects back to the same search results with a message. |
| My Reading List | Login required | List view of the user's books as cards (Layout B), with a sidebar `GET` form (search, status radios with whole-list counts, sort) and an **Apply** button, pagination, Edit/Delete per card, and an empty-list message. |
| Edit book | Login required, owner only | Update view: read-only book info, form fields for status, rating, and notes only. Success message and redirect to the list. |
| Delete book | Login required, owner only | Delete view: confirmation page with Delete and Cancel. Deletes only on `POST`. Success message and redirect to the list. |

- All owner-only pages look the book up within the current user's books, so another user's book returns 404.
- Login URL, login redirect, and logout redirect are configured in settings so Django never uses its default profile URL.
- User feedback uses Django's messages framework, shown as Bootstrap alerts in the shared layout.
- No separate book detail page.

### Visual design (from the prototype)
- Layout B: a dark top navbar (Search Open Library, My Reading List, username, Log out button) and a footer with a "Data from Open Library" link.
- Book cards with covers and status badges (Want to Read = gray, Reading = blue, Finished = green), and star-style ratings with "Not rated" when empty.
- Cleaner "No cover" placeholders than in the prototype.
- Responsive: the sidebar stacks above the grid on small screens, with one card per row on phones.
- The same styling on every page, including the auth, edit, and delete pages.

### API
| Method | Endpoint | Behavior |
|---|---|---|
| GET | `/api/books/` | The user's books, filtered, sorted, and paginated with the shared helper |
| GET | `/api/books/<id>/` | One of the user's books |
| PATCH | `/api/books/<id>/` | Update status, rating, and/or notes (validated: status choices, rating 1–5) |
| DELETE | `/api/books/<id>/` | Remove one of the user's books |

- No create endpoint.
- The serializer exposes the book's ID, Open Library fields (read-only), status, rating, notes, and created date. It never exposes or accepts the user.
- Authentication classes in order: **token first, then session**, so unauthenticated requests get **401** and logged-in browser users can use the browsable API. All endpoints require authentication.
- The queryset is always limited to the requesting user, so other users' books return 404.
- Tokens are created with DRF's management command and are never stored in code, docs, screenshots, or commits.

### Script 2 (API client)
- Interactive command-line script in the same style as script 1: small functions to list books, update a status, and run the flow, with the standard main guard.
- Configuration from environment variables: the token (required) and the API base URL (optional, defaulting to the local development server).
- Reads the **first page** of the paginated list response and says so. Validates the ID (must be a number) and status (one of the three codes) before sending. Uses `PATCH` to update the status. Prints "Before" (from the list data) and "After" (from the `PATCH` response).
- 10-second timeout. Friendly messages for every error case in user story 65. Never shows a traceback.

### Settings and secrets
- Secret key, debug flag, and allowed hosts come from environment variables, using only the standard library. A clearly fake development key and `DEBUG=True` are the local defaults. Allowed hosts default to localhost addresses.
- If debug is off and no secret key is provided, startup fails with a configuration error.
- The secret key Django generates when the project is created is removed before the first commit.
- The SQLite database file stays out of version control.

### Admin
- SavedBook is registered with columns (title, user, status, rating, created at), filters (status, created at), and search (title, author, username). Access is limited to staff (Django default).

### Testing and quality
- All automated tests run with `uv run pytest` (pytest + pytest-django, plain `assert` style), including the existing script 1 tests. Ruff linting and format checks must pass.
- Highest-value behaviors to test, to be distributed across phases by the implementation plan:
  - model rules (defaults, rating limits, the uniqueness constraint)
  - the filtering helper (search on title/author, status, sort, invalid values, combinations)
  - the Open Library record conversion (missing/empty data)
  - saving (success, duplicate, invalid work key, user set by the server)
  - ownership (404 for other users on pages and the API)
  - search page outcomes (blank, results, singular, none, unavailable, with the service faked)
  - edit/delete (only allowed fields, `POST`-only delete)
  - home page counts (only the user's own books)
  - auth flow (auto-login, redirects, `POST` logout, login-required redirects)
  - API (401 without a token, `PATCH` limited to the allowed fields, pagination shape)
  - script 2 (each error path and the before/after output, with HTTP faked using pytest's `monkeypatch`)
- **TDD constraint:** the `/tdd` skill allows **at most three behaviors per phase**. The implementation plan must choose at most three TDD behaviors in each phase and cover the remaining behaviors with normal tests written in the same phase.
- Tests never call the real Open Library API or a running server. Live behavior is checked during manual browser testing.
- Every phase ends with manual browser verification by the student and a separate Git commit.

## Out of Scope

- Shelves, collections, tags, or any grouping beyond reading status.
- Creating books through the API (books are saved only from the website search).
- Editing Open Library fields (title, author, year, cover, work key) after saving.
- A separate book detail page.
- Searching Open Library by author, subject, or general query (title search only), and paging beyond the first 10 Open Library results.
- Fetching extra details (descriptions, editions, author pages) from Open Library.
- Caching Open Library responses, background jobs, or automatic refresh of saved book data.
- JavaScript-driven interactions (instant filtering, AJAX saving, pop-up confirmations) or a JavaScript frontend framework.
- Email verification, password reset, social login, user profiles, or account deletion pages.
- Sharing lists with, or viewing lists of, other users.
- Script 2 paging beyond the first page, or updating fields other than status.
- Deployment to a public server. The app runs locally for the class. Deployment requirements are documented only.
- *Writing* the reflection. The student writes it in their own words. The project must still **collect the evidence** for it (see Further Notes).

## Further Notes

- **Open Library User-Agent and rate limits.** Open Library documents a limit of 1 request per second, or 3 per second for identified requests. It asks applications that make regular, frequent use of its APIs (for example, multiple calls per minute) to send a User-Agent containing the application name **and** a contact email or phone number. This project deliberately sends a **name-only** User-Agent to keep personal contact details out of the public repository. That is reasonable for a locally run class project that makes one request per user search, but it is a **known limitation**: a deployed or heavily used version should add contact details (kept in configuration, not code) and consider caching. Open Library's error codes and rate-limit responses are undocumented, so all failures are handled generically. Its Covers API asks for a courtesy link back, which the footer's "Data from Open Library" link provides.
- **Testing strategy for external calls.** Script 1 avoided mocking. The web app's Open Library calls and script 2's HTTP calls are faked in tests with pytest's built-in `monkeypatch`, because behaviors such as "Open Library unavailable", 401, and 404 can't be tested reliably against live services.
- **Security notes.** Tokens, passwords, and real secret keys must never appear in code, docs, screenshots, or `PROMPTS.md`. If a token appears in a screenshot, delete and regenerate it. If deployed, the app requires HTTPS (to protect tokens), a strong secret key, `DEBUG` off, and correct allowed hosts.
- **Workflow requirements carried forward.** A phased implementation plan (`/prd-to-plan`) and a `CLAUDE.md` follow this PRD. Each phase uses `/implement` (and `/tdd` within its limit), runs pytest and Ruff, includes manual browser verification, updates `PROMPTS.md`, and gets its own commit. The README must document setup, environment variables, running the server, creating a token, running both scripts, and running the tests.
- **Evidence for the reflection.** During every phase, `PROMPTS.md` records the prompts used, the decisions made, and **actual bugs found and how they were fixed**, including failing test output or error messages when relevant. Screenshots of key results are captured during manual browser verification and kept in a screenshots folder in the repository, for example:
  - the home page logged out and logged in
  - sign-up and login
  - Open Library search results, no results, and the error alert
  - saving a book, and the duplicate message
  - the reading list with search, filter, sort, and pagination
  - edit and delete
  - a 404 when accessing another user's book
  - the browsable API
  - a 401 without a token
  - both scripts running

  Screenshots must not show tokens or passwords. These records support the student's reflection, which answers the **five required reflection questions** from the course instructions in the student's own words. The questions themselves are not reproduced here. The student should provide them before the reflection phase so the evidence collected matches what they ask.
- **Keeping project documents accurate.** `CLAUDE.md` (created after the implementation plan) describes the project's structure, commands, conventions, and workflow. It must be updated whenever a phase changes any of those. `PROMPTS.md` is updated in every phase.

- **Related documents.** Design decisions with full detail, the layout prototype and its decision record, the Open Library API research, and the script 1 plan.

## Assignment Requirements Coverage

| Requirement | Where it is addressed |
|---|---|
| Consume an external API | Open Library title search through the Open Library service module, with error handling (Implementation Decisions: Open Library service module; stories 18–27) |
| Provide our own DRF API | List, detail, `PATCH`, and `DELETE` endpoints with token and session authentication (API section; stories 52–60) |
| Save and manage data in SQLite | SavedBook model in SQLite, with save, edit, and delete pages (Data model; stories 28–49) |
| Authentication and access restrictions | Sign-up, login, and logout; login-required pages; per-user querysets returning 404; API 401; staff-only admin (stories 1–14, 52–53, 59, 67) |
| Searching with Q objects, filtering, sorting, pagination | Shared filtering helper (Q objects on title/author, status filter, four sorts) and 10-per-page pagination on the website and API (stories 36–43, 54) |
| Script 1 (external API) | Already complete and tested (`main.py`); stays independent |
| Script 2 (our API: list records, update a field) | Interactive API client that lists books and updates status, with before/after output (stories 61–66) |
| API research from official sources | Completed in the Open Library API research document; its findings drive the service module and Further Notes |
| At least one prototype for a design decision | Completed: three-layout UI prototype, with Layout B chosen and recorded |
| PRD, phased plan, `CLAUDE.md` | This PRD; the plan and `CLAUDE.md` follow |
| Automated tests, linting, formatting | pytest + pytest-django, Ruff lint and format checks, `/tdd` within its 3-behavior limit (Testing and quality) |
| Manual browser testing | Required at the end of every phase |
| Separate commits per phase | One commit per completed, verified phase |
| `PROMPTS.md` and `CLAUDE.md` accuracy | Updated every phase (Further Notes) |
| Run documentation | README covers setup, environment variables, server, token creation, both scripts, and tests |
| Reflection with evidence and screenshots | Evidence (bugs, fixes, screenshots) collected every phase; the student writes the reflection answering the five required questions |
