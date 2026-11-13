# API Options for Project #2: Building With APIs

**Date:** 2026-11-12

**Question:** Which free public API best supports a beginner Django + Django REST Framework project where users search an external API, save selected items to a local SQLite database, edit information about their saved items, and manage their own collections?

## Summary

Three APIs were evaluated against their official docs, terms pages, and live requests made on 2026-11-12:

| API | App idea | Key needed? |
|---|---|---|
| **Open Library** (Internet Archive) | Reading list / bookshelf | No |
| **Art Institute of Chicago (AIC) API** | Personal art gallery / museum favorites | No |
| **TheMealDB** | Recipe box | Uses a shared test key `1` in the URL; no signup for educational use |

**Recommendation: Open Library.** It needs no key or signup. Search is a single GET URL with simple `page` and `limit` pagination. An empty search returns a clear `numFound: 0`. Its rate limit is documented. Open Library asks developers to cache responses and claims no new copyright over its data. Book records also fit "save, then annotate" well: users can add reading status, a rating, and notes. TheMealDB has the simplest responses but no pagination, a mandatory attribution clause, and error handling that returns HTTP 200 for most problems. AIC has the best-documented errors and the clearest CC0 license, but its free-text search never comes back empty, and its advanced search uses Elasticsearch syntax, which is harder for a beginner.

PokéAPI, TMDB, Jikan, and RAWG were not evaluated in depth. TMDB and RAWG require an account and API key, and PokéAPI's data (fixed Pokémon records) gives users less to annotate. These reasons were not checked against those APIs' docs in this session; see "Open questions".

## Decision

**Decided 2026-11-12: Project #2 will use the Open Library API.** The student made this choice after reviewing the findings below.

**Why Open Library**
- No API key, account, or signup is needed [1].
- Search is one GET URL with standard `page`/`limit` pagination [2].
- An empty search returns HTTP 200 with `numFound: 0` and `docs: []`, so "no results" is easy to detect (observed; see §1.6).
- The rate limit is documented: 1 req/s, or 3 req/s with an identifying User-Agent [1].
- Saving data locally is encouraged ("Cache responses whenever possible") [1], and the Internet Archive asserts no new copyright over the data [4].
- Each book has a stable work key (e.g. `/works/OL27448W`) that can serve as the unique ID for a saved item. User-edited fields (status, rating, notes, shelf) don't overlap with API fields (§5).

**Why not the Art Institute of Chicago API**
- Free-text `q` search never returns zero results. A nonsense term returned the whole collection, so "no results" can't be detected without Elasticsearch query syntax (observed; see §2.6).
- Responses are more nested, and image URLs must be built from `image_id` via IIIF [5].
- Pagination is capped at 100 per page and 1,000 results total [5].
- Its strengths (consistent JSON errors, a clear CC0 license) didn't outweigh the extra search complexity for a beginner.

**Why not TheMealDB**
- Attribution is required [8].
- There is no pagination [7], and search results appeared capped at 25 (observed; undocumented).
- Most errors return HTTP 200 with `{"meals": null}` or `{"meals": "Invalid ID"}`, and unknown paths return HTML 404 pages, so error handling needs extra checks (observed; see §3.6).
- Ingredients come as 20 flat numbered fields, and all values are strings (§3.3).
- The rate limit is referenced in its terms but not published [8], and the free test key `1` is only for development or educational use [7].

**Carry forward (still open):** Open Library's error codes and rate-limit-exceeded response are undocumented, so failed responses should be handled generically. `author_name` is a list. Requests should send a descriptive User-Agent [1]. See §6 for remaining unverified items.

---

## 1. Open Library

### 1.1 Data and app idea
Open Library offers APIs for book search, works and editions, authors, subjects, covers, lists, and more [1]. Any Open Library page can also return `.json` by adding the extension to its identifier [1]. **App idea:** a reading list. Users search for books, save a work (title, author, first publish year, cover ID, Open Library key), then edit local fields such as status (want to read / reading / finished), rating, and notes, grouped into their own shelves.

### 1.2 Cost, key, attribution
- No API key is mentioned anywhere on the developer API page [1]. The live requests below worked with no key or account (observed 2026-11-12).
- Developers are asked to identify themselves: *"If your application will make regular, frequent use of Open Library's APIs (e.g. multiple calls per minute), please add a HEADER that specifies a User-Agent string with (a) the name of your application and (b) your contact email or phone number"* [1].
- Attribution: the Covers API page says *"A courtesy link back to Open Library is appreciated"* [3]. This is a request, not a requirement. No attribution requirement for metadata was found on the licensing page [4].

### 1.3 Search endpoint, parameters, pagination
- Endpoint: `https://openlibrary.org/search.json` [2].
- Parameters [2]: `q` (the Solr query), `title`, `author` (used in the doc's examples), `fields` (which fields to return; `*` returns everything, "please use sparingly"), `sort` (e.g. `new`, `old`, `random`, `key`; default is relevance), `lang` (influences results but doesn't exclude any), `page` + `limit` (*"Note `page` starts at 1"*), or `offset` + `limit`.
- Example request (observed 2026-11-12):
  `https://openlibrary.org/search.json?q=the+lord+of+the+rings&fields=key,title,author_name,first_publish_year,cover_i&limit=2`
- Response shape (key fields, observed 2026-11-12):
  ```json
  {
    "numFound": 1106, "start": 0, "numFoundExact": true,
    "docs": [
      { "key": "/works/OL27448W", "title": "The Lord of the Rings",
        "author_name": ["J.R.R. Tolkien"], "first_publish_year": 1954,
        "cover_i": 14625765 }
    ]
  }
  ```
  `author_name` is a **list**, not a single string.
- Detail for a saved item: `https://openlibrary.org/works/OL27448W.json` returns the work record, including `description` (observed 2026-11-12).
- Cover images: `https://covers.openlibrary.org/b/id/{cover_i}-M.jpg` returned an image (observed 2026-11-12). URL format per the Covers API docs [3].

### 1.4 Rate limits and reliability
- Documented in the "Rate Limits" section [1]:
  - Default (non-identified requests): **1 request per second**
  - Identified requests (with User-Agent and email): **3 requests per second**
  - *"Violations may result in aggressive rate limiting or blocking."*
- Covers API: *"The cover access by ids other than CoverID and OLID are rate-limited. Currently only 100 requests/IP are allowed for every 5 minutes."* [3]. Covers fetched by cover ID (`/b/id/...`) are not covered by that limit.
- Caching advice: under "Please Do", the page says *"Cache responses whenever possible"* [1]. It also says *"These APIs are not intended to serve as a bulk data backend or high-traffic commercial infrastructure."* [1]
- Status page: none was found in the official docs. `status.openlibrary.org` did not resolve (observed 2026-11-12). Uptime/SLA: not documented.

### 1.5 Storing data locally
- Licensing page [4]: *"The Internet Archive does not assert any new copyright or other proprietary rights over any of the material in the Open Library database. There may be existing rights issues on some contributions and in some jurisdictions. … we are attempting to make a database that can be openly used for a wide variety of purposes."*
- The API page explicitly encourages caching (*"Cache responses whenever possible"*) and asks developers not to bulk-download through the API: *"Please do not use our APIs to bulk download metadata … For bulk access, please download our free monthly data dumps"* [1].
- Conclusion: saving the specific books a user selects is consistent with these pages.

### 1.6 Errors and unavailable responses
- Status codes and error bodies are **not documented** on the search docs [2] or the developer API page [1].
- Observed on 2026-11-12:
  - **Empty search:** HTTP 200, `{"numFound":0, ..., "docs":[]}`.
  - **Not found (work):** `GET /works/OL999999999999W.json` returned HTTP 404 with body `{"error": "notfound", "key": "/works/OL999999999999W"}`. The response had no `Content-Type` header.
  - **Rate limit exceeded:** the status code and body are not documented, and this was not tested (to avoid abusing the service). The docs only say violations may lead to "aggressive rate limiting or blocking" [1].
  - **Covers:** *"By default it returns a blank image if the cover cannot be found. If you append ?default=false to the end of the URL, then it returns a 404 instead."* Exceeding the covers limit returns *"403 Forbidden"* [3].

---

## 2. Art Institute of Chicago (AIC) API

### 2.1 Data and app idea
A JSON REST API over the museum's public data: artworks, agents (artists), places, galleries, exhibitions, and more. It is *"the same tool that powers our website"* [5]. Images are served separately through a IIIF Image API [5]. **App idea:** a personal gallery. Users search artworks, save favorites (title, artist, date, image ID), and add their own notes, tags, or "seen in person" flags, organized into collections.

### 2.2 Cost, key, attribution
- *"You may access our API without authentication."* [5] (Authentication section.)
- Courtesy header: *"please add a AIC-User-Agent header with the name of your project and a contact email to your API requests"* [5].
- Licensing, as stated in the docs and returned in every response's `info.license_text` (observed 2026-11-12): *"The `description` field in this response is licensed under a Creative Commons Attribution 4.0 Generic License (CC-By) … All other data in this response is licensed under a Creative Commons Zero (CC0) 1.0 designation and the Terms and Conditions of artic.edu."* [5]. So attribution is required only if you reuse the `description` field.
- Images: *"we recommend only using images from artworks that are tagged as public domain"* (filter with `is_public_domain`) [5].

### 2.3 Search endpoint, parameters, pagination
- Endpoint: `GET https://api.artic.edu/api/v1/artworks/search` [5].
- Parameters [5]: `q` (search query), `query` (Elasticsearch Query DSL for complex queries), `sort`, `from`/`size` (Elasticsearch-style pagination), `facets`. Pagination also accepts `page` (1-based) and `limit` (default 12) [5]. `fields` limits the returned fields: *"We encourage you to use it because it makes your queries run faster"* [5].
- Limits [5]: *"limit cannot exceed 100. Additionally, you cannot request more than 1,000 records from a single search query through any combination of limit and page."*
- Example request (observed 2026-11-12):
  `https://api.artic.edu/api/v1/artworks/search?q=monet&limit=2&fields=id,title,artist_display,date_display,image_id`
- Response shape (key fields, observed 2026-11-12):
  ```json
  {
    "pagination": { "total": 133287, "limit": 2, "offset": 0,
                    "total_pages": 66644, "current_page": 1 },
    "data": [
      { "_score": 129.8, "id": 16568, "title": "Water Lilies",
        "date_display": "1906",
        "artist_display": "Claude Monet (French, 1840–1926)",
        "image_id": "3c27b499-af56-f0d5-93b5-a7f2f1ad5813" }
    ],
    "info": { "license_text": "...", "license_links": ["..."] },
    "config": { "iiif_url": "https://www.artic.edu/iiif/2" }
  }
  ```
- Detail: `GET /api/v1/artworks/{id}` [5].
- Image URL: `https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg`. The `843,` size is recommended because it is most likely to be cached already [5].

### 2.4 Rate limits and reliability
- *"Anonymous users are throttled to 60 requests per minute."* [5]. Live responses carried `x-ratelimit-limit: 60` and `x-ratelimit-remaining` headers (observed 2026-11-12).
- Best practices [5]: *"Cache API responses in your system when possible"*, use `fields`, batch detail lookups with `?ids=`. When scraping, *"throttle your requests to no more than one per second."*
- Weekly data dumps are available on GitHub for bulk needs [5].
- Status page / uptime SLA: not documented.

### 2.5 Storing data locally
- The API data is CC0 (except `description`, which is CC-BY 4.0) [5].
- Terms [6]: *"certain data about the museum's collections, publications, and programs has been made available through AIC's Public API under the CC0 license. You are welcome to use any images or data with the label "CC0 Public Domain Designation," or otherwise stated as made available by AIC under the CC0 license, for any purpose, including commercial and noncommercial uses, without additional permission from AIC."*
- The docs also say *"Cache API responses in your system when possible"* [5]. Storing selected records is clearly allowed. If you store `description`, credit AIC under CC-BY.

### 2.6 Errors and unavailable responses
- The docs do not include a status-code table. Error bodies observed on 2026-11-12 use a consistent JSON format `{"status": <code>, "error": "...", "detail": "..."}`:
  - **Not found:** `GET /artworks/999999999` → 404 `{"status":404,"error":"Not found","detail":"The item you requested cannot be found."}`
  - **Bad ID:** `GET /artworks/abc` → 400 `{"status":400,"error":"Invalid syntax","detail":"The identifier syntax is invalid."}`
  - **limit > 100:** 403 `{"status":403,"error":"Invalid limit","detail":"You have requested too many resources per page. Please set a smaller limit."}`
  - **Past 1,000 results** (`limit=100&page=11`): 403 `{"status":403,"error":"Invalid number of results","detail":"You have requested too many results. Please refine your parameters."}`
- **Empty search caveat (observed):** a nonsense `q` (`q=xyzzyplugh`) returned HTTP 200 with `pagination.total` equal to the entire collection (133,287) and low-score results. `q=monet&limit=0` reported the same total. Free-text `q` search therefore never comes back empty, so `total == 0` cannot be used to detect "no results". An Elasticsearch `query[term][title.keyword]=xyzzyplugh` search did return `total: 0, data: []`.
- **Rate limit exceeded:** the status code and body are not documented, and this was not tested.

---

## 3. TheMealDB

### 3.1 Data and app idea
A crowd-sourced recipe database. Each meal has a name, category, area (cuisine), instructions, thumbnail, tags, a YouTube link, and up to 20 ingredient/measure pairs [7]. A live response is shown below. **App idea:** a recipe box. Users search meals by name, save recipes, and add personal notes, ratings, "made it" dates, or tweaked ingredients, grouped into collections (e.g., "Weeknight dinners").

### 3.2 Cost, key, attribution
- *"The API and site will always remain free at point of access."* [7]
- Key: *"You can use the test API key "1" during development of your app or for educational use … However you must become a supporter if releasing publicly on an appstore."* [7]. The key is part of the URL path (`/api/json/v1/1/`). No signup is needed for the test key.
- The supporter key adds the full database *"rather than limited to 100 items"*, multi-ingredient filters, and more [7].
- **Attribution is required:** *"You can use our custom artwork in your projects but must mention us as the source of the data."* and should *"link back to our website where appropriate"* [8].

### 3.3 Search endpoint, parameters, pagination
- Endpoints [7] (all GET, test key `1`):
  - Search by name: `https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata`
  - List by first letter: `.../search.php?f=a`
  - Lookup by ID: `.../lookup.php?i=52772`
  - Random: `.../random.php`
  - Filter by ingredient, category, or area: `.../filter.php?i=chicken_breast`, `?c=Seafood`, `?a=Canadian`
  - Lists: `.../categories.php`, `.../list.php?c=list` (also `a=list`, `i=list`)
- **Pagination: none documented** [7]. Each search returns one array.
- Response shape (key fields, observed 2026-11-12):
  ```json
  { "meals": [ {
      "idMeal": "52771", "strMeal": "Spicy Arrabiata Penne",
      "strCategory": "Vegetarian", "strArea": "Italian",
      "strInstructions": "Bring a large pot of water to a boil...",
      "strMealThumb": "https://www.themealdb.com/images/media/meals/ustsqw1468250014.jpg",
      "strTags": "Pasta,Curry", "strYoutube": "https://www.youtube.com/watch?v=1IszT_guI08",
      "strIngredient1": "penne rigate", "strMeasure1": "1 pound",
      "...": "... through strIngredient20 / strMeasure20 (empty string or null when unused)",
      "strSource": null, "strCreativeCommonsConfirmed": null
  } ] }
  ```
  Ingredients are 20 flat numbered fields, not a list. All values, including `idMeal`, are strings.
- Observed on 2026-11-12: `search.php?s=chicken` and `search.php?s=` (empty) each returned 25 meals.

### 3.4 Rate limits and reliability
- Rate limit: **not documented.** The terms mention staying *"within the rate limit"* for apps but never state a number [8]. The API page gives none either [7].
- Status page / uptime: not documented. The terms say *"refunds may be issued in the event of server faults that affect the usability of the service"* [8] (applies to paid supporters).
- Caching advice: not documented.

### 3.5 Storing data locally
- Terms [8]: *"You can scrape, copy and modify any content returned from the API, as long as you use the official end points. Please do not scrape our website. You also cannot remove or alter any copyright or trademark notices."*
- *"You cannot resell our API in any way without specific permission."* [8]
- Image licensing varies by item: *"You can check the 'strCreativeCommons' tag on artwork to make sure its CC licensed."* [8]
- Conclusion: saving selected recipes locally is allowed, with credit to TheMealDB as the data source.

### 3.6 Errors and unavailable responses
- Error behavior is **not documented** [7].
- Observed on 2026-11-12. Most failures return **HTTP 200**, so you have to inspect the body:
  - **Empty search:** `search.php?s=zzqqxxnotathing` → 200 `{"meals":null}` (`null`, not `[]`).
  - **Not found by ID:** `lookup.php?i=99999999` → 200 `{"meals":null}`.
  - **Non-numeric ID:** `lookup.php?i=abc` → 200 `{"meals":"Invalid ID"}`. Here `meals` is a **string**, not a list.
  - **Unknown endpoint or invalid key path** (`/v1/2/search.php`): HTTP 404 with an **HTML** IIS error page, not JSON.
- **Rate limit exceeded:** not documented, not tested.

---

## 4. Comparison

| | Open Library | Art Institute of Chicago | TheMealDB |
|---|---|---|---|
| **Key / signup** | None [1] | None; anonymous access [5] | Test key `1` in URL; no signup for educational use [7] |
| **Search support** | Yes: `q`, `title`, `author`, `sort`, `fields` [2] | Yes: `q` plus Elasticsearch `query` DSL [5]; `q` never returns empty (observed) | Name search, first letter, single-value filters [7] |
| **Pagination** | `page`/`limit` or `offset`/`limit` [2] | `page`/`limit` (max 100/page, max 1,000 results) or `from`/`size` [5] | None [7] |
| **Rate limit** | 1 req/s (3 req/s identified) [1] | 60 req/min anonymous [5] | Not documented |
| **Local storage allowed** | Yes; "Cache responses whenever possible"; IA claims no new copyright [1][4] | Yes; CC0 (description CC-BY 4.0) [5][6] | Yes; "scrape, copy and modify" via official endpoints; attribution required [8] |
| **Attribution** | Courtesy link "appreciated" (covers) [3] | Only for `description` (CC-BY) [5] | Required [8] |
| **Error handling clarity** | Medium: 200 + `numFound:0` for empty; JSON 404; undocumented | High: consistent JSON `{status,error,detail}` (observed); undocumented table | Low: 200 + `null` or string; HTML 404; undocumented |
| **Response simplicity** | Simple; `author_name` is a list | Nested; image URL must be built from `image_id` | Very flat but 20 numbered ingredient fields; all strings |
| **Beginner friendliness** | **High** | Medium | Medium-High (simple, but quirky errors and no pagination) |

## 5. Recommendation

**Use Open Library for a beginner.** Reasons, tied to the findings above:

1. **No key, no account.** Nothing to sign up for, nothing to keep secret in settings, and no key in the URL [1].
2. **Search and pagination are simple and standard.** One GET URL with `q`, `page` (starting at 1), and `limit` [2]. The `fields` parameter keeps responses small [2].
3. **"No results" is easy to detect.** An empty search returns HTTP 200 with `numFound: 0` and `docs: []` (observed). AIC's `q` search never returns zero results (observed). TheMealDB returns `null` instead of a list (observed).
4. **The rate limit is documented and generous for a class project** (1 req/s, or 3 req/s with an identifying User-Agent) [1].
5. **Saving data locally is encouraged.** *"Cache responses whenever possible"* [1], and the Internet Archive *"does not assert any new copyright"* over the data [4].
6. **The data fits "save, then edit."** A work's stable key (e.g. `/works/OL27448W`) is a natural unique ID for a saved item. User fields (status, rating, notes, shelf) don't overlap with API fields.

Things to keep in mind: `author_name` is a list. Error codes are undocumented, so handle any non-200 response generically. Send a descriptive `User-Agent`.

**Runner-up:** TheMealDB, if the student prefers recipes. It has the flattest JSON, but it requires attribution, has no pagination, and needs extra checks for `null` / `"Invalid ID"`. **AIC** is the most rigorously licensed and has the best error bodies, but it suits a student who is comfortable building image URLs and possibly Elasticsearch queries.

## 6. Open questions / unverified

- **Rate-limit-exceeded responses** (status code, body, `Retry-After`) for all three APIs: not documented and deliberately not tested.
- **Open Library 404 content type:** the observed 404 body was JSON-shaped but had no `Content-Type` header. Whether this is consistent across endpoints is unverified.
- **Open Library general terms of service:** only the developer licensing page [4] and API page [1] were reviewed. Any broader Internet Archive terms that might apply were not checked.
- **Missing fields in Open Library search docs** (e.g. a doc without `cover_i`): in one 100-result sample, every doc had `cover_i`. Whether fields can be absent was not established from the docs.
- **TheMealDB result cap:** `s=chicken` and `s=` both returned exactly 25 meals. Whether the free key caps search results at 25 is not documented. The API page only mentions a 100-item limit on listing the full database [7].
- **TheMealDB rate limit:** referenced in the terms ("within the rate limit") but no number is published [8].
- **AIC pagination ceiling:** the docs disagree with each other. The "Scraping Data" section says *"you cannot paginate beyond 10,000 results"*, but the "Pagination" section says 1,000 [5]. A live request at `limit=100&page=11` returned 403, which confirms **1,000** (observed 2026-11-12).
- **AIC `q` relevance:** why a nonsense `q` returns the whole collection is not explained in the docs. Only the behavior was observed.
- **Status pages / uptime:** none found for any of the three APIs.
- **APIs not evaluated:** PokéAPI, TMDB, Jikan, and RAWG were not checked against their docs in this session. The reasons given in the summary for skipping them are unverified.

## References

1. Open Library, "Developers / APIs" (incl. Bulk Access, Please Do / Do Not, Rate Limits) — https://openlibrary.org/developers/api
2. Open Library, "Search API" — https://openlibrary.org/dev/docs/api/search
3. Open Library, "Covers API" — https://openlibrary.org/dev/docs/api/covers
4. Open Library, "Licensing" — https://openlibrary.org/developers/licensing
5. Art Institute of Chicago, "API Documentation" (Quick Start, Best Practices, Data Dumps, Scraping Data, Images, Copyright, Authentication, Pagination, Artworks endpoints) — https://api.artic.edu/docs/
6. Art Institute of Chicago, "Terms and Conditions" (Copyrights and Fair Use / Open Access) — https://www.artic.edu/terms
7. TheMealDB, "Free Recipe API" — https://www.themealdb.com/api.php
8. TheMealDB, "Terms of Use" — https://www.themealdb.com/terms_of_use.php

Live requests were made to `openlibrary.org`, `covers.openlibrary.org`, `api.artic.edu`, and `www.themealdb.com` on 2026-11-12 with a generic User-Agent (`student-research-client/1.0`) and no personal information.
