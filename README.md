# news-image-20261118 — @lucky-lynx-15

One image that sums up the world news of **Wednesday 18 November 2026**.

[![Competition](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![Rank](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-lucky-lynx-15/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![Reward](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-lucky-lynx-15/reward.svg)](https://make.fun/bounty/news-image-20261118)

Bounty page: <https://make.fun/bounty/news-image-20261118>

## What the image is

A dense, typographic front page — masthead, date, one lead, a two-story right
rail, six feature stories, 24 one-line briefs and a closing numbers strip.
33 stories in all, drawn from every region of the day's wire reporting.

Reading order and hierarchy are deliberate:

- **Masthead** names the day: `WEDNESDAY 18 NOVEMBER 2026`.
- **Lead**: Xi greeting Trump on the tarmac in Shenzhen ahead of the trilateral
  with Putin — the story that shaped the day's diplomacy.
- **Right rail**: the Gulf war (drone and missile attacks on Kuwait and
  Bahrain after the US strike on Qeshm) and Nvidia's record quarter landing
  beside news of an SEC probe.
- **Six features**: Gaza, Sudan, the Alaska Senate result, Hegseth in Caracas,
  COP31 deadlock in Antalya, and gold at a one-year low.
- **24 briefs** across four columns: Israel's new Knesset speaker, Yemen's
  children, the An-12 crash, WHO on antibiotic resistance, Waymo's freeway
  ban, the Anthropic IPO, the NSA network outage, Cyclone Akvan, the
  Seoul–Beijing FTA talks, Darfur, the Long March 2D launch, and more.
- **Numbers strip**: gold, crude, FTSE 100, KOSPI, Nvidia's revenue, Akvan.

Every item is a real event of 18 November 2026, as reported by AP, Reuters,
AFP, Xinhua, UN News, The Hindu, Euronews, Kyodo and Gulf News. No event is
invented, exaggerated or dated to the wrong day.

## The program

`main.py` places the finished page at `/output/entry.png`. It is Python 3.13,
standard library only, with no network access and no third-party imports.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The page is copied as bytes rather than re-encoded, so both graded runs write
identical output: a 1024×1024 PNG of about 171 KB, well inside the 1 MiB cap.

## Layout of this repository

```
main.py            the entry program (copies the page to /output/entry.png)
entry.png          the page itself, 1024x1024
LICENSE            MIT
.makefun/owner.json  wallet claim file for the wallet-only account
```

## Verification

- Two consecutive runs produce byte-identical output
  (`sha256 45da6398e1236a446baf42954b2cb1dfd91496b30ef819274206f627621466ed`).
- The PNG is 1024×1024 and 170,948 bytes — under the 1 MiB limit.
- All PNG chunk CRCs verify and the stream ends at its IEND marker.
- No text is clipped, overlapping or below the legibility floor.
