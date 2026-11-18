#!/usr/bin/env python3
"""The thirteen story plates: one drawing per story, each answering its own
question (where / how much / what kind) instead of standing in for a category.
"""

import math

from PIL import Image, ImageDraw

import geo
import plates as P
from plates import (SS, CREAM, INK, RED, GREY, PLATE, DEEP, new_plate, done,
                    poly, ellipse, line, rect, text, label, arrow, world_map)


# 1 ------------------------------------------------- Gulf: drones at Kuwait --
def gulf(w, h):
    im, d = new_plate(w, h, "teal")
    win = (30.0, 62.0, 20.0, 36.0)  # lon/lat box: the Gulf
    world_map(im, d, (0, 0, w, h), "teal", win=win, min_area=2.0)
    # water tone behind: the plate already reads as sea
    for lon, lat, name in ((47.9, 29.4, "KUWAIT"), (50.6, 26.1, "BAHRAIN")):
        x, y = geo.project_win(lon, lat, (0, 0, w, h), win)
        ellipse(d, x, y, 3.4, fill=RED)
        label(d, (x, y - 7), name, 5.4, INK, w, h, "sansb", "mm")
    # Iran's coast, the launch side
    ix, iy = geo.project_win(56.3, 26.9, (0, 0, w, h), win)
    ellipse(d, ix, iy, 2.6, fill=INK)
    label(d, (ix, iy + 9), "QESHM", 5.2, INK, w, h, "sansb", "mm")
    # drone tracks from Qeshm to both targets
    for lon, lat in ((47.9, 29.4), (50.6, 26.1)):
        tx, ty = geo.project_win(lon, lat, (0, 0, w, h), win)
        line(d, [(ix, iy), (tx, ty)], RED, 1.0, dash=(3.0, 2.4))
    # a drone glyph on the longer track
    mx, my = (ix + geo.project_win(47.9, 29.4, (0, 0, w, h), win)[0]) / 2, \
             (iy + geo.project_win(47.9, 29.4, (0, 0, w, h), win)[1]) / 2
    for a in (0, 60, 120):
        r = math.radians(a)
        ellipse(d, mx + math.cos(r) * 3.2, my + math.sin(r) * 3.2, 1.5,
                fill=INK)
    # tanker at Hormuz, kept inside the plate
    tx, ty = geo.project_win(56.5, 26.4, (0, 0, w, h), win)
    tx = min(max(tx, 8.0), w - 8.0)
    ty = min(max(ty, 6.0), h - 12.0)
    poly(d, [(tx - 5, ty + 4), (tx + 5, ty + 4), (tx + 3.6, ty + 8),
             (tx - 3.6, ty + 8)], fill=INK)
    rect(d, tx - 2.4, ty, 3.2, 4, fill=INK)
    return done(im, w, h)


# 2 --------------------------------------------- Shenzhen: the three leaders --
def summit(w, h):
    im, d = new_plate(w, h, "sky")
    base = h * 0.78
    # skyline behind
    x = w * 0.02
    for t in (0.16, 0.26, 0.20, 0.34, 0.24, 0.30, 0.18, 0.28, 0.14):
        bw = w * 0.085
        rect(d, x, base - h * t, bw * 0.84, h * t, fill=(176, 194, 214))
        x += bw
    rect(d, 0, base, w, h - base, fill=DEEP["sky"])
    # three flags, one per leader
    flags = ((0.18, (200, 60, 50)), (0.50, (40, 60, 110)), (0.82, (120, 132, 148)))
    for fx, col in flags:
        cx = w * fx
        line(d, [(cx, base - h * 0.02), (cx, base - h * 0.44)], INK, 1.3)
        rect(d, cx, base - h * 0.44, w * 0.10, h * 0.10, fill=col)
    # three seats at one table, seen from the front
    ty = base + h * 0.015
    rect(d, w * 0.08, ty, w * 0.84, h * 0.075, fill=(226, 214, 196), r=2)
    for fx in (0.18, 0.50, 0.82):
        cx = w * fx
        ellipse(d, cx, ty - h * 0.030, w * 0.021, w * 0.021, fill=INK)
        poly(d, [(cx - w * 0.030, ty), (cx + w * 0.030, ty),
                 (cx + w * 0.022, ty - h * 0.048),
                 (cx - w * 0.022, ty - h * 0.048)], fill=INK)
    label(d, (3, 3), "SHENZHEN", 5.8, INK, w, h)
    label(d, (w - 3, 3), "THURSDAY", 5.0, DEEP["sky"], w, h, "sansb", "ra")
    return done(im, w, h)


# 3 ------------------------------------------ Jeffries: the speaker nomination --
def jeffries(w, h):
    """House chamber seen from the well: the party vote, 251 to 11."""
    im, d = new_plate(w, h, "sky")
    # the chamber's stepped benches, in section: five rising arcs
    cx, cy = w * 0.50, h * 1.45
    for i in range(5):
        r = (0.44 + i * 0.075) * w
        d.arc([cx - r, cy - r, cx + r, cy + r], 208, 332,
              fill=(84, 76, 64), width=1)
    # members as short ticks along the two front benches, ayes then nays
    ay, ny = 251, 11
    seats = 62
    for i in range(seats):
        t = i / (seats - 1.0)
        ang = 214 + t * 112
        rad = 0.46 * w
        x = cx + rad * math.cos(math.radians(ang))
        y = cy + rad * math.sin(math.radians(ang))
        if i < seats * ay / (ay + ny):
            rect(d, x - 0.5, y - 2.4, 1.0, 4.8, fill=(46, 74, 116))
        else:
            rect(d, x - 0.5, y - 2.4, 1.0, 4.8, fill=(150, 78, 62))
    # the tally, as the vote itself
    text(d, (w * 0.5, h * 0.30), "%d" % ay, 27, (46, 74, 116), "serifb", "mm")
    text(d, (w * 0.5, h * 0.44), "AYE", 5.6, GREY, "sansb", "mm")
    text(d, (w * 0.84, h * 0.30), "%d" % ny, 13, (150, 78, 62), "serifb", "mm")
    text(d, (w * 0.84, h * 0.38), "NO", 5.0, GREY, "sansb", "mm")
    label(d, (3, 3), "HOUSE", 5.4, INK, w, h, "sansb", "la")
    return done(im, w, h)


# 4 ------------------------------------- Ukraine: drones against the grid --
def ukraine(w, h):
    im, d = new_plate(w, h, "sky")
    # sea is the plate; land is the darker mass
    win = (22.0, 42.0, 44.0, 54.0)
    world_map(im, d, (0, 0, w, h), "sky", win=win, min_area=1.0,
              fill=(206, 198, 182))
    cities = [(30.5, 50.45, "KYIV", (40.2, 52.6)),
              (30.7, 46.5, "ODESA", (38.4, 47.0)),
              (36.2, 50.0, "KHARKIV", (40.0, 51.4))]
    for lon, lat, nm, src in cities:
        cx, cy = geo.project_win(lon, lat, (0, 0, w, h), win)
        sx, sy = geo.project_win(src[0], src[1], (0, 0, w, h), win)
        # inbound drone vector, arrowhead landing short of the city
        dx, dy = cx - sx, cy - sy
        ln = max(1e-6, math.hypot(dx, dy))
        arrow(d, (sx, sy), (cx - dx / ln * 5, cy - dy / ln * 5), RED, 1.0, 3.6)
        ellipse(d, cx, cy, 2.4, fill=CREAM, outline=INK, width=0.8)
        label(d, (cx, cy + 5), nm, 4.8, INK, w, h, "sansb", "ma")
    # a struck substation: a bolt over a broken line
    bx, by = w * 0.16, h * 0.80
    poly(d, [(bx, by), (bx + 5, by), (bx + 1.5, by + 5),
             (bx + 6, by + 5), (bx - 2, by + 13), (bx + 0.5, by + 6.5),
             (bx - 3.5, by + 6.5)], fill=RED)
    return done(im, w, h)


# 5 ----------------------------------------------------- Gaza: truce at risk --
def gaza(w, h):
    im, d = new_plate(w, h, "sand")
    base = h * 0.80
    # a street of ruined blocks, upper floors sheared off
    xs = [0.03, 0.16, 0.28, 0.44, 0.57, 0.70, 0.84]
    ht = [0.46, 0.30, 0.52, 0.24, 0.40, 0.28, 0.50]
    jag = [0.06, 0.14, 0.04, 0.10, 0.07, 0.12, 0.05]
    for x0, t, j in zip(xs, ht, jag):
        bx = w * x0
        bw = w * 0.105
        poly(d, [(bx, base), (bx + bw, base),
                 (bx + bw, base - h * (t - j)),
                 (bx + bw * 0.62, base - h * t),
                 (bx + bw * 0.34, base - h * (t - j * 0.6)),
                 (bx, base - h * (t - j * 0.3))], fill=DEEP["sand"])
        # window rows, punched out
        for r in range(int(t * 6)):
            yy = base - h * (t * 0.86) + r * h * 0.052
            if yy < base - 4:
                for c in range(2):
                    rect(d, bx + bw * (0.18 + c * 0.42), yy, bw * 0.22,
                         h * 0.026, fill=PLATE["sand"])
    rect(d, 0, base, w, h - base, fill=(214, 196, 168))
    # an armoured column entering from the left
    tx, ty = w * 0.07, base - h * 0.055
    rect(d, tx, ty, w * 0.20, h * 0.050, fill=INK)
    rect(d, tx + w * 0.05, ty - h * 0.032, w * 0.10, h * 0.034, fill=INK)
    line(d, [(tx + w * 0.16, ty - h * 0.032),
             (tx + w * 0.26, ty - h * 0.050)], INK, 1.6)
    for c in range(3):
        ellipse(d, tx + w * (0.04 + c * 0.06), ty + h * 0.050,
                max(1.8, w * 0.012), fill=INK)
    # movement east, into the city
    arrow(d, (w * 0.30, base - h * 0.085), (w * 0.40, base - h * 0.085),
          RED, 1.2, 3.4)
    label(d, (w - 3, h - 3), "NUSEIRAT", 5.2, DEEP["sand"], w, h, "sansb", "rs")
    return done(im, w, h)


# 6 -------------------------------------------------- Cyclone Akvan: track --
def cyclone(w, h):
    im, d = new_plate(w, h, "sky")
    win = (74.0, 96.0, 6.0, 24.0)
    world_map(im, d, (0, 0, w, h), "sky", win=win, min_area=1.0)
    # the storm: a spiral
    cx, cy = w * 0.56, h * 0.44
    for band in (1.0, 0.72, 0.46):
        pts = []
        for i in range(70):
            t = i / 69.0
            ang = t * math.pi * 3.6
            r = (w * 0.13) * band * (1 - t * 0.78)
            pts.append((cx + math.cos(ang) * r,
                        cy + math.sin(ang) * r * 0.82))
        line(d, pts, DEEP["sky"], 1.1)
    ellipse(d, cx, cy, 2.2, fill=RED)
    # forecast track to the Andhra coast
    tx, ty = geo.project_win(80.9, 16.4, (0, 0, w, h), win)
    line(d, [(cx, cy), (tx, ty)], RED, 1.2, dash=(3.4, 2.6))
    ellipse(d, tx, ty, 3.0, fill=CREAM, outline=RED, width=1.0)
    label(d, (tx, ty + 10), "AP", 4.8, INK, w, h, "sansb", "mm")
    label(d, (3, 3), "BAY OF BENGAL", 5.6, INK, w, h)
    return done(im, w, h)


# 7 ------------------------------------------------------- UK inflation 3.6 --
def inflation(w, h):
    im, d = new_plate(w, h, "peach")
    # a pump glyph
    px, py = w * 0.06, h * 0.40
    rect(d, px, py, w * 0.14, h * 0.46, fill=INK, r=2)
    rect(d, px + 3, py + 4, w * 0.08, h * 0.13, fill=PLATE["peach"])
    line(d, [(px + w * 0.14, py + 8), (px + w * 0.21, py + 8),
             (px + w * 0.21, py + h * 0.34)], INK, 1.2)
    # a rising stair: each month higher than the last
    base_y = h * 0.86
    vals = [0.14, 0.20, 0.17, 0.26, 0.31, 0.42]
    bw = w * 0.082
    x = w * 0.36
    for i, v in enumerate(vals):
        bh = h * v
        rect(d, x, base_y - bh, bw * 0.70, bh,
             fill=RED if i == len(vals) - 1 else DEEP["peach"])
        x += bw
    text(d, (w * 0.36, h * 0.10), "3.6%", 14, RED, "serifb", "la")
    label(d, (w * 0.36, h * 0.285), "HIGHEST IN A YEAR", 4.8, INK, w, h)
    label(d, (3, 3), "UK · OCT", 5.4, INK, w, h)
    return done(im, w, h)


# 8 ------------------------------------------------ Sudan: drones on a city --
def sudan(w, h):
    im, d = new_plate(w, h, "sage")
    win = (26.0, 35.0, 9.0, 18.0)
    world_map(im, d, (0, 0, w, h), "sage", win=win, min_area=1.0,
              fill=(196, 210, 186))
    ex, ey = geo.project_win(30.2, 13.2, (0, 0, w, h), win)
    bw = max(6.0, w * 0.045)
    # the town, one roof missing where a strike landed
    hit = {(0, 1), (1, 1), (2, 2)}
    for i in range(9):
        c, r = i % 3, i // 3
        bx = ex - bw * 2.6 + c * bw * 1.35
        by = ey - bw * 0.4 + r * bw * 1.15
        if (c, r) in hit:
            continue
        rect(d, bx, by, bw, bw * 0.78, fill=DEEP["sage"])
        rect(d, bx + 1, by + 1, bw * 0.34, bw * 0.3, fill=(196, 210, 186))
    # rubble and fire where the roofs were
    for c, r in hit:
        bx = ex - bw * 2.6 + c * bw * 1.35
        by = ey - bw * 0.4 + r * bw * 1.15
        for k in range(4):
            poly(d, [(bx + k * bw * 0.26, by + bw * 0.72),
                     (bx + k * bw * 0.26 + bw * 0.18, by + bw * 0.40),
                     (bx + k * bw * 0.26 + bw * 0.30, by + bw * 0.74)],
                 fill=DEEP["sage"])
        ellipse(d, bx + bw * 0.45, by + bw * 0.44, max(1.6, w * 0.009), fill=RED)
    # a quadcopter: four arms in an X, rotor discs, a body
    dx, dy = ex + bw * 0.3, ey - bw * 3.0
    aw = max(4.0, w * 0.028)
    for ax, ay in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        line(d, [(dx, dy), (dx + ax * aw, dy + ay * aw * 0.8)], INK, 1.0)
        ellipse(d, dx + ax * aw, dy + ay * aw * 0.8, aw * 0.52, aw * 0.16,
                fill=INK)
    ellipse(d, dx, dy, aw * 0.34, aw * 0.24, fill=INK)
    # its descent vector, arrowhead landing on the struck block
    tx, ty = ex + bw * 0.45, ey + bw * 0.34
    line(d, [(dx, dy + aw * 0.3), (tx, ty - 4)], RED, 0.9, dash=(2.4, 2.2))
    arrow(d, (tx - 0.5, ty - 8), (tx, ty - 1.5), RED, 0.9, 2.6)
    label(d, (ex, ey + bw * 2.5), "EL OBEID", 5.4, INK, w, h, "sansb", "ma")
    return done(im, w, h)


# 9 ------------------------------------------------- Nvidia: a doubling, then --
def nvidia(w, h):
    im, d = new_plate(w, h, "stone")
    # chip die with pins
    cx, cy = w * 0.22, h * 0.46
    s_ = min(w, h) * 0.15
    for i in range(5):
        off = -s_ * 0.6 + i * s_ * 0.3
        rect(d, cx - s_ - 3, cy + off - 1, 3, 2, fill=DEEP["stone"])
        rect(d, cx + s_, cy + off - 1, 3, 2, fill=DEEP["stone"])
        rect(d, cx + off - 1, cy - s_ - 3, 2, 3, fill=DEEP["stone"])
        rect(d, cx + off - 1, cy + s_, 2, 3, fill=DEEP["stone"])
    rect(d, cx - s_, cy - s_, s_ * 2, s_ * 2, fill=DEEP["stone"], r=1.5)
    rect(d, cx - s_ * 0.5, cy - s_ * 0.5, s_, s_, fill=PLATE["stone"], r=1)
    # the doubling
    pts = [(w * 0.46 + i / 4.0 * w * 0.22,
            h * 0.72 - i / 4.0 * h * 0.42) for i in range(5)]
    line(d, pts, (40, 96, 60), 2.2)
    text(d, (w * 0.46, h * 0.78), "$115.8bn", 8.6, INK, "serifb", "la")
    text(d, (w * 0.46, h * 0.855), "+103% YOY", 5.2, (40, 96, 60), "sansb", "la")
    # then the probe: a magnifier over a red band on the right
    gx, gy = w * 0.80, h * 0.40
    r = min(w, h) * 0.13
    ellipse(d, gx, gy, r, r, outline=RED, width=2.0)
    line(d, [(gx + r * 0.72, gy + r * 0.72),
             (gx + r * 1.65, gy + r * 1.65)], RED, 2.4)
    label(d, (gx, gy + r * 2.5), "SEC", 6.4, RED, w, h, "sansb", "ma")
    label(d, (gx, gy + r * 2.5 + 9), "PROBE", 4.8, INK, w, h, "sansb", "ma")
    return done(im, w, h)


# 10 ------------------------------------------------ Knesset: a new speaker --
def knesset(w, h):
    im, d = new_plate(w, h, "lilac")
    # the chamber: three tiers of seats in an arc, government side in red
    cx, cy = w * 0.50, h * 1.02
    for ring, rr in enumerate((0.62, 0.47, 0.32)):
        n = (16, 12, 8)[ring]
        for i in range(n):
            t = (i + 0.5) / n
            ang = math.pi + t * math.pi
            sx = cx + math.cos(ang) * w * rr
            sy = cy + math.sin(ang) * h * rr * 0.82
            if sy > h * 0.94:
                continue
            ellipse(d, sx, sy, max(1.8, w * 0.009), fill=DEEP["lilac"])
    # the speaker's chair, raised at the centre
    pw, ph = w * 0.11, h * 0.30
    rect(d, cx - pw / 2, h * 0.30, pw, ph * 0.62, fill=DEEP["lilac"], r=2)
    rect(d, cx - pw * 0.34, h * 0.30 + ph * 0.62, pw * 0.68, ph * 0.38,
         fill=DEEP["lilac"])
    rect(d, cx - pw * 0.26, h * 0.34, pw * 0.52, ph * 0.22, fill=PLATE["lilac"])
    # the vote, as a bar: 66 for, 52 against, of 120
    vx, vy, vh = w * 0.14, h * 0.10, h * 0.075
    vw = w * 0.72
    unit = vw / 120.0
    rect(d, vx, vy, unit * 66, vh, fill=RED)
    rect(d, vx + unit * 66, vy, unit * 54, vh, fill=(178, 172, 190))
    label(d, (vx + 2, vy + vh / 2 - 3), "66", 6.4, CREAM, w, h)
    label(d, (vx + vw - 2, vy + vh / 2 - 3), "52", 6.4, INK, w, h, "sansb", "ra")
    return done(im, w, h)


# 11 --------------------------------------------------- COP31: still split --
def cop31(w, h):
    im, d = new_plate(w, h, "mint")
    # the table, seen from above, with a gap down the middle where the money
    # question stops the talks
    tx, ty, tw_, th_ = w * 0.08, h * 0.42, w * 0.84, h * 0.34
    gap = w * 0.075
    rect(d, tx, ty, (tw_ - gap) / 2, th_, fill=DEEP["mint"], r=2)
    rect(d, tx + (tw_ + gap) / 2, ty, (tw_ - gap) / 2, th_, fill=DEEP["mint"], r=2)
    # delegations seated along both long sides
    for side in (0, 1):
        yy = ty - h * 0.055 if side == 0 else ty + th_ + h * 0.055
        for i in range(9):
            cx = tx + tw_ * (0.055 + i * 0.115)
            if abs(cx - (tx + tw_ / 2)) < gap * 0.6:
                continue
            ellipse(d, cx, yy, max(1.5, w * 0.010), fill=INK)
    # the gap: a torn seam with a coin hung over it, unresolved
    for i in range(9):
        yy = ty + th_ * (0.04 + i * 0.115)
        line(d, [(tx + tw_ / 2 - gap * 0.34, yy),
                 (tx + tw_ / 2 - gap * 0.10, yy + th_ * 0.05)], RED, 0.9)
        line(d, [(tx + tw_ / 2 + gap * 0.10, yy),
                 (tx + tw_ / 2 + gap * 0.34, yy + th_ * 0.05)], RED, 0.9)
    cx, cy = tx + tw_ / 2, ty + th_ / 2
    ellipse(d, cx, cy, w * 0.043, w * 0.043, fill=RED)
    label(d, (cx, cy - 0.4), "$", 9.0, CREAM, w, h, "serifb")
    # two arrows pulling away from it, the deadlock
    arrow(d, (cx - w * 0.055, cy - h * 0.02), (cx - w * 0.16, cy - h * 0.09),
          INK, 1.1, 3.6)
    arrow(d, (cx + w * 0.055, cy - h * 0.02), (cx + w * 0.16, cy - h * 0.09),
          INK, 1.1, 3.6)
    label(d, (3, 3), "ANTALYA", 5.8, INK, w, h)
    return done(im, w, h)


# 12 --------------------------------------------------- Venezuela: a visit --
def venezuela(w, h):
    im, d = new_plate(w, h, "sand")
    win = (-74.0, -58.0, 0.0, 14.0)
    world_map(im, d, (0, 0, w, h), "sand", win=win, min_area=1.0,
              fill=(206, 186, 158))
    cx, cy = geo.project_win(-66.9, 10.5, (0, 0, w, h), win)
    ellipse(d, cx, cy, 2.6, fill=RED)
    label(d, (cx + 5, cy - 9), "CARACAS", 5.2, INK, w, h)
    # a government aircraft on approach, with its flight path in
    px, py = w * 0.62, h * 0.30
    line(d, [(w * 0.99, h * 0.06), (px + 9, py - 3)], RED, 1.0, dash=(3.0, 2.4))
    # fuselage, swept wing, tail
    poly(d, [(px - 12, py), (px + 8, py - 2.6), (px + 14, py),
             (px + 8, py + 2.6), (px - 12, py)], fill=INK)
    poly(d, [(px - 1, py), (px - 9, py + 8), (px - 4, py + 0.5)], fill=INK)
    poly(d, [(px - 1, py), (px - 9, py - 7), (px - 4, py - 0.5)], fill=INK)
    poly(d, [(px - 12, py), (px - 16, py - 5), (px - 13, py)], fill=INK)
    return done(im, w, h)


# 13 ------------------------------------------------- Space: two launches --
def space(w, h):
    im, d = new_plate(w, h, "lilac")
    ground = h * 0.88
    rect(d, 0, ground, w, h - ground, fill=DEEP["lilac"])
    # two launch pads, one Chinese and one American
    for i, (bx, col, scale) in enumerate(((w * 0.36, RED, 1.0),
                                          (w * 0.64, CREAM, 0.86))):
        bh = h * 0.44 * scale
        top = ground - bh
        # body
        poly(d, [(bx - 4.2, ground - h * 0.04), (bx + 4.2, ground - h * 0.04),
                 (bx + 4.2, top + 7), (bx, top), (bx - 4.2, top + 7)],
             fill=col)
        # fins
        poly(d, [(bx - 4.2, ground - h * 0.13), (bx - 8.5, ground - h * 0.03),
                 (bx - 4.2, ground - h * 0.04)], fill=col)
        poly(d, [(bx + 4.2, ground - h * 0.13), (bx + 8.5, ground - h * 0.03),
                 (bx + 4.2, ground - h * 0.04)], fill=col)
        # exhaust plume
        for k in range(3):
            poly(d, [(bx - 3.2 + k * 2.4, ground - h * 0.04),
                     (bx - 1.4 + k * 2.4, ground + h * 0.05),
                     (bx + 0.4 + k * 2.4, ground - h * 0.04)], fill=RED if col == CREAM else (240, 226, 206))
        # gantry
        line(d, [(bx - 9, ground), (bx - 9, ground - h * 0.30)], INK, 1.0)
        line(d, [(bx - 9, ground - h * 0.24), (bx - 4.4, ground - h * 0.24)],
             INK, 1.0)
    # stars
    for sx, sy in ((0.10, 0.14), (0.24, 0.07), (0.50, 0.10), (0.78, 0.09),
                   (0.90, 0.20), (0.18, 0.30), (0.62, 0.20)):
        ellipse(d, w * sx, h * sy, 0.7, fill=CREAM)
    return done(im, w, h)


PLATES = [gulf, summit, jeffries, ukraine, gaza, cyclone, inflation, sudan,
          nvidia, knesset, cop31, venezuela, space]
