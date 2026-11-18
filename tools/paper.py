#!/usr/bin/env python3
"""Dev tool: render the 18 Nov 2026 front page PNG (build machine only).

Bands are measured, not assumed: each band's height comes from its content at
the chosen type size, and the whole stack must fit the sheet before drawing.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W = H = 1024
PAPER = (246, 242, 232)
INK = (24, 22, 20)
RED = (150, 26, 22)
GREY = (90, 84, 76)
RULE = (168, 160, 148)
HAIR = (208, 202, 192)
NAVY = (22, 48, 82)

HERE = Path(__file__).resolve().parent
# the build tree keeps fonts beside tools/; the shipped entry keeps them inside
# tools/, so try both and use whichever exists
FONTS = next((p for p in (HERE / "fonts", HERE.parent / "fonts") if p.is_dir()),
             HERE / "fonts")
_cache = {}


def font(n, s):
    k = (n, s)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(str(FONTS / n), s)
    return _cache[k]


def serif(s):
    return font("DejaVuSerif-Bold.ttf", s)


def bold(s):
    return font("DejaVuSans-Bold.ttf", s)


def reg(s):
    return font("DejaVuSans.ttf", s)


def tw(d, s, f):
    return d.textlength(s, font=f)


def tracked(d, x, y, s, f, fill, tr):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tr


def tracked_w(d, s, f, tr):
    return sum(d.textlength(c, font=f) + tr for c in s) - (tr if s else 0)


def wrap(d, s, f, w):
    out, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if not cur or tw(d, t, f) <= w:
            cur = t
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def block_h(d, kick, head, dek, w, hs, ds, max_head, max_dek, k_size=10):
    """Measured height of kicker + headline + dek, or None if it won't fit."""
    hf = bold(hs)
    hlines = wrap(d, head, hf, w)
    if len(hlines) > max_head:
        return None
    lead = round(hs * 1.08)
    dh = 0
    dlines = []
    if dek:
        df = reg(ds)
        dlines = wrap(d, dek, df, w)
        if len(dlines) > max_dek:
            return None
        dh = 6 + len(dlines) * round(ds * 1.34)
    return dict(kick=kick, hf=hf, hlines=hlines, lead=lead, df=reg(ds),
                dlines=dlines, dlead=round(ds * 1.34), k_size=k_size,
                h=k_size + 5 + len(hlines) * lead + dh, hs=hs, ds=ds)


def draw_block(d, x, y, b, color_k=RED):
    tracked(d, x, y, b["kick"].upper(), bold(b["k_size"]), color_k, 1.4)
    yy = y + b["k_size"] + 5
    for ln in b["hlines"]:
        d.text((x, yy), ln, font=b["hf"], fill=INK)
        yy += b["lead"]
    if b["dlines"]:
        yy += 6
        for ln in b["dlines"]:
            d.text((x, yy), ln, font=b["df"], fill=GREY)
            yy += b["dlead"]
    return yy
