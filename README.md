# ToolStack — Tool Review & Comparison Site Layout

A clean, fast-loading, fully semantic HTML/CSS website template for a tool review and comparison site.

## Files

| File | Purpose |
|---|---|
| `index.html` | Main homepage with hero, category cards, review list, comparison table, and newsletter CTA |
| `style.css` | Single stylesheet — all layout, typography, and responsive rules |

## Design Decisions

### Performance
- **Zero external dependencies** — no frameworks, no icon fonts, no CDN calls
- Single CSS file, inlined critical structure via `system-ui` font stack (no web font download)
- Minimal JavaScript: 12 lines for the mobile nav toggle only
- No animations or transitions that trigger layout reflow

### Accessibility
- Semantic HTML5 elements throughout (`<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`, `<section>`)
- `aria-label`, `aria-current`, `aria-expanded`, and `aria-controls` on interactive elements
- Visible `:focus-visible` outlines for keyboard navigation
- Screen-reader-only `.sr-only` class for the email label
- Colour contrast ratios exceed WCAG AA for all text/background combinations

### Responsive Breakpoints
| Breakpoint | Behaviour |
|---|---|
| > 600px | Horizontal navigation, 3-column card grid, 3-column footer |
| ≤ 768px | Footer collapses to single column |
| ≤ 600px | Hamburger nav toggle, single-column layout throughout |

### Typography
- `clamp()` fluid type scale — no fixed breakpoints needed for headings
- `max-width: 70ch` on paragraphs for optimal line length
- `line-height: 1.7` for comfortable body text reading

## Placeholder Pages Needed
The nav links reference these files (not yet created):
- `automation-tools.html`
- `seo-tools.html`
- `hosting.html`
- `about.html`
- `contact.html`
- `privacy.html`
- `affiliate-disclosure.html`

## Usage
Open `index.html` directly in a browser — no build step, no server required.
