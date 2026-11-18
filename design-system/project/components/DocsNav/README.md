# DocsNav

The docs layout from SID's research center: a 16rem sidebar with search and a page list, and a content column held to `measure`.

**Markup.** `<div class="hs-docs">` with `<aside class="hs-docs__side">` and `<main class="hs-docs__main">`. The sidebar holds the Lockup or a section title, an `hs-search` field (an `<input>` and an `hs-kbd` hint), and a `<ul>` of links. The consumer provides the pages and sets `aria-current="page"` on the open one.

- The open page is a solid `ink` block with `on-ink` text, like SID. Hover is a `klein-wash` tint.
- Sidebar ground is `surface` with a `rule` hairline on its right edge. Content sits on `ground`.
- Page title in `title`, an italic one-line summary under it in `body` and `ink-soft`, sections in `title-sm`.
- Below 640px the sidebar stacks above the content.
- The search field's border is `ink-soft` (a control border, 10:1). Show the shortcut as text (⌘K) and wire it in the page.
