# Reading List: Building With APIs

A personal **reading list** website for CIDM3312 Project #2. You search the
[Open Library](https://openlibrary.org) API by title, save books to your own list, and track each
book's reading status, an optional 1–5 star rating, and notes. The same list is available through a
token-protected **Django REST Framework** API, and two small command-line scripts show how to use
Open Library and our own API from Python.

## Features

- **Accounts:** sign up (you are logged in automatically), log in, and log out (a button, `POST` only).
- **Search Open Library** by title (up to 10 results with covers) and save a book to your list with
  one click. Saving the same book twice is prevented.
- **My Reading List** (`/books/`): book cards with a status badge (Want to Read / Reading / Finished),
  a search box (title or author), a status filter, sorting (newest, oldest, title, author), and
  10 books per page. The sidebar shows how many books you have in each status.
- **Edit** a book's status, rating, and notes, or **delete** it (with a confirmation page).
  Book details from Open Library (title, author, year, cover) can't be edited.
- **Home page:** your reading counts and quick links when you're logged in.
- **Privacy:** every page and API endpoint shows only your own books. Another user's book returns 404.
- **REST API** at `/api/books/` with token or session login (see [API](#api)).
- **Admin site** at `/admin/` for staff users.
- **Script 1** (`main.py`): search Open Library from the terminal.
- **Script 2** (`api_script.py`): list your books through our API and change one book's status.

**Built with:** Python 3.14, Django 6.1, Django REST Framework 3.18, SQLite, Bootstrap 5 (from a CDN),
`requests`, pytest, and Ruff, managed with [uv](https://docs.astral.sh/uv/).

## Requirements

- **Python 3.14** (the project pins it in `.python-version`)
- **uv** ([installation guide](https://docs.astral.sh/uv/getting-started/installation/)).
  uv can download Python 3.14 for you if it isn't installed.
- Git, to clone the repository

Every command below starts with `uv run`, which runs it inside the project's environment.
You never need to activate a virtual environment or use `pip`.

## Setup

Run these commands from the project folder (the one that contains `manage.py`).

**1. Get the code and install the dependencies**

```bash
git clone https://github.com/TrentWesley/project-two-building-with-apis.git
cd project-two-building-with-apis
uv sync
```

`uv sync` creates `.venv/` and installs everything listed in `pyproject.toml` and `uv.lock`,
including the test and lint tools.

**2. Create the database**

```bash
uv run manage.py migrate
```

This creates `db.sqlite3` (SQLite). The file is gitignored and is never committed.

**3. Create an admin user (optional, but useful)**

```bash
uv run manage.py createsuperuser
```

Follow the prompts. Regular users can also sign up on the website at `/accounts/signup/`.

## Running the website

```bash
uv run manage.py runserver
```

Open http://127.0.0.1:8000 in your browser. Stop the server with **Ctrl+C**.

For local development you don't need to set any environment variables: `DEBUG` is on by default and
a clearly fake development secret key is used. See [Environment variables](#environment-variables).

| Page | URL |
|---|---|
| Home | `/` |
| Sign up / Log in | `/accounts/signup/` · `/accounts/login/` |
| Search Open Library | `/search/` |
| My Reading List | `/books/` |
| API (browsable when logged in) | `/api/books/` |
| Admin (staff only) | `/admin/` |

## Environment variables

All settings that are secret or differ between computers come from environment variables.
**Never** put real values in code, in this README, in screenshots, or in commits.

| Variable | Used by | Required? | Default |
|---|---|---|---|
| `DJANGO_SECRET_KEY` | Django | Only when `DJANGO_DEBUG` is `False` | A fake development key (allowed only while `DEBUG` is on) |
| `DJANGO_DEBUG` | Django | No | `True`. Only the exact text `True` turns debug on; anything else turns it off. |
| `DJANGO_ALLOWED_HOSTS` | Django | No | `localhost,127.0.0.1` (comma-separated, no spaces) |
| `READING_LIST_TOKEN` | Script 2 | **Yes**, for script 2 | None |
| `READING_LIST_API_URL` | Script 2 | No | `http://127.0.0.1:8000` |

If `DJANGO_DEBUG` is `False` and `DJANGO_SECRET_KEY` is not set, Django refuses to start with:
`Set the DJANGO_SECRET_KEY environment variable when DJANGO_DEBUG is False.` This is on purpose, so
the fake key can never be used in production.

**Setting a variable for the current terminal only** (it disappears when you close the terminal):

PowerShell (use **single quotes**: in double quotes, PowerShell treats `$` as the start of a variable,
and secret keys can contain `$`):

```powershell
$env:DJANGO_DEBUG = 'False'
$env:DJANGO_SECRET_KEY = '<your-secret-key>'
$env:DJANGO_ALLOWED_HOSTS = 'localhost,127.0.0.1'
Remove-Item Env:DJANGO_DEBUG        # remove a variable again
```

Bash:

```bash
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY='<your-secret-key>'
export DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
unset DJANGO_DEBUG                  # remove a variable again
```

To generate a strong secret key, run the command below. Treat its output like a password.

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or generate one and store it in `DJANGO_SECRET_KEY` without showing it (this also avoids any quoting
problems):

```powershell
$env:DJANGO_SECRET_KEY = uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
export DJANGO_SECRET_KEY="$(uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")"
```

## API tokens (keep them secret)

Script 2 and other API clients log in with a personal **token**. Anyone with your token can read and
change your reading list, so treat it like a password:

- Set it only as an environment variable in your terminal. Never save it in a file in this project.
- Never paste it into code, docs, `PROMPTS.md`, commit messages, or screenshots.
- If a token is ever exposed, replace it (see "Replacing a token" below).

**Recommended: load your token without showing it on screen.** The commands below get your token from
the database (creating one if you don't have one yet) and store it straight in `READING_LIST_TOKEN`.
Replace `<your-username>` with your website username.

PowerShell:

```powershell
$env:READING_LIST_TOKEN = uv run manage.py shell -v 0 -c "from django.contrib.auth.models import User; from rest_framework.authtoken.models import Token; print(Token.objects.get_or_create(user=User.objects.get(username='<your-username>'))[0].key)"
"Token is set (length $($env:READING_LIST_TOKEN.Length))"
```

Bash:

```bash
export READING_LIST_TOKEN="$(uv run manage.py shell -v 0 -c "from django.contrib.auth.models import User; from rest_framework.authtoken.models import Token; print(Token.objects.get_or_create(user=User.objects.get(username='<your-username>'))[0].key)")"
echo "Token is set (length ${#READING_LIST_TOKEN})"
```

The second line should print `Token is set (length 40)`. The token itself never appears.
If it prints `length 0`, the token wasn't loaded: check the error shown above it. Usually the username
is misspelled (it's case-sensitive), or `uv run manage.py migrate` hasn't been run yet.

**Alternative:** DRF's built-in command creates a token too, but it **prints the token** on screen,
so make sure nothing is being recorded:

```bash
uv run manage.py drf_create_token <your-username>
```

**Replacing a token:** `uv run manage.py drf_create_token -r <your-username>` deletes the old token and
creates a new one (it also prints the new token). Then load the new token as shown above.

**When you're finished**, remove the token from your terminal:

```powershell
Remove-Item Env:READING_LIST_TOKEN     # PowerShell
```

```bash
unset READING_LIST_TOKEN               # Bash
```

## Running the scripts

### Script 1: search Open Library (`main.py`)

```bash
uv run main.py
```

Type a book title. The script searches Open Library and prints the total number of matches and the
first 5 results as `title by author`. A blank title or a network problem gets a friendly message.
It needs internet access but not the Django server or a token.

### Script 2: update a book's status through our API (`api_script.py`)

1. Start the website in one terminal: `uv run manage.py runserver`
2. In a second terminal, set `READING_LIST_TOKEN` privately (see [API tokens](#api-tokens-keep-them-secret)).
3. Run:

   ```bash
   uv run api_script.py
   ```

4. The script lists the **first page** of your books (up to 10) as `[id] title - status`. Enter a book
   ID, then a new status: `want_to_read`, `reading`, or `finished`. It updates the book and prints:

   ```
   Before: want_to_read
   After: finished
   ```

   If the book you chose isn't on the first page, it prints `Before: not available (...)` instead of
   guessing.
5. Remove the token from your terminal when you're done.

To use a server at a different address, set `READING_LIST_API_URL` (for example
`http://localhost:9000`) before running the script.

Instead of a traceback, script 2 shows a friendly message for:
- a missing token
- a rejected token (401)
- an empty list
- a blank or non-numeric ID, or a blank or invalid status (checked before anything is sent)
- a book that isn't yours or doesn't exist (404)
- other rejected requests (4xx)
- server errors (500 or higher)
- the server not running, a request taking longer than 10 seconds, or a response that isn't valid JSON

## API

All endpoints require login and only ever return **your own** books.

| Method | URL | What it does |
|---|---|---|
| `GET` | `/api/books/` | Your books, 10 per page, as `{"count", "next", "previous", "results"}` |
| `GET` | `/api/books/<id>/` | One of your books |
| `PATCH` | `/api/books/<id>/` | Change `status`, `rating` (1–5 or `null`), and/or `notes` |
| `DELETE` | `/api/books/<id>/` | Remove one of your books (returns 204) |

- **List options:** `?q=` (search title or author), `?status=` (`want_to_read`, `reading`,
  `finished`), `?sort=` (`newest`, `oldest`, `title`, `author`), and `?page=`. These work the same as
  the My Reading List page. The `next` and `previous` links keep your options.
- **Read-only fields:** `id`, `work_key`, `title`, `author`, `first_publish_year`, `cover_id`, and
  `created_at` can't be changed. If you send them in a `PATCH`, they are ignored.
- **Responses:**
  - **401:** no token or an invalid token
  - **404:** another user's book (or one that doesn't exist)
  - **400:** an invalid status, or a rating outside 1–5
  - **405:** `POST /api/books/` and `PUT /api/books/<id>/` aren't allowed (books are added from the
    website search, and only `PATCH` can change a book)

**Logging in to the API:**
- **Token:** send the header `Authorization: Token <your-token>`.
- **Browser:** if you're logged in to the website, open http://127.0.0.1:8000/api/books/ to use DRF's
  browsable API (session login).

Example with the token from `READING_LIST_TOKEN` (PowerShell, then Bash):

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/books/ -Headers @{ Authorization = "Token $env:READING_LIST_TOKEN" }
```

```bash
curl -H "Authorization: Token $READING_LIST_TOKEN" http://127.0.0.1:8000/api/books/
```

## Tests and code quality

```bash
uv run pytest                     # all tests: script 1, script 2, and the Django app
uv run ruff check .               # lint
uv run ruff format --check .      # check formatting (use "uv run ruff format ." to fix it)
uv run manage.py makemigrations --check --dry-run   # confirm no model changes are missing a migration
uv run manage.py check            # Django system check
```

The tests never call the real Open Library API, need a running server, or use a real token.
External calls are replaced with fakes using pytest's built-in `monkeypatch`.

## Open Library attribution and limitations

- Book data and covers come from **[Open Library](https://openlibrary.org)**, run by the Internet
  Archive. Every page's footer links back to Open Library, as its Covers API asks.
- On the Python side, only the Django app's search module and script 1 call Open Library. Each search
  is one request with a 10-second timeout. If Open Library is slow or down, you see a friendly
  message, and the technical details go to the server log.
- Cover images are loaded by your **browser** directly from `covers.openlibrary.org`. Books without
  a cover show a placeholder instead.
- **Rate limits:** Open Library documents a limit of about 1 request per second, or 3 per second for
  identified requests. This project makes one request per search.
- **User-Agent limitation:** requests identify the app as `CIDM3312-BookSearch/1.0`, with **no contact
  details**, to keep personal information out of this public repository. Open Library asks apps that
  make frequent requests to include a contact email or phone number. That's fine for a class project
  run locally, but a deployed or heavily used version should add contact details through
  configuration (not code) and consider caching.

## Deployment security notes

This project is set up for local development and has not been deployed. A real deployment would need
at least:

- **HTTPS**, so tokens, passwords, and session cookies aren't sent in plain text
- **A strong, secret `DJANGO_SECRET_KEY`** set in the server's environment (never committed)
- **`DJANGO_DEBUG=False`**, so error pages don't reveal code or settings
- **`DJANGO_ALLOWED_HOSTS`** set to the site's real domain name(s)
- A way to serve static files with `DEBUG` off (Django's development server doesn't do this), and a
  production database and web server instead of `runserver` and the local `db.sqlite3` file

## Project layout

```
manage.py            Django entry point
config/              Django project: settings and root URLs
books/               The only Django app: model, views, forms, search/filter helper,
                     Open Library service, API (serializers.py, api.py, api_urls.py), admin, templates, tests
templates/           Shared base layout, home page, and login/sign-up pages
main.py              Script 1: search Open Library from the terminal
api_script.py        Script 2: list your books via our API and update a status
test_main.py         Tests for script 1
test_api_script.py   Tests for script 2
prd/ plans/ docs/    Requirements, implementation plan, design decisions, and research
PROMPTS.md           Log of the AI-assisted development sessions
CLAUDE.md            Guidance for Claude Code when working on this project
```
