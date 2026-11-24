[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b15-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b15-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

A one-image front page summing up 23 November 2026: 31 stories across 6 regions.

## The day

- **AI rout hits Asia** — Kospi −3.3% to 4,708.54, sheds 161 pts; intraday −5.8%. Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.
- **US lead over China at record low** — Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.

Plus 10 more stories (Bessent/Nvidia, FBI NCIC hack, Trump on Iran, Nasdaq futures, Skubal's $450M Mets deal, Tom Jackson, states vs SpaceX, Anthropic IPO at $83/share, Poland's missile claim, Russia's nuclear-satellite claim) and 18 more in ALSO ON MONDAY, a world map with numbered pins, and a DATE CHECK box that keeps 22/21/19 November stories out of the day's news.

## How it is built

`draw.py` (Pillow) renders the 1024×1024 front page to `entry.png`. `main.py` is stdlib-only: it verifies the PNG header and copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run

```sh
python3 draw.py        # regenerate entry.png
python3 main.py        # copy entry.png to $MAKEFUN_OUTPUT_DIR (default: out/)
```

Scenes are drawn illustrations, not photographs. Sources: Reuters, AP, Bloomberg, AFP, Yonhap, BBC, WSJ, NYT, ESPN, Lowy Institute (Asia Power Index 2026).
