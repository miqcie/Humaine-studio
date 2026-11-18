# TopNav

The site header: lockup on the left, a few text links, and one ink-block call to action on the right.

**Markup.** `<nav class="hs-nav" aria-label="Main">` holding the Lockup, a `<ul>` of links, and an `hs-btn hs-btn--ink`. The consumer provides the links (four at most) and marks the current one with `aria-current="page"`.

- Links are `ink`, Schibsted Grotesk 500 at 15px, no underline until hover.
- The current page gets a 2px `klein` underline. That is the only Klein in the header, so keep the call to action ink, not Klein.
- Vertical padding `space-6`; it wraps on narrow screens. Use the page's side gutter (at least `space-4`).
- No background fill, no shadow, no bottom border. Whitespace separates it from the page.
