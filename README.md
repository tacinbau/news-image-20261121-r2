# THE WORLD — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One day, everywhere: **143 stories from 54 regions**, all dated Saturday,
21 November 2026 — a single-page broadsheet front page.

## Inside

- **3 heroes** — Russia's mass strike on Kyiv spills into Poland
  (400+ drones, 110 missiles; NATO calls it a grave breach); the AI-led
  market rout (S&P −3.7%, Nasdaq −5.3%, Nikkei −5.1%); BepiColombo enters
  Mercury orbit at 18:24 UTC after an 8-year journey.
- **140 briefs in 3 columns** — War & Diplomacy, Americas, Middle East,
  Europe, Africa, Asia-Pacific, Markets & Business, Science & Health,
  Sport, Culture & Life. Datelines in bold, one line each, nothing clipped.
- **Market strip** — Friday 20 Nov closes, labelled as such (markets shut
  Saturday): S&P 500 6,910 −3.7%, Dow 48,147 −1.9%, Nasdaq 22,618 −5.3%.
- **Saturday in UTC** — timeline from the 00:09 Peru M6.7 quake to the
  18:24 Mercury orbit insertion.
- **Quote of the Day** — NATO chief Mark Rutte in Warsaw: "I can
  guarantee that NATO will defend every inch of Polish territory."
- **DATE CHECK footer** — every story is dated Sat 21 Nov 2026; it names
  the near-misses that were excluded (ICJ Rohingya ruling and the
  Anthropic IPO, Thu 19 Nov; UK–EU signing, Tesla Argentina, the UEFA
  draw, the EU–Indonesia deal and the Gupta sentence, Fri 20 Nov).

## How it is made

`main.py` is **stdlib-only** (`hashlib`, `math`, `os`, `struct`, `zlib`):
no PIL, no network, no third-party code. It draws a 1024×1024 RGB PNG
with an embedded 5×7 bitmap font and its own PNG encoder, and writes
only to `$MAKEFUN_OUTPUT_DIR/entry.png` — nothing is written next to
the script, so it runs cleanly from a read-only directory. Output is
deterministic: two runs produce byte-identical files.

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # writes /tmp/out/entry.png
```

## Sources

AP, Reuters, BBC, AFP, USGS, ESA, NYT, CNN — all stories checked
against live reporting dated 21 November 2026.
