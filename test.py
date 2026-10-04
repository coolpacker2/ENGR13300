#!/usr/bin/env python3
"""
svg_creases_to_dxf.py
=====================
Convert an SVG origami crease pattern into a clean single-line (centerline)
DXF for CAD / CNC / laser work (e.g. import into Fusion 360).

Pipeline (vector only, no pixel grid anywhere)
----------------------------------------------
MODE "strokes" (default, exact, recommended)
    Your crease lines are stroked paths. The path geometry IS the centerline,
    so we never need to compute one:
      1. Parse every path/line/polyline/rect/... with svgpathtools
         (group transforms are applied).
      2. Straight segments stay exact; Beziers/arcs are flattened to within
         --curve-tol.
      3. Snap near-coincident vertices (--tol).
      4. Node the network: split every segment at crossings, T-junctions,
         near-miss ends and overlaps (spatial index, so it scales).
      5. De-duplicate overlapping strokes, merge collinear chains.
      6. Write LINE entities with ezdxf.

MODE "outlines" (fallback)
    Use only when the SVG contains stroke OUTLINES (filled thin shapes, e.g.
    after Inkscape "Stroke to Path"). The centerline is estimated with a
    vector Voronoi medial axis of the densely sampled boundary, then spur
    pruned, Douglas-Peucker straightened, end-extended and noded as above.
    Treat this as an approximation. If you still have the original stroked
    paths, use "strokes".

Dependencies:  pip install svgpathtools shapely networkx ezdxf numpy scipy
(scipy is only needed for --mode outlines)

Usage:
    python svg_creases_to_dxf.py pattern.svg pattern.dxf
    python svg_creases_to_dxf.py pattern.svg pattern.dxf --scale 0.2645833
    python svg_creases_to_dxf.py outlined.svg out.dxf --mode outlines
"""
import argparse
import math
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

import ezdxf
import networkx as nx
import numpy as np
import shapely
from ezdxf import units
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree
from svgpathtools import Document, Line


# --------------------------------------------------------------------------
# Units
# --------------------------------------------------------------------------
def auto_scale(svg_file):
    """SVG user units -> mm using width + viewBox. Falls back to 1.0."""
    try:
        root = ET.parse(svg_file).getroot()
        vb, w = root.get("viewBox"), root.get("width")
        if not vb or not w:
            return 1.0
        m = re.match(r"\s*([0-9.eE+-]+)\s*([a-z%]*)", w)
        val, unit = float(m.group(1)), m.group(2)
        f = {"": 25.4 / 96, "px": 25.4 / 96, "mm": 1.0, "cm": 10.0,
             "in": 25.4, "pt": 25.4 / 72, "pc": 25.4 / 6}.get(unit)
        vbw = float(re.split(r"[,\s]+", vb.strip())[2])
        return val * f / vbw if f and vbw else 1.0
    except Exception:
        return 1.0


# --------------------------------------------------------------------------
# Path flattening
# --------------------------------------------------------------------------
def flatten_segment(seg, tol):
    """Return complex points approximating seg within tol (SVG units)."""
    if isinstance(seg, Line):
        return [seg.start, seg.end]
    n = 4
    while True:
        pts = [seg.point(k / n) for k in range(n + 1)]
        worst = max(abs(seg.point((k + 0.5) / n) - (pts[k] + pts[k + 1]) / 2)
                    for k in range(n))
        if worst <= tol or n >= 1024:
            return pts
        n *= 2


def make_converter(scale, flip_y):
    sy = -scale if flip_y else scale
    return lambda z: (z.real * scale, z.imag * sy)


def strokes_to_segments(paths, conv, curve_tol_svg):
    segs = []
    for path in paths:
        for seg in path:
            try:
                xy = [conv(z) for z in flatten_segment(seg, curve_tol_svg)]
            except Exception:
                continue
            for p, q in zip(xy, xy[1:]):
                if p != q:
                    segs.append((p, q))
    return segs


# --------------------------------------------------------------------------
# Vertex snapping + network noding
# --------------------------------------------------------------------------
class Snapper:
    """Greedy spatial-hash clustering; the first point seen is the representative."""

    def __init__(self, tol):
        self.tol, self.grid, self.pts = tol, defaultdict(list), []

    def get(self, x, y):
        c = self.tol
        cx, cy = int(math.floor(x / c)), int(math.floor(y / c))
        best, bd = None, self.tol
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for i in self.grid.get((cx + dx, cy + dy), ()):
                    d = math.hypot(self.pts[i][0] - x, self.pts[i][1] - y)
                    if d <= bd:
                        best, bd = i, d
        if best is None:
            best = len(self.pts)
            self.pts.append((x, y))
            self.grid[(cx, cy)].append(best)
        return best


def node_segments(segs, tol):
    """
    Split straight segments at every crossing / T-junction / near-miss /
    overlap endpoint and snap everything to a common vertex set.
    Returns (vertex_list, set_of_edges(i, j)).
    """
    if not segs:
        return [], set()
    A = np.array([s[0] for s in segs], float)
    B = np.array([s[1] for s in segs], float)
    n = len(segs)
    tree = STRtree([LineString([A[i], B[i]]) for i in range(n)])
    splits = [[0.0, 1.0] for _ in range(n)]

    def cross(u, v):
        return u[0] * v[1] - u[1] * v[0]

    for i in range(n):
        a, d = A[i], B[i] - A[i]
        L2 = d @ d
        L = math.sqrt(L2)
        lo, hi = np.minimum(A[i], B[i]) - tol, np.maximum(A[i], B[i]) + tol
        for j in tree.query(box(lo[0], lo[1], hi[0], hi[1])):
            if j == i:
                continue
            c, f = A[j], B[j] - A[j]
            Lj = math.hypot(*f)
            # j's endpoints lying on (within tol of) segment i -> T-junction / overlap
            for p in (A[j], B[j]):
                t = ((p - a) @ d) / L2
                if 0.0 < t < 1.0 and np.hypot(*(p - (a + t * d))) <= tol:
                    splits[i].append(t)
            # crossing (allowing ends to over/undershoot by tol)
            den = cross(d, f)
            if abs(den) > 1e-12 * L * Lj:
                t = cross(c - a, f) / den
                u = cross(c - a, d) / den
                if -tol / L <= t <= 1 + tol / L and -tol / Lj <= u <= 1 + tol / Lj:
                    splits[i].append(min(1.0, max(0.0, t)))

    snap = Snapper(tol)
    for i in range(n):                       # originals get priority as representatives
        snap.get(*A[i])
        snap.get(*B[i])
    edges = set()
    for i in range(n):
        d = B[i] - A[i]
        ids = [snap.get(*(A[i] + t * d)) for t in sorted(set(splits[i]))]
        for u, v in zip(ids, ids[1:]):
            if u != v:
                edges.add((min(u, v), max(u, v)))
    return snap.pts, edges


def merge_collinear(G, pos, dev_tol):
    """Remove degree-2 nodes that lie on the straight line between their neighbours."""
    changed = True
    while changed:
        changed = False
        for n in list(G.nodes):
            if n not in G or G.degree(n) != 2:
                continue
            a, b = list(G.neighbors(n))
            if a == b or G.has_edge(a, b):
                continue
            ab = pos[b] - pos[a]
            L = np.hypot(*ab)
            if L == 0:
                continue
            t = ((pos[n] - pos[a]) @ ab) / (L * L)
            dev = abs(ab[0] * (pos[n] - pos[a])[1] - ab[1] * (pos[n] - pos[a])[0]) / L
            if 0 < t < 1 and dev <= dev_tol:
                G.remove_node(n)
                G.add_edge(a, b)
                changed = True


def clean_network(segs, tol, dev_tol):
    pts, edges = node_segments(segs, tol)
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = {i: np.array(p) for i, p in enumerate(pts)}
    merge_collinear(G, pos, dev_tol)
    return G, pos


def graph_to_segments(G, pos):
    return [(tuple(pos[u]), tuple(pos[v])) for u, v in G.edges]


# --------------------------------------------------------------------------
# Outline mode: Voronoi medial axis of the (vector) stroke outlines
# --------------------------------------------------------------------------
def outlines_to_polygon(paths, conv, curve_tol_svg):
    rings = []
    for path in paths:
        for sub in path.continuous_subpaths():
            pts = []
            for seg in sub:
                pts += [conv(z) for z in flatten_segment(seg, curve_tol_svg)[:-1]]
            if len(pts) >= 3:
                p = Polygon(pts).buffer(0)
                if not p.is_empty and p.area > 0:
                    rings.append(p)
    if not rings:
        raise SystemExit("No closed shapes found - outlines mode needs filled outlines.")
    # even-odd nesting by containment depth: even = solid, odd = hole
    tree = STRtree(rings)
    solids, holes = [], []
    for i, p in enumerate(rings):
        depth = sum(1 for j in tree.query(p.representative_point(), predicate="within")
                    if j != i)
        (solids if depth % 2 == 0 else holes).append(p)
    geom = unary_union(solids)
    return geom.difference(unary_union(holes)) if holes else geom


def _sample_ring(coords, spacing):
    out, sv, s = [], [], 0.0
    for (x1, y1), (x2, y2) in zip(coords[:-1], coords[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        k = max(1, math.ceil(L / spacing))
        for m in range(k):
            t = m / k
            out.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
            sv.append(s + t * L)
        s += L
    return out, sv, s


def _dp(points, tol):
    """Douglas-Peucker returning kept indices."""
    keep = {0, len(points) - 1}
    stack = [(0, len(points) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = points[i], points[j]
        ab = b - a
        L = np.hypot(*ab)
        seg = points[i + 1:j]
        if L == 0:
            dist = np.hypot(*(seg - a).T)
        else:
            dist = np.abs(ab[0] * (seg[:, 1] - a[1]) - ab[1] * (seg[:, 0] - a[0])) / L
        k = int(np.argmax(dist))
        if dist[k] > tol:
            m = i + 1 + k
            keep.add(m)
            stack += [(i, m), (m, j)]
    return sorted(keep)


def simplify_chains(G, pos, tol):
    anchors = {n for n in G if G.degree(n) != 2}
    for comp in nx.connected_components(G):          # pure loops need an anchor
        if not comp & anchors:
            anchors.add(next(iter(comp)))
    H, seen = nx.Graph(), set()
    for a in anchors:
        for nb in G.neighbors(a):
            if frozenset((a, nb)) in seen:
                continue
            chain, prev, cur = [a, nb], a, nb
            seen.add(frozenset((a, nb)))
            while cur not in anchors:
                nxt = next(x for x in G.neighbors(cur) if x != prev)
                seen.add(frozenset((cur, nxt)))
                chain.append(nxt)
                prev, cur = cur, nxt
            P = np.array([pos[c] for c in chain])
            kept = [chain[i] for i in _dp(P, tol)]
            H.add_edges_from(zip(kept, kept[1:]))
    return H


def prune_spurs(G, pos, min_len):
    changed = True
    while changed:
        changed = False
        for n in [x for x in G if G.degree(x) == 1]:
            if n not in G or G.degree(n) != 1:
                continue
            path, length, prev, cur = [n], 0.0, None, n
            while True:
                nbrs = [x for x in G.neighbors(cur) if x != prev]
                if not nbrs:
                    break
                nxt = nbrs[0]
                length += float(np.hypot(*(pos[nxt] - pos[cur])))
                prev, cur = cur, nxt
                if G.degree(cur) == 2:
                    path.append(cur)
                else:
                    break
            if G.degree(cur) >= 3 and length < min_len:
                G.remove_nodes_from(path)
                changed = True


def extend_dangling_ends(G, pos, poly):
    """Medial axis stops ~half a stroke-width short of butt caps; ray-cast the end back out."""
    for n in [x for x in G if G.degree(x) == 1]:
        nb = next(iter(G.neighbors(n)))
        d = pos[n] - pos[nb]
        L = np.hypot(*d)
        if L == 0:
            continue
        d /= L
        r = poly.boundary.distance(Point(pos[n]))
        ray = LineString([pos[n], pos[n] + d * (4 * r + 1e-9)])
        inter = ray.intersection(poly)
        parts = [inter] if inter.geom_type == "LineString" else list(getattr(inter, "geoms", []))
        parts = [p for p in parts if p.geom_type == "LineString" and p.distance(Point(pos[n])) < 1e-6]
        if parts:
            end = np.array(parts[0].coords[-1])
            if np.hypot(*(end - pos[n])) > 0:
                pos[n] = end


def medial_axis_segments(poly, spacing, ratio, prune_len, simplify_tol):
    from scipy.spatial import Voronoi

    polys = list(getattr(poly, "geoms", [poly]))
    pts, ring_id, sval, rlen, rid = [], [], [], [], 0
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            c, sv, total = _sample_ring(list(ring.coords), spacing)
            pts += c
            sval += sv
            ring_id += [rid] * len(c)
            rlen += [total] * len(c)
            rid += 1
    P = np.array(pts)
    ring_id, sval, rlen = map(np.array, (ring_id, sval, rlen))
    rng = np.random.default_rng(0)                  # break cocircular degeneracies
    vor = Voronoi(P + rng.normal(scale=spacing * 1e-4, size=P.shape))
    V = vor.vertices
    inside = shapely.contains_xy(poly, V[:, 0], V[:, 1])

    G = nx.Graph()
    for (i, j), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        if v1 < 0 or v2 < 0 or not (inside[v1] and inside[v2]):
            continue
        if ring_id[i] == ring_id[j]:
            arc = abs(sval[i] - sval[j])
            arc = min(arc, rlen[i] - arc)
            if arc <= ratio * np.hypot(*(P[i] - P[j])):
                continue                              # both sites on the same side
        G.add_edge(v1, v2)
    pos = {n: V[n].copy() for n in G}

    prune_spurs(G, pos, prune_len)
    G = simplify_chains(G, pos, simplify_tol)
    extend_dangling_ends(G, pos, poly)
    return graph_to_segments(G, pos)


# --------------------------------------------------------------------------
# DXF output
# --------------------------------------------------------------------------
def write_dxf(G, pos, out_path, layer="CREASE", decimals=6):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.MM
    doc.header["$INSUNITS"] = 4                      # millimetres
    doc.layers.add(layer, color=7)
    msp = doc.modelspace()
    count = 0
    for u, v in G.edges:
        p = tuple(round(float(c), decimals) for c in pos[u])
        q = tuple(round(float(c), decimals) for c in pos[v])
        if p != q:
            msp.add_line(p, q, dxfattribs={"layer": layer})
            count += 1
    doc.saveas(out_path)
    return count


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg")
    ap.add_argument("dxf")
    ap.add_argument("--mode", choices=["strokes", "outlines"], default="strokes")
    ap.add_argument("--scale", default="auto",
                    help="SVG unit -> mm factor, or 'auto' (width/viewBox; default). "
                         "96-dpi px -> mm is 0.2645833")
    ap.add_argument("--tol", type=float, default=0.01,
                    help="snap/join tolerance in output units (mm). Gaps and overshoots "
                         "smaller than this are healed. Default 0.01")
    ap.add_argument("--curve-tol", type=float, default=0.005,
                    help="max deviation when flattening curves (mm). Default 0.005")
    ap.add_argument("--collinear-tol", type=float, default=0.002,
                    help="merge collinear chains within this deviation (mm). Default 0.002")
    ap.add_argument("--no-flip-y", action="store_true",
                    help="keep SVG's y-down orientation (default flips so DXF is not mirrored)")
    # outlines-mode only (all default to values derived from estimated stroke width)
    ap.add_argument("--spacing", type=float, help="[outlines] boundary sample spacing")
    ap.add_argument("--prune", type=float, help="[outlines] remove spurs shorter than this")
    ap.add_argument("--simplify", type=float, help="[outlines] straightening tolerance")
    ap.add_argument("--ratio", type=float, default=1.5, help="[outlines] ridge filter ratio")
    args = ap.parse_args()

    scale = auto_scale(args.svg) if args.scale == "auto" else float(args.scale)
    print(f"scale = {scale:.7g} mm per SVG unit")
    conv = make_converter(scale, not args.no_flip_y)
    paths = Document(args.svg).paths()
    print(f"parsed {len(paths)} paths")
    curve_svg = args.curve_tol / scale

    if args.mode == "strokes":
        segs = strokes_to_segments(paths, conv, curve_svg)
    else:
        poly = outlines_to_polygon(paths, conv, curve_svg)
        w = 2 * poly.area / poly.length               # thin-shape width estimate
        spacing = args.spacing or w / 4
        prune = args.prune or 2 * w
        simp = args.simplify or spacing * 0.5
        print(f"estimated stroke width {w:.4f}; spacing {spacing:.4f}")
        segs = medial_axis_segments(poly, spacing, args.ratio, prune, simp)

    print(f"{len(segs)} raw segments")
    G, pos = clean_network(segs, args.tol, args.collinear_tol)
    n = write_dxf(G, pos, args.dxf)
    print(f"wrote {n} LINE entities, {G.number_of_nodes()} vertices -> {args.dxf}")


if __name__ == "__main__":
    sys.exit(main())