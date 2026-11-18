# TickRow

A row of small solid squares that counts or marks progress, with a short stat beside it; SID's square markers, which also echo the Mondrian mark.

**Markup.** `<div class="hs-ticks">` holding `<div class="hs-ticks__row" role="img" aria-label="…">` of empty `<i>` elements and a `<span class="hs-ticks__stat">`. The consumer provides the count, which squares are on, and an aria-label that states the number ("3 of 8 steps done").

- Squares are `tick` (10px) on a `space-4` gap. Default `ink`; `is-on` = `klein`; one `is-signal` (`chrome`) at most per view, for the one thing to look at.
- Never more than about 12 squares. For more, write the number.
- The stat is plain text: ">1T tokens in production", "6 posts since 2021". No icons.
