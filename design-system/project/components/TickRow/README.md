# TickRow

A row of small squares that counts or marks progress, with a short stat beside it; SID's square markers, which also echo the Mondrian mark.

**Markup.** `<div class="hs-ticks">` holding `<div class="hs-ticks__row" role="img" aria-label="…">` of empty `<i>` elements and a `<span class="hs-ticks__stat">`. The consumer provides the count, the state of each square, and an aria-label that states the number ("3 of 8 steps done").

- Squares are `tick` (10px) on a `space-4` gap.
- **State is shape first, color second**, so it reads in grayscale and for color-blind readers:
  - default: solid `ink`, for a plain count
  - `is-on`: solid `klein`, done
  - `is-off`: hollow, 1px `ink-soft` outline, not yet
  - `is-signal`: a `chrome` square inside a 1px `ink` ring, the one thing to look at (one per view). The ring is what tells it apart: in Klein Night, chrome and the lifted Klein are both light (1.3:1)
- Do not mix plain `ink` squares and `is-on` squares in one row: they are only 1.7:1 apart.
- Never more than about 12 squares. For more, write the number.
- The stat is plain text: "12 posts since 2021", "3 of 8 steps done". No icons.
