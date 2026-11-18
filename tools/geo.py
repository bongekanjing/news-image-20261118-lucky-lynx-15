#!/usr/bin/env python3
"""Decode world-atlas TopoJSON into lon/lat rings and project them equirectangularly."""

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_topology(path):
    with open(path) as fh:
        return json.load(fh)


def decode_arcs(topo):
    tr = topo.get("transform")
    sx, sy = tr["scale"]
    tx, ty = tr["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def ring_from(arcs, ids):
    out = []
    for i in ids:
        pts = arcs[i] if i >= 0 else arcs[~i][::-1]
        out.extend(pts if not out else pts[1:])
    return out


def land_rings(topo):
    """Every outer ring and hole of the land layer, as lon/lat lists."""
    arcs = decode_arcs(topo)
    rings = []
    for geom in topo["objects"]["land"]["geometries"]:
        if geom["type"] == "Polygon":
            polys = [geom["arcs"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["arcs"]
        else:
            continue
        for poly in polys:
            for ring in poly:
                r = ring_from(arcs, ring)
                if len(r) > 3:
                    rings.append(r)
    return rings


def project(lon, lat, rect, lat_top=84.0, lat_bot=-58.0):
    """Equirectangular into rect=(x, y, w, h), cropping the poles."""
    x, y, w, h = rect
    px = x + (lon + 180.0) / 360.0 * w
    span = lat_top - lat_bot
    py = y + (lat_top - lat) / span * h
    return px, py


def project_win(lon, lat, rect, win):
    """Equirectangular into rect for a lon/lat window (lon0, lon1, lat0, lat1)."""
    x, y, w, h = rect
    lon0, lon1, lat0, lat1 = win
    px = x + (lon - lon0) / (lon1 - lon0) * w
    py = y + (lat1 - lat) / (lat1 - lat0) * h
    return px, py


def decimate(ring, step):
    if step <= 1:
        return ring
    out = ring[::step]
    if out[-1] != ring[-1]:
        out.append(ring[-1])
    return out


def polygons_px(rings, rect, step=1, min_area=4.0, win=None):
    """Project rings to pixels, dropping specks too small to read."""
    out = []
    for ring in rings:
        if win:
            px = [project_win(lo, la, rect, win) for lo, la in decimate(ring, step)]
        else:
            px = [project(lo, la, rect) for lo, la in decimate(ring, step)]
        if len(px) < 3:
            continue
        area = 0.0
        for i in range(len(px)):
            x1, y1 = px[i]
            x2, y2 = px[(i + 1) % len(px)]
            area += x1 * y2 - x2 * y1
        if abs(area) * 0.5 < min_area:
            continue
        out.append(px)
    return out


def bbox_of(ring):
    lons = [p[0] for p in ring]
    lats = [p[1] for p in ring]
    return min(lons), min(lats), max(lons), max(lats)
