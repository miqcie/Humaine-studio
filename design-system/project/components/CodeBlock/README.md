# CodeBlock

A square code block on `sunken`, with an optional mono header that names the language or file.

**Markup.** `<figure>` holding an optional `<div class="hs-code__head">` and a `<pre class="hs-code"><code>`. Wrap tokens in `<span class="k">` (keywords, `klein`), `<span class="s">` (strings, `ink-soft`) and `<span class="c">` (comments, `mute` italic). The consumer provides the code; highlighting is optional. Inline code uses `<code class="hs-inline">`.

- Three token colors only. Vermilion is not used here (it reads 4.2:1 on `sunken`).
- The block scrolls sideways inside itself; the page never does.
- A copy button, if any, is an `hs-btn hs-btn--text` in the header.
