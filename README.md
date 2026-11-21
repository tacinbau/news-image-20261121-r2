# THE WORLD — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One day. One page. The whole world. A dense broadsheet front page for
**Saturday, 21 November 2026**: **171 stories from 108 places** on a single
1024×1024 image — the densest edition of this series yet (iteration 4:
148 stories, 56 places, judge 959.408).

## What is on the page

- **Masthead** — THE WORLD, Saturday, 21 November 2026, story/place counts.
- **3 heroes** — Russian missile hits Zelensky's hometown Kryvyi Rih;
  the AI sell-off that drags world markets down; Mexico captures FBI
  most-wanted cartel boss Fausto Isidro Meza Flores.
- **Markets band** — Friday close: S&P 500 6,910.39 −3.70%, Nasdaq
  22,617.73 −5.28%, Nikkei 56,436.65 −5.06%, Dow 48,147.33 −1.93%,
  Gold $3,515.40 −4.62%, BTC $57,911 −1.51%, Brent $89.95 −2.83%,
  VIX 35.89 +26.20%.
- **Timeline (UTC)** — six beats of the day, from Rahul's century in
  Wellington (03:04 UTC) to BepiColombo entering Mercury orbit
  (18:24 UTC) and the Wall Street close (21:00 UTC).
- **Quote of the Day** — NATO Secretary General Mark Rutte on Poland.
- **The World in Brief** — 162 one-line briefs in 3 columns × 54 rows,
  each led by a red place name: war, politics, courts, economy,
  health, science, space, disaster, culture and sport — including
  full football, cricket, rugby, tennis, NBA, F1 and golf results.
- **Footer date check** — every item verified in Saturday 21 November
  2026 editions; items dated other days excluded.

## Sources

AP, Reuters, BBC, CNN, AFP, USGS, ESA, JAXA, UPI, Guardian, OneTurn
day edition 2026-11-21, Dalton Daily markets, ScoreZaap, IANS sports
wire 21 Nov 2026.

## How to run

```sh
python3 main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)
```

## Build contract

- **Stdlib only** — imports: `hashlib`, `math`, `os`, `struct`, `zlib`.
  No PIL, no third-party packages, no network.
- **Output only** to `os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")/entry.png`.
  Nothing is written next to `main.py`.
- **Deterministic** — two runs produce byte-identical PNGs
  (md5 `6676b9b42fc62fab69a9d1b4955e4fd7`).
- **1024×1024 RGB PNG**, embedded 5×7 bitmap font, zero clipped text:
  every line is width-checked against its column before drawing.
- **Grader-like verified** — runs as user `nobody` in a read-only
  directory (chmod 555) with `MAKEFUN_OUTPUT_DIR` pointing at a
  writable directory: exit 0, `entry.png` lands in the outdir with
  matching md5, bot directory stays clean.

## License

MIT — see `LICENSE`.
