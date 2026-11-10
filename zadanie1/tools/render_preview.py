#!/usr/bin/env python3
"""Render pliku layout.json do podgladu schematu (schemat.png) - w stylu rysunku z Logisima."""
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

L = json.load(open('/tmp/logisim/layout.json'))
COMPS, WIRES = L['components'], L['wires']

WIRE = '#0d7a2f'
BOX_FC, BOX_EC = '#e8effa', '#1f3a93'
TXT = '#111827'

fig, ax = plt.subplots(figsize=(17, 12.4), dpi=140)
ax.set_facecolor('white')

# ---------- przewody ----------
for x1, y1, x2, y2 in WIRES:
    ax.plot([x1, x2], [y1, y2], color=WIRE, lw=2.0, solid_capstyle='round', zorder=1)

# wezly (kropki) tam gdzie spotyka sie >=3 atomowych segmentow
from collections import Counter, defaultdict
cnt = Counter()
for x1, y1, x2, y2 in WIRES:
    cnt[(x1, y1)] += 1
    cnt[(x2, y2)] += 1
for p, n in cnt.items():
    if n >= 3:
        ax.add_patch(Circle(p, 3.2, color=WIRE, zorder=2))

def port_xy(c, name):
    dx, dy, _ = c['ports'][name]
    return (c['loc'][0] + dx, c['loc'][1] + dy)

def label_text(x, y, s, size=11, color=TXT, ha='center', va='center', style='normal', weight='normal'):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, style=style, weight=weight, zorder=6)

def box(cx, cy, w, h, text, fs=13, bubble_out=False, bubble_in=False):
    ax.add_patch(plt.Rectangle((cx - w/2, cy - h/2), w, h, facecolor=BOX_FC,
                               edgecolor=BOX_EC, lw=1.8, zorder=3))
    label_text(cx, cy, text, size=fs, weight='bold')
    if bubble_out:
        ax.add_patch(Circle((cx + w/2 + 3.4, cy), 3.4, facecolor='white', edgecolor=BOX_EC, lw=1.6, zorder=4))

for c in COMPS:
    k = c['kind']; x, y = c['loc']
    if k == 'pin_in':
        ax.add_patch(Polygon([(x-2, y), (x-26, y-9), (x-26, y+9)], closed=True,
                             facecolor='#fff8dc', edgecolor='#8a6d00', lw=1.6, zorder=3))
        label_text(x-30, y, c['attrs'].get('label', ''), size=13, weight='bold', ha='right')
    elif k == 'pin_out':
        ax.add_patch(Circle((x+2, y), 7, facecolor='white', edgecolor='#8a6d00', lw=1.8, zorder=3))
        label_text(x+13, y, c['attrs'].get('label', ''), size=12, weight='bold', ha='left')
    elif k == 'not':
        box(x-15, y, 30, 18, '1', bubble_out=True)
    elif k in ('and', 'or', 'xor', 'xnor'):
        n = len([p for p in c['ports'] if p.startswith('in')])
        h = max(26, (n - 1) * 10 + 22)
        sym = {'and': '&', 'or': '≥1', 'xor': '=1', 'xnor': '=1'}[k]
        box(x-25, y, 46, h, sym, bubble_out=(k == 'xnor'))
    elif k == 'mux':
        pts = [(x-30, y-16), (x-30, y+16), (x-6, y+24), (x-6, y-24)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=BOX_FC, edgecolor=BOX_EC, lw=1.8, zorder=3))
        label_text(x-17, y, 'MUX', size=8.5, weight='bold')
        label_text(x-17, y+9.5, '2:1', size=6.5)
    elif k == 'const':
        box(x, y, 18, 16, '1', fs=11)
    elif k == 'tunnel':
        lab = c['attrs'].get('label', '')
        w = 13 + 4.6 * len(lab)
        ax.add_patch(FancyBboxPatch((x-w/2, y-5), w, 10,
                                        boxstyle='round,pad=0.6,rounding_size=2.2',
                                        facecolor='#d3f9d8', edgecolor=WIRE, lw=1.2, zorder=3))
        label_text(x, y, lab, size=8, weight='bold', color='#0b3d1e')
    elif k == 'text':
        label_text(x, y, c['attrs'].get('text', ''), size=10.5, ha='left',
                   color='#374151', style='italic')


# podpisy mintermow pod bramkami AND4 (czytelnosc)
minterm_names = {3: "m3 = a'b'cd", 4: "m4 = a'bc'd'", 5: "m5 = a'bc'd",
                 6: "m6 = a'bcd'", 7: "m7 = a'bcd", 9: "m9 = ab'c'd",
                 12: "m12 = abc'd'", 14: "m14 = abcd'", 15: "m15 = abcd"}
and4_locs = {3: (350, 480), 4: (350, 580), 5: (350, 700),
             6: (590, 480), 7: (590, 580), 9: (590, 700),
             12: (830, 480), 14: (830, 580), 15: (830, 700)}
for m, (gx, gy) in and4_locs.items():
    label_text(gx-25, gy+35, minterm_names[m], size=7.8, color='#4b5563')

# linie oddzielajace sekcje
for yy in (412, 745):
    ax.plot([20, 1185], [yy, yy], ls='--', lw=1.2, color='#9ca3af', zorder=0)

ax.axhspan(0, 405, color='#f5f9ff', zorder=-2)
ax.axhspan(415, 740, color='#f7fff8', zorder=-2)
ax.set_xlim(0, 1240)
ax.set_ylim(880, 0)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout(pad=0.3)
plt.savefig('/home/user/edu_lab5/zadanie1/schemat.png', bbox_inches='tight', facecolor='white')
print('zapisano /home/user/edu_lab5/zadanie1/schemat.png')
