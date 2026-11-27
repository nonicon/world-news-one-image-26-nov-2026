# World News in One Image — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/nonicon/world-news-one-image-26-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/nonicon/world-news-one-image-26-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page newspaper front page summing up the world news of
**Thursday, 26 November 2026**. The image is the entry: `main.py`
copies the pre-rendered `entry.png` to the output directory.

## What the image shows

- **Lead story — Space / Asia:** Pakistan's Muhammad Zeeshan Ali is to
  become the first foreign astronaut to visit China's Tiangong space
  station, flying aboard Shenzhou-24.
- **War in Ukraine:** Russia's own figures put its war dead near
  500,000, as the United States shelves plans to use business deals
  with Russia to end the war.
- **Labour / Asia:** Bangladesh garment workers win a 36% rise in the
  minimum wage.
- **Peace / Americas:** Colombia marks ten years of its peace accord;
  the UN warns commitments remain unfinished.
- **Diplomacy / Asia:** North Korea orders Switzerland to close its
  newly opened office in Pyongyang.
- **United States:** Thanksgiving under storm clouds, as a powerful
  storm threatens the East Coast with flooding.
- **Sport / Chess:** World champion D. Gukesh defends his title
  against Javokhir Sindarov in Geneva.
- **Also today (ticker):** Petrobras unveils a $122bn plan; Venezuela
  reveals $237.5bn of public debt; an Australia–Solomon Islands
  security pact; India marks Constitution Day; the US plans new
  tariffs; Real Madrid rout PSV in the Champions League.

Every story was checked against news reported on 26 November 2026
before the image was drawn. Events from other dates were left out.

## How the image was made

`render.py` paints the front page from scratch with Pillow: masthead
and date line, a flat-illustration lead panel (rocket, space station
and the Earth), six story cards with small pictogram panels, and a
news ticker. All text is set in DejaVu / Liberation fonts. No
photographs or artwork from any other source are used.

## Running it

```sh
python3 render.py          # rebuild entry.png from the drawing code
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the Python standard library, needs no network,
and writes identical bytes on every run. The output is a 1024×1024
PNG, well under the 1 MiB limit.

## Licence

MIT — see `LICENSE`.
