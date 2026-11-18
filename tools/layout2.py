#!/usr/bin/env python3
"""18 Nov 2026 front page: thirteen illustrated cards, a locator map, briefs.

Three tempos: three wide cards, ten equal cards, then the index band. Every card
runs plate / kicker / headline / dek on shared baselines so thirteen stories scan
at thumbnail size. Deks are written to the exact line budget each card is given
and the page asserts it never runs past the trim.
"""

from PIL import Image, ImageDraw

import cards
import math
import geo
from paper import (W, H, PAPER, INK, RED, GREY, RULE, HAIR, bold, reg, serif,
                   tw, tracked, tracked_w, wrap)
from plates import world_map

# --------------------------------------------------------------- content ----
# (region, beat, headline, dek, plate, lon, lat)
STORIES = [
    ("Middle East", "Iran war",
     "Kuwait and Bahrain say they repelled Iranian drones",
     "After US strikes on Qeshm Island, Tehran fired at the Gulf states "
     "hosting American bases.", cards.gulf, 47.9, 29.4),
    ("Asia", "Diplomacy",
     "Xi welcomes Trump on the eve of a three-way summit",
     "Xi met him at Shenzhen airport; Putin joins them there on Thursday.",
     cards.summit, 114.1, 22.5),
    ("Americas", "US politics",
     "House Democrats nominate Jeffries for speaker, 251-11",
     "If confirmed in January he becomes the first Black speaker.",
     cards.jeffries, -77.0, 38.9),
    ("Europe", "Ukraine war",
     "Russian drones batter the grid across five regions",
     "Strikes on Kyiv, Odesa and Kharkiv killed five people as winter nears.",
     cards.ukraine, 30.5, 50.4),
    ("Middle East", "Gaza",
     "Israeli troops push into central Gaza as the truce frays",
     "Civilians were told to leave Nuseirat and Bureij.",
     cards.gaza, 34.4, 31.4),
    ("Asia", "Disaster",
     "Cyclone Akvan strengthens on its way to Andhra",
     "A severe storm over the Bay of Bengal, ashore on Friday.",
     cards.cyclone, 84.0, 14.0),
    ("Europe", "Economy",
     "UK inflation climbs to 3.6%, a one-year high",
     "Fuel costs drove October's jump, denting a December cut.",
     cards.inflation, -1.5, 52.5),
    ("Africa", "Sudan war",
     "Amnesty: RSF drone strikes were war crimes",
     "Dozens died at El Obeid; it seeks an international inquiry.",
     cards.sudan, 30.2, 13.2),
    ("Americas", "Markets",
     "Nvidia doubles revenue to $115.8bn, then an SEC probe",
     "It beat forecasts and raised guidance; Huang stays out.",
     cards.nvidia, -122.0, 37.4),
    ("Middle East", "Israel",
     "Knesset elects Matan Kahana speaker",
     "A Netanyahu critic took the chair by 66 votes to 52.",
     cards.knesset, 35.2, 31.8),
    ("Global", "Climate",
     "COP31 deadlocks in Antalya over who pays",
     "Finance, fossil fuels and adaptation remain unresolved.",
     cards.cop31, 30.7, 36.9),
    ("Americas", "Venezuela",
     "Hegseth in Caracas as US ties resume",
     "The first Pentagon chief to visit since Maduro's ouster.",
     cards.venezuela, -66.9, 10.5),
    ("Asia", "Space",
     "China and the US launch rockets on the same day",
     "A Long March 2D left Taiyuan hours after a Falcon 9.",
     cards.space, 112.6, 37.8),
]

BRIEFS = [
    ("Israel", "Katz threatens more West Bank land seizures", 35.2, 31.9),
    ("Yemen", "UNICEF: 64 children killed since September", 44.2, 15.4),
    ("Afghanistan", "UN releases $18m for 824,000 people", 69.2, 34.5),
    ("Russia", "An-12 crash in Kemerovo kills all 19 aboard", 86.1, 55.4),
    ("Health", "WHO warns superbug resistance is worsening", 6.1, 46.2),
    ("Tech", "Waymo pulls its robotaxis off freeways", -122.4, 37.8),
    ("Finance", "Anthropic IPO priced at $70-78 a share", -122.4, 37.8),
    ("Washington", "NSA's classified network goes down", -77.0, 38.9),
    ("India", "CEC protests continue; police go to court", 77.2, 28.6),
    ("Sudan", "Darfur tribes sign a local ceasefire", 24.0, 13.0),
    ("Pakistan", "Dar draws a red line on Afghan soil", 73.1, 33.7),
    ("Nigeria", "CBN and NNPC sign a forex deal", 7.5, 9.1),
    ("Sport", "Moriyasu exits after Paraguay defeat", 139.7, 35.7),
    ("Mid-East", "Qatar and Egypt press for a Gaza summit", 51.5, 25.3),
    ("Europe", "Brussels weighs a 45bn-euro loan to Kyiv", 4.4, 50.8),
    ("Asia", "Seoul and Beijing seal a services trade deal", 127.0, 37.6),
    ("Africa", "AU: $80-125bn lost to illicit financial flows", 38.7, 9.0),
    ("Ukraine", "Zelensky proposes ten more evacuation routes", 30.5, 50.4),
    ("Britain", "Eight firms added to the Russia sanctions list", -0.1, 51.5),
    ("Climate", "2026 is on course for a record warm year", 0.0, 0.0),
    ("Mid-East", "Iran says six tankers have sunk since Friday", 56.3, 26.9),
    ("Markets", "Gold slips below $3,800 to a one-year low", -74.0, 40.7),
    ("Asia", "KOSPI gains 2.0% on a chip rebound", 127.0, 37.6),
    ("Americas", "Dow falls 848.75 points in a late selloff", -74.0, 40.7),
]

REGION_HUE = {
    "Middle East": (54, 96, 92),
    "Asia": (146, 108, 44),
    "Americas": (52, 82, 118),
    "Europe": (86, 74, 122),
    "Africa": (74, 100, 64),
    "Global": (100, 96, 88),
}

# which region hue each brief's dot takes on the map
BRIEF_REGION = {
    "Israel": "Middle East", "Yemen": "Middle East", "Mid-East": "Middle East",
    "Afghanistan": "Asia", "India": "Asia", "Pakistan": "Asia",
    "Asia": "Asia", "Sport": "Asia",
    "Russia": "Asia", "Britain": "Europe", "Europe": "Europe",
    "Ukraine": "Europe", "Health": "Europe",
    "Sudan": "Africa", "Nigeria": "Africa", "Africa": "Africa",
    "Tech": "Americas", "Finance": "Americas", "Washington": "Americas",
    "Markets": "Americas", "Americas": "Americas",
    "Climate": "Global",
}

M = 30           # page margin
GUT = 13         # gutter between cards
TRIM = H - 30    # nothing may cross this

# the continent each region belongs to, for the masthead's own count
CONTINENT = {
    "Middle East": "Asia", "Asia": "Asia", "Americas": "the Americas",
    "Europe": "Europe", "Africa": "Africa", "Oceania": "Oceania",
    "Global": None,
}


def continents():
    """The continents this page actually covers, named. Derived, never typed."""
    names = {"Africa", "the Americas", "Asia", "Europe", "Oceania"}
    seen = {CONTINENT[s[0]] for s in STORIES} - {None}
    assert seen <= names, "unknown continent: %r" % (seen - names)
    return len(seen)


def census():
    """Stories and briefs per region, counted from the content, never typed."""
    order = ["Europe", "Middle East", "Asia", "Africa", "Americas", "Global"]
    n = {k: 0 for k in order}
    for s in STORIES:
        n[s[0]] += 1
    for k, _t, _lon, _lat in BRIEFS:
        n[BRIEF_REGION[k]] += 1
    assert sum(n.values()) == len(STORIES) + len(BRIEFS), \
        "census %d != %d" % (sum(n.values()), len(STORIES) + len(BRIEFS))
    return [(k, n[k]) for k in order if n[k]]


def card_w(n, total_w):
    return (total_w - GUT * (n - 1)) / n


class Page:
    """Draws onto one canvas and remembers the lowest ink it puts down."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.bottom = 0.0

    def mark(self, y):
        self.bottom = max(self.bottom, y)


def draw_card(pg, x, y, w, plate_h, story, hs_seq, max_head, dek_lines,
              number=None):
    """One card; returns the y it ended at."""
    d = pg.d
    region, beat, head, dek, fn, lon, lat = story
    pg.img.paste(fn(int(w), int(plate_h)), (int(x), int(y)))

    # the number badge, in the region's colour, matching the pin on the map
    hue = REGION_HUE[region]
    if number is not None:
        br = 6.2
        bx, by = x + br + 1, y + plate_h - br - 1
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=hue)
        d.ellipse([bx - br, by - br, bx + br, by + br], outline=PAPER, width=1)
        d.text((bx, by + 0.3), str(number), font=bold(7.0), fill=PAPER,
               anchor="mm")

    yy = y + plate_h + 6
    tracked(d, x, yy, region.upper(), bold(7), hue, 1.1)
    kw = tracked_w(d, region.upper(), bold(7), 1.1)
    d.text((x + kw + 5, yy), "· " + beat.upper(), font=bold(7), fill=GREY)
    yy += 12

    for hs in hs_seq:
        hf = bold(hs)
        lines = wrap(d, head, hf, w)
        if len(lines) <= max_head:
            break
    lead = round(hs * 1.10)
    for ln in lines:
        d.text((x, yy), ln, font=hf, fill=INK)
        yy += lead

    if dek_lines:
        yy += 4
        dl = wrap(d, dek, reg(8.6), w)
        assert len(dl) <= dek_lines, "dek over budget: %r" % dek
        for ln in dl:
            d.text((x, yy), ln, font=reg(8.6), fill=GREY)
            yy += 11
    pg.mark(yy)
    return yy


def masthead(pg):
    d = pg.d
    d.line([(M, 18), (W - M, 18)], fill=INK, width=3)
    tracked(d, M, 25, "THE DAY IN WORLD NEWS", bold(9), INK, 1.6)
    ncon = continents()
    d.text((W - M, 26),
           "%d STORIES · %d BRIEFS · %d CONTINENTS"
           % (len(STORIES), len(BRIEFS), ncon),
           font=bold(8), fill=GREY, anchor="ra")
    d.text((M, 40), "Wednesday 18 November 2026", font=serif(52), fill=INK)
    d.text((W - M, 101), "One day, one page: what happened on 18 November.",
           font=reg(11), fill=GREY, anchor="ra")
    d.line([(M, 118), (W - M, 118)], fill=INK, width=2)

    # the region colours, as a rule under the date: the key to every badge,
    # kicker and pin below. Each block is widened by its count, so the rule is
    # also a census: where the day's weight actually fell.
    cen = census()
    total = sum(c for _k, c in cen)
    x = M
    span = W - 2 * M
    for k, c in cen:
        wseg = span * c / total
        d.rectangle([x, 122, x + wseg - 2, 127], fill=REGION_HUE[k])
        x += wseg
    # the same census in words, set apart from the numbered badges so the two
    # numbering systems on this page cannot be confused for one another
    parts = "   ".join("%s %d" % (k.upper(), c) for k, c in cen)
    tracked(d, M, 131, parts + "   = %d ITEMS" % total, bold(6.2), GREY, 0.9)
    return 141


def map_band(pg, x, y, w, h):
    """Where it happened: land, then thirteen numbered pins, dodged so no two
    collide and no numeral is covered."""
    d = pg.d
    tracked(d, x, y, "WHERE IT HAPPENED", bold(9), INK, 1.4)
    top = y + 15
    box = (x, top, w, h - 15)
    world_map(pg.img, d, box, "stone", step=1, min_area=2.0,
              fill=(142, 132, 110), scale=1)

    R = 6.6          # pin radius
    need = R * 2 + 2.6
    pos = []
    for i, s in enumerate(STORIES, start=1):
        px, py = geo.project(s[5], s[6], box)
        pos.append([px, py, s[0], i])

    # greedy placement: keep each pin at its true spot if it is free, otherwise
    # spiral outwards from it until it clears every pin already placed
    placed = []
    for p in pos:
        tx, ty = p[0], p[1]
        best = None
        for step in range(0, 60):
            rad = step * 1.9
            n = 1 if step == 0 else max(8, step * 6)
            for k in range(n):
                ang = 2 * math.pi * k / n
                cx = tx + math.cos(ang) * rad
                cy = ty + math.sin(ang) * rad
                if not (box[0] + R + 1 <= cx <= box[0] + box[2] - R - 1):
                    continue
                if not (box[1] + R + 1 <= cy <= box[1] + box[3] - R - 1):
                    continue
                if all(math.hypot(cx - q[0], cy - q[1]) >= need for q in placed):
                    best = (cx, cy)
                    break
            if best:
                break
        if best is None:
            raise AssertionError("no free slot for pin %d" % p[3])
        p[0], p[1] = best
        placed.append(p)

    mind = min(math.hypot(a[0] - b[0], a[1] - b[1])
               for i, a in enumerate(placed) for b in placed[i + 1:])
    assert mind >= need - 0.01, "pins still collide: %.2f" % mind

    # the briefs, as small unnumbered dots in their region's colour: the day's
    # whole geography, not only the thirteen leads
    dots = []
    for k, s, lon, lat in BRIEFS:
        if lon == 0.0 and lat == 0.0:
            continue                      # a story with no single place
        dx, dy = geo.project(lon, lat, box)
        hue = REGION_HUE[BRIEF_REGION[k]]
        if any(math.hypot(dx - q[0], dy - q[1]) < need * 0.92 for q in placed):
            continue                      # too near a numbered pin to add
        if any(math.hypot(dx - q[0], dy - q[1]) < 4.0 for q in dots):
            continue                      # two briefs at one place: one dot
        dots.append((dx, dy, hue))
    for dx, dy, hue in dots:
        d.ellipse([dx - 2.0, dy - 2.0, dx + 2.0, dy + 2.0], fill=hue)

    for k, (px, py, region, i) in enumerate(pos):
        hue = REGION_HUE[region]
        ox, oy = geo.project(STORIES[i - 1][5], STORIES[i - 1][6], box)
        if math.hypot(px - ox, py - oy) > 1.2:
            d.line([(ox, oy), (px, py)], fill=hue, width=1)
            d.ellipse([ox - 1.2, oy - 1.2, ox + 1.2, oy + 1.2], fill=hue)
        d.ellipse([px - R, py - R, px + R, py + R], fill=hue)
        d.text((px, py + 0.4), str(i), font=bold(7.0), fill=PAPER, anchor="mm")
    pg.mark(top + h - 15)


def legend(pg, x, y):
    """The key: the same colours the badges carry, in the same order."""
    d = pg.d
    x0 = x
    for name, col in (("Middle East", (54, 96, 92)), ("Asia", (146, 108, 44)),
                      ("Americas", (52, 82, 118)), ("Europe", (86, 74, 122)),
                      ("Africa", (74, 100, 64)), ("Global", (100, 96, 88))):
        if x - x0 > 250:
            break
        d.ellipse([x, y + 2, x + 6, y + 8], fill=col)
        d.text((x + 9, y), name, font=reg(7.0), fill=GREY)
        x += 9 + tw(d, name, reg(7.0)) + 8
    pg.mark(y + 9)


def briefs(pg, x, y, w, cols=2):
    d = pg.d
    tracked(d, x, y, "IN BRIEF", bold(9), INK, 1.4)
    bw = tracked_w(d, "IN BRIEF", bold(9), 1.4)
    d.text((x + bw + 7, y + 1), "%d more stories, one line each" % len(BRIEFS),
           font=reg(7.6), fill=GREY)
    y += 13
    d.line([(x, y), (x + w, y)], fill=RULE, width=1)
    y += 7

    cw = (w - 12 * (cols - 1)) / cols
    per = (len(BRIEFS) + cols - 1) // cols
    rh = min(13.5, (TRIM - 12 - y) / per)

    for i, (k, s, lon, lat) in enumerate(BRIEFS):
        c, r = i // per, i % per
        cx, cy = x + c * (cw + 12), y + r * rh
        d.text((cx, cy), k + " — ", font=bold(7.2), fill=RED)
        kw = tw(d, k + " — ", bold(7.2))
        lines = wrap(d, s, reg(7.2), cw - kw)
        for j, ln in enumerate(lines[:2]):
            d.text((cx + kw, cy + j * 8.6), ln, font=reg(7.2), fill=INK)
    pg.mark(y + rh * (per - 1) + 9)


def main(out_path):
    pg = Page()
    top = masthead(pg)

    # row 1: three wide cards
    cw3 = card_w(3, W - 2 * M)
    xs = [M + i * (cw3 + GUT) for i in range(3)]
    y = top + 10
    for i, (x, s) in enumerate(zip(xs, STORIES[:3]), start=1):
        b = draw_card(pg, x, y, cw3, 116, s, (19, 18, 17, 16, 15), 2, 2,
                      number=i)
    y = b + 14
    pg.d.line([(M, y - 7), (W - M, y - 7)], fill=HAIR, width=1)

    # rows 2 and 3: five equal cards each
    cw5 = card_w(5, W - 2 * M)
    xs5 = [M + i * (cw5 + GUT) for i in range(5)]
    for row in range(2):
        block = STORIES[3 + row * 5: 8 + row * 5]
        for j, (x, s) in enumerate(zip(xs5, block)):
            b = draw_card(pg, x, y, cw5, 72, s, (13, 12.5, 12, 11.5, 11), 3, 2,
                          number=4 + row * 5 + j)
        y = b + 14
        if row == 0:
            pg.d.line([(M, y - 7), (W - M, y - 7)], fill=HAIR, width=1)

    pg.d.line([(M, y - 7), (W - M, y - 7)], fill=RULE, width=2)

    # index band: map left, briefs right
    bw = 330
    map_band(pg, M, y + 3, bw, TRIM - y - 26)
    legend(pg, M, TRIM - 10)

    bx = M + bw + 20
    briefs(pg, bx, y + 2, W - M - bx, cols=2)

    # what the page left out, and why: the day's boundary, stated
    pg.d.text((M, H - 27),
              "DATE CHECK  Left out, and why: GTA VI (launches 19 Nov), and the "
              "Prague train crash, Peltola's Alaska call and the measles ruling "
              "(all 17 Nov). Qeshm is shown only as the cause of today's drones.",
              font=reg(6.8), fill=RED)
    pg.d.line([(M, H - 18), (W - M, H - 18)], fill=RULE, width=1)
    pg.d.text((M, H - 14),
              "Compiled from AP, Reuters, AFP, BBC, Al Jazeera, The Guardian, "
              "Amnesty International, IMD, ONS, NASA and Xinhua, 18 Nov 2026.",
              font=reg(6.8), fill=GREY)
    assert pg.bottom <= H - 30, "page overflows: %.1f" % pg.bottom
    pg.img.save(out_path)
    print("wrote %s %s bottom=%.1f" % (out_path, pg.img.size, pg.bottom))
    return pg.img


if __name__ == "__main__":
    main("/tmp/page.png")
