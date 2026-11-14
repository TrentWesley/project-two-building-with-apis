# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**Project #2: Building With APIs** (CIDM3312, 200 points). A personal **reading list** website:
users search the **Open Library** API by title, save books to their own list in **SQLite**, track
a reading status (Want to Read / Reading / Finished), an optional 1–5 rating, and notes, and
manage their list through Django pages and a **Django REST Framework** API.

The student is a **beginner**. Prefer the simplest built-in Django/DRF approach, explain
choices in plain language, and avoid extra packages, apps, or abstractions.

## Source documents (read before changing behavior)

| Document | Purpose |
|---|---|
| `prd/django-reading-list.md` | Approved PRD: user stories, implementation decisions, out of scope |
| `plans/django-reading-list.md` | Approved phased plan: Phases 0–11, per-phase tests, `/tdd` behaviors, verification, commits |
| `docs/plans/django-reading-list-decisions.md` | The 22 design decisions in detail |
| `docs/research/api-options.md` | Open Library API research (official sources) |
| `prototypes/README.md` | UI prototype decision: **Layout B, card grid + sidebar** |
| `docs/plans/open-library-search-script.md` | Plan for script 1 (finished) |
| `PROMPTS.md` | Session log; update every session |

If a request conflicts with these documents, point out the conflict and ask before changing the design.

## Stack

- Python **3.14** (pinned in `.python-version`), managed with **uv**
- **Django** + **Django REST Framework** (with `rest_framework.authtoken`), added in Phase 1.
  Their versions must officially support Python 3.14.
- **SQLite** (Django default)
- **Bootstrap 5 via CDN**: no frontend build tools, no JavaScript for filtering
- **pytest** + **pytest-django** for tests, **Ruff** for linting and formatting
- `requests` for HTTP (Open Library service and both scripts)

## Project structure

```
manage.py          Django entry point (Phase 1)
config/            Django project: settings, root URLs (Phase 1)
books/             The ONLY Django app: model, views, forms, filters helper,
                   Open Library service module, API serializer/views, admin, templates, tests
templates/         Shared base layout, home page, and auth pages
main.py            Script 1: searches Open Library from the terminal (FINISHED; keep independent)
test_main.py       Tests for script 1
api_script.py      Script 2: lists my books via our API and updates a status (Phase 10)
prd/ plans/ docs/  PRD, implementation plan, decisions, research, screenshots
prototypes/        Throwaway UI prototype kept as evidence (not production code)
```

- **Do not modify `main.py`** except to fix a real bug. The Django app has its own Open Library service module.
- Do not add more Django apps. Everything belongs in `books`.

## Durable design rules

- **Model:** `SavedBook` with a `ForeignKey` to Django's `User` (`CASCADE`), unique on (`user`, `work_key`).
  Open Library fields: `work_key`, `title`, `author` (comma-joined; "Unknown author"), `first_publish_year`
  and `cover_id` (optional). User fields: `status` (`want_to_read`/`reading`/`finished`, default
  `want_to_read`), `rating` (optional, 1–5), `notes` (optional). Plus `created_at`.
- **Work key format:** `/works/OL` + digits + `W` (for example, `/works/OL27448W`).
- **Editable fields:** only `status`, `rating`, and `notes`, on the website and in the API. Open Library fields are read-only.
- **Ownership:** every book query is filtered by the current user. Another user's book returns **404**.
- **Shared filtering helper** (used by both the website list and the API list): `q` (Q objects, title OR author,
  case-insensitive), `status` (invalid means all), `sort` (`title`/`author`/`newest`/`oldest`, invalid means `newest`).
  10 per page. Bad `page` values never cause errors.
- **Open Library:** only the `books` service module calls it: `title=` search, `limit=10`, User-Agent
  `CIDM3312-BookSearch/1.0`, `timeout=10`, `raise_for_status()`, catch `RequestException` and `ValueError`.
  Views never call `requests`. Users see friendly messages, and technical details go to the server log.
- **API:** `/api/books/` (`GET`) and `/api/books/<id>/` (`GET`, `PATCH`, `DELETE`). **No create, `PUT` disabled.**
  `TokenAuthentication` listed **first**, then `SessionAuthentication`, so unauthenticated requests get 401.
- **URLs:** `/`, `/accounts/signup/`, `/accounts/login/`, `/accounts/logout/` (`POST` only), `/search/`,
  `/books/save/` (`POST`), `/books/`, `/books/<id>/edit/`, `/books/<id>/delete/`, `/api/...`, `/admin/`.
- **UI:** Layout B (dark navbar, card grid + sidebar with a `GET` form and an **Apply** button, status badges:
  gray/blue/green). The same style on every page, and responsive on phones.

## Commands

| Purpose | Command |
|---|---|
| Install / sync dependencies | `uv sync` |
| Add a dependency (dev: add `--dev`) | `uv add <package>` |
| Run all tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format check / apply | `uv run ruff format --check .` / `uv run ruff format .` |
| Migrations | `uv run manage.py makemigrations` · `uv run manage.py migrate` |
| Check migrations are current | `uv run manage.py makemigrations --check --dry-run` |
| Dev server | `uv run manage.py runserver` → http://127.0.0.1:8000 |
| Admin user | `uv run manage.py createsuperuser` |
| API token | `uv run manage.py drf_create_token <username>` |
| Script 1 / Script 2 | `uv run main.py` / `uv run api_script.py` |

The Django commands become available in Phase 1. Always use `uv run`, never a bare `python` or `pip`.

## Coding conventions

- Beginner-friendly code: short functions with one job, clear names, docstrings, plain `if/else` over clever one-liners.
- Prefer Django built-ins: `ListView`/`UpdateView`/`DeleteView`, `LoginRequiredMixin`, `LoginView`/`LogoutView`,
  `UserCreationForm`, model `choices`, validators, `UniqueConstraint`, the messages framework, `Paginator`.
- Prefer DRF built-ins: `ModelSerializer` with `read_only_fields`, generic views/viewsets, `PageNumberPagination`.
- Use `.get()` with defaults for external data, so missing fields never raise `KeyError`.
- Scripts use small functions, `timeout=10`, friendly messages (never tracebacks), and the `if __name__ == "__main__":` guard.
- Code must pass `ruff check` and `ruff format --check` with no warnings.

## Testing requirements

- All tests run with **`uv run pytest`** (plain `assert` style), including script 1 tests.
- **Tests never call the real Open Library API or need a running server.** Fake external calls with pytest's
  built-in `monkeypatch`.
- Every phase adds tests for its acceptance criteria. Checks that must pass before a phase is done:
  `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, and (from Phase 2)
  `makemigrations --check --dry-run`.
- Report test results honestly. If a test fails, show the output; never weaken a test just to make it pass.

## Required skill workflow

| Skill | When |
|---|---|
| `/research` | Investigating an API or technical question from official sources (done for Open Library) |
| `/grill-me` | Planning a design one question at a time (done) |
| `/prototype` | Answering an open design question with throwaway code (done: Layout B) |
| `/to-prd` → `/prd-to-plan` | Writing the PRD and phased plan (done) |
| `/implement` | **Every implementation phase.** Name the phase, e.g. "Phase 3 of `plans/django-reading-list.md`" |
| `/tdd` | Invoked inside `/implement`: **at most 3 behaviors per phase** (listed in the plan), with approval at RED and GREEN |

Per phase:
1. `/implement` the named phase only. Don't start the next phase.
2. `/tdd` for the phase's listed behaviors. Write normal tests for everything else.
3. Run all automated checks and fix failures.
4. Give the student manual browser verification steps, then **stop and wait** for their confirmation.
5. Update `PROMPTS.md` (prompts, decisions, **actual bugs and fixes**, results). Update `CLAUDE.md` if commands,
   structure, or conventions changed.
6. After approval: **one commit per phase**, files staged by name, then push.

Do not commit or push unless the student asks (each phase's workflow includes that request after approval).

## Security rules

- **Never** put secrets, API tokens, passwords, or real `SECRET_KEY` values in code, docs, screenshots, commit messages,
  or `PROMPTS.md`.
- Django settings come from environment variables: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.
  The fake development key is only allowed when `DEBUG` is on, and startup must fail otherwise. Remove Django's generated key.
- Script 2 reads `READING_LIST_TOKEN` (and optional `READING_LIST_API_URL`) from the environment.
- Never commit `db.sqlite3`, `.venv/`, `.env`, or caches (all gitignored). **Stage files by name**, never `git add .`.
- Don't send the student's personal information (name, email) to external services. The Open Library
  User-Agent is name-only by design. This is a documented limitation.
- If a token appears in a screenshot or output, tell the student to delete and regenerate it.
- Deployment (not planned) would require HTTPS, a strong secret key, `DEBUG=False`, and correct `ALLOWED_HOSTS`.

## Documentation and evidence

- `PROMPTS.md`: one session entry per session, in its existing format (Prompts Used, Work Completed, Decisions,
  Next Steps), including real bugs found and how they were fixed.
- Screenshots: `docs/screenshots/`, named as suggested in the plan (for example, `03-search-results.png`), with no tokens or passwords.
- README (Phase 11): setup, environment variables, server, tokens, both scripts, tests.
- **The final reflection is written by the student in their own words.** Help collect evidence, but do not write
  the reflection answers.
