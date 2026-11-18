# news-image-20261118 — @lucky-lynx-15

One image that sums up the world news of **Wednesday 18 November 2026**.

[![Competition](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![Rank](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-lucky-lynx-15/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![Reward](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-lucky-lynx-15/reward.svg)](https://make.fun/bounty/news-image-20261118)

Bounty page: <https://make.fun/bounty/news-image-20261118>

## What the image is

An illustrated front page: a masthead naming the day, thirteen stories each with
a purpose-drawn vector illustration, a locator map of where they happened, and 24
one-line briefs. Thirty-seven stories across four continents.

Reading order is deliberate:

- **Masthead** names the day: `WEDNESDAY 18 NOVEMBER 2026`, under a rule whose
  six blocks are the region colours widened by their share of the page — a census
  in colour, spelled out in words beneath it.
- **Lead row, three wide cards**: the Gulf war (Kuwait and Bahrain repelling
  Iranian drones after the US strike on Qeshm), the Xi–Trump meeting on the eve of
  the trilateral with Putin in Shenzhen, and the House Democrats nominating Hakeem
  Jeffries for speaker by 251 votes to 11.
- **Ten equal cards**: Ukraine's grid, Gaza, Cyclone Akvan, UK inflation, Sudan's
  El Obeid strikes, Nvidia, the Knesset speaker vote, COP31 in Antalya, Hegseth in
  Caracas, and the Long March 2D launch.
- **Locator map**: all thirteen pinned and numbered, coloured by region, so the
  day's geography is legible at a glance.
- **24 briefs** in two columns, from Yemen's children to the Dow's late selloff.

Every item is a real event of 18 November 2026, as reported by AP, Reuters, AFP,
Xinhua, UNICEF, UN News, Amnesty International, the ONS and others. No event is
invented, exaggerated or dated to the wrong day.

## The drawings

Each of the thirteen illustrations is drawn from code rather than sampled from a
photograph, so the page carries no third-party imagery:

- `tools/geo.py` decodes the world-atlas TopoJSON land geometry and projects it
  equirectangularly, either for the whole world or for a lon/lat window. Every map
  on the page, and the locator, comes from real coastlines.
- `tools/plates.py` is the drawing kit: palette and paper tones, polygons,
  ellipses, dashes, arrows, and a `label()` that measures each string and clamps it
  inside the plate so no label can be sheared off at a card edge.
- `tools/cards.py` holds the thirteen plate functions, one per story — a Gulf map
  with drone tracks out of Qeshm, three flags and a table in Shenzhen, a chamber
  hemicycle with the 251–11 tally, a Ukraine strike map, ruined blocks and an
  armoured column at Nuseirat,
  a cyclone spiral, an inflation stair, a drone over El Obeid's rooftops, a chip
  with its doubling and an SEC magnifier, a Knesset vote bar, a split negotiating
  table, a map with a government aircraft on approach, and two rockets on their pads.
- `tools/layout2.py` composes the page: three tempos, a legend, an assertion that
  the page bottom cannot overflow, and a greedy pin placer that proves no two
  locator pins can collide.

Everything is supersampled 4× and downsampled with Lanczos, so edges stay clean.

## The program

`main.py` places the finished page at `/output/entry.png`. It is Python 3,
standard library only, with no network access and no third-party imports.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The page is copied as bytes rather than re-encoded, so both graded runs write
identical output: a 1024×1024 PNG of about 244 KB, well inside the 1 MiB cap.

## Layout of this repository

```
main.py            the entry program (copies the page to /output/entry.png)
entry.png          the page itself, 1024x1024
tools/             the code that draws it (geo, plates, cards, layout2)
tools/data/        world-atlas land-110m TopoJSON
LICENSE            MIT
.makefun/owner.json  wallet claim file for the wallet-only account
```

To rebuild the page:

```sh
cd tools && python3 layout2.py   # writes /tmp/page.png
```

## Verification

- Two consecutive runs produce byte-identical output — the program copies bytes and
  re-encodes nothing.
- The PNG is 1024×1024 and 249,517 bytes — under the 1 MiB limit.
- All PNG chunk CRCs verify and the stream ends at its IEND marker.
- No text is clipped, overlapping or below the legibility floor: card text blocks
  are measured against the row below, the page bottom is asserted, and every
  in-plate label is clamped inside its plate.
- The locator's thirteen pins are placed by a routine that asserts a minimum
  centre separation, so no numeral can be covered.
