# THE WORLD — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tacinbau/news-image-20261121-r2/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page summing up Saturday, 21 November 2026:
**123 stories, 25 regions, one day.**

## What is on the page

- **Hero stories** — COP31 in overtime (Antalya), missiles over Riyadh,
  Wall Street rout
- **Markets strip** — Friday close: S&P 500 −3.70%, Nasdaq −5.28%,
  Dow −1.93%, gold, bitcoin, Nvidia, Anthropic, Taiwan Taiex
- **Top stories grid** — 61 stories across Ukraine, Russia, China,
  Turkiye, the Middle East, Mexico, Peru, India, the Philippines,
  South Africa, the UK, the USA, France and more
- **The day in brief** — 54 more items: sport, culture, tech, health
- **Timeline in UTC** — Peru M6.7 quake, Riyadh intercepts, GTA VI,
  COP31, BepiColombo at Mercury, Chapo Isidro captured
- **Quote of the day** — "Putin is a killer." — Volodymyr Zelenskyy, Kyiv
- **Region tally + date check** — every item first reported
  Sat 21 Nov 2026; items from other dates excluded

## Run it

Stdlib only — no Pillow, no network, no fonts from disk.
Text is rendered with an embedded 5x7 bitmap font and the PNG is
encoded by hand (zlib + struct).

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
```

Writes `$MAKEFUN_OUTPUT_DIR/entry.png` — a deterministic 1024x1024
RGB PNG. Two runs produce identical bytes.

## Sources

AP · Reuters · BBC · CNN · AFP · USGS · ESA · Schwab · Arab News ·
GMA · Hindustan Times · NY Post

## License

MIT — see [LICENSE](LICENSE).
