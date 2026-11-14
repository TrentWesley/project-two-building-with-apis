# Prototypes

Throwaway prototypes used to make design decisions before building the Django application. They are kept in the repository as evidence for the assignment. **They are not production code.**

## Reading List Layouts (`reading-list-layouts.html`)

**Date:** 2026-11-14
**Skill:** `/prototype` (UI branch, "no existing UI: establish the convention")
**How to open:** double-click the file, or run `start prototypes\reading-list-layouts.html` from the project folder. Use the dark panel in the bottom-right corner (or the `←`/`→` keys) to switch layouts.

### 1. Design question

> Which of three structurally different Bootstrap layouts should the **My Reading List** page use? The chosen layout becomes the visual convention for the whole website.

During planning we had decided *what* the reading-list page shows: cover, title, author, status, rating, search box, status filter, sort dropdown, Edit/Delete buttons, and pagination. We had not decided *how it looks*. The project had no UI yet, so this was the largest open design decision.

### 2. Layouts compared

All three layouts used the same 13 sample books (12 real Open Library works with real covers, plus one book with no cover and no year), the same working search, filter, and sort rules (mirroring the agreed `filter_books` rules), 10 books per page, and stubbed Edit/Delete buttons.

| Key | Layout | Description |
|---|---|---|
| A | Table | Dense rows with small covers. Columns for title/year, author, status, rating, and actions. All filters in one toolbar row above the table. |
| **B** | **Card grid + sidebar** | Large covers on cards (1–3 per row depending on screen width). Search, status filter (radio buttons with counts), and sort in a left sidebar. |
| C | Compact list grouped by status | One-line rows under Want to Read / Reading / Finished headings. Status filter as pill tabs with counts. Search and sort in the header. |

Observed trade-off: Layout C groups only the books on the current page, so with pagination a status group can be split across pages.

### 3. Decision: Layout B (Card grid + sidebar)

Selected by the student after comparing all three layouts in the browser, because:

- Book covers and information are easy to see.
- The sidebar keeps searching, filtering, and sorting organized.
- Reading statuses, ratings, and Edit/Delete buttons are clearly visible.
- It looks like a complete reading-list website.
- It balances usability and appearance well.

### 4. Impact on the final implementation

- **Site-wide convention:** Bootstrap 5, a dark top navbar (Search Open Library, My Reading List, username, Log out), cards with soft shadows, and the status badge colors used in the prototype (Want to Read = gray, Reading = blue, Finished = green). Every page (search, edit, delete, login, sign-up) follows this style.
- **My Reading List page:** card grid of saved books with a left filter sidebar containing the search box (`q`), status radio buttons with counts (`status`), and sort dropdown (`sort`), with Bootstrap pagination below the grid. The search, filter, sort, and pagination behavior stays exactly as agreed in the plan (shared `filter_books` helper, 10 per page, parameters preserved across pages).
- **Open Library search results** follow the same card style, with a Save button or an "In your list" label on each card.
- **Improvements requested for the final version:**
  - Cleaner "No cover" placeholders (for example, a neutral book icon or the title on a soft background instead of plain gray text).
  - Good behavior on small screens: the sidebar stacks above the grid on phones, and cards drop to one per row.
  - A consistent design across all pages.
- **Not carried over:** the prototype's JavaScript, in-memory data, and variant switcher. The real pages are Django templates driven by server-side views and normal `GET`/`POST` forms.
