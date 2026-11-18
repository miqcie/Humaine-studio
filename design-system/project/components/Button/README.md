# Button

A solid square block that fits tight to its label, taken from SID's "highlight" button.

**Markup.** `<a class="hs-btn">` for navigation, `<button class="hs-btn">` for actions. The consumer provides the label text; an icon is optional and goes before the label.

| Variant | Class | Fill / text | Use |
|---|---|---|---|
| Primary | `hs-btn` | `klein` / `on-klein` | The one main action per view: "Get in touch", "Read the post". |
| Ink | `hs-btn hs-btn--ink` | `ink` / `on-ink` | A second strong action, and the nav call to action. |
| Text | `hs-btn hs-btn--text` | underline in `ink` | A third, quiet action beside the others: "Talk to us". |

**Rules**
- One primary button per view. Put actions in `hs-actions` (gap `space-6`), primary first.
- Labels are verbs in sentence case, two or three words. No arrows or emoji in the label.
- Padding is 0.25em on the sides and zero top and bottom; the line height makes the block. Do not add padding or round the corners.
- Hover darkens the fill (`klein-press`, `ink-soft`). There is no scale or bounce.
- Disabled: the `disabled` attribute (40% opacity). Say why next to it.
