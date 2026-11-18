# DataTable

A table separated by hairline rules, with a mono header on `sunken` and tabular figures.

**Markup.** `<table class="hs-table">` with `<thead>` and `<tbody>`. Add `class="num"` to number cells and their header so they right-align. Add `class="is-current"` to the one row the text is about (`klein-wash`). The consumer provides the rows and a `<caption>` or a nearby heading.

- Row rules are `rule` at 1px. No vertical lines, no zebra stripes, no outer box.
- Numbers use tabular lining figures and a true minus sign (−).
- Status cells use StatusPill, never a colored word alone.
- Wrap wide tables in a container with `overflow-x: auto`.
