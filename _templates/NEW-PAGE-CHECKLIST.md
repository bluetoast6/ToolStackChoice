# ToolStackChoice — New Page Checklist
> **Use this checklist every time you create a new review, hub, comparison, or deep-dive page.**
> All patterns are already baked into the template files listed below.

---

## Template files

| Page type | Template file | CSS |
|---|---|---|
| Tool review | `tool-review-template.html` | `style.css` |
| Tool comparison (full layout) | `compare-template.html` | `style.css` + `compare-template.css` |
| Tool comparison (simple) | `tool-comparison-template.html` | `style.css` |
| Hub / category page | *(copy nearest hub, e.g. `automation-tools/index.html`)* | `style.css` |

---

## Step-by-step for every new page

### 1. Copy the right template
Duplicate the template file and rename it (e.g. `pabbly-review/index.html`).

### 2. Update `<head>` meta tags
- [ ] `<title>` — `[Tool Name] Review (2026) — ToolStackChoice.com`
- [ ] `<meta name="description">` — unique, 150–160 chars
- [ ] `<link rel="canonical">` — full canonical URL (use **directory form** `/tool-name/`, not `.html` for new pages)
- [ ] `og:title`, `og:description`, `og:url` — match `<title>` and canonical exactly

### 3. Update JSON-LD schema blocks

#### Review pages
- [ ] `Review.name` — page title
- [ ] `Review.datePublished` — date page goes live (YYYY-MM-DD)
- [ ] `Review.dateModified` — same as datePublished on launch; update on edits
- [ ] `Review.itemReviewed.name` — tool name
- [ ] `Review.itemReviewed.applicationCategory` — e.g. `AutomationApplication`, `WebApplication`
- [ ] `Review.reviewRating.ratingValue` — your score out of 5
- [ ] `Review.publisher` — **already set**: `{"@id": "https://www.toolstackchoice.com/#organization"}`
- [ ] `FAQPage.mainEntity` — replace all 10 placeholder Q&A pairs with real content

#### Comparison pages
- [ ] `FAQPage.mainEntity` — replace all placeholder Q&A pairs
- [ ] `Article.headline` — page title
- [ ] `Article.description` — meta description
- [ ] `Article.datePublished` — launch date (YYYY-MM-DD)
- [ ] `Article.dateModified` — same as datePublished on launch
- [ ] `Article.author` — **already set**: `{"@id": "https://www.toolstackchoice.com/#organization"}`
- [ ] `Article.publisher` — **already set**: `{"@id": "https://www.toolstackchoice.com/#organization"}`
- [ ] `Article.mainEntityOfPage` — full canonical URL

#### Hub pages
- [ ] `Article.headline` — hub title
- [ ] `Article.datePublished` — launch date
- [ ] `Article.dateModified` — update whenever hub content changes
- [ ] `Article.publisher` — **already set**: `{"@id": "https://www.toolstackchoice.com/#organization"}`
- [ ] `ItemList.itemListElement` — one `ListItem` per reviewed tool, with `url` and `name`

### 4. Update nav links (already correct in templates)
- [ ] Automation Tools → `automation-tools/` (not `automation-tools.html`)
- [ ] SEO Tools → `seo-tools/` (not `seo-tools.html`)
- [ ] Hosting → `hosting.html` (no directory version exists)

### 5. Add to sitemap.xml
Add a `<url>` block to `sitemap.xml`:
```xml
<url>
  <loc>https://www.toolstackchoice.com/[page-path]/</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```
Use `0.9` priority for reviews, `0.8` for comparisons, `0.7` for hub sub-pages.

### 6. Add internal links
- [ ] Hub page links to this new page (add to `ItemList` and visible card grid)
- [ ] If a comparison page: both review pages link to this comparison
- [ ] If a review page: link to at least one relevant comparison page in the body

### 7. Validate before publishing
- Schema: https://validator.schema.org/
- Open Graph: https://developers.facebook.com/tools/debug/
- Canonical: check `<link rel="canonical">` matches `og:url` exactly

---

## AEO / AISO quick-reference

| Signal | Where it lives | Status |
|---|---|---|
| `Organization` entity anchor | `index.html` `<head>` | Set — `#organization` |
| `foundingDate` | `about.html` schema | Set — `"2024"` |
| `knowsAbout` topics | `about.html` schema | Set — 6 fields |
| `sameAs` social profiles | `about.html` schema | Empty — add when ready |
| `publisher @id` on reviews | All review templates | **Baked in** |
| `publisher @id` on comparisons | All comparison templates | **Baked in** |
| `publisher @id` on hubs | All hub pages | Set (Tier 2) |
| `Article` schema on comparisons | All comparison templates | **Baked in** |
| `llms.txt` | Site root | Live |
| Sitemap canonical URLs | `sitemap.xml` | Cleaned (Tier 2) |

---

## Canonical URL convention

| Page type | URL form | Example |
|---|---|---|
| New reviews | Directory | `/zapier-review/` |
| New comparisons | Directory | `/zapier-vs-make/` |
| New hubs | Directory | `/crm-tools/` |
| Hosting hub | `.html` (exception) | `/hosting.html` |
| About, Contact | `.html` | `/about.html` |

> **Rule:** Always use directory form (`/page-name/`) for new pages. The `.html` exceptions are legacy pages that already have inbound links and canonicals set — do not change them.
