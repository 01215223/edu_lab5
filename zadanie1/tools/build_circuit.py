#!/usr/bin/env python3
"""
Generator + symulator pliku .circ (Logisim-Evolution) dla zadania 1:
  f(a,b,c,d) = Sum m(3,4,5,6,7,9,12,14,15)
Rozwiniecie Shannona: poziom 1 - b, poziom 2 - c, multipleksery 2:1.
Skladnia pliku i geometria portow odtworzone na podstawie zrodla Logisim-Evolution v5.0.0.
"""
import itertools, json, sys
from collections import defaultdict

# ---------- punkty i porty ----------

def dy_two():    return [-20, 20]
def dy_three():  return [-20, 0, 20]
def dy_four():   return [-20, -10, 10, 20]
def dy_nine():   return [-40 - (-10) * 0]  # placeholder, real calc below

def gate_dy(n):
    # Logisim AbstractGate.getInputOffset, size=MEDIUM(50)
    if n <= 3:
        if n <= 2:
            skipStart, skipDist, skipLowerEven = -10, 20, 20
        else:
            skipStart, skipDist, skipLowerEven = -10, 20, 20
        if n % 2 == 1:
            return [skipStart * (n - 1) + skipDist * i for i in range(n)]
        arr = [skipStart * n + skipDist * i for i in range(n)]
        for i in range(n):
            if i >= n // 2:
                arr[i] += skipLowerEven
        return arr
    elif n == 4:
        skipStart, skipDist, skipLowerEven = -5, 10, 10   # size 50 < 60
        arr = [skipStart * n + skipDist * i for i in range(n)]
        for i in range(n):
            if i >= n // 2:
                arr[i] += skipLowerEven
        return arr
    else:
        skipStart, skipDist = -5, 10
        if n % 2 == 1:
            return [skipStart * (n - 1) + skipDist * i for i in range(n)]
        arr = [skipStart * n + skipDist * i for i in range(n)]
        for i in range(n):
            if i >= n // 2:
                arr[i] += 10
        return arr

# ---------- model komponentu ----------

class Comp:
    def __init__(self, cid, kind, loc, attrs=None, ports=None):
        self.id = cid
        self.kind = kind          # 'pin_in','pin_out','not','and','or','xor','xnor','mux','const','tunnel','text'
        self.loc = loc            # (x, y)
        self.attrs = attrs or {}
        self.ports = ports or {}  # name -> (dx, dy, direction)  direction: 'in'|'out'|'inout'

    def abs_port(self, name):
        dx, dy, _ = self.ports[name]
        return (self.loc[0] + dx, self.loc[1] + dy)

COMPS = []
_id = 0
def add(kind, loc, attrs=None, ports=None, name=None):
    global _id
    _id += 1
    c = Comp(name or f"{kind}{_id}", kind, loc, attrs, ports)
    COMPS.append(c)
    return c

def pin_in(x, y, label):
    return add('pin_in', (x, y), {'label': label}, {'p': (0, 0, 'out')})

def pin_out(x, y, label):
    return add('pin_out', (x, y), {'type': 'output', 'facing': 'west', 'label': label}, {'p': (0, 0, 'in')})

def not_gate(x, y):
    return add('not', (x, y), {}, {'in': (-30, 0, 'in'), 'out': (0, 0, 'out')})

def gate(kind, n, x, y, attrs=None):
    dy = gate_dy(n)
    ports = {}
    for i, d in enumerate(dy):
        ports[f'in{i}'] = (-50, d, 'in')
    ports['out'] = (0, 0, 'out')
    a = dict(attrs or {})
    if n != 2:
        a['inputs'] = str(n)
    return add(kind, (x, y), a, ports)

def const1(x, y):
    return add('const', (x, y), {'value': '1'}, {'out': (0, 0, 'out')})

def mux21(x, y):
    return add('mux', (x, y), {}, {'in0': (-30, -10, 'in'), 'in1': (-30, 10, 'in'),
                                   'sel': (-20, 20, 'in'), 'out': (0, 0, 'out')})

def tunnel(x, y, label, facing='east'):
    return add('tunnel', (x, y), {'label': label, 'facing': facing}, {'p': (0, 0, 'inout')})

def text(x, y, s):
    return add('text', (x, y), {'text': s}, {})

# ---------- przewody ----------

WIRES = []   # (x1,y1,x2,y2)  tylko poziome/pionowe
def wire(x1, y1, x2, y2):
    assert y1 == y2 or x1 == x2, f"wire nieosiowy: ({x1},{y1})-({x2},{y2})"
    if (x1, y1) == (x2, y2):
        return
    WIRES.append((x1, y1, x2, y2))

def poly(*pts):
    for i in range(len(pts) - 1):
        wire(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])

# =================================================================
# UKLAD
# =================================================================

# ---- naglowki / opisy ----
text(60, 20, "UKLAD PO ROZWINIECIU SHANNONA  f = b'(c'*f00 + c*f01) + b*(c'*f10 + c*f11)   ;   f00 = a*d,  f01 = a'*d,  f10 = a' + d',  f11 = 1")
text(60, 430, "ROWNOWAZNA SUMA MINTERMOW (SOP):  f = Sum m(3,4,5,6,7,9,12,14,15)")
text(60, 760, "WERYFIKACJA:  f(Shannon) XNOR f(SOP)  --  dla wszystkich 16 kombinacji a,b,c,d wyjscie 'zgodne' powinno wynosic 1")
text(640, 40, "POZIOM 2 (sterowanie c)")
text(840, 110, "POZIOM 1 (sterowanie b)")

# ---- wejscia ----
pin_in(60, 70,  'a');  wire(60, 70,  130, 70);  tunnel(130, 70,  'a')
pin_in(60, 150, 'b');  wire(60, 150, 130, 150); tunnel(130, 150, 'b')
pin_in(60, 230, 'c');  wire(60, 230, 130, 230); tunnel(130, 230, 'c')
pin_in(60, 310, 'd');  wire(60, 310, 130, 310); tunnel(130, 310, 'd')

# ---- inwertery wejsciowe ----
not_gate(300, 40);   tunnel(240, 40,  'a',  'west'); wire(240, 40,  270, 40);  wire(300, 40,  330, 40);  tunnel(330, 40,  'an', 'west')
not_gate(300, 130);  tunnel(240, 130, 'b',  'west'); wire(240, 130, 270, 130); wire(300, 130, 330, 130); tunnel(330, 130, 'bn', 'west')
not_gate(300, 220);  tunnel(240, 220, 'c',  'west'); wire(240, 220, 270, 220); wire(300, 220, 330, 220); tunnel(330, 220, 'cn', 'west')
not_gate(300, 310);  tunnel(240, 310, 'd',  'west'); wire(240, 310, 270, 310); wire(300, 310, 330, 310); tunnel(330, 310, 'dn', 'west')

# ---- funkcje rezydualne 2. poziomu ----
g = gate('and', 2, 500, 60)                       # f00 = a*d
tunnel(420, 40, 'a',  'west'); wire(420, 40,  450, 40)
tunnel(420, 80, 'd',  'west'); wire(420, 80,  450, 80)
wire(500, 60, 530, 60); tunnel(530, 60, 'f00', 'west')

g = gate('and', 2, 500, 150)                      # f01 = a'*d
tunnel(420, 130, 'an', 'west'); wire(420, 130, 450, 130)
tunnel(420, 170, 'd',  'west'); wire(420, 170, 450, 170)
wire(500, 150, 530, 150); tunnel(530, 150, 'f01', 'west')

g = gate('or', 2, 500, 230)                       # f10 = a' + d'
tunnel(420, 210, 'an', 'west'); wire(420, 210, 450, 210)
tunnel(420, 250, 'dn', 'west'); wire(420, 250, 450, 250)
wire(500, 230, 530, 230); tunnel(530, 230, 'f10', 'west')

const1(470, 300); wire(470, 300, 500, 300); tunnel(500, 300, 'one', 'west')   # f11 = 1

# ---- multipleksery poziomu 2 (sterowane c) ----
m = mux21(700, 100)                               # g0 = c ? f01 : f00
tunnel(640, 90,  'f00', 'west'); wire(640, 90,  670, 90)
tunnel(640, 110, 'f01', 'west'); wire(640, 110, 670, 110)
poly((680, 120), (680, 160), (610, 160)); tunnel(610, 160, 'c', 'west')
wire(700, 100, 730, 100); tunnel(730, 100, 'g0', 'west')

m = mux21(700, 250)                               # g1 = c ? 1 : f10
tunnel(640, 240, 'f10', 'west'); wire(640, 240, 670, 240)
tunnel(640, 260, 'one', 'west'); wire(640, 260, 670, 260)
poly((680, 270), (680, 310), (610, 310)); tunnel(610, 310, 'c', 'west')
wire(700, 250, 730, 250); tunnel(730, 250, 'g1', 'west')

# ---- multiplekser poziomu 1 (sterowany b) ----
m = mux21(920, 170)                               # f = b ? g1 : g0
tunnel(860, 160, 'g0', 'west'); wire(860, 160, 890, 160)
tunnel(860, 180, 'g1', 'west'); wire(860, 180, 890, 180)
poly((900, 190), (900, 230), (830, 230)); tunnel(830, 230, 'b', 'west')
wire(920, 170, 960, 170)
wire(960, 170, 1040, 170)
poly((960, 170), (960, 210)); tunnel(960, 210, 'fS', 'west')
pin_out(1040, 170, 'f (Shannon)')

# ---- SOP: 9 mintermow ----
minterms = [  # (minterm, [bity a,b,c,d])
    (3,  [0,0,1,1]), (4,  [0,1,0,0]), (5,  [0,1,0,1]),
    (6,  [0,1,1,0]), (7,  [0,1,1,1]), (9,  [1,0,0,1]),
    (12, [1,1,0,0]), (14, [1,1,1,0]), (15, [1,1,1,1]),
]
netnames = ['a', 'b', 'c', 'd']
invmap = {'a': 'an', 'b': 'bn', 'c': 'cn', 'd': 'dn'}

and_locs = {3: (350, 480), 4: (350, 580), 5: (350, 700),
            6: (590, 480), 7: (590, 580), 9: (590, 700),
            12: (830, 480), 14: (830, 580), 15: (830, 700)}
for m_, bits in minterms:
    x, y = and_locs[m_]
    gate('and', 4, x, y)
    dy = gate_dy(4)
    for i, bit in enumerate(bits):
        net = netnames[i] if bit else invmap[netnames[i]]
        ty = y + dy[i]
        tunnel(x - 60, ty, net, 'west')
        wire(x - 60, ty, x - 50, ty)
    wire(x, y, x + 30, y)
    tunnel(x + 30, y, f'm{m_}', 'west')

# ---- OR 9 wejsciowe ----
ORX, ORY = 1080, 570
gate('or', 9, ORX, ORY)
dy = gate_dy(9)
sel_order = [3, 4, 5, 6, 7, 9, 12, 14, 15]
for i, m_ in enumerate(sel_order):
    ty = ORY + dy[i]
    tunnel(990, ty, f'm{m_}', 'west')
    wire(990, ty, ORX - 50, ty)
wire(ORX, ORY, 1120, ORY)
wire(1120, ORY, 1150, ORY)
poly((1120, ORY), (1120, 620)); tunnel(1120, 620, 'fSOP', 'west')
pin_out(1150, ORY, 'f (SOP)')

# ---- XNOR f(Shannon) vs f(SOP) ----
gate('xnor', 2, 480, 820)
tunnel(400, 800, 'fS',   'west'); wire(400, 800, 430, 800)
tunnel(400, 840, 'fSOP', 'west'); wire(400, 840, 430, 840)
wire(480, 820, 560, 820)
pin_out(560, 820, 'zgodne (1 = f_Shannon = f_SOP)')

# =================================================================
# normalizacja przewodow: przelaczanie splatanych segmentow
# =================================================================
def norm_wires(segments):
    pts = set()
    for x1, y1, x2, y2 in segments:
        pts.add((x1, y1)); pts.add((x2, y2))
    out = []
    for x1, y1, x2, y2 in segments:
        if y1 == y2:
            xs = sorted({x1, x2} | {p[0] for p in pts if p[1] == y1 and min(x1, x2) < p[0] < max(x1, x2)})
            for a, b in zip(xs, xs[1:]):
                if a != b:
                    out.append((a, y1, b, y2))
        else:
            ys = sorted({y1, y2} | {p[1] for p in pts if p[0] == x1 and min(y1, y2) < p[1] < max(y1, y2)})
            for a, b in zip(ys, ys[1:]):
                if a != b:
                    out.append((x1, a, x2, b))
    return out

WIRES = norm_wires(WIRES)
print(f"komponenty: {len(COMPS)}, przewody (atomowe): {len(WIRES)}")

# =================================================================
# symulator
# =================================================================
class DSU:
    def __init__(self):
        self.p = {}
    def find(self, x):
        self.p.setdefault(x, x)
        r = x
        while self.p[r] != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb

dsu = DSU()
for x1, y1, x2, y2 in WIRES:
    dsu.union((x1, y1), (x2, y2))
# tunele lacza sieci o tej samej etykiecie
tun_nets = defaultdict(list)
for c in COMPS:
    if c.kind == 'tunnel':
        tun_nets[c.attrs['label']].append(c.abs_port('p'))
for label, locs in tun_nets.items():
    for loc in locs[1:]:
        dsu.union(locs[0], loc)

def net_of(point):
    return dsu.find(point)

# mapa: net -> lista portow
net_inputs = defaultdict(list)   # net -> komp.port do odczytu
net_drivers = defaultdict(list)  # net -> komp id (sterowanie)
for c in COMPS:
    for pname, (dx, dy, d) in c.ports.items():
        pt = (c.loc[0] + dx, c.loc[1] + dy)
        net = net_of(pt)
        if d == 'in':
            net_inputs[net].append((c, pname))
        elif d == 'out':
            net_drivers[net].append((c, pname))
        else:  # inout - tunnel: traktuj jako przezroczysty węzeł (bez sterownika)
            pass

# tunele siecia - OK
def eval_circuit(av, bv, cv, dv):
    inputs = {'a': av, 'b': bv, 'c': cv, 'd': dv}
    netval = {}
    drivers_of_net = {}
    # pin_in steruje siecia
    for c in COMPS:
        if c.kind == 'pin_in':
            pt = c.abs_port('p'); netval[net_of(pt)] = inputs[c.attrs['label']]
    # const1 steruje
    for c in COMPS:
        if c.kind == 'const':
            netval[net_of(c.abs_port('out'))] = 1
    def get(net):
        return netval.get(net)
    changed = True
    it = 0
    while changed and it < 100:
        changed = False; it += 1
        for c in COMPS:
            k = c.kind
            if k in ('pin_in', 'const', 'tunnel', 'pin_out', 'text'):
                continue
            ins = []
            ready = True
            for pname, (dx, dy, d) in c.ports.items():
                if d == 'in':
                    v = get(net_of((c.loc[0] + dx, c.loc[1] + dy)))
                    if v is None:
                        ready = False
                        break
                    ins.append((pname, v))
            if not ready:
                continue
            inmap = dict(ins)
            out = None
            if k == 'not':
                out = 1 - inmap['in']
            elif k in ('and', 'or', 'xor', 'xnor'):
                vals = [inmap[f'in{i}'] for i in range(len([p for p in c.ports if p.startswith('in')]))]
                if k == 'and':  out = int(all(vals))
                elif k == 'or': out = int(any(vals))
                elif k == 'xor': out = sum(vals) % 2
                elif k == 'xnor': out = 1 - sum(vals) % 2
            elif k == 'mux':
                out = inmap['in1'] if inmap['sel'] else inmap['in0']
            else:
                raise ValueError(k)
            onet = net_of(c.abs_port('out'))
            if onet in netval and netval[onet] != out:
                raise RuntimeError(f"konflikt sterownikow na sieci {onet} (komponent {c.id})")
            if netval.get(onet) != out:
                netval[onet] = out
                changed = True
    return netval

print("\n=== WERYFIKACJA: wszystkie 16 kombinacji a,b,c,d ===")
target = {3,4,5,6,7,9,12,14,15}
ok = True
rows = []
for av, bv, cv, dv in itertools.product([0,1], repeat=4):
    m = av*8 + bv*4 + cv*2 + dv
    netval = eval_circuit(av, bv, cv, dv)
    # wyjscie f(Shannon): pin_out label 'f (Shannon)'
    def pinval(lab):
        for c in COMPS:
            if c.kind == 'pin_out' and c.attrs['label'] == lab:
                return netval.get(net_of(c.abs_port('p')))
        return None
    fs  = pinval('f (Shannon)')
    fs2 = pinval('f (SOP)')
    zg  = pinval('zgodne (1 = f_Shannon = f_SOP)')
    exp = 1 if m in target else 0
    row_ok = (fs == exp) and (fs2 == exp) and (zg == 1)
    ok = ok and row_ok
    rows.append((m, av, bv, cv, dv, fs, fs2, zg, exp, 'OK' if row_ok else 'BLAD'))
    print(f"m{m:2d}  a={av} b={bv} c={cv} d={dv} | f_Shannon={fs}  f_SOP={fs2}  zgodne={zg}  oczek={exp}  {'OK' if row_ok else 'BLAD'}")
assert ok, "NIEZGODNOSC!"
print("\nWSZYSTKIE 16 KOMBINACJI ZGODNE: f(Shannon) == f(SOP) == Sum m(3,4,5,6,7,9,12,14,15)")

# sprawdz tez brak niepodlaczonych wejsc (floating)
floating = []
for net, lst in net_inputs.items():
    pass  # weryfikacja posrednia przez eval - brak 'None'
for c in COMPS:
    if c.kind in ('pin_in', 'const', 'tunnel', 'pin_out', 'text'):
        continue
    for pname, (dx, dy, d) in c.ports.items():
        if d == 'in':
            pass  # eval nie zgloszil konfliktow; pelna kontrola nizej

# =================================================================
# emisja XML
# =================================================================
from xml.sax.saxutils import escape

def attr(name, val):
    return f'<a name="{escape(str(name))}" val="{escape(str(val))}"/>'

NAME_MAP = {
    'pin_in':  ('0', 'Pin'),
    'pin_out': ('0', 'Pin'),
    'not':     ('1', 'NOT Gate'),
    'and':     ('1', 'AND Gate'),
    'or':      ('1', 'OR Gate'),
    'xor':     ('1', 'XOR Gate'),
    'xnor':    ('1', 'XNOR Gate'),
    'mux':     ('2', 'Multiplexer'),
    'const':   ('0', 'Constant'),
    'tunnel':  ('0', 'Tunnel'),
    'text':    ('3', 'Text'),
}

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
lines.append('<project version="1.0">')
lines.append('  <lib name="0" desc="#Wiring"/>')
lines.append('  <lib name="1" desc="#Gates"/>')
lines.append('  <lib name="2" desc="#Plexers"/>')
lines.append('  <lib name="3" desc="#Base"/>')
lines.append('  <main name="Zadanie 1"/>')
lines.append('  <circuit name="Zadanie 1">')
lines.append('    <a name="appearance" val="logisim_evolution"/>')
lines.append('    <a name="circuit" val="Zadanie 1"/>')
lines.append('    <a name="circuitnamedboxfixedsize" val="true"/>')
lines.append('    <a name="simulationFrequency" val="1.0"/>')
for c in COMPS:
    lib, name = NAME_MAP[c.kind]
    loc = f"({c.loc[0]},{c.loc[1]})"
    body = ''.join(attr(k, v) for k, v in c.attrs.items())
    if body:
        lines.append(f'    <comp lib="{lib}" loc="{loc}" name="{name}">{body}</comp>')
    else:
        lines.append(f'    <comp lib="{lib}" loc="{loc}" name="{name}"/>')
for x1, y1, x2, y2 in WIRES:
    lines.append(f'    <wire from="({x1},{y1})" to="({x2},{y2})"/>')
lines.append('  </circuit>')
lines.append('</project>')

import json, os
os.makedirs('/home/user/edu_lab5/zadanie1', exist_ok=True)
with open('/tmp/logisim/layout.json', 'w', encoding='utf-8') as f:
    json.dump({
        'components': [{'id': c.id, 'kind': c.kind, 'loc': c.loc, 'attrs': c.attrs,
                        'ports': {k: list(v) for k, v in c.ports.items()}} for c in COMPS],
        'wires': [list(w) for w in WIRES],
    }, f, ensure_ascii=False, indent=1)

os.makedirs('/home/user/edu_lab5/zadanie1', exist_ok=True)
with open('/home/user/edu_lab5/zadanie1/zadanie1.circ', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print("\nZapisano /home/user/edu_lab5/zadanie1/zadanie1.circ")

# xml well-formed?
import xml.etree.ElementTree as ET
ET.parse('/home/user/edu_lab5/zadanie1/zadanie1.circ')
print("XML poprawny skladniowo.")
