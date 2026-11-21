# THE WORLD — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page visual newspaper for 21 November 2026, drawn from scratch by
`main.py` using **only the Python standard library** — no Pillow, no network,
no third-party packages. It renders a 1024×1024 PNG with its own embedded
5×7 bitmap font and its own PNG encoder.

## What is on the page

- **148 stories, 56 places, 1 day** — 3 lead stories (COP31 overtime in
  Antalya, Russia's renewed mass strikes on Ukraine, the Wall Street AI rout),
  130 one-line briefs in 3 columns, a "By the Numbers" strip (Friday close:
  S&P 500 6,910 −3.70%, Nasdaq 22,618 −5.28%, Nvidia $125.53 −14%, gold
  $3,539, bitcoin below $60,000), a UTC timeline, and a Quote of the Day.
- **Facts verified live** from AP, Reuters, BBC, CNN, AFP, USGS, ESA,
  ATP Tour, IMD and UN News for Saturday 21 November 2026. A DATE CHECK in
  the footer names the other-dated items deliberately excluded (ICJ Myanmar
  ruling 19 Nov, US–Venezuela military ties 18 Nov, South Sudan vote delay
  18 Nov, UK settlement sanctions 18 Nov, Gaza Board of Peace warning
  18 Nov, Anthropic IPO debut 19 Nov).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
# writes /output/entry.png (1024x1024 RGB, deterministic)
```

The program writes **only** to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`/output`) and never writes next to its own source file, so it runs cleanly
from a read-only directory.

## Files

- `main.py` — the whole newspaper (stdlib-only: `os`, `struct`, `zlib`,
  `hashlib`, `math`)
- `entry.png` — reference render (md5 `2e812ed9fc714fde44635002c5c1d561`)
- `README.md`, `LICENSE`, `prompt.txt`

## License

MIT — see `LICENSE`.
