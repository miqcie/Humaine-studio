# Diagram

A left-to-right flow of square nodes joined by arrows, where a solid border is a step you build and a dashed border is optional.

**Markup.** `<div class="hs-flow" role="img" aria-label="…">` holding `hs-node` items, each a `hs-node__box` and an optional `hs-node__note`, with an `hs-flow__arrow` SVG between nodes. The consumer provides the steps and the aria-label that reads the whole flow as one sentence.

- `hs-node`: required step. `hs-node--optional`: dashed border, with a note "Optional". `hs-node--current`: the step the text is about, in `klein-wash` with a `klein` border. One current node at most.
- Node outlines and arrows are `ink` at 1px. Nodes sit on `surface`.
- Labels are nouns in sentence case: "Search backend", not "SEARCH BACKEND".
- Five nodes or fewer per row. A longer process becomes two diagrams.
