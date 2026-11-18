# Link

An underlined inline link whose underline thickness follows the text weight, and thickens on hover.

**Markup.** `<a class="hs-link" href="…">` inside running text. The consumer provides the link text, which names where it goes ("the SID-2 documentation"), never "click here".

- `hs-link`: `klein` text, for links inside body copy.
- `hs-link hs-link--quiet`: inherits the text color (`ink` or `ink-soft`), for footers and captions where Klein would be one accent too many.
- The underline is always visible. Hover thickens it to about 0.1em and moves to `klein-press`. Focus shows the 2px `focus` outline.
- External links open in the same tab unless they leave a task the reader is in the middle of.
