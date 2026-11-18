# StatusPill

A short uppercase word on a square fill that states a status.

**Markup.** `<span class="hs-pill hs-pill--ok">Live</span>`. The consumer provides the word (one or two words, e.g. Live, Check, Failed, Draft).

| Class | Fill / text | Means |
|---|---|---|
| `hs-pill--ok` | `status-ok` (Klein) / `on-klein` | Done, live, passed |
| `hs-pill--warn` | `status-warn` (chrome) / `on-chrome` | Needs a look |
| `hs-pill--err` | `status-err` (vermilion) / `surface` | Failed, blocked |
| `hs-pill--quiet` | outline `ink-soft` | Neutral: draft, archived |

- There is no green. Klein and vermilion stay apart for color-blind readers, and the word carries the meaning.
- Square corners, Recursive 500 with `--mono-axes` at 11px, letter spacing 0.06em.
