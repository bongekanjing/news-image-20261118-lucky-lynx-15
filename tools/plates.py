#!/usr/bin/env python3
"""Vector plates for the 18 Nov 2026 front page.

Every plate answers the story's own question -- where, how much, or what kind --
with a shape rather than a category icon. Drawn on a 4x supersample and reduced
so edges land clean at thumbnail size.
"""

import math

from PIL import Image, ImageDraw

import geo
from paper import font

SS = 4  # supersample factor


# ---------------------------------------------------------------- palette ----
CREAM = (246, 242, 232)
INK = (24, 22, 20)
RED = (162, 30, 24)
GREY = (110, 103, 94)

PLATE = {
    "teal": (206, 224, 220),
    "sand": (233, 220, 198),
    "sage": (214, 224, 206),
    "sky": (208, 221, 234),
    "peach": (238, 214, 199),
    "lilac": (221, 214, 232),
    "stone": (226, 222, 213),
    "mint": (206, 228, 214),
}

DEEP = {
    "teal": (54, 96, 92),
    "sand": (128, 102, 62),
    "sage": (74, 100, 64),
    "sky": (52, 82, 118),
    "peach": (140, 74, 48),
    "lilac": (86, 74, 122),
    "stone": (100, 96, 88),
    "mint": (48, 104, 72),
}

_LAND = None


def land():
    global _LAND
    if _LAND is None:
        topo = geo.load_topology(str(_HERE_DATA / "land-110m.json"))
        _LAND = geo.land_rings(topo)
    return _LAND


from pathlib import Path

_HERE_DATA = Path(__file__).resolve().parent / "data"
if not _HERE_DATA.is_dir():
    _HERE_DATA = Path(__file__).resolve().parent.parent / "data"


# ------------------------------------------------------------- primitives ----
def new_plate(w, h, tone):
    im = Image.new("RGB", (w * SS, h * SS), PLATE[tone])
    return im, ImageDraw.Draw(im)


def done(im, w, h):
    return im.resize((w, h), Image.LANCZOS)


def poly(d, pts, fill=None, outline=None, width=1):
    p = [(x * SS, y * SS) for x, y in pts]
    d.polygon(p, fill=fill, outline=outline)
    if outline and width > 1:
        d.line(p + [p[0]], fill=outline, width=int(width * SS), joint="curve")


def ellipse(d, cx, cy, rx, ry=None, fill=None, outline=None, width=1):
    ry = rx if ry is None else ry
    box = [(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS]
    d.ellipse(box, fill=fill, outline=outline,
              width=max(1, int(width * SS)))


def line(d, pts, fill, width=1.5, dash=None):
    p = [(x * SS, y * SS) for x, y in pts]
    if dash:
        on, off = dash
        segs = []
        carry = 0.0
        for i in range(len(p) - 1):
            x1, y1 = p[i]
            x2, y2 = p[i + 1]
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue
            t = 0.0
            while t < dist:
                if carry < on:
                    step = min(on - carry, dist - t)
                    a = (x1 + dx * t / dist, y1 + dy * t / dist)
                    b = (x1 + dx * (t + step) / dist, y1 + dy * (t + step) / dist)
                    segs.append((a, b))
                    carry += step
                else:
                    step = min(off - (carry - on), dist - t)
                    carry += step
                t += step
                if carry >= on + off:
                    carry = 0.0
        for a, b in segs:
            d.line([a, b], fill=fill, width=max(1, int(width * SS)))
        return
    d.line(p, fill=fill, width=max(1, int(width * SS)), joint="curve")


def rect(d, x, y, w, h, fill=None, outline=None, width=1, r=0):
    box = [x * SS, y * SS, (x + w) * SS, (y + h) * SS]
    if r:
        d.rounded_rectangle(box, radius=r * SS, fill=fill, outline=outline,
                            width=max(1, int(width * SS)))
    else:
        d.rectangle(box, fill=fill, outline=outline,
                    width=max(1, int(width * SS)))


_ALIAS = {
    "sansb": "DejaVuSans-Bold.ttf",
    "sans": "DejaVuSans.ttf",
    "serifb": "DejaVuSerif-Bold.ttf",
    "serif": "DejaVuSerif.ttf",
}


def text(d, xy, s, size, fill, fnt="sansb", anchor="la", track=0.0):
    f = font(_ALIAS.get(fnt, fnt), max(6, int(size * SS)))
    x, y = xy[0] * SS, xy[1] * SS
    if track:
        for ch in s:
            d.text((x, y), ch, font=f, fill=fill, anchor=anchor)
            x += d.textlength(ch, font=f) + track * SS
        return
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def label(d, xy, s, size, fill, w, h, fnt="sansb", anchor="la", pad=3.0):
    """Text kept inside the plate: a label that would cross an edge is nudged
    back in rather than sheared off by the card boundary."""
    f = font(_ALIAS.get(fnt, fnt), max(6, int(size * SS)))
    tw_ = d.textlength(s, font=f) / SS
    th_ = size
    x, y = xy
    if anchor[0] == "r":
        x -= tw_
    elif anchor[0] == "m":
        x -= tw_ / 2
    if anchor[1] == "s":
        y -= th_
    elif anchor[1] == "m":
        y -= th_ / 2
    x = min(max(pad, x), w - pad - tw_)
    y = min(max(pad, y), h - pad - th_)
    text(d, (x, y), s, size, fill, fnt, "la")


def arrow(d, p1, p2, fill, width=2.0, head=5.0):
    line(d, [p1, p2], fill, width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for s in (0.5, -0.5):
        a = ang + math.pi + s
        line(d, [p2, (p2[0] + math.cos(a) * head, p2[1] + math.sin(a) * head)],
             fill, width)


def world_map(img, d, rect_box, tone, win=None, step=1, fill=None,
              min_area=6.0, alpha=None, scale=None):
    """Landmasses of the world (or a lon/lat window) into rect_box, clipped.

    rect_box is in logical (unscaled) coordinates. `scale` is how many device
    pixels the target image has per logical pixel -- SS for a plate being drawn
    on a supersampled canvas, 1 for the finished page.
    """
    scale = SS if scale is None else scale
    x, y, w, h = rect_box
    body = fill or DEEP[tone]
    layer = Image.new("RGB", (max(1, int(w * SS)), max(1, int(h * SS))),
                      PLATE[tone])
    ld = ImageDraw.Draw(layer)
    for p in geo.polygons_px(land(), (0, 0, w, h), step=step,
                             min_area=min_area, win=win):
        ld.polygon([(px * SS, py * SS) for px, py in p], fill=body)
    if scale != SS:
        layer = layer.resize((max(1, int(w * scale)),
                              max(1, int(h * scale))), Image.LANCZOS)
    if alpha is not None:
        layer = Image.blend(
            Image.new("RGB", layer.size, PLATE[tone]), layer, alpha)
    img.paste(layer, (int(x * scale), int(y * scale)))
    return layer
