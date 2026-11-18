# Button

A solid square block, 44px tall, with the label set in Schibsted Grotesk 500.

**Markup.** `<a class="hs-btn">` for navigation, `<button class="hs-btn">` for actions. The consumer provides the label text; an icon is optional and goes before the label.

| Variant | Class | Fill / text | Use |
|---|---|---|---|
| Primary | `hs-btn` | `klein` / `on-klein` | The one main action per view: "Get in touch", "Read the post". |
| Ink | `hs-btn hs-btn--ink` | `ink` / `on-ink` | A second strong action, and the nav call to action. |
| Text | `hs-btn hs-btn--text` | underline in `ink` | A third, quiet action beside the others: "Talk to us". |

**Rules**
- One primary button per view. Put actions in `hs-actions` (gap `space-6`), primary first.
- Labels are verbs in sentence case, two or three words. No arrows or emoji in the label.
- Every button is at least 44px tall, so it is a comfortable touch target on a phone. Primary and ink buttons have `space-4` padding on the sides. Corners stay square.
- The one exception is a small inline action inside a dense header, such as Copy in a code block, where the button drops the minimum height.
- Hover darkens the fill (`klein-press`, `ink-soft`). There is no scale or bounce.
- Disabled: the `disabled` attribute (40% opacity). Say why next to it.
